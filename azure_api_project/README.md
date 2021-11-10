# Azure APIs project <!-- omit in toc -->

- [Before launching this project](#before-launching-this-project)
- [Composition](#composition)
- [Technologies used](#technologies-used)
  - [Web](#web)
  - [App](#app)

This project runs two different smaller projects to provide a more interesting project. The main goal is to count peoples on an image, and if there is too many people on it, play a a text message on speakers.

I have therefore divided this project into two parts : 
- The first one will generate TTS and configuration files for future usage
- The second one will analize an image and play, or not, the previously generated TTS files.

## Before launching this project

You will need the following tools installed on your machine to run this project :
- [`Python`](https://www.python.org/)
- [`Poetry`](https://github.com/python-poetry/poetry)
- [`Docker`](https://www.docker.com/)
- [`Docker Compose`](https://docs.docker.com/compose/)

## Composition

Each parts have a dedicated documentation on how to use it. You will be able to find them into the [`web`](web) and [`app`](app) directories.

## Technologies used

### Web

- Interface web:
  - [HTML](https://developer.mozilla.org/fr/docs/Web/HTML)
  - [Bootstrap](https://getbootstrap.com/)
- API :
  - [Python](https://www.python.org/)
    - [Sanic](https://sanicframework.org/en/)
    - [PyYAML](https://pyyaml.org/)
    - [Azure Translator API](https://azure.microsoft.com/fr-fr/services/cognitive-services/translator/)
    - [Azure Speech SDK](https://docs.microsoft.com/fr-fr/azure/cognitive-services/speech-service/speech-sdk?tabs=linux%2Cubuntu%2Cios-xcode%2Cmac-xcode%2Candroid-studio)
  - [Poetry](https://github.com/python-poetry/poetry)

### App

- [Python](https://www.python.org/)
  - [PyYAML](https://pyyaml.org/)
  - [Playsound](https://github.com/TaylorSMarks/playsound)
  - [Azure Computer Vision SDK](https://docs.microsoft.com/fr-fr/azure/cognitive-services/computer-vision/)
- [Poetry](https://github.com/python-poetry/poetry)
