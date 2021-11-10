"""Read command line args and call required methods"""


import argparse
import os
from box import build as build_exec, run as run_exec, env as env_exec, setup, colors

def build_parser(build_subparser):
  """Define all accepted arguments for build command"""

  build_subparser.add_argument(
    "build_filename",
    type = argparse.FileType("r"),
    help = "YAML build configuration file.",
    metavar = "FILE"
  )
  return build_subparser


def run_parser(run_subparser: argparse.ArgumentParser):
  """Define all accepted arguments for run command"""

  run_subparser.add_argument(
    "run_env",
    type = str,
    help = "The environment you want to run. Must be built before run calling the 'run' command.",
    metavar = "ENV"
  )
  run_subparser.add_argument(
    "-s",
    "--share",
    help = "Share a file / directory to the target box.",
    type = str,
    default = None
  )
  run_subparser.add_argument(
    "-a",
    "--addargs",
    help = "If the 'run' directive contains '$ARGS', then add the given arguments to it.",
    type = str,
    default = None
  )
  return run_subparser


def env_parser(env_subparser: argparse.ArgumentParser):
  """Define all accepted arguments for env command"""

  env_sub = env_subparser.add_subparsers(
    metavar = "ENV_COMMAND",
    dest = "env_command"
  )

  list = env_sub.add_parser(
    "list",
    help = "List all your built environments."
  )

  delete = env_sub.add_parser(
    "delete",
    help = "Delete the selected environment"
  )

  delete.add_argument(
    "selected_env",
    type = str,
    help = "The environment you want to delete.",
    metavar = "ENV"
  )

  return env_subparser
  

def get_args():
  """Define all accepted arguments and return a Parameters object"""

  parser = argparse.ArgumentParser(
    description = "A CLI program to run applications in isolated environments.",
    epilog = "You can run `box COMMAND --help` for more information about the sub-command."
  )

  subparsers = parser.add_subparsers(
    metavar = "COMMAND",
    required = True,
    dest = "command_name"
  )

  build = subparsers.add_parser(
    "build",
    help = "Build an environment based on the input YAML file."
  )

  run = subparsers.add_parser(
    "run",
    help = "Run an application in an already built isolated environment."
  )

  env = subparsers.add_parser(
    "env",
    help = "Interact with built isolated environments."
  )

  install = subparsers.add_parser(
    "setup",
    help = "Setup your box base environment."
  )

  build = build_parser(build)
  run = run_parser(run)
  env = env_parser(env)

  args = parser.parse_args()

  if(args.command_name == "build"):
    build_exec.start_build(args.build_filename.name)
  elif(args.command_name == "run"):
    if args.share:
      run_exec.check_share(args.share)
    run_exec.start_run(
      env_name = args.run_env, 
      share_path = args.share,
      add_args = args.addargs
    )
  elif(args.command_name == "env"):
    if args.env_command == "list":
      env_exec.list_env()
    elif args.env_command == "delete":
      env_list = env_exec.read_env_file()
      if env_exec.is_env_exist(args.selected_env, env_list):
        env_list = env_exec.delete_env(args.selected_env, env_list)
        build_exec.write_changes(env_list)
      else:
        print(f"{colors.FAIL}ERROR:{colors.ENDC} Environment named {args.selected_env} doesn't exist. Try to build it before running this command again.")
        os._exit(1)
  elif(args.command_name == "setup"):
    if os.path.isdir("/var/lib/box"):
      answer = ""
      message = f"{colors.FAIL}ERROR:{colors.ENDC} box directory already exist.\nRunning setup again will delete all your ressources under this directory.\nWould you like to continue [Y/N]? "
      
      while answer not in ["y", "n"]:
        answer = input(message).lower()

      if answer != "y":
        exit(0)

    setup.check_installation()