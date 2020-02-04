# CAST Imaging System
Cast Imaging provides MRI-like visibility into the most complex software systems. Imaging System intelligently organizes complex applications into logical application layers. Save time and money analyzing and mapping complex software and shorten the learning curve for new developers. Break down monolithic applications, visualize future designs and plan migrations from existing designs. Make architectural visibility accessible and scalable across the organization.

## Pre-requisites

* Docker
* docker-compose
* Python

## Operating System

* Ubuntu
* centOS

## Setup

Clone the repository
```
git clone https://github.com/CAST-Extend/com.castsoftware.imaging.dockersetup.git
```

Navigate to the directory and run the install script
```
python imaging.py -n install
```
This will install Imaging System to the default location `/opt/CAST/container_support` and the cli tool to `/usr/local/bin`. 

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
                        update the image tag
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
Head over to `localhost` in the browser to use Imaging System. 

#### Logs

Run `imaging -s logs {containerName}` to view the logs for a specific container.

Imaging System container names are `nginx`, `login`, `neo4j`, `etl`, `server`, `sourcecode`.

## Config

Imaging system relies on these ports to be open and free: `[80, 443, 8080, 9000, 9001, 9980, 7473, 7474, 7687]`
If you want to use your own port number, change the corresponding port's mapping in the `docker-compose.yml` file.

For example, to change port `8080` to `8090` on the host machine, the mapping will be updated as: 
> 8090:8080
