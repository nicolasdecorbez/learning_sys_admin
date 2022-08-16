"""
Read command line args and return all parameters to use.
"""


import sys
import argparse
from dataclasses import dataclass
import yaml
from src import analyze_room


@dataclass
class Parameters:
    """Create a list of parameters for configuration."""

    max_allowed: ""
    image_path: ""
    french_audio: ""
    english_audio: ""


def generate_params(max_allowed, image_path, french_audio, english_audio):
    """Format function arguments into a Parameters object."""

    return Parameters(max_allowed, image_path, french_audio, english_audio)


def verify_filename(filename, extension):
    """Verify the file extension."""

    return filename.endswith(extension)


def read_max_allowed_yaml(filename):
    """Read content of the YAML configuration file."""

    with open(filename, 'r') as configuration:
        try:
            result = yaml.safe_load(configuration)
            if max_allowed := result.get("max_allowed"):
                return max_allowed
            print(f"WARNING: Can't find 'max_allowed' column into '{filename}'.")
            print("> Exiting the program.")
            sys.exit(1)
        except yaml.YAMLError as error:
            print(f"Error while trying to read {filename} : {error}")
            sys.exit(1)


def check_input_files(config, image, french, english):
    """Check if filenames are compliant."""

    is_valid_filename = {
        "config": verify_filename(config, ".yml") or verify_filename(config, ".yaml"),
        "image": verify_filename(image, ".jpg") or verify_filename(image, ".jpeg"),
        "audio_fr": verify_filename(french, ".wav"),
        "audio_en": verify_filename(english, ".wav")
    }
    if not is_valid_filename.get("config"):
        print(f"Invalid YAML config file : {config}")
        print("It must me a .yml or .yaml file.")
        return False
    if not is_valid_filename.get("image"):
        print(f"Invalid image : {config}")
        print("It must me a .jpg or .jpeg file.")
        return False
    if not is_valid_filename.get("audio_fr"):
        print(f"Invalid audio file : {french}")
        print("They must me a .wav file.")
        return False
    if not is_valid_filename.get("audio_en"):
        print(f"Invalid audio file : {english}")
        print("They must me a .wav file.")
        return False
    return True


def read_input():
    """Define all accepted arguments and read the command line."""

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config",
                        type=argparse.FileType("r"),
                        help="YAML configuration file",
                        required=True)
    parser.add_argument("-i", "--image",
                        type=argparse.FileType("r"),
                        help="Image to analyze. Must be a .jpg or .jpeg file",
                        required=True)
    parser.add_argument("-f", "--french",
                        type=argparse.FileType("r"),
                        help="French audio file. Must be a .wav file",
                        required=True)
    parser.add_argument("-e", "--english",
                        type=argparse.FileType("r"),
                        help="English audio file. Must be a .wav file",
                        required=True)
    args = parser.parse_args()

    is_input_valid = check_input_files(
        args.config.name,
        args.image.name,
        args.french.name,
        args.english.name
    )

    if not is_input_valid:
        return 0

    parameters = generate_params(
        read_max_allowed_yaml(args.config.name),
        args.image.name,
        args.french.name,
        args.english.name
    )
    analyze_room.analyze_room(parameters)
