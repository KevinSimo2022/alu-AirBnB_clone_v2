#!/usr/bin/python3
from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder of
    my AirBnB Clone repo
    """
    try:
        # Create a directory to store the archive files
        local("mkdir -p versions")

        # Create the name of the archive file
        file_name = "web_static_{}.tgz".format(
            datetime.utcnow().strftime("%Y%m%d%H%M%S"))

        # Compress the web_static directory into the archive file
        local("tar -cvzf versions/{} web_static".format(file_name))

        # Return the path to the archive file
        return "versions/{}".format(file_name)
    except BaseException:
        return None
