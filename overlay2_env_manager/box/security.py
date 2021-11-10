"""Check, before build runtime, if the input files are compliant"""

import yaml
import sys


def verify_filename(filename, extension):
  """Verify the file extension"""

  return filename.endswith(extension)


def missing_column(column, filename):
  """Error message if a required column is missing into the YAML file"""

  print(f"ERROR: Can't find required column '{column}' into '{filename}'.")
  print("> Exiting the program.")
  sys.exit(1)


def check_input_files(build):
  """Check if filename are compliant"""

  is_valid_filename = verify_filename(build, ".yml") or verify_filename(build, ".yaml")

  if not is_valid_filename:
    print(f"ERROR: Invalid build config file : {build}")
    print("> It must me a .yml or .yaml file.")
    sys.exit(1)

  return is_valid_filename


def check_build_file(filename):
  """Check if the build file is not missing any required column"""

  with open(filename, "r") as build:
    try:
      file = yaml.safe_load(build)
      tests = ["name", "run"]

      for test in tests:
        value = file.get(test)
        if not value:
          missing_column(test, filename)

    except yaml.YAMLError as error:
      print(f"Error while trying to read {filename} : {error}")
      sys.exit(1)


def build_verifications(filename):
  """Call all security functions for build option"""

  check_input_files(filename)
  check_build_file(filename)