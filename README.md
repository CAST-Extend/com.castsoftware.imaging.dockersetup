#### *****Important Update*****
This repository is no longer supported. 
Get the latest Imaging System for Linux here: https://extend.castsoftware.com/#/extension?id=com.castsoftware.imaging.linux&version=latest

# CAST Imaging System
Cast Imaging provides MRI-like visibility into the most complex software systems. Imaging System intelligently organizes complex applications into logical application layers. Save time and money analyzing and mapping complex software and shorten the learning curve for new developers. Break down monolithic applications, visualize future designs and plan migrations from existing designs. Make architectural visibility accessible and scalable across the organization.

## Pre-requisites

* Docker
* docker-compose
* Python

## Operating System

* Ubuntu 64-bit
* centOS 64-bit

## Setup

Download the zip file from [releases](https://github.com/CAST-Extend/com.castsoftware.imaging.dockersetup/releases) or clone the repository and checkout to the version you want to install. 
```
git clone https://github.com/CAST-Extend/com.castsoftware.imaging.dockersetup
cd com.castsoftware.imaging.dockersetup.git
git checkout v1.11.3
```

Run the install script
```
sudo python imaging.py -n install
```
This will install Imaging System to the default location `/opt/CAST/container_support` and the cli tool to `/usr/local/bin`. 

To specify a custom installation location
```
sudo python imaging.py -n install -d "/install/here/"
```
The cli tool will always be installed to `/usr/local/bin`

`Note:` When specifying a custom installation directory, be careful to not use `(~)` to depict the home directory, and provide the full path instead. When running commands with `sudo`, `(~)` will expand to home directory of the root user and not the currently logged in user that you might be expecting. 

#### ETL Automation

Download the three assets from the [releases](https://github.com/CAST-Extend/com.castsoftware.imaging.dockersetup/releases) page: `etl-automation`, `exporter`, `automation-scripts.zip`

Place the two binaries in the `etl-automation` folder of your installation directory, where the `etl_config.json` file is contained. Extract the contents of `automation-scripts.zip` to the same folder. 

Make sure the two binaries have execute permissions: 
```
$ sudo chmod +x etl-automation exporter
```

## Usage

Run `imaging` or `imaging --help` for the start-up options
```
usage: imaging [-h] [-s command [command ...]] [-n INSTALL [INSTALL ...]]
               [-u UNINSTALL [UNINSTALL ...]] [-d DIR]
               [--updateimage KEY=VALUE [KEY=VALUE ...]]

Imaging setup manager!

optional arguments:
  -h, --help            show this help message and exit
  -s command [command ...], --service command [command ...]
                        imaging.py -s status
  -n INSTALL [INSTALL ...], --install INSTALL [INSTALL ...]
                        install Imaging service
  -u UNINSTALL [UNINSTALL ...], --uninstall UNINSTALL [UNINSTALL ...]
                        uninstall Imaging service
  -d DIR, --dir DIR     location to install/uninstall Imaging service
  --updateimage KEY=VALUE [KEY=VALUE ...]
                        Update individual image tags.
  --update KEY=VALUE 
                        Update Imaging System.
```

Start Imaging System with `imaging -s start`
```
Creating network "container_support_default" with the default driver
Creating neo4j      ... done
Creating sourcecode ... done
Creating server     ... done
Creating etl        ... done
Creating login      ... done
Creating nginx      ... done
```
Head over to `localhost` in the browser to use Imaging System. Use the `admin/admin` or `cast/cast` credentials to login for the first time.

#### Logs

Run `imaging -s logs`***`container-name`*** to view the logs for a specific container.

Imaging System container names are `nginx`, `login`, `neo4j`, `etl`, `server`, `sourcecode`.

#### Stop Imaging System

Run `imaging -s stop` to stop Imaging System from running by stopping all containers.

Use `imaging -s stop`***`container-name`*** to stop a specific container.

#### Restart Imaging System

Run `imaging -s restart` to restart Imaging System.

Use `imaging -s restart`***`container-name`*** to restart a specific container.

Any changes to the configuration files of containers will require a specific restart of that container, or whole Imaging System.

`Note:` Changes to `docker-compose.yml` will always require `imaging -s start`.

#### Status

Run `imaging -s status` to get the status of all running containers.

```
$ imaging -s status

CONTAINER ID        IMAGE                                  COMMAND                  CREATED             STATUS              PORTS                                                      NAMES
ccdc922052b6        castimaging/imaging-fe:1.10.0          "nginx -g 'daemon of…"   22 hours ago        Up 22 hours         0.0.0.0:80->80/tcp, 0.0.0.0:443->443/tcp                   nginx
f26820c6c9df        castimaging/imaginglogin:1.10.0        "/bin/sh -c 'java -j…"   22 hours ago        Up 22 hours         8080/tcp, 0.0.0.0:8084->8084/tcp                           login
66a09ae5396e        castimaging/imagingetl:1.10.0          "/bin/sh -c './imagi…"   22 hours ago        Up 22 hours         0.0.0.0:9001->9001/tcp                                     etl
453dc3aea77c        castimaging/imagingservice:1.10.0      "/bin/sh -c './imagi…"   22 hours ago        Up 22 hours         0.0.0.0:9000->9000/tcp, 9001/tcp                           server
b9d993c42173        castimaging/imagingsourcecode:1.10.0   "/bin/sh -c 'java -j…"   22 hours ago        Up 22 hours         0.0.0.0:9980->9980/tcp                                     sourcecode
f15057a6e740        castimaging/imagingneo4j:1.10.0        "/sbin/tini -g -- /d…"   22 hours ago        Up 22 hours         0.0.0.0:7473-7474->7473-7474/tcp, 0.0.0.0:7687->7687/tcp   neo4j
Done
```

#### ETL Automation

Configure the `etl_config.json` file in the `etl-automation` directory accordingly. The file contains the following parameters:

```
PORT //Database Port
HOST //Database Instance
SCHEMA //Database schema name
OUTPUTDIR //Directory to place exported zip file of application
IMAGING_HOSTNAME //Your Imaging Instance URL/IP
IMAGING_PORT //Port of your Imaging Instance
IMAGING_ADMIN_USER //Name of admin user of your Imaging Instance
TOKEN //Same as proxy.config.token.values in login/application.properties file
USERNAME //Database username
PASSWORD //Database password
LOG_PATH (OPTIONAL) //Logfile will be generated if provided
```

Run the `etl-automation` executable with the config file:
```
sudo ./etl-automation -CONFIG etl_config.json
```

#### Exporter

The exporter is a standalone tool that can be run by itself.

Make sure you have the extracted contents of `automation_scripts.zip` and that the binary has execute permissions: `sudo chmod +x exporter`

```
$ ./exporter
usage: --schema my_local --user operator --host my_host --port 2282 --outputdir my_csv_folder_path

Connect to a schema, extract data and generate csvs from local service

optional arguments:
  -h, --help            show this help message and exit
  --log LOG             output log file path (default: None)
  --outputdir OUTPUTDIR
                        output directory (default: None)
  --debug               print debug messages (default: False)
  --debuginfo DEBUGINFO
                        control check files YES or NO default is NO (default:
                        NO)
  --cfg CFG             Regeneration of config files YES or NO default is NO
                        (default: NO)
  --aiptable AIPTABLE   force the extraction of AIP Tables YES or NO default
                        is NO (default: NO)
  --user USER           username used to connect to CSS server (default:
                        operator)
  --password PASSWORD   password used to connect to CSS server (default:
                        CastAIP)
  --host HOST           host for CSS server (default: localhost)
  --port PORT           knowledge base port (default: 2282)
  --schema SCHEMA       knowledge base name (default: None)
  --version             show program's version number and exit
```

Example:
```
$ mkdir zips
$ ./exporter --host 192.168.0.1 --schema your_app_local --port 2282  --outputdir zips
```

#### Uninstalling

Run `imaging -u uninstall` to uninstall Imaging System.

If you encounter permission issues while uninstalling, use `sudo su -` to enter an interactive login shell as root user and run the command. 

`Note:` The uninstall does not delete your installation directory. 

## Config

Imaging system relies on these ports to be open and free: `[80, 443, 8084, 9000, 9001, 9980, 7473, 7474, 7687]`
If you want to use your own port number, change the corresponding port's mapping in the `docker-compose.yml` file present in your installation directory (default: `/opt/CAST/container_support/`).

For example, to change port `8084` to `8080` on the host machine, the `8084:8084` mapping will be updated as: 
> 8080:8084

Run the `imaging -s start` command again to apply your changes.

## Security Modes

Imaging System supports three security modes: `local`, `LDAP`, and `SAML`.

Any change in the security mode must **ALWAYS** be accompanied by running the `server/switchSecurityMode.sh` script.

## Upgrades

To either upgrade or downgrade Imaging System version, pass the version number as an argument(**KEY=VALUE**) to the update command. Example: `imaging --update v=1.10.0`.

This will restart version 1.10.0 of Imaging System. Versions are maintained in the `.env` file. Use the update command to update this file and restart Imaging System anytime.
