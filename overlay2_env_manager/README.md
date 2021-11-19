# overlay2_env_manager

This is a very basic environment manager.

Written in [Python3](https://www.python.org/) and based on a [Debian filesystem](https://refspecs.linuxfoundation.org/FHS_3.0/fhs/index.html), it offers you 4 differents commands:
- `box setup` : it will create all files required by `box`
- `box build [configuration_file]` : build a new environment based on a `yaml` configuration file. 
- `box run [env]` : run a previously built environment.
- `box env [command]` : interact with already built environments.

## Installation

I used [poetry](https://python-poetry.org/) as a dependency manager for the whole project. 

To install this project, you can run the following commands:
```console
$ poetry install
```

> If you still don't want to use `poetry`, you can find all required dependencies into the [project file](pyproject.toml)

## How to use it

Now, we will see what is required to run your custom environments !

### Configuration

First, you will have to write a *configuration file* in [YAML](https://yaml.org/). Let's have a look at an example : 
```yaml
---
name: str
repositories:
 - key: str
   repository: str
requirements:
 - str
user: str
run: str
```

As we can see, you can adapt few parameters to your needs:
- `name`: *required*, provide the env. name
- `repositories`: provide additional repository from custom sources
  - `key`: the key url to download
  - `repository`: see [SourceList](https://wiki.debian.org/fr/SourcesList)
- `requirements`: a list of program to install into your custom env.
- `user`: create a custom user. if not specified, use `root`
- `run`: *required*, the command to run at startup

> Please keep in mind that you have to provide valid key and repository, unless the build will not perform.

Sample configuration files can be found under the [build_files](build_files/) directory.

### Runtime

> Because of complex file manipulations, mounts, etc. box must be run as root (using `sudo` or `su`)

First of all, you will have to run the setup:
```console
# poetry run box setup
```

This will create the `/var/lib/box` directory will all required files for runtime.

Then, you can build for example [`user_tester.yaml`](build_files/user_tester.yaml):
```console
# poetry run box build build_files/user_tester.yaml
```

After that, you can test it by running this `run` command:
```console
# poetry run box run user-tester
[...]

Launching user-tester
––––––––––––––––––––––––––––––––––


toto


––––––––––––––––––––––––––––––––––
```

> The `run` command can take to optionnal args : `--share` and `--addargs`
> - `--share` is to share a file or directory from your host to your env.
> - `--addargs` is to provide additional args to your `run` command if you provided the `$ARGS` keyword (see [mongodb](build_files/mongo.yaml) for example)

Finally, you can list your environement : 
```console
# poetry run box env list

Name         Location                      User    Run
-----------  ----------------------------  ------  ----------
echo         /var/lib/box/env/echo         root    echo $ARGS
user-tester  /var/lib/box/env/user-tester  toto    whoami
```

Or delete an existing environement : 
```console
# poetry run box env delete echo
# poetry run box env list

Name         Location                      User    Run
-----------  ----------------------------  ------  ----------
user-tester  /var/lib/box/env/user-tester  toto    whoami
```

## Code

All source code is located under the [box](box) directory.
