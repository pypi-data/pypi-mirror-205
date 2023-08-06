
# RUNFALCON BUILD TOOLS

  

This package contains tools to facilitate building and deployment applications for runfalcon team

  

## REQUIEREMENTS

Before installing RUNFALCON BUILD TOOLS, be sure you have installed:

- Git Client ([Installer](https://git-scm.com/downloads))
- Docker ([Installer](https://docs.docker.com/desktop/install/windows-install/))
- AWS cli V2 ([Installer](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html))

  
## USAGE

`python3 -m runfalconbuildtools <command> <operation> [args]`

Where `args` represents a list of `operation` arguments in format: `key1=value1` `value2=value2` `...`

### Command `s3-artifact`
Downloads an artifact from S3 repository

| Operation | Description | Example |
|--|--|--|
| `get` | Download an specific artifact | To download apache-jmeter-runfalcon version 1.0.0 run: `python3 -m runfalconbuildtools s3-artifact get name=apache-jmeter-runfalcon version=1.0.0 outdir=./jmeter` |

### Command `code-artifact`
Downloads an artifact from AWS Code artifact repository

| Operation | Description | Example |
|--|--|--|
| `get` | Download an specific artifact | To download runfalcon-agent-receiver version 1.0.10 run: `python3 -m runfalconbuildtools code-artifact get domain=runfalcon repository=Runfalcon package=runfalcon-agent-receiver namespace=com.runfalcon.agentreceiver package-version=1.0.10 format=maven outdir=./artifacts` |


### Command `config`
Manage configuration files

| Operation | Description | Example |
|--|--|--|
| `json` | Modify values in a json formatted file | To change `config-1` in json file `my-json.json` run: `python3 -m runfalconbuildtools config json file=my-json.json config-1="new value"` |
| `properties` | Modify values in a properties file | To change `config-1` in properties file `my-props.properties` run: `python3 -m runfalconbuildtools config properties file=my-props.properties config-1="new value"` |
| `download` | Downloads properties file from runfalcon repo | To download config file of `my-app` for `STAGE` environment in curren directory run: `python3 -m runfalconbuildtools config download application=my-app env=STAGE outdir=.` |

### Command `keys`
Handle key files for applications

| Operation | Description | Example |
|--|--|--|
| `get` | Download keys files for an application | To downlaod ssh keys for application `my-app` into current directory, for `STAGE` enviroment run: `python3 -m runfalconbuildtools keys get application=my-app name=ssh env=STAGE outdir=.` |

### Command `ssl`
Handle ssl certificate files for applications

| Operation | Description | Example |
|--|--|--|
| `download` | Download ssl certificate files for an application | To downlaod ssl certificate files for application `my-app` into current directory, for `STAGE` enviroment run: `python3 -m runfalconbuildtools ssl download application=my-app env=STAGE outdir=.` |

