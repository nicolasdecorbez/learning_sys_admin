"""Define all methods related to env management"""


import os
import sys
import yaml
import shutil
from subprocess import STDOUT, check_call
from tabulate import tabulate
from box import colors, mount
from dataclasses import dataclass

boxenv_file = "/var/lib/box/env.yaml"
boxenv_dir = "/var/lib/box/env"


@dataclass
class EnvParameters:
  """Create a list of env parameters"""

  version: str
  environments: list


def read_env_file():
  """Read the box env file listing all informations about each env"""
  
  with open(boxenv_file, "r") as config:
    try:
      file = yaml.safe_load(config)
      return EnvParameters(
        version = file.get("version"),
        environments = file.get("environments")
      )
    except yaml.YAMLError as error:
      print(f"{colors.FAIL}ERROR:{colors.ENDC} error while trying to read {boxenv_file} : {error}")
      sys.exit(1)


def is_env_exist(env_name, base_env: EnvParameters):
  """check if a previous version of the env exist"""

  return any(
      (env_node.get("name") == env_name) for env_node in base_env.environments)
  

def delete_env(env_name, base_env: EnvParameters):
  """Delete an env by its name"""

  path = f"/var/lib/box/env/{env_name}"
  shutil.rmtree(path)

  for env_node in base_env.environments:
    if(env_node.get("name") == env_name):
      base_env.environments.remove(env_node)

  return base_env


def create_env(env_node, base_env: EnvParameters, config):
  """Create an environment base on the env_node parameter"""

  path = "/var/lib/box/env/" + env_node.get("name")
  suffixes = ["", "/files", "/buffer", "/runtime"]
  base = "/var/lib/box/base"

  for suffix in suffixes:
    os.makedirs(path + suffix)

  # mount our overlay fs
  mount.overlay_mount(
      lower=base,
      upper=f"{path}/files",
      work=f"{path}/buffer",
      merged=f"{path}/runtime",
  )

  # mount proc & sys, create dev...
  mount.mount_env(f"{path}/runtime")

  # create a child process to run build
  pid = os.fork()

  if pid > 0:
    info = os.waitpid(pid, 0)
    if os.WIFEXITED(info[1]) : 
      code = os.WEXITSTATUS(info[1]) 
      if code == 0:
        print(f"{colors.OKBLUE}BUILD:{colors.ENDC} Build suceeded !")
      else:
        print(f"{colors.FAIL}ERROR:{colors.ENDC} Build failed with error code : {code}")

  else:
    os.chroot(f"{path}/runtime")
    os.chdir("/")
    install_requirements(config)
    os._exit(os.EX_OK)

  # umount proc & sys, delete dev...
  mount.umount_env(f"{path}/runtime")

  # umount overlay
  os.system(f"umount -v {path}/runtime")

  if not base_env.environments:
    base_env.environments = [env_node]
  else: 
    base_env.environments.append(env_node)

  return base_env


def install_requirements(config):
  """Install all requirements for a new environment"""

  if config.user != "root":
    print(f"{colors.OKBLUE}BUILD:{colors.ENDC} Create a new user...")
    try: 
      check_call(
        ["useradd", "--uid", "666", config.user],
        stdout=open(os.devnull,"wb"),
        stderr=STDOUT
      )
      print(f"> User '{config.user}' has been created with UID 666.")
    except OSError as error:
      print(f"ERROR: {error}")
      os._exit(os.EX_OSERR)

  if config.repositories:
    # Install requirements before adding the keys

    print(f"{colors.OKBLUE}BUILD:{colors.ENDC} Add repositories...")
    check_call(
      ["apt-get", "-y", "update"],
      stdout=open(os.devnull,"wb"), 
      stderr=STDOUT
    )
    check_call(
      ["apt-get", "install", "-y", "wget"],
      stdout=open(os.devnull,"wb"),
      stderr=STDOUT
    )
    check_call(
      ["apt-get", "install", "-y", "gnupg"],
      stdout=open(os.devnull,"wb"), 
      stderr=STDOUT
    )

    for repo in config.repositories:
      # Retrive only the key-name
      splited_repo_key = repo.get("key").split("/")
      key_name = splited_repo_key[len(splited_repo_key) - 1]
      list_path = f"/etc/apt/sources.list.d/{config.name}-repository.list"

      try:
        # Download and add the repo key
        check_call(
          ["wget", repo.get("key")],
          stdout=open(os.devnull,"wb"), 
          stderr=STDOUT
        )
        check_call(
          ["apt-key", "add", key_name],
          stdout=open(os.devnull,"wb"), 
          stderr=STDOUT
        )

        # Add a source list
        if not os.path.isdir("/etc/apt/sources.list.d"):
          os.makedirs("/etc/apt/sources.list.d/")

        check_call(
          ["touch", list_path],
          stdout=open(os.devnull,"wb"), 
          stderr=STDOUT
        )
        with open(list_path, "a") as file:
          file.write(repo.get("repository"))
          file.close()

        # Reload local package database
        check_call(
          ["apt-get", "-y", "update"],
          stdout=open(os.devnull,"wb"), 
          stderr=STDOUT
        )

      except OSError as error:
        print(f"ERROR: {error}")
        os._exit(os.EX_OSERR)

  if config.requirements:
    print(f"{colors.OKBLUE}BUILD:{colors.ENDC} Add requierements...")
    check_call(
      ["apt-get", "-y", "update"],
      stdout=open(os.devnull,"wb"), 
      stderr=STDOUT
    )
    for req in config.requirements:
      try: 
        check_call(
          ['apt-get', 'install', '-y', req],
          stdout=open(os.devnull,'wb'),
          stderr=STDOUT
        )
      except OSError as error:
        print(f"ERROR: {error}")
        os._exit(os.EX_OSERR)


def list_env():
  """Output all installed environments"""

  envs = read_env_file().environments
  headers = ["Name", "Location", "User", "Run"]
  list = []

  if not envs:
    print(f"{colors.FAIL}ERROR:{colors.ENDC} No environments found. Try to build one before running this command.")
    os._exit(1)

  for env in envs:
    # Retrieve each environment and push it to list
    name = env.get("name")
    location = env.get("path")
    user = env.get("user")
    command = env.get("run")
    list.append([name, location, user, command])

  tab = tabulate(list, headers = headers)
  print(tab)