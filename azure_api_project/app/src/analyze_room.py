"""
Analyze a photo and play TTS messages if
there is too many people on this photo.
"""

import yaml
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from playsound import playsound


def authentication():
    """Authenticate to the Azure Ressource."""

    secrets_file = ".secrets/api.yml"
    with open(secrets_file, "r") as secrets:
        try:
            result = yaml.safe_load(secrets)
            subscription_key = result.get("subscription_key")
            endpoint = result.get("endpoint")
        except yaml.YAMLError as error:
            print(f"Error while trying to read {secrets_file} : {error}")
            sys.exit(1)
    return ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))


def count_person_from_image(image_path):
    """Count the number of person on the image."""

    client = authentication()
    with open(image_path, "rb") as image:
        analyze_result = client.detect_objects_in_stream(image)
        persons = [
            item for item
            in analyze_result.objects
            if item.object_property == "person"
        ]
        return len(persons)
    return 0


def group_tts(fr_tts, en_tts):
    """Group all TTS files into an object"""

    return {"FR": fr_tts, "EN": en_tts}


def play_audio(tts_audios):
    """Play TTS messages."""

    for lang in tts_audios:
        playsound(tts_audios.get(lang))


def analyze_room(parameters):
    """Main function to redirect to send_audio as needed."""

    person = count_person_from_image(parameters.image_path)
    if person > parameters.max_allowed:
        print("WARNING: Too many people in the studio.")
        print("> Sending alert message...")
        tts_audios = group_tts(parameters.french_audio, parameters.english_audio)
        play_audio(tts_audios)
    else:
        print("Social distancing is respected. Exiting...")
