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

Download the zip file from git or clone the repository
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

   Name                 Command               State                                   Ports
----------------------------------------------------------------------------------------------------------------------------
etl          /bin/sh -c ./imagingetl -C ...   Up      0.0.0.0:9001->9001/tcp
login        /bin/sh -c java -jar -Xmx1 ...   Up      0.0.0.0:8084->8084/tcp
neo4j        /sbin/tini -g -- /docker-e ...   Up      0.0.0.0:7473->7473/tcp, 0.0.0.0:7474->7474/tcp, 0.0.0.0:7687->7687/tcp
nginx        nginx -g daemon off;             Up      0.0.0.0:443->443/tcp, 0.0.0.0:80->80/tcp
server       /bin/sh -c ./imagingservic ...   Up      0.0.0.0:9000->9000/tcp
sourcecode   /bin/sh -c java -jar -Xmx1 ...   Up      0.0.0.0:9980->9980/tcp
Done
```

## Config

Imaging system relies on these ports to be open and free: `[80, 443, 8084, 9000, 9001, 9980, 7473, 7474, 7687]`
If you want to use your own port number, change the corresponding port's mapping in the `docker-compose.yml` file present in your installation direcory (default: `/opt/CAST/container_support/`).

For example, to change port `8084` to `8080` on the host machine, the `8084:8084` mapping will be updated as: 
> 8080:8084

Run the `imaging -s start` command again to apply your changes.
