"""Check and install the required files for Box execution"""


import os
import stat
import shutil
import requests
import tarfile


cwd = os.getcwd()
env_file = f"{cwd}/config_files/env.yaml"

box_dir = "/var/lib/box"
base_dir = f"{box_dir}/base"
env_dir = f"{box_dir}/env"
box_env_file = f"{box_dir}/env.yaml"

url = "https://github.com/debuerreotype/docker-debian-artifacts/raw/3503997cf522377bc4e4967c7f0fcbcb18c69fc8/buster/slim/rootfs.tar.xz"
target_xz = "/var/lib/box/debian.tar.xz"


def create_box_dir(dir):
  """Create the base box directory into /var/lib"""

  print(f"INFO: Creating the directory : {dir}")
  os.makedirs(dir)


def create_env_file():
  """Create the env. file with all our already built env."""

  print(f"INFO: Creating the box configuration file : {box_env_file}")
  shutil.copyfile(env_file, box_env_file)


def populate_base_dir():
  """Download a Debian env. archive and export it to /var/lib/box/base"""

  print("INFO: Creating the 'base' directory.")
  if os.path.isdir(base_dir):
    shutil.rmtree(base_dir)

  response = requests.get(url, stream = True)
  if response.status_code == 200:
    with open(target_xz, "wb") as f:
      f.write(response.raw.read())

  unzip = tarfile.open(target_xz)
  unzip.extractall(base_dir)
  unzip.close()
  os.remove(target_xz)


def populate_dev(directory):
  """Create all missing files into base box env /dev.
     - for '/dev', based on https://tldp.org/LDP/lfs/LFS-BOOK-6.1.1-HTML/chapter06/devices.html and FHS"""

  # Reset our permissions to avoid conflict.
  os.umask(0)

  if not os.path.isfile(f"{directory}/dev/console"):
    os.mknod(
        path=f"{directory}/dev/console",
        mode=0o620 | stat.S_IFCHR,
        device=os.makedev(5, 1),
    )

  if not os.path.isfile(f"{directory}/dev/null"):
    os.mknod(
        path=f"{directory}/dev/null",
        mode=0o666 | stat.S_IFCHR,
        device=os.makedev(1, 3),
    )

  if not os.path.isfile(f"{directory}/dev/zero"):
    os.mknod(
        path=f"{directory}/dev/zero",
        mode=0o666 | stat.S_IFCHR,
        device=os.makedev(1, 5),
    )

  if not os.path.isfile(f"{directory}/dev/tty"):
    os.mknod(
        path=f"{directory}/dev/tty",
        mode=0o666 | stat.S_IFCHR,
        device=os.makedev(5, 0),
    )

  if not os.path.isfile(f"{directory}/dev/random"):
    os.mknod(
        path=f"{directory}/dev/random",
        mode=0o444 | stat.S_IFCHR,
        device=os.makedev(1, 8),
    )

  if not os.path.isfile(f"{directory}/dev/urandom"):
    os.mknod(
        path=f"{directory}/dev/urandom",
        mode=0o444 | stat.S_IFCHR,
        device=os.makedev(1, 9),
    )

  # Change owner of console & tty files -> root:tty
  for filename in ["console", "tty"]:
    os.chown(f"{directory}/dev/{filename}", 0, 5)


def check_installation():
  """Check if Box is already installed"""
  
  print("Checking for any Box installation.")
  try:
    if os.path.isdir(box_dir):
      shutil.rmtree(box_dir)
    create_box_dir(box_dir)
    create_box_dir(env_dir)
    create_env_file()
    populate_base_dir()
    populate_dev(base_dir)

  except OSError as error:
    exit(error)
