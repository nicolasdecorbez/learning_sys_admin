# Web Application <!-- omit in toc -->

- [What is this ?](#what-is-this-)
- [Installation](#installation)
- [Usage](#usage)
- [Code](#code)

## What is this ?

The role of the web application is to enter a warning message (in french) and a maximum limit of people allowed in a room ; then the message will be : 
- used to generate TTS files
- translated in english (with TTS transformation too)

The limit will be stored in a configuration file, in `YAML`, for future execution.

## Installation

Using [`Docker`](https://www.docker.com/) and [`docker-compose`](https://docs.docker.com/compose/):
```console
$ docker-compose up -d
```

Using [Poetry](https://github.com/python-poetry/poetry) (inside [api](api) folder only):
```console
$ poetry install
```

> We strongly recommends you to use Docker to run this part.

## Usage

You must configure your secrets with theses env. variables :
- `AZ_SPEECH_KEY`: Azure Speech API key
- `AZ_SPEECH_REGION`: Azure Speech API region
- `AZ_TRANSLATE_KEY`: Azure Translate API key
- `AZ_TRANSLATE_REGION`: Azure Translate API region

I also implemented more variables to customize outputs files :
- `YAML_CONFIG_PATH`: Configuration file path
- `TTS_PATH`: TTS files path (directory only)
- `FRENCH_TTS_NAME`: The french TTS filename 
- `ENGLISH_TTS_NAME`: The english TTS filename

> You can find a usage example into the [`docker-compose.yml`](docker-compose.yml) file.

Then, if you ran this stack with `Docker`, access to [localhost](http://localhost) to interact with this part of the project.

## Code

See [`api/src`](api/src) and [`website/html`](website/html)
