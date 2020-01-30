#!/usr/bin/env python


# importing the required modules
import argparse
import os
import subprocess
import sys
import re
import shutil
import platform
import stat


services_list = ("login", "sourcecode", "nginx", "server", "etl", "neo4j")

action_list = ("start", "stop", "restart", "status",
               "logs", "kill","pull", "events", "install", "uninstall")
installation_location = "need-to-replace"
compose_file = "-f "+"\"" + installation_location + "docker-compose.yml\" "

images = {'FE_IMAGE_TAG': 'imaging-fe', 'ETL_IMAGE_TAG': 'imagingetl', 'SERVER_IMAGE_TAG': 'imagingservice',
          'LOGIN_IMAGE_TAG': 'imaginglogin',  'NEO4J_IMAGE_TAG': 'imagingneo4j', 'SOURCECODE_IMAGE_TAG': 'imagingsourcecode'}


def action(args):

    action = args[0]
    if len(args) > 1:

        service_name = args[1]

        if service_name in services_list:

            cmd = "docker-compose " + compose_file + action + " " + service_name
            output = run(cmd)

            return output
        else:
            raise Exception("service name not found")
    # stop all the services
    cmd = "docker-compose "+compose_file+action
    if action == "start":
        cmd = "docker-compose "+compose_file+" up -d "
    output = run(cmd)
    return output.decode("utf-8")

# run the docker-compose commands


def run(cmd):

    try:
        output = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

        err = output.stderr.read().strip()
        if err != "":
            return err
        return "Done"

    except Exception as error:

        return error


def get_config_location():

    if platform.system() == "Linux":
        return "/opt/CAST/container_support/"
    if platform.system() == "Darwin":
        return os.path.expanduser('~')+"/CAST/container_support/"
    if platform.system() == "Windows":
        return "C:\Program Files\CAST\container_support"+"\\"
    else:
        raise Exception("Platform not supported")


def get_exec_location():

    if platform.system() in ["Linux", "Darwin"]:
        return "/usr/local/bin/imaging"
    if platform.system() == "Windows":
        return "C:\Program Files\CAST\container_support\imaging"
    else:
        raise Exception("Not able to find location to install executable")


def uninstall(location=None):

    if location is None:
        location = get_config_location()
    try:
        cmd = "docker-compose "+compose_file+" down"
        run(cmd)
        os.remove(get_exec_location())
        return "Imaging service uninstalled successfully"
    except Exception as e:
        return e


def recursive_copy_files(source_path=None, destination_path=None, override=False):
    """
    Recursive copies files from source  to destination directory.
    :param source_path: source directory
    :param destination_path: destination directory
    :param override if True all files will be overridden otherwise skip if file exist
    :return: count of copied files
    """
    if destination_path is None:
        destination_path = get_config_location()
    if not destination_path.endswith('/'):
        destination_path = destination_path+"/"    

    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
    items = os.listdir(os.getcwd())
    for item in items:
        if os.path.isdir(item):
            path = os.path.join(destination_path, item)
            if not os.path.exists(path):

                shutil.copytree(item, path)
        else:
            file = os.path.join(destination_path, item)
            if not os.path.exists(file) or override:
                shutil.copyfile(item, file)

    return "Imaging service install successfully"


def update_config_file_location(dir_location):

    try:
        with open('imaging.py', 'r+') as f:
            data = f.read()
            final = open(get_exec_location(), 'w+')
            final.seek(0)
            if not dir_location.endswith('/'):
                dir_location = dir_location+"/"

            final.write(re.sub("need-to-replace", dir_location, data))
            f.close()
            final.truncate()
            final.close()

        if platform.system() != "Windows":
            os.chmod(get_exec_location(), stat.S_IRWXU |
                     stat.S_IRWXG | stat.S_IRWXO)
    except Exception as e:
        print(e)


class UpdateImage(argparse.Action):

    imagesNeedToUpdate = dict()

    def __call__(self, parser, namespace, values, option_string=None):

        if values:
            for item in values:
                split_items = item.split("=", 1)
                key = split_items[
                    0
                ].strip()  # we remove blanks around keys, as is logical
                value = split_items[1]

                self.imagesNeedToUpdate[key] = value
        try:

            print(self.checkKeys())
        except Exception as error:
            print(error)

    def checkKeys(self):
        try:

            for key, value in self.imagesNeedToUpdate.items():

                if images.get(key) is None:
                    raise Exception("Not a valid image tag")
                return self.checkImages(key, value)

            return action(["start"])
        except Exception as error:
            print(error)

    def checkImages(self, imagename, imagetag):

        try:

            imageslist = subprocess.check_output(
                "docker images " + images[imagename]+":"+imagetag+" --format {{.Repository}}:{{.Tag}}",shell=True)
            if len(imageslist) == 0:
                raise Exception(images[imagename]+":"+imagetag+" is not present on the host")
            return self.checkEnvFile(imagename, imagetag)
        except Exception as error:
            return error

    def checkEnvFile(self, imagename, imagetag):

        try:
            newimage = imagename+"="+imagetag
            if os.path.exists(installation_location+".env"):

                with open( installation_location+".env", 'r+') as f:
                    filedata = f.read()
                    for line in filedata.split('\n'):

                        if line.startswith('#'):
                            continue
                        if re.search(imagename,line) != None :
                            final = open(installation_location+".env",'w+')
                            final.seek(0)
                            final.write(re.sub(line,newimage,filedata))
                            final.truncate()
                            final.close()
                            return "Image Updated successfully.Restart the services"
                    f.close()
            with open(installation_location+".env",'a+') as file:

                file.write('\n'+newimage)
                file.close()
                return "Image Updated successfully.Restart the services"

        except Exception as error:
            return error


def main():

    # create parser object
    parser = argparse.ArgumentParser(description="Imaging setup manager!")

# defining arguments for parser object
    parser.add_argument("-s", "--service", type=str, nargs='+',
                        metavar="command", default=None,
                        help="imaging.py -s status")
    parser.add_argument("-n", "--install", type=str, nargs='+',
                        default=None, help="install Imaging service")
    parser.add_argument("-u", "--uninstall", type=str, nargs='+',
                        default=None, help="uninstall Imaging service")
    parser.add_argument("-d", "--dir", type=str,
                        help="location to install/uninstall Imaging service")
    parser.add_argument(
        "--updateimage",
        metavar="KEY=VALUE",
        nargs="+",
        help="update the image tag",
        action=UpdateImage,
    )

    if len(sys.argv) < 2:
        parser.print_help()
        return
# # parse the arguments from standard input
    args = parser.parse_args()

# calling functions depending on type of argument

    if args.service is not None:
        if args.service[0] in action_list:
            if args.service[0] == "status":
                args.service[0] = "ps"
            print(action(args.service))
            return
        else:
            print("Not a valid command")
            return
    if args.install is not None:
        if args.install[0] == "install":
            print("Installing the Imaging service")
            if args.dir is not None:
                recursive_copy_files(os.getcwd(), args.dir[0], override=False)
                update_config_file_location(args.dir[0])
                return
            try:
                update_config_file_location(get_config_location())
                print(recursive_copy_files(override=True))
                return
            except Exception as e:
                print(e)
            return
        else:
            print("Not a valid command")
            return
    if args.uninstall is not None:
        if args.uninstall[0] == "uninstall":
            print("Uninstalling the Imaging service")
            if args.dir is not None:
                print(uninstall(args.dir[0]))
                return
            print(uninstall())
        else:
            print("Not a valid command")


if __name__ == "__main__":

    # calling the main function
    main()
