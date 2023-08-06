"""
OTAC Module to implement functions to apply Archive Center settings

Class: OTAC
Methods:

__init__ : class initializer
config : returns config data set
execCommand: exec a command on Archive Center

"""

__author__ = "Dr. Marc Diefenbruch"
__copyright__ = "Copyright 2023, OpenText"
__credits__ = ["Kai-Philip Gatzweiler"]
__maintainer__ = "Dr. Marc Diefenbruch"
__email__ = "mdiefenb@opentext.com"

import requests
import os
import logging

logger = logging.getLogger(os.path.basename(__file__))

requestHeaders = {"Content-Type": "application/x-www-form-urlencoded"}


class OTAC:
    """Used to automate stettings in OpenText Archive Center."""

    _config = None

    def __init__(
        self, protocol: str, hostname: str, port: int, username: str, password: str
    ):
        """Initialize the OTAC object

        Args:
            protocol (string): Either http or https.
            hostname (string): The hostname of the PowerDocs Server Manager to communicate with.
            port (integer): The port number used to talk to the PowerDocs Server Manager.
            username (string): The admin user name of PowerDocs Server Manager.
            password (string): The admin password of PowerDocs Server Manager.
        """

        otacConfig = {}

        if hostname:
            otacConfig["hostname"] = hostname
        else:
            otacConfig["hostname"] = ""

        if protocol:
            otacConfig["protocol"] = protocol
        else:
            otacConfig["protocol"] = "http"

        if port:
            otacConfig["port"] = port
        else:
            otacConfig["port"] = 80

        if username:
            otacConfig["username"] = username
        else:
            otacConfig["username"] = "admin"

        if password:
            otacConfig["password"] = password
        else:
            otacConfig["password"] = ""

        otacBaseUrl = protocol + "://" + otacConfig["hostname"]
        if str(port) not in ["80", "443"]:
            otacBaseUrl += ":{}".format(port)
        otacExecUrl = otacBaseUrl + "/archive/admin/exec"
        otacConfig["execUrl"] = otacExecUrl

        self._config = otacConfig

    def config(self):
        return self._config

    def credentials(self):
        return {
            "username": self.config()["username"],
            "password": self.config()["password"],
        }

    def hostname(self):
        return self.config()["hostname"]

    def setHostname(self, hostname: str):
        self.config()["hostname"] = hostname

    def setCredentials(self, username: str = "", password: str = ""):
        if username:
            self.config()["username"] = username
        else:
            self.config()["username"] = "admin"

        if password:
            self.config()["password"] = password
        else:
            self.config()["password"] = ""

    def baseUrl(self):
        return self.config()["baseUrl"]

    def execUrl(self):
        return self.config()["execUrl"]

    def execCommand(self, command: str):
        payload = {
            "command": command,
            "user": self.config()["username"],
            "passwd": self.config()["password"],
        }

        requestUrl = self.execUrl()
        logger.info(
            "Execute command -> {} on Archive Center (user -> {}); calling -> {}".format(
                command, payload["user"], requestUrl
            )
        )
        execResponse = requests.post(requestUrl, data=payload, headers=requestHeaders)
        if not execResponse.ok:
            logger.error(
                "Failed to execute command -> {}; error -> {}".format(
                    command, execResponse.text.replace("\n", " ")
                )
            )

        return execResponse

    # end method definition
