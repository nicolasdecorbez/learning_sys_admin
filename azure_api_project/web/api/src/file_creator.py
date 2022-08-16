"""
Retrieve data from the request before calling functions
to create the configuration file and call the TTS synthesizer
"""

import os
import yaml
from src import audio


def create_yaml_params(max_allowed):
    """
    Return an object with all parameters
    to write into the YAML configuration file.
    """

    if isinstance(max_allowed, str):
        max_allowed = int(max_allowed)

    return {"max_allowed": max_allowed}


def generate_files(request_data):
    """Main function to send corrects arguments to file creation functions."""

    path = (
        os.getenv("YAML_CONFIG_PATH")
        or "../../Ressources/Configuration/configuration"
    )

    yaml_params = create_yaml_params(request_data.max_allowed)
    generate_yaml(yaml_params, path)
    generate_audios(request_data.message)


def generate_yaml(yaml_params, path):
    """Create the YAML configuration file with formated parameters"""

    if not path.endswith(".yml") and not path.endswith(".yaml"):
        path = f"{path}.yml"
    with open(path, "w") as configuration:
        yaml.dump(yaml_params, configuration)
        print(f"API: Successfully created '{path}'")


def generate_audios(message):
    """Create two TTS audio files, with one translated in english"""
    speech_configuration = audio.get_speech_configuration()
    audio.create_audio_files(speech_configuration, message)
