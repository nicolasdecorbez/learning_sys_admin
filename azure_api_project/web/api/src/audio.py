"""
Synthesize plain text into TTS files, then translate it
and synthesize the translated version too.
"""

import os
import uuid
import requests
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer
from azure.cognitiveservices.speech.audio import AudioOutputConfig

def get_keys_from_env(service):
    """Retrive Secret Keys from env variables"""

    if service == "speech":
        speech_key = os.getenv("AZ_SPEECH_KEY")
        speech_region = os.getenv("AZ_SPEECH_REGION")

        if not speech_key:
            speech_key = "<YOUR_SUBSCRIPTION_KEY>"
        if not speech_region:
            speech_region = "<YOUR_REGION>"

        return {"key": speech_key, "region": speech_region}

    elif service == "translate":
        translate_key = os.getenv("AZ_TRANSLATE_KEY")
        translate_region = os.getenv("AZ_TRANSLATE_REGION")

        if not translate_key:
            translate_key = "<YOUR_SUBSCRIPTION_KEY>"
        if not translate_region:
            translate_region = "<YOUR_REGION>"

        return {"key": translate_key, "region": translate_region}

    return 0

def get_speech_configuration():
    """Create a configuration file for Azure Speech."""

    speech_info = get_keys_from_env("speech")
    return SpeechConfig(
        subscription=speech_info.get("key"), region=service_info.get("region")
    )


def get_translate_configuration():
    """Define few informations to configure Azure Translate."""

    translate_info = get_keys_from_env("translate")
    return {
        "subscription_key": translate_info.get("key"),
        "endpoint": "https://api.cognitive.microsofttranslator.com/translate",
        "location": translate_info.get("region"),
    }


def get_path_from_env():
    """Define path and filename for TTS files."""

    tts_base_path = os.getenv("TTS_PATH")
    tts_fr_name = os.getenv("FRENCH_TTS_NAME")
    tts_en_name = os.getenv("ENGLISH_TTS_NAME")

    if not tts_base_path:
        tts_base_path = "../../Ressources/Audio/"

    if not tts_fr_name:
        tts_fr_name = "french_tts_message.wav"

    if not tts_en_name:
        tts_en_name = "english_tts_message.wav"

    return {
        "base": tts_base_path,
        "french": tts_fr_name,
        "english": tts_en_name,
    }


def message_synthesizer(language, message, speech_config):
    """Synthesize text into audio message, and save it."""

    path = get_path_from_env()
    if language != "french":
        message = translate_message(message)
        speech_config.speech_synthesis_voice_name = "en-GB-MiaNeural"
        filename = path.get("base") + path.get("english")
    else:
        speech_config.speech_synthesis_voice_name = "fr-FR-DeniseNeural"
        filename = path.get("base") + path.get("french")

    audio_config = AudioOutputConfig(filename=filename)
    speech_synthesizer = SpeechSynthesizer(
        speech_config=speech_config,
        audio_config=audio_config
    )
    speech_synthesizer.speak_text_async(message)
    print(f"API: Successfully synthesized '{message}' into '{filename}'")


def translate_message(message):
    """Translate a french message into an english one using Az Translate."""

    translate_config = get_translate_configuration()
    params = {
        'api-version': '3.0',
        'from': 'fr',
        'to': ['en']
    }
    headers = {
        'Ocp-Apim-Subscription-Key': translate_config.get("subscription_key"),
        'Ocp-Apim-Subscription-Region': translate_config.get("location"),
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    body = [{
        'text': message
    }]

    request = requests.post(
        translate_config.get("endpoint"),
        params=params,
        headers=headers,
        json=body
    )
    response = request.json()
    return response[0].get("translations")[0].get("text")


def create_audio_files(speech_config, message):
    """Create audio files for each languages"""

    message_synthesizer("french", message, speech_config)
    message_synthesizer("english", message, speech_config)
