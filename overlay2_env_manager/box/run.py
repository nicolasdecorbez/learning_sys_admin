"""Run command methods to start an already created new environment"""


import os
import re
from dataclasses import dataclass
from box import env, mount, colors


@dataclass
class RunParameters:
  """Create a list of parameters for run command"""

  name: str
  path: str
  run: str
  user: str


def generate_run_config(env_name, env_list):
  """Retrieve all env parameters and return a formated RunParameters object"""

  for env_node in env_list.environments:
    if(env_node.get("name") == env_name):
      return RunParameters(
        name = env_node.get("name"),
        path = env_node.get("path"),
        run = env_node.get("run"),
        user = env_node.get("user"),
      )


def mount_run(path):
  """Mount all necessary files and dir to out target env"""

  # mount our overlay fs
  mount.overlay_mount(
    lower = "/var/lib/box/base",
    upper = path + "/files",
    work = path + "/buffer",
    merged = path + "/runtime"
  )
  # mount proc & sys, create dev...
  mount.mount_env(path + "/runtime")


def umount_run(path):
  """Umount all previously mounted files and dir"""

  # mount proc & sys, create dev...
  mount.umount_env(path + "/runtime")
  # umount overlay
  os.system("umount -v " + path + "/runtime")


def launch_app(env_config: RunParameters, add_args):
  """Launch the application into a subprocess"""

  pid = os.fork()

  if pid > 0:
    info = os.waitpid(pid, 0)
    print(f"{colors.OKCYAN}\n––––––––––––––––––––––––––––––––––\n{colors.ENDC}")
    if os.WIFEXITED(info[1]) : 
      code = os.WEXITSTATUS(info[1]) 
      if code != 0:
        print(f"{colors.FAIL}ERROR:{colors.ENDC} Run failed with error code : {code}")
  
  else:
    print(f"{colors.OKCYAN}\nLaunching {env_config.name}")
    print(f"––––––––––––––––––––––––––––––––––\n{colors.ENDC}")
    print(colors.WARNING)
    os.chroot(env_config.path + "/runtime")
    os.chdir("/")

    if(env_config.user != "root"):
      os.setuid(666)

    if "$ARGS" in env_config.run:
      before_args = env_config.run.index("$ARGS")
      if add_args:
        os.system(env_config.run[0:before_args] + add_args)
      else:
        os.system(env_config.run[0:before_args])
    else:
      os.system(env_config.run)

    print(colors.ENDC)
    os._exit(os.EX_OK)


def start_run(env_name, add_args, share_path):
  """Call all checks & requirements before executing the run"""

  env_list = env.read_env_file()
  if env_list.environments and env.is_env_exist(env_name, env_list):
    env_config = generate_run_config(env_name, env_list)
    mount_run(env_config.path)

    if share_path:
      mount.share_mount(share_path, env_config.path)

    launch_app(env_config, add_args)

    if share_path:
      mount.share_umount(share_path, env_config.path)

    umount_run(env_config.path)
  else:
    print(f"{colors.FAIL}ERROR:{colors.ENDC} Environment named {env_name} doesn't exist. Try to build it before running this command again.")
    os._exit(1)


def check_share(share: str):
  """Check if the share synthax is correct"""

  regex = "..*:..*"
  if re.search(regex, share):
    source = share.split(":", 1)[0]
    if not os.path.exists(source):
      print(f"{colors.FAIL}ERROR:{colors.ENDC} {source} not found !")
      os._exit(1)
  else:
    print(f"{colors.FAIL}ERROR:{colors.ENDC} Invalid share syntax. It must be 'source_path:dest_path'")
    os._exit(1)

