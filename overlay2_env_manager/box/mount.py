"""Define all methods related to mount env"""

import os

def generate_symlinks(directory):
  """Generate a list of symlinks to create for runtime."""

  return [
      {
          "src": f"{directory}/proc/self/fd",
          "dst": f"{directory}/dev/fd"
      },
      {
          "src": f"{directory}/proc/self/fd/0",
          "dst": f"{directory}/dev/stdin"
      },
      {
          "src": f"{directory}/proc/self/fd/1",
          "dst": f"{directory}/dev/stdout"
      },
      {
          "src": f"{directory}/proc/self/fd/2",
          "dst": f"{directory}/dev/stderr"
      },
      {
          "src": f"{directory}/proc/kcore",
          "dst": f"{directory}/dev/core"
      },
  ]


def mount_env(directory):
  """Mount missing files necessary for runtime"""

  try:
    # Mount proc & sys file system.
    os.system(f"mount -vt proc proc {directory}/proc")
    os.system(f"mount -vt sysfs sysfs {directory}/sys")

    # Make sym links from proc to dev dir.
    for link in generate_symlinks(directory):
      os.symlink(link.get("src"), link.get("dst"))

  except OSError as error:
    print(f"ERROR : {error}") 


def umount_env(directory):
  """Umount previously mounted files"""

  try:
    # Delete symlinks.
    for link in generate_symlinks(directory):
      os.remove(link.get("dst"))

    # Umount proc & sys file system.
    os.system(f"umount -v {directory}/proc")
    os.system(f"umount -v {directory}/sys")

  except OSError as error:
    print(f"ERROR : {error}") 

def overlay_mount(lower, upper, work, merged):
  """Mount an overlay fs to manage our instances"""
  try:
    os.system(
        f"mount -vt overlay overlay -o lowerdir={lower} -o upperdir={upper} -o workdir={work} {merged}"
    )
  except OSError as error:
    print(f"ERROR: {error}")


def share_mount(share_path, box_path):
  """Mount a file to share to the box env"""

  source = share_path.split(":", 1)[0]
  dest_full_path: str = f"{box_path}/runtime" + share_path.split(":", 1)[1]

  if os.path.isfile(source):
    # On retire le filename pour la création des dir parents
    parent_dir = dest_full_path[:dest_full_path.rindex("/")]
    if not os.path.isdir(parent_dir):
      os.makedirs(parent_dir)
    if not os.path.exists(dest_full_path):
      os.system(f"touch {dest_full_path}")
  elif not os.path.isdir(dest_full_path):
    os.makedirs(dest_full_path)

  os.system(f"mount -v --bind {source} {dest_full_path}")


def share_umount(share_path, box_path):
  """Umount a file / dir to share to the box env"""

  os.system(f"umount -v {box_path}/runtime" + share_path.split(":", 1)[1])