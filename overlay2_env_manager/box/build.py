"""Build command methods to generate a brand new environment"""

import sys
import yaml
from box import security, colors, env
from dataclasses import dataclass

@dataclass
class BuildParameters:
  """Create a list of parameters for build command"""

  name: str
  user: str
  requirements: list
  repositories: list
  run: str


def build_configuration(filename):
  """Generate an object with the build configuration"""

  with open(filename, "r") as build:
    try:
      file = yaml.safe_load(build)

      ext_repos = file.get("repositories")
      alt_user = file.get("user")
      req = file.get("requirements")

      if not ext_repos:
        print(f"{colors.OKBLUE}INFO:{colors.ENDC} No additional repositories specified. Running with default APT repositories.")
        ext_repos = None

      if not alt_user:
        print(f"{colors.OKBLUE}INFO:{colors.ENDC} No user specified. Performing build with 'root' user.")
        alt_user = "root"

      if not req:
        print(f"{colors.OKBLUE}INFO:{colors.ENDC} No requirements specified. Using only native debian commands.")
        req = None

      return BuildParameters(
        name = file.get("name"),
        user = alt_user,
        requirements = req,
        repositories = ext_repos,
        run = file.get("run")
      )

    except yaml.YAMLError as error:
      print(f"{colors.FAIL}ERROR:{colors.ENDC} error while trying to read {filename} : {error}")
      sys.exit(1)


def start_build(filename):
  """Call all checks & requirements before executing the build"""

  security.build_verifications(filename)
  config = build_configuration(filename)
  env_list = env.read_env_file()

  new_node = {
    "name": config.name,
    "path": "/var/lib/box/env/" + config.name,
    "user": config.user,
    "run": config.run 
  }
  
  if env_list.environments and env.is_env_exist(config.name, env_list):
    env_list = env.delete_env(config.name, env_list)

  env_list = env.create_env(new_node, env_list, config)

  write_changes(env_list)


def write_changes(env_list: env.EnvParameters):
  """Write the new env to the env.yaml file"""

  to_write = {
    "version": env_list.version,
    "environments": env_list.environments
  }

  with open("/var/lib/box/env.yaml", "w") as file:
    try:
      yaml.dump(to_write, file)
    except yaml.YAMLError as error:
      print(f"{colors.FAIL}ERROR:{colors.ENDC} error while trying to read env.yaml : {error}")
      sys.exit(1)
