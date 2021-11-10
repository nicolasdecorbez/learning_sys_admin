# Image analyzer & tts file reader <!-- omit in toc -->

- [What is this ?](#what-is-this-)
- [Installation](#installation)
- [Usage](#usage)
- [Options](#options)
- [Configuration](#configuration)
- [Code](#code)

## What is this ?

A python script that analyzes an image and counts the number of people on it using Azure Computer Vision.

If the number exceeds the limit specified into the [configuration file](../assets/Configuration/configuration.yml), the program will play both [TTS files](../assets/Audio/)

## Installation

J'ai utilisé [poetry](https://github.com/python-poetry/poetry) afin de gérer mes dépendances. Pour installer le projet, il suffit de lancer :
```console
$ cd step 2
$ poetry install
```

## Usage

Before running this script, make sure you have, at least :
- a `.jpg` / `.jpeg` image to analyze.
- a `YAML` configuration file (`.yml` / `.yaml`).
- two `.wav` audio files (usually TTS).

```console
poetry run social-distancing <OPTIONS>
```

## Options

- `-h, --help` : print help about this program
- `-c FILE, --config FILE` : configuration file (see [web](../web))
- `-i FILE, --image FILE` : image to analyze
- `-f FILE, --french FILE` : french TTS file
- `-e FILE, --english FILE` : english TTS file

## Configuration

Secrets like API Keys are to modify here : [.secrets/api.yml](.secrets/api.yml).

To generate all required file in a proper way, except the image, please take a look at the [web part](../web) of this project.

## Code

See [src](src).
