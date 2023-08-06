"""
OTCS Module to implement functions to read / write Content Server objects
such as Users, Groups, Nodes, Workspaces, ...

Class: OTCS
Methods:

__init__ : class initializer
config : returns config data set
cookie : returns cookie information
credentials: returns set of username and password
setCredentials: set new credentials
isConfigured: returns true if the OTCS pod is ready to serve requests
baseUrl : returns OTCS base URL
csUrl: return the Extended ECM (OTCS) URL
restUrl : returns OTCS REST base URL

parseRequestResponse: process result into Json
lookupResultValue: lookup a property value based on a provided key / value pair in the response properties of an Extended ECM REST API call
existResultItem: returns True if an item with a key/value pair is in a REST response. False otherwise.
getResultValue: read a value from the REST response. This handles many specifics of OTCS REST APIs

authenticate : authenticates at OTCS server

applyConfig: Apply Content Server administration settings from XML file

getGroup: Lookup Content Server group
getUser: Lookup Content Server user
addGroup: Add Content Server group
addUser: Add Content Server user
searchUser: Find a user based on search criteria
updateUser: Update a defined field for a user
updateUserProfile: Update a defined field for a user profile
updateUserPhoto: Update a user with a profile photo (which must be an existing node)
isProxy: check if a user (login name) is a proxy of the current user
getUserProxies: get the list of proxy users for the current user
updateUserProxy: add a proxy to the current (authenticated) user
addFavorite: Add a favorite for the current (authenticated) user
getGroupMembers: Get Content Server group members
addGroupMember: Add a user or group to a target group

getNode: Get a node based on the node ID
getNodeByParentAndName: Get a node based on the parent ID and name
getNodeByVolumeAndPath: Get a node based on the volume ID and path
getNodeFromNickname: Get a node based on the nickname
getSubnodes: get children nodes of a parent node
renameNode: Change the name and description of a node
getVolumes: Get all Volumes
getVolume: Get Volume information based on the volume type ID
uploadFileToVolume: Fetch a file from a URL or local filesystem and upload
                    it to a Extended ECM volume
uploadFileToParent: upload a document to a parent folder
addDocumentVersion: add a version to an Extended ECM document
downloadDocument: download a document

search: search for a search term using Extended ECM search engine

getExternalSystemConnection: Get Extended ECM external system connection
addExternalSystemConnection: Add Extended ECM external system connection

createTransportWorkbench: Create a Workbench in the Transport Volume
unpackTransportPackage: Unpack an existing Transport Package into an existing Workbench
deployWorkbench: Deploy an existing Workbench
deployTransport: Main method to deploy a transport. This uses subfunctions to upload,
                 unpackage and deploy the transport, and creates the required workbench
replaceInXmlFiles: Replaces all occurrences of the search pattern with the replace string in all
                   XML files in the directory and its subdirectories.
replaceTransportPlaceholders: Search and replace strings in the XML files of the transport packlage

getWorkspaceTypes: Get all workspace types configured in Extended ECM
getBusinessObjectType: Get information for a specific business object type
getWorkspaceCreateForm: Get the Workspace create form
getWorkspace: get a workspace node
getWorkspaceByNameAndType: Lookup workspace based on workspace name and workspace type name
createWorkspace: Create a new business workspace
createWorkspaceRelationship: Create a relationship between two workspaces
getWorkspaceRelationships: get a list of related workspaces
getWorkspaceRoles: Get the Workspace roles
addMemberToWorkspace: Add member to workspace role. Check that the user is not yet a member
removeMemberFromWorkspace: Remove member from workspace role
assignWorkspacePermissions: update workspace permissions for a given role

createItem: create an item in Extended ECM (e.g. folder or URL item)
updateItem: update an item in Extended ECM (e.g. folder or URL item)

getWebReportParameters: Get parameters of a Web Report
runWebReport: Run a Web Report that is identified by its nick name
installCSApplication: Install a CS Application (based on WebReports)

assignItemToUserGroup: assign an item (e.g. Workspace or document) to a list of users or groups

assignPermission: assign permissions to an item for a defined user or group
convertPermissionStringToPermissionValue: convert a list of permission names to a permission value
convertPermissionValueToPermissionString: convert a permission value to a list of permission strings

assignClassification: assign a classification to an item
assignRMClassification: assign a Records management classification to an item

registerWorkspaceTemplate: register a workspace template for Extended ECM for Engineering

getRecordsManagementRSIs: get the ist of RSIs together with their RSI schedules
getRecordsManagementCodes: get Records Management Codes
updateRecordsManagementCodes: update the Records Management Codes
createRecordsManagementRSI: create a new Records Management RSI item
createRecordsManagementRSISchedule: create a schedule for an existing RSI item
createRecordsManagementHold: create a Records Management Hold
importRecordsManagementCodes: import RM codes from a config file
importRecordsManagementRSIs: import RM RSIs from a config file
importRecordsManagementSettings: import Records Management settings from a config file
importPhysicalObjectsCodes: import Physical Objects codes from a config file
importPhysicalObjectsSettings: import Physical Objects settings from a config file
importPhysicalObjectsLocators: import Physical Objects locators from a config file
importSecurityClearanceCodes: import Securioty Clearance codes from a config file

assignUserSecurityClearance: assign a Security Clearance level to a user
assignUserSupplementalMarkings: assign a list of Supplemental Markings to a user

"""

__author__ = "Dr. Marc Diefenbruch"
__copyright__ = "Copyright 2023, OpenText"
__credits__ = ["Kai-Philip Gatzweiler"]
__maintainer__ = "Dr. Marc Diefenbruch"
__email__ = "mdiefenb@opentext.com"

import os
import logging
import requests
import json
import urllib.parse
from datetime import datetime
import zipfile
import re

logger = logging.getLogger(os.path.basename(__file__))

requestJsonHeaders = {
    "accept": "application/json;charset=utf-8",
    "Content-Type": "application/json",
}

requestFormHeaders = {
    "accept": "application/json;charset=utf-8",
    "Content-Type": "application/x-www-form-urlencoded",
}

requestDownloadHeaders = {
    "accept": "application/octet-stream",
    "Content-Type": "application/json",
}


class OTCS(object):
    """Used to automate stettings in OpenText Extended ECM."""

    _config = None
    _cookie = None

    def __init__(
        self, protocol: str, hostname: str, port: int, username: str, password: str, user_partition: str = "Content Server Members", resource_name: str = "cs", default_license: str = "X3"
    ):
        """Initialize the OTCS object

        Args:
            protocol (string): Either http or https.
            hostname (string): The hostname of Extended ECM server to communicate with.
            port (integer): The port number used to talk to the Extended ECM server.
            username (string): The admin user name of Extended ECM.
            password (string): The admin password of Extended ECM.
            user_partition (string): Name of the OTDS partition for OTCS users.
        """

        # Initialize otcsConfig as an empty dictionary
        otcsConfig = {}

        if hostname:
            otcsConfig["hostname"] = hostname
        else:
            otcsConfig["hostname"] = "otcs-admin-0"

        if protocol:
            otcsConfig["protocol"] = protocol
        else:
            otcsConfig["protocol"] = "http"

        if port:
            otcsConfig["port"] = port
        else:
            otcsConfig["port"] = 8080

        if username:
            otcsConfig["username"] = username
        else:
            otcsConfig["username"] = "admin"

        if password:
            otcsConfig["password"] = password
        else:
            otcsConfig["password"] = ""

        if user_partition:
            otcsConfig["partition"] = user_partition
        else:
            otcsConfig["partition"] = ""

        if resource_name:
            otcsConfig["resource"] = resource_name
        else:
            otcsConfig["resource"] = ""

        if default_license:
            otcsConfig["license"] = default_license
        else:
            otcsConfig["license"] = ""

        otcsBaseUrl = protocol + "://" + otcsConfig["hostname"]
        if str(port) not in ["80", "443"]:
            otcsBaseUrl += ":{}".format(port)
        otcsConfig["baseUrl"] = otcsBaseUrl

        otcsConfig["configuredUrl"] = otcsBaseUrl + "/cssupport/csconfigured"

        otcsUrl = otcsBaseUrl + "/cs/cs"
        otcsConfig["csUrl"] = otcsUrl

        otcsRestUrl = otcsUrl + "/api"
        otcsConfig["restUrl"] = otcsRestUrl

        otcsConfig["authenticationUrl"] = otcsRestUrl + "/v1/auth"
        otcsConfig["usersUrl"] = otcsRestUrl + "/v1/members"
        otcsConfig["groupsUrl"] = otcsRestUrl + "/v1/members"
        otcsConfig["membersUrl"] = otcsRestUrl + "/v2/members"
        otcsConfig["nodesUrl"] = otcsRestUrl + "/v1/nodes"
        otcsConfig["nodesUrlv2"] = otcsRestUrl + "/v2/nodes"
        otcsConfig["nicknameUrl"] = otcsRestUrl + "/v2/nicknames"
        otcsConfig["importSettingsUrl"] = otcsRestUrl + \
            "/v2/import/settings/admin"
        otcsConfig["searchUrl"] = otcsRestUrl + "/v2/search"
        otcsConfig["volumeUrl"] = otcsRestUrl + "/v2/volumes"
        otcsConfig["externalSystem"] = otcsRestUrl + "/v2/externalsystems"
        otcsConfig["businessworkspacetypes"] = (
            otcsRestUrl + "/v2/businessworkspacetypes"
        )
        otcsConfig["businessworkspacecreateform"] = (
            otcsRestUrl + "/v2/forms/businessworkspaces/create"
        )
        otcsConfig["businessworkspaces"] = otcsRestUrl + \
            "/v2/businessworkspaces"
        otcsConfig["favoritesUrl"] = otcsRestUrl + "/v2/members/favorites"
        otcsConfig["webReportsUrl"] = otcsRestUrl + "/v1/webreports"
        otcsConfig["csApplicationsUrl"] = otcsRestUrl + "/v2/csapplications"
        otcsConfig["xEngProjectTemplateUrl"] = (
            otcsRestUrl + "/v2/xengcrt/projecttemplate"
        )
        otcsConfig["rsisUrl"] = otcsRestUrl + "/v2/rsis"
        otcsConfig["rsiSchedulesUrl"] = otcsRestUrl + "/v2/rsischedules"
        otcsConfig["recordsManagementUrl"] = otcsRestUrl + \
            "/v1/recordsmanagement"
        otcsConfig["recordsManagementUrlv2"] = otcsRestUrl + \
            "/v2/recordsmanagement"
        otcsConfig["userSecurityUrl"] = otcsRestUrl + \
            "/v2/members/usersecurity"
        otcsConfig["physicalObjectsUrl"] = otcsRestUrl + "/v1/physicalobjects"
        otcsConfig["securityClearancesUrl"] = otcsRestUrl + \
            "/v1/securityclearances"
        otcsConfig["holdsUrl"] = otcsRestUrl + "/v1/holds"
        otcsConfig["holdsUrlv2"] = otcsRestUrl + "/v2/holds"

        self._config = otcsConfig

    def config(self):
        return self._config

    def cookie(self):
        return self._cookie

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

    def csUrl(self):
        return self.config()["csUrl"]

    def restUrl(self):
        return self.config()["restUrl"]

    def requestFormHeader(self):
        """Deliver the request header used for the CRUD REST API calls.
           Consists of Cookie + Form Headers (see global vasriable)

        Args:
            None.
        Return:
            Dict of request header values.
        """

        # create union of two dicts: cookie and headers
        # (with Python 3.9 this would be easier with the "|" operator)
        requestHeader = {}
        requestHeader.update(self.cookie())
        requestHeader.update(requestFormHeaders)

        return requestHeader

    # end method definition

    def requestJsonHeader(self):
        """Deliver the request header used for the CRUD REST API calls.
           Consists of Cookie + Json Headers (see global vasriable)

        Args:
            None.
        Return:
            Dict of request header values.
        """

        # create union of two dicts: cookie and headers
        # (with Python 3.9 this would be easier with the "|" operator)
        requestHeader = {}
        requestHeader.update(self.cookie())
        requestHeader.update(requestJsonHeaders)

        return requestHeader

    # end method definition

    def requestDownloadHeader(self):
        """Deliver the request header used for the CRUD REST API calls.
           Consists of Cookie + Form Headers (see global vasriable)

        Args:
            None.
        Return:
            Dict of request header values.
        """

        # create union of two dicts: cookie and headers
        # (with Python 3.9 this would be easier with the "|" operator)
        requestHeader = {}
        requestHeader.update(self.cookie())
        requestHeader.update(requestDownloadHeaders)

        return requestHeader

    # end method definition

    def parseRequestResponse(
        self,
        response_object: object,
        additional_error_message: str = "",
        show_error: bool = True,
    ) -> dict:
        """Converts the request response to a Python dict in a safe way
           that also handles exceptions.

            Content Server may produce corrupt response when it gets restarted
            or hitting resource limits. So we try to avoid a fatal error and bail
            out more gracefully.

        Args:
            response_object (object): this is reponse object delivered by the request call
        Return: a python dict object or null in case of an error
        """

        if not response_object:
            return None

        try:
            dict_object = json.loads(response_object.text)
        except json.JSONDecodeError as e:
            if additional_error_message:
                message = "Cannot decode response as JSon. {}; error -> {}".format(
                    additional_error_message, e
                )
            else:
                message = "Cannot decode response as JSon; error -> {}".format(
                    e)
            if show_error:
                logger.error(message)
            else:
                logger.warning(message)
            return None
        else:
            return dict_object

    def lookupResultValue(self, response: dict, key: str, value: str, return_key: str) -> str:
        """Lookup a property value based on a provided key / value pair in the response properties of an Extended ECM REST API call.

        Args:
            response (dictionary): REST response from an OTCS REST Call
            key (string): property name (key)
            value (string): value to find in the item with the matching key
            return_key (string): determines which value to return based on the name of the dict key

        Returns:
            str: value of the property with the key defined in "return_key"
        """

        if not response:
            return None
        if not "results" in response:
            return None

        results = response["results"]
        # check if results is a list or a dict (both is possible - dependent on the actual REST API):
        if isinstance(results, dict):
            # result is a dict - we don't need index value:
            data = results["data"]
            if isinstance(data, dict):
                # data is a dict - we don't need index value:
                properties = data["properties"]
                if key in properties and properties[key] == value and return_key in properties:
                    return properties[return_key]
                else:
                    return None
            elif isinstance(data, list):
                # data is a list - this has typically just one item, so we use 0 as index
                for item in data:
                    properties = item["properties"]
                    if key in properties and properties[key] == value and return_key in properties:
                        return properties[return_key]
                return None
            else:
                logger.error(
                    "Data needs to be a list or dict but it is -> {}".format(type(data)))
                return None
        elif isinstance(results, list):
            # result is a list - we need index value
            for result in results:
                data = result["data"]
                if isinstance(data, dict):
                    # data is a dict - we don't need index value:
                    properties = data["properties"]
                    if key in properties and properties[key] == value and return_key in properties:
                        return properties[return_key]
                elif isinstance(data, list):
                    # data is a list we iterate through the list and try to find the key:
                    for item in data:
                        properties = item["properties"]
                        if key in properties and properties[key] == value and return_key in properties:
                            return properties[return_key]
                else:
                    logger.error(
                        "Data needs to be a list or dict but it is -> {}".format(type(data)))
                    return None
            return None
        else:
            logger.error(
                "Result needs to be a list or dict but it is -> {}".format(type(results)))
            return None

    def existResultItem(self, response: dict, key: str, value: str, property_name: str = "properties") -> bool:
        """Check existence of key / value pair in the response properties of an Extended ECM REST API call.

        Args:
            response (dictionary): REST response from an OTCS REST Call
            key (string): property name (key)
            value (string): value to find in the item with the matching key

        Returns:
            boolean: True if the value was found, False otherwise
        """

        if not response:
            return False
        if not "results" in response:
            return False

        results = response["results"]
        # check if results is a list or a dict (both is possible - dependent on the actual REST API):
        if isinstance(results, dict):
            # result is a dict - we don't need index value:
            if not "data" in results:
                return False
            data = results["data"]
            if isinstance(data, dict):
                # data is a dict - we don't need index value:
                properties = data[property_name]
                if isinstance(properties, dict):
                    if key in properties:
                        return properties[key] == value
                    else:
                        return False
                elif isinstance(properties, list):
                    # properties is a list we iterate through the list and try to find the key:
                    for item in properties:
                        if key in item and item[key] == value:
                            return True
                else:
                    logger.error(
                        "Properties needs to be a list or dict but it is -> {}".format(type(properties)))
                    return False
            elif isinstance(data, list):
                # data is a list - this has typically just one item, so we use 0 as index
                for item in data:
                    properties = item[property_name]
                    if key in properties and properties[key] == value:
                        return True
                return False
            else:
                logger.error(
                    "Data needs to be a list or dict but it is -> {}".format(type(data)))
                return False
        elif isinstance(results, list):
            # result is a list - we need index value
            for result in results:
                if not "data" in result:
                    continue
                data = result["data"]
                if isinstance(data, dict):
                    # data is a dict - we don't need index value:
                    properties = data[property_name]
                    if key in properties and properties[key] == value:
                        return True
                elif isinstance(data, list):
                    # data is a list we iterate through the list and try to find the key:
                    for item in data:
                        properties = item[property_name]
                        if key in properties and properties[key] == value:
                            return True
                else:
                    logger.error(
                        "Data needs to be a list or dict but it is -> {}".format(type(data)))
                    return False
            return False
        else:
            logger.error(
                "Result needs to be a list or dict but it is -> {}".format(type(results)))
            return False

    def getResultValue(self, response: dict, key: str, index: int = 0, property_name: str = "properties") -> str:
        """Read an item value from the REST API response. This is considering
           the most typical structures delivered by V2 REST API of Extended ECM.
           See developer.opentext.com for more details.

        Args:
            response (dictionary): REST API response object
            key (string): key to find (e.g. "id", "name", ...)
            index (integer, optional): In case a list of results is delivered the index
                                       to use (1st element has index  0). Defaults to 0.

        Returns:
            string: value of the item with the given key
        """

        # First do some sanity checks:
        if not response:
            logger.info("Empty REST response - returning None")
            return None
        if not "results" in response:
            logger.error("No 'results' key in REST response - returning None")
            return None

        results = response["results"]
        if not results:
            logger.info("No results found!")
            return None

        # check if results is a list or a dict (both is possible - dependent on the actual REST API):
        if isinstance(results, dict):
            # result is a dict - we don't need index value

            # this is a special treatment for the businessworkspaces REST API - it returns
            # for "Create business workspace" the ID directly in the results dict (without data substructure)
            if key in results:
                return results[key]
            data = results["data"]
            if isinstance(data, dict):
                # data is a dict - we don't need index value:
                properties = data[property_name]
            elif isinstance(data, list):
                # data is a list - this has typically just one item, so we use 0 as index
                properties = data[0][property_name]
            else:
                logger.error(
                    "Data needs to be a list or dict but it is -> {}".format(type(data)))
                return None
            logger.debug(
                "Properties of results (dict) -> {}".format(properties))
            # For nearly all OTCS REST Calls perperties is a dict:
            if isinstance(properties, dict):
                if not key in properties:
                    logger.error(
                        "Key -> {} is not in result properties!".format(key))
                    return None
                return properties[key]
            # but there are some strange ones that have other names for
            # properties and may use a list - see e.g. /v2/holds
            elif isinstance(properties, list):
                if index > len(properties) - 1:
                    logger.error(
                        "Illegal Index -> {} given. List has only -> {} elements!".format(index, len(properties)))
                    return None
                return properties[index][key]
            else:
                logger.error(
                    "Properties needs to be a list or dict but it is -> {}".format(type(properties)))
                return False
        elif isinstance(results, list):
            # result is a list - we need a valid index:
            if index > len(results) - 1:
                logger.error(
                    "Illegal Index -> {} given. List has only -> {} elements!".format(index, len(results)))
                return None
            data = results[index]["data"]
            if isinstance(data, dict):
                # data is a dict - we don't need index value:
                properties = data[property_name]
            elif isinstance(data, list):
                # data is a list - this has typically just one item, so we use 0 as index
                properties = data[0][property_name]
            else:
                logger.error(
                    "Data needs to be a list or dict but it is -> {}".format(type(data)))
                return None
            logger.debug(
                "Properties of results (list, index -> {}) -> {}".format(index, properties))
            if not key in properties:
                logger.error(
                    "Key -> {} is not in result properties!".format(key))
                return None
            return properties[key]
        else:
            logger.error(
                "Result needs to be a list or dict but it is -> {}".format(type(results)))
            return None

    # end method definition

    def isConfigured(self) -> bool:
        """Checks if the Content Server pod is ready to receive requests.

        Args:
            None.
        Return: True if pod is ready. False if pod is not yet ready.
        """

        requestUrl = self.config()["configuredUrl"]

        logger.info("Trying to retrieve OTCS url -> {}".format(requestUrl))

        try:
            checkcsConfiguredResponse = requests.get(
                requestUrl, headers=requestJsonHeaders
            )
        except Exception as e:
            logger.warning(
                "Unable to connect to -> {} : {}".format(requestUrl, e))
            logger.warning("OTCS service may not be ready yet.")
            return False

        if checkcsConfiguredResponse.ok:
            return True
        else:
            return False

    # end method definition

    def authenticate(self, revalidate: bool = False):
        """Authenticate at Content Server and retrieve OTCS Ticket.

        Args:
            revalidate (boolean): determinse if a re-athentication is enforced
                                  (e.g. if session has timed out with 401 error)
        Return: Cookie information. Also stores cookie information in self._cookie
        """

        # Already authenticated and session still valid?
        if self._cookie and not revalidate:
            return self._cookie

        otcs_ticket = "NotSet"

        logger.info(
            "Requesting OTCS ticket from -> {}".format(
                self.config()["authenticationUrl"]
            )
        )

        authenticateResponse = None
        try:
            authenticateResponse = requests.post(
                self.config()["authenticationUrl"],
                data=self.credentials(),
                headers=requestFormHeaders,
            )
        except Exception as e:
            logger.warning(
                "Unable to connect to -> {} : {}".format(
                    self.config()["authenticationUrl"], e
                )
            )
            logger.warning("OTCS service may not be ready yet.")
            return None

        if authenticateResponse.ok:
            authenticate_dict = self.parseRequestResponse(
                authenticateResponse, "This can be normal during restart", False
            )
            if not authenticate_dict:
                return None
            else:
                otcs_ticket = authenticate_dict["ticket"]
                logger.info("Ticket -> {}".format(otcs_ticket))
        else:
            logger.error(
                "Failed to request an OTCS ticket; error -> {}".format(
                    authenticateResponse.text
                )
            )
            return None

        # Store authentication ticket:
        self._cookie = {
          "otcsticket": otcs_ticket,
          "LLCookie": otcs_ticket
          }
        self.otcsticket = otcs_ticket
        return self._cookie

    # end method definition

    def applyConfig(self, xmlfilepath: str):
        """Apply Content Server administration settings from XML file

        Args:
            xmlfilepath (string): name + path of the XML settings file
        Return:
            Import response (json) or None if the import fails.
            response["results"]["data"]["restart"] indicates if the settings
            require a restart of the OTCS services.
        """

        logger.info(
            "Applying admin settings from file -> {}".format(xmlfilepath))
        filename = os.path.basename(xmlfilepath)

        if not os.path.exists(xmlfilepath):
            logger.error(
                "The file -> {} does not exist in path -> {}!".format(
                    filename, os.path.dirname(xmlfilepath)
                )
            )
            return None

        llconfig_file = {"file": (filename, open(xmlfilepath), "text/xml")}

        requestUrl = self.config()["importSettingsUrl"]
        requestHeader = self._cookie

        retries = 0
        while True:
            importResponse = requests.post(
                requestUrl,
                files=llconfig_file,
                headers=requestHeader,
                cookies=self.cookie(),
            )
            if importResponse.ok:
                logger.debug(
                    "Admin settings in file -> {} have been applied".format(xmlfilepath))
                return self.parseRequestResponse(importResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif importResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to import settings file -> {}; status -> {}; error -> {}".format(
                        xmlfilepath, importResponse.status_code, importResponse.text
                    )
                )
                return None

    # end method definition

    def getGroup(self, name: str, show_error: bool = False):
        """Lookup Content Server group.

        Args:
            name (string): name of the group
            showError (boolean): if True, treat as error if group is not found
        Return:
            Group information (json) or None if the group is not found.
            The returned information has a structure like this:
            "data": [
                {
                    "id": 0,
                    "name": "string",
                    ...
                }
            ]
            To access the id of the first group found use ["data"][0]["id"]
        """

        # Add query parameters (these are NOT passed via JSon body!)
        # type = 1 ==> Group
        requestUrl = self.config()["groupsUrl"] + \
            "?where_type=1&query={}".format(name)
        requestHeader = self.requestFormHeader()

        logger.info(
            "Get group with name -> {}; calling -> {}".format(name, requestUrl))

        retries = 0
        while True:
            getGroupResponse = requests.get(
                requestUrl, headers=requestHeader, cookies=self.cookie()
            )
            if getGroupResponse.ok:
                return self.parseRequestResponse(getGroupResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif getGroupResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                if show_error:
                    logger.error(
                        "Failed to get group -> {}; status -> {}; error -> {}".format(
                            name, getGroupResponse.status_code, getGroupResponse.text
                        )
                    )
                else:
                    logger.info("Group -> {} not found.".format(name))
                return None

    # end method definition

    def getUser(self, name: str, show_error: bool = False):
        """Lookup Content Server user based on the name.

        Args:
            name (string): name of the user
            show_error (boolean): treat as error if user is not found
        Return:
            User information (json) or None if the user is not found.
            The returned information has a structure like this:
            "data": [
                {
                    "id": 0,
                    "name": "string",
                    "first_name": "string",
                    "last_name": "string",
                    "type": "string",
                    "name_formatted": "string",
                    "initials": "string"
                }
            ]
            To access the (login) name of the first user found use ["data"][0]["name"]
        """

        # Add query parameters (these are NOT passed via JSon body!)
        # type = 0 ==> User
        requestUrl = self.config()["usersUrl"] + \
            "?where_type=0&query={}".format(name)
        requestHeader = self.requestFormHeader()

        logger.info(
            "Get user with name -> {}; calling -> {}".format(name, requestUrl))

        retries = 0
        while True:
            getUserResponse = requests.get(
                requestUrl, headers=requestHeader, cookies=self.cookie()
            )
            if getUserResponse.ok:
                return self.parseRequestResponse(getUserResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif getUserResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                if show_error:
                    logger.error(
                        "Failed to get user -> {}; status -> {}; error -> {}".format(
                            name, getUserResponse.status_code, getUserResponse.text
                        )
                    )
                else:
                    logger.info("User -> {} not found.".format(name))
                return None

    # end method definition

    def addGroup(self, name: str):
        """Add Content Server group.

        Args:
            name (string): name of the group
        Return:
            Group information (json) or None if the group couldn't be created (e.g. because it exisits already).
        """

        groupPostBody = {"type": 1, "name": name}

        requestUrl = self.config()["groupsUrl"]
        requestHeader = self.requestFormHeader()

        logger.info(
            "Adding group -> {}; calling -> {}".format(name, requestUrl))
        logger.debug("Group Attributes -> {}".format(groupPostBody))

        retries = 0
        while True:
            groupResponse = requests.post(
                requestUrl,
                data=groupPostBody,
                headers=requestHeader,
                cookies=self.cookie(),
            )
            if groupResponse.ok:
                return self.parseRequestResponse(groupResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif groupResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to add group -> {}; status -> {}; error -> {}".format(
                        name, groupResponse.status_code, groupResponse.text
                    )
                )
                return None

    # end method definition

    def addUser(
        self,
        name: str,
        password: str,
        first_name: str,
        last_name: str,
        email: str,
        base_group: str,
        privileges: list = ["Login", "Public Access"],
    ):
        """Add Content Server user.

        Args:
            name (string): login name of the user
            password (string): password of the user
            first_name (string): first name of the user
            last_name (string): last name of the user
            email (string): email address of the user
            base_group (string): base group of the user (e.g. department)
            privileges (list): values are Login, Public Access, Content Manager, Modify Users, Modify Groups, User Admin Rights, Grant Discovery, System Admin Rights

        Return:
            User information (json) or None if the user couldn't be created (e.g. because it exisits already).
        """

        userPostBody = {
            "type": 0,
            "name": name,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "business_email": email,
            "group_id": base_group,
            "privilege_login": ("Login" in privileges),
            "privilege_public_access": ("Public Access" in privileges),
            "privilege_content_manager": ("Content Manager" in privileges),
            "privilege_modify_users": ("Modify Users" in privileges),
            "privilege_modify_groups": ("Modify Groups" in privileges),
            "privilege_user_admin_rights": ("User Admin Rights" in privileges),
            "privilege_grant_discovery": ("Grant Discovery" in privileges),
            "privilege_system_admin_rights": ("System Admin Rights" in privileges)
        }

        requestUrl = self.config()["usersUrl"]
        requestHeader = self.requestFormHeader()

        logger.info("Adding user -> {}; calling -> {}".format(name, requestUrl))

        retries = 0
        while True:
            userResponse = requests.post(
                requestUrl,
                data=userPostBody,
                headers=requestHeader,
                cookies=self.cookie(),
            )
            if userResponse.ok:
                return self.parseRequestResponse(userResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif userResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to add user -> {}; status -> {}; error -> {}".format(
                        name, userResponse.status_code, userResponse.text
                    )
                )
                return None

    # end method definition

    def searchUser(self, value: str, field: str = "where_name"):
        """Find a user based on search criteria.

        Args:
            value (string): field value
            field (string): user field to search with (where_name, where_first_name, where_last_name)
        Return:
            User information (json) or None if the user couldn't be found (e.g. because it doesn't exist).
        """

        requestUrl = self.config()["membersUrl"] + "?" + field + "=" + value
        requestHeader = self.requestFormHeader()

        logger.info(
            "Searching user by field -> {}, value -> {}; calling -> {}".format(
                field, value, requestUrl
            )
        )

        retries = 0
        while True:
            userResponse = requests.get(
                requestUrl, headers=requestHeader, cookies=self.cookie()
            )
            if userResponse.ok:
                return self.parseRequestResponse(userResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif userResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Cannot find user with -> {} = {}; status -> {}; error -> {}".format(
                        field, value, userResponse.status_code, userResponse.text
                    )
                )
                return None

    # end method definition

    def updateUser(self, user_id: int, field: str, value: str):
        """Update a defined field for a user.

        Args:
            user_id (integer): ID of the user
            value (string): field value
            field (string): user field
        Return:
            User information (json) or None if the user couldn't be updated (e.g. because it doesn't exist).
        """

        userPutBody = {field: value}

        requestUrl = self.config()["membersUrl"] + "/" + str(user_id)
        requestHeader = self.requestFormHeader()

        logger.info(
            "Updating user with ID -> {}, field -> {}, value -> {}; calling -> {}".format(
                user_id, field, value, requestUrl
            )
        )
        logger.debug("User Attributes -> {}".format(userPutBody))

        retries = 0
        while True:
            userResponse = requests.put(
                requestUrl,
                data=userPutBody,
                headers=requestHeader,
                cookies=self.cookie(),
            )
            if userResponse.ok:
                return self.parseRequestResponse(userResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif userResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to update user -> {}; status -> {}; error -> {}".format(
                        user_id, userResponse.status_code, userResponse.text
                    )
                )
                return None

    # end method definition

    def updateUserProfile(self, field: str, value):
        """Update a defined field for a user profile.
           IMPORTANT: this method needs to be called by the authenticated user

        Args:
            value (string): field value
            field (string): user field
        Return:
            User information (json) or None if the user couldn't be updated (e.g. because it doesn't exist).
        """

        userProfilePutBody = {"SmartUI": {field: value}}

        requestUrl = self.config()["membersUrl"] + "/preferences"
        requestHeader = self.requestFormHeader()

        logger.info(
            "Updating profile for current user, field -> {}, value -> {}; calling -> {}".format(
                field, value, requestUrl
            )
        )
        logger.debug("User Attributes -> {}".format(userProfilePutBody))

        retries = 0
        while True:
            # This REST API needs a special treatment: we encapsulate the payload as JSON into a "body" tag.
            userProfileResponse = requests.put(
                requestUrl,
                data={"body": json.dumps(userProfilePutBody)},
                headers=requestHeader,
                cookies=self.cookie(),
            )
            if userProfileResponse.ok:
                return self.parseRequestResponse(userProfileResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif userProfileResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to update profile of current user; status -> {}; error -> {}".format(
                        userProfileResponse.status_code, userProfileResponse.text
                    )
                )
                return None

    # end method definition

    def updateUserPhoto(self, user_id: int, photo_id: int):
        """Update a user with a profile photo (which must be an existing node).

        Args:
            user_id (integer): ID of the user
            photo_id (integer): Node ID of the photo
        Return:
            Node information (json) or None if no node with this nickname is found.
        """

        updateUserPutBody = {"photo_id": photo_id}

        requestUrl = self.config()["usersUrl"] + "/" + str(user_id)
        requestHeader = self.requestFormHeader()

        logger.info(
            "Update user ID -> {} with photo ID -> {}; calling -> {}".format(
                user_id, photo_id, requestUrl
            )
        )

        retries = 0
        while True:
            updateUserResponse = requests.put(
                requestUrl,
                data=updateUserPutBody,
                headers=requestHeader,
                cookies=self.cookie(),
            )
            if updateUserResponse.ok:
                return self.parseRequestResponse(updateUserResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif updateUserResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to update user with ID -> {}; status -> {}; error -> {}".format(
                        user_id, updateUserResponse.status_code, updateUserResponse.text
                    )
                )
                return None

    # end method definition

    def isProxy(self, user_name: str) -> bool:
        """Check if a user is defined as proxy of the current user

        Args:
            user_name (string): user  to test (login name)

        Returns:
            bool: True is user is proxy of current user. False if not.
        """

        response = self.getUserProxies()
        if not response or not "proxies" in response:
            return False
        proxies = response["proxies"]

        for proxy in proxies:
            if proxy["name"] == user_name:
                return True
        return False

    # end method definition

    def getUserProxies(self):
        """Get list of user proxies.
           This method needs to be called as the user the proxy is acting for.
        Args: None
        Return:
            Node information (json) or None if REST call fails.
        """

        requestUrl = self.config()["usersUrl"] + "/proxies"
        requestHeader = self.requestFormHeader()

        logger.info(
            "Get proxy users for current user; calling -> {}".format(
                requestUrl)
        )

        retries = 0
        while True:

            # This REST API needs a special treatment: we encapsulate the payload as JSON into a "add_assignment" tag.
            proxyResponse = requests.get(
                requestUrl,
                headers=requestHeader,
                cookies=self.cookie(),
            )
            if proxyResponse.ok:
                return self.parseRequestResponse(proxyResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif proxyResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to get proxy users for current user; status -> {}; error -> {}".format(
                        proxyResponse.status_code, proxyResponse.text
                    )
                )
                return None

    # end method definition

    def updateUserProxy(
        self, proxy_user_id: int, from_date: str = None, to_date: str = None
    ):
        """Update a user with a proxy user (which must be an existing user).
           This method needs to be called as the user the proxy is acting for.
           Optional this method can be provided with a time span the proxy should be active.

           Example payload for proxy user 19340 without time span:
           add_proxy:  {"19340":{}}

           Example payload for proxy user 19340 with time span:
           add_proxy: {"19340":{"from_date": "2022-10-01", "to_date": "2022-10-31"}}

        Args:
            user_id (integer): ID of the user
            from_date (string): Optional: start date for proxy (format YYYY-MM-DD)
            to_date (string): Optional: end date for proxy (format YYYY-MM-DD)
        Return:
            Node information (json) or None if REST call fails.
        """

        post_dict = {}
        if from_date and to_date:
            post_dict["from_date"] = from_date
            post_dict["to_date"] = to_date

        proxyPostBody = {str(proxy_user_id): post_dict}

        requestUrl = self.config()["usersUrl"] + "/proxies"
        requestHeader = self.requestFormHeader()

        logger.info(
            "Assign proxy user with ID -> {} to current user; calling -> {}".format(
                proxy_user_id, requestUrl
            )
        )

        retries = 0
        while True:

            # This REST API needs a special treatment: we encapsulate the payload as JSON into a "add_assignment" tag.
            proxyResponse = requests.post(
                requestUrl,
                data={"add_proxy": json.dumps(proxyPostBody)},
                headers=requestHeader,
                cookies=self.cookie(),
            )
            if proxyResponse.ok:
                return self.parseRequestResponse(proxyResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif proxyResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to assign proxy user with ID -> {} to current user; status -> {}; error -> {}".format(
                        proxy_user_id, proxyResponse.status_code, proxyResponse.text
                    )
                )
                return None

    # end method definition

    def addFavorite(self, node_id: int):
        """Add a favorite for the current (authenticated) user.

        Args:
            nodeid (integer): ID of the node.
        Return:
            Response (json) or None if the favorite creation has failed.
        """

        requestUrl = self.config()["favoritesUrl"] + "/" + str(node_id)
        requestHeader = self.requestFormHeader()

        logger.info(
            "Adding favorite for node ID -> {}; calling -> {}".format(
                node_id, requestUrl
            )
        )

        retries = 0
        while True:
            addFavoriteResponse = requests.post(
                requestUrl, headers=requestHeader, cookies=self.cookie()
            )
            if addFavoriteResponse.ok:
                return self.parseRequestResponse(addFavoriteResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif addFavoriteResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to add favorite for node ID -> {}; status -> {}; error -> {}".format(
                        node_id,
                        addFavoriteResponse.status_code,
                        addFavoriteResponse.text,
                    )
                )
                return None

    # end method definition

    def getGroupMembers(self, group: int, member_type: int, limit: int = 100):
        """Get Content Server group members.

        Args:
            group (integer): ID of the group.
            member_type (integer): users = 0, groups = 1
            limit (integer): max number of results (internal default is 25)
        Return:
            Group members (json) or None if the group members couldn't be found.
        """

        # default limit is 25 which may not be enough for groups with many members
        # where_type = 1 makes sure we just get groups and not users
        requestUrl = (
            self.config()["membersUrl"]
            + "/"
            + str(group)
            + "/members?where_type="
            + str(member_type)
            + "&limit="
            + str(limit)
        )
        requestHeader = self.requestFormHeader()

        logger.info(
            "Getting members of group -> {}; calling -> {}".format(
                group, requestUrl)
        )

        retries = 0
        while True:
            groupMembersResponse = requests.get(
                requestUrl, headers=requestHeader, cookies=self.cookie()
            )
            if groupMembersResponse.ok:
                return self.parseRequestResponse(groupMembersResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif groupMembersResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to get members of group -> {}; status -> {}; error -> {}".format(
                        group,
                        groupMembersResponse.status_code,
                        groupMembersResponse.text,
                    )
                )
                return None

    # end method definition

    def addGroupMember(self, member: int, group: int):
        """Add a user or group to a target group.

        Args:
            member (integer): ID of the user or group to add.
            group (integer): ID of the target group.
        Return:
            Response (json) or None if the adding fails.
        """

        groupMemberPostBody = {"member_id": member}

        requestUrl = self.config()["membersUrl"] + \
            "/" + str(group) + "/members"
        requestHeader = self.requestFormHeader()

        logger.info(
            "Adding member -> {} to group -> {}; calling -> {}".format(
                member, group, requestUrl
            )
        )

        retries = 0
        while True:
            groupMemberResponse = requests.post(
                requestUrl,
                data=groupMemberPostBody,
                headers=requestHeader,
                cookies=self.cookie(),
            )
            if groupMemberResponse.ok:
                return self.parseRequestResponse(groupMemberResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif groupMemberResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to add member -> {} to group -> {}; status -> {}; error -> {}".format(
                        member,
                        group,
                        groupMemberResponse.status_code,
                        groupMemberResponse.text,
                    )
                )
                return None

    # end method definition

    def getNode(self, node_id: int):
        """Get a node based on the node ID.

        Args:
            node_id (integer) is the node Id of the node
        Return:
            Node information (json) or None if no node with this ID is found.
            "results": [
                {
                    "data": [
                        {
                            "columns": [
                                {
                                "data_type": 0,
                                "key": "string",
                                "name": "string",
                                "sort_key": "string"
                                }
                            ],
                            "properties": [
                                {
                                    "advanced_versioning": true,
                                    "container": true,
                                    "container_size": 0,
                                    "create_date": "string",
                                    "create_user_id": 0,
                                    "description": "string",
                                    "description_multilingual": {
                                        "en": "string",
                                        "de": "string"
                                    },
                                    "external_create_date": "2019-08-24",
                                    "external_identity": "string",
                                    "external_identity_type": "string",
                                    "external_modify_date": "2019-08-24",
                                    "external_source": "string",
                                    "favorite": true,
                                    "guid": "string",
                                    "hidden": true,
                                    "icon": "string",
                                    "icon_large": "string",
                                    "id": 0,
                                    "modify_date": "2019-08-24",
                                    "modify_user_id": 0,
                                    "name": "string",
                                    "name_multilingual": {
                                        "en": "string",
                                        "de": "string"
                                    },
                                    "owner": "string",
                                    "owner_group_id": 0,
                                    "owner_user_id": 0,
                                    "parent_id": 0,
                                    "reserved": true,
                                    "reserved_date": "string",
                                    "reserved_user_id": 0,
                                    "status": 0,
                                    "type": 0,
                                    "type_name": "string",
                                    "versionable": true,
                                    "versions_control_advanced": true,
                                    "volume_id": 0
                                }
                            ]
                        }
                    ]
                }
            ]
        """

        requestUrl = self.config()["nodesUrlv2"] + "/" + str(node_id)
        requestHeader = self.requestFormHeader()

        logger.info(
            "Get node with ID -> {}; calling -> {}".format(node_id, requestUrl))

        retries = 0
        while True:
            getNodeResponse = requests.get(
                requestUrl, headers=requestHeader, cookies=self.cookie()
            )
            if getNodeResponse.ok:
                return self.parseRequestResponse(getNodeResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif getNodeResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to get node with ID -> {}; status -> {}; error -> {}".format(
                        node_id, getNodeResponse.status_code, getNodeResponse.text
                    )
                )
                return None

    # end method definition

    def getNodeByParentAndName(self, parent_id: int, name: str, show_error: bool = False):
        """Get a node based on the parent ID and name. This method does basically
           a query with "where_name" and the "result" is a list.

        Args:
            parent_id (integer) is the node Id of the parent node
            name (string) is the name of the node to get
            show_error (boolean): treat as error if node is not found
        Return:
            Node information (json) or None if no node with this name is found in parent.
            Access to node ID with: response["results"][0]["data"]["properties"]["id"]
        """

        # Add query parameters (these are NOT passed via JSon body!)
        query = {"where_name": name}
        encoded_query = urllib.parse.urlencode(query, doseq=True)

        requestUrl = (
            self.config()["nodesUrlv2"]
            + "/"
            + str(parent_id)
            + "/nodes?{}".format(encoded_query)
        )
        requestHeader = self.requestFormHeader()

        logger.info(
            "Get node with name -> {} and parent ID -> {}; calling -> {}".format(
                name, parent_id, requestUrl
            )
        )

        retries = 0
        while True:
            getNodeResponse = requests.get(
                requestUrl, headers=requestHeader, cookies=self.cookie()
            )
            if getNodeResponse.ok:
                return self.parseRequestResponse(getNodeResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif getNodeResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                if show_error:
                    logger.error(
                        "Failed to get node with name -> {} and parent ID -> {}; status -> {}; error -> {}".format(
                            name,
                            parent_id,
                            getNodeResponse.status_code,
                            getNodeResponse.text,
                        )
                    )
                else:
                    logger.info(
                        "Node with name -> {} and parent ID -> {} not found.".format(
                            name, parent_id
                        )
                    )
                return None

    # end method definition

    def getNodeByVolumeAndPath(self, volume_type: int, path: list):
        """Get a node based on the volume and path (list of container items).

        Args:
            volume_type (integer): Volume type ID (default is 141 = Enterprise Workspace)
                "Records Management"                = 550
                "Content Server Document Templates" = 20541
                "O365 Office Online Volume"         = 1296
                "Categories Volume"                 = 133
                "Perspectives"                      = 908
                "Perspective Assets"                = 954
                "Facets Volume"                     = 901
                "Transport Warehouse"               = 525
                "Transport Warehouse Workbench"     = 528
                "Transport Warehouse Package"       = 531
                "Event Action Center Configuration" = 898
                "Classification Volume"             = 198
                "Support Asset Volume"              = 1309
                "Physical Objects Workspace"        = 413
                "Extended ECM"                      = 882
                "Enterprise Workspace"              = 141
                "Business Workspaces"               = 862
            path (list): list of container items (top down), last item is name of to be retrieved item.
                         If path is empty the node of the volume is returned.
        Return:
            Node information (json) or None if no node with this path is found.
        """

        # Preparation: get volume IDs for Transport Warehouse (root volume and Transport Packages)
        response = self.getVolume(volume_type)
        if not response:
            logger.error("Volume Type -> {} not found!".format(volume_type))
            return None

        volume_id = self.getResultValue(response, "id")
        logger.info("Volume ID -> {}".format(volume_id))

        current_item_id = volume_id

        # in case the path is an empty list
        # we will have the node of the volume:
        node = self.getNode(current_item_id)

        for path_element in path:
            node = self.getNodeByParentAndName(current_item_id, path_element)
            current_item_id = self.getResultValue(node, "id")
            if not current_item_id:
                logger.error(
                    "Cannot find path element -> {} in container with ID -> {}.".format(
                        path_element, current_item_id
                    )
                )
                return None
            logger.debug(
                "Traversing path element -> {}".format(current_item_id))

        return node

    # end method definition

    def getNodeFromNickname(self, nickname: str, show_error: bool = False):
        """Get a node based on the nickname.

        Args:
            nickname (string): Nickname of the node.
            show_error (boolean): treat as error if node is not found
        Return:
            Node information (json) or None if no node with this nickname is found.
        """

        requestUrl = self.config()["nicknameUrl"] + "/" + nickname + "/nodes"
        requestHeader = self.requestFormHeader()

        logger.info(
            "Get node with nickname -> {}; calling -> {}".format(
                nickname, requestUrl)
        )

        retries = 0
        while True:
            getNodeResponse = requests.get(
                requestUrl, headers=requestHeader, cookies=self.cookie()
            )
            if getNodeResponse.ok:
                return self.parseRequestResponse(getNodeResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif getNodeResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                if show_error:
                    logger.error(
                        "Failed to get node with nickname -> {}; status -> {}; error -> {}".format(
                            nickname, getNodeResponse.status_code, getNodeResponse.text
                        )
                    )
                else:
                    logger.info(
                        "Node with nickname -> {} not found.".format(
                            nickname)
                    )
                return None

    # end method definition

    def getSubnodes(
        self,
        parent_node_id: int,
        filter_node_types: int = -2,
        filter_name: str = "",
        show_hidden: bool = False,
        limit: int = 100,
        page: int = 1,
    ):
        """Get a subnodes of a parent node ID.

        Args:
            parent_node_id (integer) is the node Id of the node
            filter_node_types (integer): -1 get all containers
                                         -2 get all searchable objects
                                         -3 get all non-containers
            filter_name (string): filter nodes for specific name
            show_hidden (boolean): list also hidden items
            limit (integer): maximum number of results
            page (integer): number of result page
        Return:
            Subnodes information (json) or None if no node with this parent ID is found.
        """

        # Add query parameters (these are NOT passed via JSon body!)
        query = {
            "where_type": filter_node_types,
            "limit": limit,
        }
        if filter_name:
            query["where_name"] = filter_name
        if show_hidden:
            query["show_hidden"] = show_hidden
        if page > 1:
            query["page"] = page

        encodedQuery = urllib.parse.urlencode(query, doseq=True)

        requestUrl = (
            self.config()["nodesUrlv2"]
            + "/"
            + str(parent_node_id)
            + "/nodes"
            + "?{}".format(encodedQuery)
        )
        requestHeader = self.requestFormHeader()

        logger.info(
            "Get subnodes of parent node with ID -> {}; calling -> {}".format(
                parent_node_id, requestUrl
            )
        )

        retries = 0
        while True:
            getNodesResponse = requests.get(
                requestUrl, headers=requestHeader, cookies=self.cookie()
            )
            if getNodesResponse.ok:
                return self.parseRequestResponse(getNodesResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif getNodesResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to get subnodes for parent node with ID -> {}; status -> {}; error -> {}".format(
                        parent_node_id,
                        getNodesResponse.status_code,
                        getNodesResponse.text,
                    )
                )
                return None

    # end method definition

    def renameNode(self, node_id: int, name: str, description: str, name_multilingual: dict = {}, description_multilingual: dict = {}):
        """Change the name and description of a node.

        Args:
            node_id (integer): ID of the node. You can use the getVolume() function below to
                               to the node id for a volume.
            name (string): New name of the node.
            description (string): New description of the node.
        Return:
            Rename response (json) or None if the renaming fails.
        """

        renameNodePutBody = {"name": name, "description": description}

        if name_multilingual:
            renameNodePutBody["name_multilingual"] = name_multilingual
        if description_multilingual:
            renameNodePutBody["description_multilingual"] = description_multilingual

        requestUrl = self.config()["nodesUrlv2"] + "/" + str(node_id)
        requestHeader = self.requestFormHeader()

        logger.info(
            "Renaming node -> {} to -> {}; calling -> {}".format(
                node_id, name, requestUrl
            )
        )

        retries = 0
        while True:
            nodeRenameResponse = requests.put(
                requestUrl,
                data={"body": json.dumps(renameNodePutBody)},
                headers=requestHeader,
                cookies=self.cookie(),
            )
            if nodeRenameResponse.ok:
                return self.parseRequestResponse(nodeRenameResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif nodeRenameResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to rename node -> {} to -> {}; status -> {}; error -> {}".format(
                        node_id,
                        name,
                        nodeRenameResponse.status_code,
                        nodeRenameResponse.text,
                    )
                )
                return None

    # end method definition

    def getVolumes(self):
        """Get all Volumes.

        Args:
            None
        Return:
            Volume Details (json) or None if an error occured.
            ["results"]["data"]["properties"]["id"] is the node ID of the volume.
        """

        requestUrl = self.config()["volumeUrl"]
        requestHeader = self.requestFormHeader()

        logger.info("Get volumes; calling -> {}".format(requestUrl))

        retries = 0
        while True:
            getVolumeResponse = requests.get(
                requestUrl, headers=requestHeader, cookies=self.cookie()
            )
            if getVolumeResponse.ok:
                return self.parseRequestResponse(getVolumeResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif getVolumeResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to get volumes; status -> {}; error -> {}".format(
                        getVolumeResponse.status_code, getVolumeResponse.text
                    )
                )
                return None

    # end method definition

    def getVolume(self, volume_type: int):
        """Get Volume information based on the volume type ID.

        Args:
            volume_type (integer): ID of the volume type
        Return:
            Volume Details (json) or None if volume is not found.
            ["results"]["data"]["properties"]["id"] is the node ID of the volume.
        """

        requestUrl = self.config()["volumeUrl"] + "/" + str(volume_type)
        requestHeader = self.requestFormHeader()

        logger.info(
            "Get volume type -> {}; calling -> {}".format(
                volume_type, requestUrl)
        )

        retries = 0
        while True:
            getVolumeResponse = requests.get(
                requestUrl, headers=requestHeader, cookies=self.cookie()
            )
            if getVolumeResponse.ok:
                return self.parseRequestResponse(getVolumeResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif getVolumeResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to get volume type -> {}; status -> {}; error -> {}".format(
                        volume_type,
                        getVolumeResponse.status_code,
                        getVolumeResponse.text,
                    )
                )
                return None

    # end method definition

    def search(
        self,
        search_term: str,
        look_for: str = "complexQuery",
        modifier: str = "",
        slice_id: int = 0,
        query_id: int = 0,
        template_id: int = 0,
        limit: int = 100,
        page: int = 1,
    ):
        """Search for a search term.

        Args:
            parent_node_id (integer) is the node Id of the node
            search_term (string), e.g. "test or OTSubType: 189"
            look_for (string): 'allwords', 'anywords', 'exactphrase', and 'complexquery'.
                              If not specified, it defaults to 'complexQuery'.
            modifier (string): 'synonymsof', 'relatedto', 'soundslike', 'wordbeginswith', and 'wordendswith'.
                               If not specified or specify any value other than the available options,
                               it will be ignored.
            slide_id (integer): ID of an existing search slice
            query_id (integer): ID of an saved search query
            template_id (integer): ID of an saved search template
            limit (integer): maximum number of results
            page (integer): number of result page
        Return:
            Subnodes information (json) or None if no node with this parent ID is found.
        """

        searchPostBody = {
            "where": search_term,
            "lookfor": look_for,
            "page": page,
            "limit": limit,
        }

        if modifier:
            searchPostBody["modifier"] = modifier
        if slice_id > 0:
            searchPostBody["slice_id"] = slice_id
        if query_id > 0:
            searchPostBody["query_id"] = query_id
        if template_id > 0:
            searchPostBody["template_id"] = template_id

        requestUrl = self.config()["searchUrl"]
        requestHeader = self.requestFormHeader()

        logger.info(
            "Serarch for term -> {}; calling -> {}".format(
                search_term, requestUrl)
        )

        retries = 0
        while True:
            getNodesResponse = requests.post(
                requestUrl,
                data=searchPostBody,
                headers=requestHeader,
                cookies=self.cookie(),
            )
            if getNodesResponse.ok:
                return self.parseRequestResponse(getNodesResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif getNodesResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to search for term -> {}; status -> {}; error -> {}".format(
                        search_term,
                        getNodesResponse.status_code,
                        getNodesResponse.text,
                    )
                )
                return None

    # end method definition

    def getExternalSystemConnection(self, connection_name: str, show_error: bool = False):
        """Get Extended ECM external system connection (e.g. SAP, Salesforce, SuccessFactors).

        Args:
            connection_name (string): Name of the connection
            show_error (boolean): treat as error if node is not found
        Return:
            External system Details (json) or None if the REST call fails.
        """

        requestUrl = self.config()["externalSystem"] + \
            "/" + connection_name + "/config"
        requestHeader = self.cookie()

        logger.info(
            "Get external system connection -> {}; calling -> {}".format(
                connection_name, requestUrl
            )
        )

        retries = 0
        while True:
            externalSystemResponse = requests.get(
                requestUrl, headers=requestHeader, cookies=self.cookie()
            )
            if externalSystemResponse.ok:
                return self.parseRequestResponse(externalSystemResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif externalSystemResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                if show_error:
                    logger.error(
                        "Failed to get external system connection -> {}; status -> {}; error -> {}".format(
                            connection_name,
                            externalSystemResponse.status_code,
                            externalSystemResponse.text,
                        )
                    )
                else:
                    logger.info(
                        "External system -> {} not found.".format(
                            connection_name)
                    )
                return None

    # end method definition

    def addExternalSystemConnection(
        self,
        connection_name: str,
        connection_type: str,
        as_url: str,
        base_url: str,
        username: str,
        password: str,
        authentication_method: str = "BASIC",  # either BASIC or OAUTH
        client_id: str = None,
        client_secret: str = None,
    ):
        """Add Extended ECM external system connection (e.g. SAP, Salesforce, SuccessFactors).

        Args:
            connection_name (string): Name of the connection
            connection_type (string): Type of the connection (HTTP, SF, SFInstance)
            as_url (string)
            base_url (string)
            username (string)
            password (string)
            authentication_method: wither BASIC (using username and password) or OAUTH
            client_id: OAUTH Client ID (only required if authenticationMethod = OAUTH)
            client_secret: OAUTH Client Secret (only required if authenticationMethod = OAUTH)
        Return:
            External system Details (json) or None if the REST call fails.
        """

        externalSystemPostBody = {
            "external_system_name": connection_name,
            "conn_type": connection_type,
            "asurl": as_url,
            "baseurl": base_url,
            "username": username,
            "password": password,
        }

        if authentication_method == "OAUTH" and client_id and client_secret:
            externalSystemPostBody["authentication_method"] = str(
                authentication_method)
            externalSystemPostBody["client_id"] = str(client_id)
            externalSystemPostBody["client_secret"] = str(client_secret)

        requestUrl = self.config()["externalSystem"]
        requestHeader = self.cookie()

        logger.info(
            "Creating external system connection -> {} of type -> {} and URL -> {}; calling -> {}".format(
                connection_name, connection_type, as_url, requestUrl
            )
        )

        retries = 0
        while True:
            externalSystemResponse = requests.post(
                requestUrl,
                data=externalSystemPostBody,
                headers=requestHeader,
                cookies=self.cookie(),
            )
            if externalSystemResponse.ok:
                return self.parseRequestResponse(externalSystemResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif externalSystemResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to create external system connection -> {}; status -> {}; error -> {}".format(
                        connection_name,
                        externalSystemResponse.status_code,
                        externalSystemResponse.text,
                    )
                )
                return None

    # end method definition

    def downloadConfigFile(self, otcs_url_suffix: str, file_path: str) -> bool:
        """ Download a config file from a given OTCS URL. This is NOT
            for downloading documents from within the OTCS repository
            but for configuration files such as app packages for MS Teams.

        Args:
            otcs_url_suffix (str): OTCS URL suffix starting typically starting 
                                   with /cs/cs?func=,
                                   e.g. /cs/cs?func=officegroups.DownloadTeamsPackage
            file_path (str): local path to save the file (direcotry + filename)

        Returns:
            boolean: True if the download succeeds, False otherwise
        """


        requestUrl = self.config()["baseUrl"] + otcs_url_suffix
        # requestHeader = self.cookie()
        requestHeader = self.requestDownloadHeader()

        logger.info(
            "Download config file from URL -> {}".format(requestUrl))

        try:
            response = requests.get(requestUrl, headers=requestHeader, cookies=self.cookie())
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            logger.error("Http Error -> {}".format(errh))
            return False
        except requests.exceptions.ConnectionError as errc:
            logger.error("Error Connecting -> {}".format(errc))
            return False
        except requests.exceptions.Timeout as errt:
            logger.error("Timeout Error -> {}".format(errt))
            return False
        except requests.exceptions.RequestException as err:
            logger.error("Request error -> {}".format(err))
            return False

        content = response.content

        # Open file in write binary mode
        with open(file_path, 'wb') as file:
            # Write the content to the file
            file.write(content)

        logger.info(
            "Successfully downloaded config file -> {} to -> {}; status code -> {}".format(
                requestUrl, file_path, response.status_code
            )
        )

        return True

    # end method definition

    def uploadFileToVolume(
        self, package_url: str, file_name: str, mime_type: str, volume_type: int
    ):
        """Fetch a file from a URL or local filesystem and upload it to a Content Server volume.

        Args:
            package_url (string): URL to download file
            file_name (string): name of the file
            mime_type (string): mimeType of the file
            volume_type (integer): type (ID) of the volume
        Return:
            Upload response (json) or None if the upload fails.
        """

        if package_url.startswith("http"):
            # Download file from remote location specified by the packageUrl
            # this must be a public place without authentication:
            logger.info(
                "Download transport package from URL -> {}".format(package_url))

            try:
                package = requests.get(package_url)
                package.raise_for_status()
            except requests.exceptions.HTTPError as errh:
                logger.error("Http Error -> {}".format(errh))
                return None
            except requests.exceptions.ConnectionError as errc:
                logger.error("Error Connecting -> {}".format(errc))
                return None
            except requests.exceptions.Timeout as errt:
                logger.error("Timeout Error -> {}".format(errt))
                return None
            except requests.exceptions.RequestException as err:
                logger.error("Request error -> {}".format(err))
                return None

            logger.info(
                "Successfully downloaded package -> {}; status code -> {}".format(
                    package_url, package.status_code
                )
            )
            file = package.content

        elif os.path.exists(package_url):
            logger.info("Using local package -> {}".format(package_url))
            file = open(package_url, "rb")

        else:
            logger.warning("Cannot access -> {}".format(package_url))
            return None

        uploadPostData = {"type": str(volume_type), "name": file_name}
        uploadPostFiles = [("file", (f"{file_name}", file, mime_type))]

        requestUrl = self.config()["nodesUrlv2"]
        requestHeader = (
            self.cookie()
        )  # for some reason we have to omit the other header parts here - otherwise we get a 500 response

        logger.info(
            "Uploading package -> {} with mime type -> {}; calling -> {}".format(
                file_name, mime_type, requestUrl
            )
        )

        retries = 0
        while True:
            uploadResponse = requests.post(
                requestUrl,
                data=uploadPostData,
                files=uploadPostFiles,
                headers=requestHeader,
                cookies=self.cookie(),
            )
            if uploadResponse.ok:
                return self.parseRequestResponse(uploadResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif uploadResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to upload file -> {} to volume -> {}; status -> {}; error -> {}".format(
                        package_url,
                        volume_type,
                        uploadResponse.status_code,
                        uploadResponse.text,
                    )
                )
                return None

    # end method definition

    def uploadFileToParent(
        self, file_url: str, file_name: str, mime_type: str, parent_id: int
    ):
        """Fetch a file from a URL or local filesystem and upload it to a Content Server parent (folder).

        Args:
            file_url (string): URL to download file or local file
            file_name (string): name of the file
            mime_type (string): mimeType of the file
            parent_id (integer): parent (ID) of the file to upload
        Return:
            Upload response (json) or None if the upload fails.
        """

        if file_url.startswith("http"):
            # Download file from remote location specified by the fileUrl
            # this must be a public place without authentication:
            logger.info("Download file from URL -> {}".format(file_url))

            try:
                response = requests.get(file_url)
                response.raise_for_status()
            except requests.exceptions.HTTPError as errh:
                logger.error("Http Error -> {}".format(errh))
                return None
            except requests.exceptions.ConnectionError as errc:
                logger.error("Error Connecting -> {}".format(errc))
                return None
            except requests.exceptions.Timeout as errt:
                logger.error("Timeout Error -> {}".format(errt))
                return None
            except requests.exceptions.RequestException as err:
                logger.error("Request error -> {}".format(err))
                return None

            logger.info(
                "Successfully downloaded file -> {}; status code -> {}".format(
                    file_url, response.status_code
                )
            )
            file_content = response.content

        elif os.path.exists(file_url):
            logger.info("Uploading local file -> {}".format(file_url))
            file_content = open(file_url, "rb")

        else:
            logger.warning("Cannot access -> {}".format(file_url))
            return None

        uploadPostData = {
            "type": str(144),
            "name": file_name,
            "parent_id": str(parent_id),
        }
        uploadPostFiles = [("file", (f"{file_name}", file_content, mime_type))]

        requestUrl = self.config()["nodesUrlv2"]
        requestHeader = (
            self.cookie()
        )  # for some reason we have to omit the other header parts here - otherwise we get a 500 response

        logger.info(
            "Uploading file -> {} with mime type -> {} to parent -> {}; calling -> {}".format(
                file_name, mime_type, parent_id, requestUrl
            )
        )

        retries = 0
        while True:
            uploadResponse = requests.post(
                requestUrl,
                data=uploadPostData,
                files=uploadPostFiles,
                headers=requestHeader,
                cookies=self.cookie(),
            )
            if uploadResponse.ok:
                return self.parseRequestResponse(uploadResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif uploadResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to upload file -> {} to parent -> {}; status -> {}; error -> {}".format(
                        file_url,
                        parent_id,
                        uploadResponse.status_code,
                        uploadResponse.text,
                    )
                )
                return None

    # end method definition

    def addDocumentVersion(
        self, node_id: int, file_url: str, file_name: str, mime_type: str = "text/plain", description: str = ""
    ):
        """Fetch a file from a URL or local filesystem and upload it as a new document version.

        Args:
            node_id (integer): ID of the document to add add version to
            file_url (string): URL to download file or local file
            file_name (string): name of the file
            mime_type (string): mimeType of the file
            description (string): description of the version
        Return:
            Add version response (json) or None if the upload fails.
        """

        if file_url.startswith("http"):
            # Download file from remote location specified by the fileUrl
            # this must be a public place without authentication:
            logger.info("Download file from URL -> {}".format(file_url))

            try:
                response = requests.get(file_url)
                response.raise_for_status()
            except requests.exceptions.HTTPError as errh:
                logger.error("Http Error -> {}".format(errh))
                return None
            except requests.exceptions.ConnectionError as errc:
                logger.error("Error Connecting -> {}".format(errc))
                return None
            except requests.exceptions.Timeout as errt:
                logger.error("Timeout Error -> {}".format(errt))
                return None
            except requests.exceptions.RequestException as err:
                logger.error("Request error -> {}".format(err))
                return None

            logger.info(
                "Successfully downloaded file -> {}; status code -> {}".format(
                    file_url, response.status_code
                )
            )
            file_content = response.content

        elif os.path.exists(file_url):
            logger.info("Uploading local file -> {}".format(file_url))
            file_content = open(file_url, "rb")

        else:
            logger.warning("Cannot access -> {}".format(file_url))
            return None

        uploadPostData = {
            "description": description
        }
        uploadPostFiles = [("file", (f"{file_name}", file_content, mime_type))]

        requestUrl = self.config()["nodesUrlv2"] + \
            "/" + str(node_id) + "/versions"
        requestHeader = (
            self.cookie()
        )  # for some reason we have to omit the other header parts here - otherwise we get a 500 response

        logger.info(
            "Uploading document version -> {} with mime type -> {} to document node -> {}; calling -> {}".format(
                file_name, mime_type, node_id, requestUrl
            )
        )

        retries = 0
        while True:
            uploadResponse = requests.post(
                requestUrl,
                data=uploadPostData,
                files=uploadPostFiles,
                headers=requestHeader,
                cookies=self.cookie(),
            )
            if uploadResponse.ok:
                return self.parseRequestResponse(uploadResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif uploadResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to add version -> {} to document -> {}; status -> {}; error -> {}".format(
                        file_url,
                        node_id,
                        uploadResponse.status_code,
                        uploadResponse.text,
                    )
                )
                return None

    # end method definition

    def getLatestDocumentVersion(self, node_id: int):
        """Get latest version of a node based on the node ID.

        Args:
            node_id (integer) is the node Id of the node
        Return:
            Node information (json) or None if no node with this ID is found.
        """

        requestUrl = self.config()["nodesUrl"] + \
            "/" + str(node_id) + "/versions/latest"
        requestHeader = self.requestFormHeader()

        logger.info(
            "Get latest version of document with node ID -> {}; calling -> {}".format(node_id, requestUrl))

        retries = 0
        while True:
            getNodeResponse = requests.get(
                requestUrl, headers=requestHeader, cookies=self.cookie()
            )
            if getNodeResponse.ok:
                return self.parseRequestResponse(getNodeResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif getNodeResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to get latest version of document with node ID -> {}; status -> {}; error -> {}".format(
                        node_id, getNodeResponse.status_code, getNodeResponse.text
                    )
                )
                return None

    # end method definition

    def downloadDocument(self, node_id: int, file_path: str, version_number: str = ""):
        """Download a document from Extended ECM to local file system.

        Args:
            node_id (integer): node ID of the document to download
            version (string): version of the document to download.
                              If version = "" then download the latest
                              version.
            file_path (string): local file path (directory)
            file_name (string): name of the file
        Return:
            True if the document has been download to the specified file.
            False otherwise.
        """

        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            logger.error("Directory -> {} does not exist".format(directory))
            return False

        if not version_number:
            response = self.getLatestDocumentVersion(node_id)
            version_number = response["data"]["version_number"]

        requestUrl = self.config()["nodesUrlv2"] + \
            "/" + str(node_id) + "/versions/" + \
            str(version_number) + "/content/" + str(node_id)
        requestHeader = self.requestDownloadHeader()

        logger.info(
            "Download document with node ID -> {}; calling -> {}".format(node_id, requestUrl))

        retries = 0
        while True:
            getNodeResponse = requests.get(
                requestUrl, headers=requestHeader, cookies=self.cookie()
            )
            if getNodeResponse.ok:
                #                content = self.parseRequestResponse(getNodeResponse)["data"]
                content = getNodeResponse.content
                break
            # Check if Session has expired - then re-authenticate and try once more
            elif getNodeResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to download document with node ID -> {}; status -> {}; error -> {}".format(
                        node_id, getNodeResponse.status_code, getNodeResponse.text
                    )
                )
                return False

        logger.info(
            "Writing document content to file -> {}".format(file_path))

        # Open file in write binary mode
        with open(file_path, 'wb') as file:
            # Write the content to the file
            file.write(content)

        return True

        # end method definition

    def createTransportWorkbench(self, workbench_name: str):
        """Create a Workbench in the Transport Volume.

        Args:
            workbench_name (string): name of the workbench to be created
        Return:
            Create response (json) or None if the creation fails.
        """

        createWorbenchPostData = {"type": "528", "name": workbench_name}

        requestUrl = self.config()["nodesUrlv2"]
        requestHeader = self.requestFormHeader()

        logger.info(
            "Create transport workbench -> {}; calling -> {}".format(
                workbench_name, requestUrl
            )
        )
        retries = 0
        while True:
            createResponse = requests.post(
                requestUrl,
                data=createWorbenchPostData,
                headers=requestHeader,
                cookies=self.cookie(),
            )
            if createResponse.ok:
                return self.parseRequestResponse(createResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif createResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to create transport workbench -> {}; status -> {}; error -> {}".format(
                        workbench_name, createResponse.status_code, createResponse.text
                    )
                )
                return None

    # end method definition

    def unpackTransportPackage(self, package_id: int, workbench_id: int):
        """Unpack an existing Transport Package into an existing Workbench.

        Args:
            package_iD (integer): ID of package to be unpacked
            workbench_iD (integer): ID of target workbench
        Return:
            Unpack response (json) or None if the unpacking fails.
        """

        unpackPackagePostData = {"workbench_id": workbench_id}

        requestUrl = self.config()["nodesUrlv2"] + \
            "/" + str(package_id) + "/unpack"
        requestHeader = self.requestFormHeader()

        logger.info(
            "Unpack transport package with ID -> {} into workbench with ID -> {}; calling -> {}".format(
                package_id, workbench_id, requestUrl
            )
        )

        retries = 0
        while True:
            unpackResponse = requests.post(
                requestUrl,
                data=unpackPackagePostData,
                headers=requestHeader,
                cookies=self.cookie(),
            )
            if unpackResponse.ok:
                return self.parseRequestResponse(unpackResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif unpackResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to unpack package -> {}; to workbench -> {}; status -> {}; error -> {}".format(
                        package_id,
                        workbench_id,
                        unpackResponse.status_code,
                        unpackResponse.text,
                    )
                )
                return None

    # end method definition

    def deployWorkbench(self, workbench_id: int):
        """Deploy an existing Workbench.

        Args:
            workbench_iD (integer): ID of the workbench to be deployed
        Return:
            Deploy response (json) or None if the deployment fails.
        """

        requestUrl = self.config()["nodesUrlv2"] + \
            "/" + str(workbench_id) + "/deploy"
        requestHeader = self.requestFormHeader()

        logger.info(
            "Deploy workbench with ID -> {}; calling -> {}".format(
                workbench_id, requestUrl
            )
        )

        retries = 0
        while True:
            # As this is a potentially long-running request we put it in try / except:
            try:
                deployResponse = requests.post(
                    requestUrl, headers=requestHeader, cookies=self.cookie()
                )
            except Exception as e:
                logger.error(
                    "Error deploying workbench -> {} : error -> {}".format(
                        workbench_id, e
                    )
                )
                return None
            if deployResponse.ok:
                response_dict = self.parseRequestResponse(deployResponse)
                if not response_dict:
                    logger.error(
                        "Error deploying workbench -> {}".format(workbench_id))
                    return None
                return response_dict
            # Check if Session has expired - then re-authenticate and try once more
            elif deployResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.warning(
                    "Failed to depoloy workbench -> {}; status -> {}; error -> {}".format(
                        workbench_id, deployResponse.status_code, deployResponse.text
                    )
                )
                return None

    # end method definition

    def deployTransport(
        self, package_url: str, package_name: str, package_description: str = "", replacements: list = []
    ):
        """Main method to deploy a transport. This uses subfunctions to upload,
           unpackage and deploy the transport, and creates the required workbench.

        Args:
            package_url (string): URL to download the transport package.
            package_name (string): name of the transport package ZIP file
            package_description (string): description of the transport package
            replacements (list of dicts): list of replacement values to be applied
                                          to all XML files in transport; dict needs to have two values:
                                         * placeholder: text to replace
                                         * value: text to replace with
        Return:
            Deploy response (json) or None if the deployment fails.
        """

        # Preparation: get volume IDs for Transport Warehouse (root volume and Transport Packages)
        response = self.getVolume(525)
        transport_root_volume_id = self.getResultValue(response, "id")
        if not transport_root_volume_id:
            logger.error("Failed to retrieve transport root volume")
            return None
        logger.info(
            "Transport root volume ID -> {}".format(transport_root_volume_id))

        response = self.getNodeByParentAndName(
            transport_root_volume_id, "Transport Packages"
        )
        transport_package_volume_id = self.getResultValue(response, "id")
        if not transport_package_volume_id:
            logger.error("Failed to retrieve transport package volume")
            return None
        logger.info(
            "Transport package volume ID -> {}".format(
                transport_package_volume_id)
        )

        # Step 1: Upload Transport Package
        logger.info(
            "Check if transport package -> {} already exists...".format(
                package_name)
        )
        response = self.getNodeByParentAndName(
            transport_package_volume_id, package_name)
        package_id = self.getResultValue(response, "id")
        if package_id:
            logger.info(
                "Transport package -> {} does already exist; existing package ID -> {}".format(
                    package_name, package_id
                )
            )
        else:
            logger.info(
                "Transport package -> {} does not yet exist, loading from -> {}".format(
                    package_name, package_url
                )
            )
            # If we have string replacements configured execute them now:
            if replacements:
                logger.info("Transport -> {} has replacements -> {}".format(package_name, replacements))
                self.replaceTransportPlaceholders(package_url, replacements)
            else:
                logger.info("Transport -> {} has no replacements!".format(package_name))
            # Upload package to Extended ECM:
            response = self.uploadFileToVolume(
                package_url, package_name, "application/zip", 531
            )
            package_id = self.getResultValue(response, "id")
            if not package_id:
                logger.error(
                    "Failed to upload transport package -> {}".format(
                        package_url)
                )
                return None
            logger.info(
                "Successfully uploaded transport package -> {}; new package ID -> {}".format(
                    package_name, package_id
                )
            )

        # Step 2: Create Transport Workbench (if not yet exist)
        workbench_name = package_name.split(".")[0]
        logger.info(
            "Check if workbench -> {} is already deployed...".format(
                workbench_name)
        )
        # check if the package name has the suffix "(deployed)" - this indicates it is alreadey
        # successfully deployed (see renaming at the end of this method)
        response = self.getNodeByParentAndName(
            transport_root_volume_id, workbench_name + " (deployed)"
        )
        workbench_id = self.getResultValue(response, "id")
        if workbench_id:
            logger.info(
                "Workbench -> {} has already been deployed successfully; existing workbench ID -> {}; skipping transport".format(
                    workbench_name, workbench_id
                )
            )
            # we return and skip this transport...
            return response
        else:
            logger.info(
                "Check if workbench -> {} already exists...".format(
                    workbench_name)
            )
            response = self.getNodeByParentAndName(
                transport_root_volume_id, workbench_name
            )
            workbench_id = self.getResultValue(response, "id")
            if workbench_id:
                logger.info(
                    "Workbench -> {} does already exist but is not successfully deployed; existing workbench ID -> {}".format(
                        workbench_name, workbench_id
                    )
                )
            else:
                response = self.createTransportWorkbench(workbench_name)
                workbench_id = self.getResultValue(response, "id")
                if not workbench_id:
                    logger.error(
                        "Failed to create workbench -> {}".format(
                            workbench_name)
                    )
                    return None
                logger.info(
                    "Successfully created workbench -> {}; new workbench ID -> {}".format(
                        workbench_name, workbench_id
                    )
                )

        # Step 3: Unpack Transport Package to Workbench
        logger.info(
            "Unpack transport package -> {} ({}) to workbench -> {} ({})".format(
                package_name, package_id, workbench_name, workbench_id
            )
        )
        response = self.unpackTransportPackage(package_id, workbench_id)
        if response == None:
            logger.error(
                "Failed to unpack the transport package -> {}".format(
                    package_name)
            )
            return None
        logger.info(
            "Successfully unpackaged to workbench -> {} ({})".format(
                workbench_name, workbench_id
            )
        )

        # Step 4: Deploy Workbench
        logger.info(
            "Deploy workbench -> {} ({})".format(workbench_name, workbench_id))
        response = self.deployWorkbench(workbench_id)
        if response == None:
            logger.warning(
                "Failed to to deploy workbench -> {}".format(workbench_name))
            return None

        logger.info(
            "Successfully deployed workbench -> {} ({})".format(
                workbench_name, workbench_id
            )
        )
        self.renameNode(
            workbench_id,
            workbench_name + " (deployed)",
            package_description,
        )

        return response

    # end method definition

    def replaceInXmlFiles(self, directory: str, search_pattern: str, replace_string: str) -> bool:
        """ Replaces all occurrences of the search pattern with the replace string in all XML files
            in the directory and its subdirectories.

        Args:
            directory (string): directory to traverse for XML files
            search_pattern (sting): string to search in the XML file
            replace_string (string): replacement string

        Returns:
            bool: True if a replacement happened, False otherwise
        """
        # Define the regular expression pattern to search for
        pattern = re.compile(search_pattern)
        found = False

        # Traverse the directory and its subdirectories
        for subdir, dirs, files in os.walk(directory):
            for file in files:
                # Check if the file is an XML file
                if file.endswith(".xml"):
                    # Read the contents of the file
                    file_path = os.path.join(subdir, file)
                    with open(file_path, "r") as f:
                        contents = f.read()

                    # Replace all occurrences of the search pattern with the replace string
                    new_contents = pattern.sub(replace_string, contents)

                    # Write the updated contents to the file if there were replacements
                    if contents != new_contents:
                        logger.info("Found search string -> {} in XML file -> {}. Updating content...".format(search_pattern, file_path))
                        # Write the updated contents to the file
                        with open(file_path, "w") as f:
                            f.write(new_contents)
                        found = True

        return found
    
        # end method definition

    def replaceTransportPlaceholders(self, zip_file_path: str, replacements: list) -> bool:
        """ Search and replace strings in the XML files of the transport packlage

        Args:
            zip_file_path (string): path to transport zip file
            replacements (list of dicts): list of replacement values; dict needs to have two values:
                                         * placeholder: text to replace
                                         * value: text to replace with

        Returns:
            Filename to the updated zip file
        """

        if not os.path.isfile(zip_file_path):
            logger.error("Zip file -> {} not found.".format(zip_file_path))
            return False

        # Extract the zip file to a temporary directory
        zip_file_folder = os.path.splitext(zip_file_path)[0]
        with zipfile.ZipFile(zip_file_path, "r") as zfile:
            zfile.extractall(zip_file_folder)

        modified = False

        # Replace search pattern with replace string in all XML files in the directory and its subdirectories
        for replacement in replacements:
            logger.info("Replace -> {} with -> {} in Transport package -> {}".format(replacement["placeholder"], replacement["value"], zip_file_folder))
            found = self.replaceInXmlFiles(zip_file_folder, replacement["placeholder"], replacement["value"])
            if found:
                logger.info("Found replacement string -> {} in Transport package -> {}".format(replacement["placeholder"], zip_file_folder))
                modified = True
            else:
                logger.warning("Did not find replacement string -> {} in Transport package -> {}".format(replacement["placeholder"], zip_file_folder))

        if not modified:
            logger.warning("None of the replacements have been found in transport -> {}".format(zip_file_folder))
            return False

        # Create the new zip file and add all files from the directory to it
        new_zip_file_path = os.path.dirname(zip_file_path) + "/new_" + os.path.basename(zip_file_path)
        logger.info("Content of transport -> {} has been modified - repacking to new zip file -> {}".format(zip_file_folder, new_zip_file_path))
        with zipfile.ZipFile(new_zip_file_path, "w", zipfile.ZIP_DEFLATED) as zip_ref:
            for subdir, dirs, files in os.walk(zip_file_folder):
                for file in files:
                    file_path = os.path.join(subdir, file)
                    rel_path = os.path.relpath(file_path, zip_file_folder)
                    zip_ref.write(file_path, arcname=rel_path)

        # Close the new zip file and delete the temporary directory
        zip_ref.close()
        old_zip_file_path = os.path.dirname(zip_file_path) + "/old_" + os.path.basename(zip_file_path)
        logger.info("Rename orginal transport zip file -> {} to -> {}".format(zip_file_path, old_zip_file_path))
        os.rename(zip_file_path, old_zip_file_path)
        logger.info("Rename new transport zip file -> {} to -> {}".format(new_zip_file_path, zip_file_path))
        os.rename(new_zip_file_path, zip_file_path)

        # Return the path to the new zip file
        return True

        # end method definition

    def getWorkspaceTypes(self):
        """Get all workspace types configured in Extended ECM.

        Args:
            None
        Return:
            Workspace Types (json) or None if the request fails.
        """

        requestUrl = (
            self.config()["businessworkspacetypes"]
            + "?expand_templates=true&expand_wksp_info=true"
        )
        requestHeader = self.requestFormHeader()

        logger.info("Get workspace types; calling -> {}".format(requestUrl))

        retries = 0
        while True:
            workspaceTypeResponse = requests.get(
                requestUrl, headers=requestHeader, cookies=self.cookie()
            )
            if workspaceTypeResponse.ok:
                return self.parseRequestResponse(workspaceTypeResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif workspaceTypeResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to get workspace types; status -> {}; error -> {}".format(
                        workspaceTypeResponse.status_code, workspaceTypeResponse.text
                    )
                )
                return None

    # end method definition

    def getBusinessObjectType(self, external_system_id: str, type_name: str):
        """Get business object type information.

        Args:
            external_system_id (string): external system Id (such as "TM6")
            type_name (string): type name (such as "SAP Customer")
        Return:
            Workspace Type information (json) or None if the request fails.
        """

        requestUrl = (
            self.config()["externalSystem"]
            + "/"
            + str(external_system_id)
            + "/botypes/"
            + str(type_name)
        )
        requestHeader = self.requestFormHeader()

        logger.info(
            "Get business object type -> {} for external system -> {}; calling -> {}".format(
                type_name, external_system_id, requestUrl
            )
        )

        retries = 0
        while True:
            businessObjectTypeResponse = requests.get(
                requestUrl, headers=requestHeader, cookies=self.cookie()
            )
            if businessObjectTypeResponse.ok:
                return self.parseRequestResponse(businessObjectTypeResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif businessObjectTypeResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to get business object type -> {}; status -> {}; error -> {}".format(
                        type_name,
                        businessObjectTypeResponse.status_code,
                        businessObjectTypeResponse.text,
                    )
                )
                return None

    # end method definition

    def getWorkspaceCreateForm(
        self,
        template_id: int,
        external_system_id: int = None,
        bo_type: int = None,
        bo_id: int = None,
        parent_id: int = None,
    ):
        """Get the Workspace create form.

        Args:
            template_id (integer): ID of the workspace template
            external_system_id (string): identifier of the external system (None if no external system)
            bo_type (string): business object type (None if no external system)
            bo_id (string): business object identifier / key (None if no external system)
            parent_id (string): parent ID of the workspaces. Needs only be specified in special
                                cases where workspace location cannot be derived from workspace
                                type definition, e.g. sub-workspace
        Return:
            Workspace Create Form data (json) or None if the request fails.
        """

        requestUrl = self.config()[
            "businessworkspacecreateform"
        ] + "?template_id={}".format(template_id)
        # Is a parent ID specifified? Then we need to add it to the request URL
        if parent_id is not None:
            requestUrl += "&parent_id={}".format(parent_id)
        # Is this workspace connected to a business application / external system?
        if external_system_id and bo_type and bo_id:
            requestUrl += "&ext_system_id={}".format(external_system_id)
            requestUrl += "&bo_type={}".format(bo_type)
            requestUrl += "&bo_id={}".format(bo_id)
            logger.info(
                "Use business object connection -> ({}, {}, {}) for workspace template -> {}".format(
                    external_system_id, bo_type, bo_id, template_id
                )
            )
        requestHeader = self.requestFormHeader()

        logger.info(
            "Get workspace create form for template -> {}; calling -> {}".format(
                template_id, requestUrl
            )
        )

        retries = 0
        while True:
            workspaceCreateFormResponse = requests.get(
                requestUrl, headers=requestHeader, cookies=self.cookie()
            )
            if workspaceCreateFormResponse.ok:
                return self.parseRequestResponse(workspaceCreateFormResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif workspaceCreateFormResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to get workspace create form for template -> {}; status -> {}; error -> {}".format(
                        template_id,
                        workspaceCreateFormResponse.status_code,
                        workspaceCreateFormResponse.text,
                    )
                )
                return None

    # end method definition

    def getWorkspace(self, node_id: int):
        """Get a workspace based on the node ID.

        Args:
            node_id (integer) is the node Id of the workspace
        Return:
            Node information (json) or None if no node with this ID is found.
        """

        requestUrl = self.config()["businessworkspaces"] + "/" + str(node_id)
        requestHeader = self.requestFormHeader()

        logger.info(
            "Get workspace with ID -> {}; calling -> {}".format(
                node_id, requestUrl)
        )

        retries = 0
        while True:
            getWorkspaceResponse = requests.get(
                requestUrl, headers=requestHeader, cookies=self.cookie()
            )
            if getWorkspaceResponse.ok:
                return self.parseRequestResponse(getWorkspaceResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif getWorkspaceResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to get workspace with ID -> {}; status -> {}; error -> {}".format(
                        node_id,
                        getWorkspaceResponse.status_code,
                        getWorkspaceResponse.text,
                    )
                )
                return None

    # end method definition

    def getWorkspaceByNameAndType(
        self, name: str, type_name: str, expanded_view: bool = True
    ):
        """Lookup workspace based on workspace name and workspace type name.

        Args:
            name (string): name of the workspace
            type_name (string): name of the workspace type
            expanded_view (boolean): if 'False' then just search in recently
                                     accessed business workspace for this name and type
                                     if 'True' (this is the default) then search in all
                                     workspaces for this name and type
        Return:
            Workspace information (json) or None if the workspace is not found.
        """

        # Add query parameters (these are NOT passed via JSon body!)
        query = {
            "where_name": name,
            "where_workspace_type_name": type_name,
            "expanded_view": expanded_view,
        }
        encodedQuery = urllib.parse.urlencode(query, doseq=True)

        requestUrl = self.config()["businessworkspaces"] + \
            "?{}".format(encodedQuery)
        requestHeader = self.requestFormHeader()

        logger.info(
            "Get workspace with name -> {} and type -> {}; calling -> {}".format(
                name, type_name, requestUrl
            )
        )

        retries = 0
        while True:
            getWorkpaceResponse = requests.get(
                requestUrl, headers=requestHeader, cookies=self.cookie()
            )
            if getWorkpaceResponse.ok:
                return self.parseRequestResponse(getWorkpaceResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif getWorkpaceResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.warning(
                    "Failed to get workspace -> {} of type -> {}; status -> {}; error -> {}".format(
                        name,
                        type_name,
                        getWorkpaceResponse.status_code,
                        getWorkpaceResponse.text,
                    )
                )
                return None

    # end method definition

    def createWorkspace(
        self,
        workspace_template_id: int,
        workspace_name: str,
        workspace_description: str,
        workspace_type: int,
        category_data: dict = {},
        external_system_id: int = None,
        bo_type: int = None,
        bo_id: int = None,
        parent_id: int = None,
    ):
        """Create a new business workspace.

        Args:
            workspace_template_id (integer): ID of the workspace template
            workspace_name (string): name of the workspace
            workspace_description (string): description of the workspace
            workspace_type (integer): type ID of the workspace
            category_data (dict): category and attributes
            external_system_id (string): identifier of the external system (None if no external system)
            bo_type (string): business object type (None if no external system)
            bo_id (string): business object identifier / key (None if no external system)
            parent_id (string): parent ID of the workspaces. Needs only be specified in special
                                cases where workspace location cannot be derived from workspace
                                type definition
        Return:
            Workspace Create Form data (json) or None if the request fails.
        """

        createWorkspacePostData = {
            "template_id": str(workspace_template_id),
            "name": workspace_name,
            "description": workspace_description,
            "wksp_type_id": str(workspace_type),
            "type": str(848),
            "roles": category_data,
        }

        # Is this workspace connected to a business application / external system?
        if external_system_id and bo_type and bo_id:
            createWorkspacePostData["ext_system_id"] = str(external_system_id)
            createWorkspacePostData["bo_type"] = str(bo_type)
            createWorkspacePostData["bo_id"] = str(bo_id)
            logger.info(
                "Use business object connection -> ({}, {}, {}) for workspace -> {}".format(
                    external_system_id, bo_type, bo_id, workspace_name
                )
            )

        # If workspace creation location cannot be derived from the workspace type
        # there may be an optional parent parameter passed to this method. This can
        # also be the case if workspaces are nested into eachother:
        if parent_id is not None:
            createWorkspacePostData["parent_id"] = parent_id
            logger.info(
                "Use specified location -> {} for workspace -> {}".format(
                    parent_id, workspace_name
                )
            )
        else:
            logger.info(
                "Determine location of workspace -> {} via workspace type -> {}".format(
                    workspace_name, workspace_type
                )
            )

        requestUrl = self.config()["businessworkspaces"]
        requestHeader = self.requestFormHeader()

        logger.info(
            "Create workspace -> {} with type -> {} from template -> {}; calling -> {}".format(
                workspace_name, workspace_type, workspace_template_id, requestUrl
            )
        )

        retries = 0
        while True:
            # This REST API needs a special treatment: we encapsulate the payload as JSON into a "body" tag.
            # See https://developer.opentext.com/apis/14ba85a7-4693-48d3-8c93-9214c663edd2/4403207c-40f1-476a-b794-fdb563e37e1f/07229613-7ef4-4519-8b8a-47eaff639d42#operation/createBusinessWorkspace
            workspaceResponse = requests.post(
                requestUrl,
                headers=requestHeader,
                data={"body": json.dumps(createWorkspacePostData)},
                cookies=self.cookie(),
            )
            if workspaceResponse.ok:
                return self.parseRequestResponse(workspaceResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif workspaceResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to create workspace -> {} from template -> {}; status -> {}; error -> {}".format(
                        workspace_name,
                        workspace_template_id,
                        workspaceResponse.status_code,
                        workspaceResponse.text,
                    )
                )
                return None

    # end method definition

    def createWorkspaceRelationship(
        self, workspace_id: int, related_workspace_id: int, relationship_type: str = "child"
    ):
        """Create a relationship between two workspaces.

        Args:
            workspace_id: ID of the workspace
            related_workspace_id: ID of the related workspace
            relationship_type: "parent" or "child" - "child is default if omitted
        Return:
            Workspace Relationship data (json) or None if the request fails.
        """

        createWorkspaceRelationshipPostData = {
            "rel_bw_id": str(related_workspace_id),
            "rel_type": relationship_type,
        }

        requestUrl = self.config()["businessworkspaces"] + "/{}/relateditems".format(
            workspace_id
        )
        requestHeader = self.requestFormHeader()

        logger.info(
            "Create workspace relationship between -> {} and -> {}; calling -> {}".format(
                workspace_id, related_workspace_id, requestUrl
            )
        )

        retries = 0
        while True:
            workspaceRelationshipResponse = requests.post(
                requestUrl,
                headers=requestHeader,
                data=createWorkspaceRelationshipPostData,
                cookies=self.cookie(),
            )
            if workspaceRelationshipResponse.ok:
                return self.parseRequestResponse(workspaceRelationshipResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif workspaceRelationshipResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to create workspace relationship between -> {} and -> {}; status -> {}; error -> {}".format(
                        workspace_id,
                        related_workspace_id,
                        workspaceRelationshipResponse.status_code,
                        workspaceRelationshipResponse.text,
                    )
                )
                return None

    # end method definition

    def getWorkspaceRelationships(self, workspace_id: int):
        """Get the Workspace relationships to other workspaces.

        Args:
            workspace_id: ID of the workspace template
        Return:
            Workspace relationships (json) or None if the request fails.
        """

        requestUrl = (
            self.config()["businessworkspaces"] + "/" +
            str(workspace_id) + "/relateditems"
        )
        requestHeader = self.requestFormHeader()

        logger.info(
            "Get related workspaces for workspace -> {}; calling -> {}".format(
                workspace_id, requestUrl
            )
        )

        retries = 0
        while True:
            workspaceRolesResponse = requests.get(
                requestUrl, headers=requestHeader, cookies=self.cookie()
            )
            if workspaceRolesResponse.ok:
                return self.parseRequestResponse(workspaceRolesResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif workspaceRolesResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to get related workspaces of workspace -> {}; status -> {}; error -> {}".format(
                        workspace_id,
                        workspaceRolesResponse.status_code,
                        workspaceRolesResponse.text,
                    )
                )
                return None

    # end method definition

    def getWorkspaceRoles(self, workspace_id: int):
        """Get the Workspace roles.

        Args:
            workspace_id: ID of the workspace template
        Return:
            Workspace Roles data (json) or None if the request fails.
        """

        requestUrl = (
            self.config()["businessworkspaces"] + "/" +
            str(workspace_id) + "/roles"
        )
        requestHeader = self.requestFormHeader()

        logger.info(
            "Get workspace roles of workspace -> {}; calling -> {}".format(
                workspace_id, requestUrl
            )
        )

        retries = 0
        while True:
            workspaceRolesResponse = requests.get(
                requestUrl, headers=requestHeader, cookies=self.cookie()
            )
            if workspaceRolesResponse.ok:
                return self.parseRequestResponse(workspaceRolesResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif workspaceRolesResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to get roles of workspace -> {}; status -> {}; error -> {}".format(
                        workspace_id,
                        workspaceRolesResponse.status_code,
                        workspaceRolesResponse.text,
                    )
                )
                return None

    # end method definition

    def addMemberToWorkspace(self, workspace_id: int, role_id: int, member_id: int, show_warning: bool = True):
        """Add member to a workspace role. Check that the user is not yet a member.

        Args:
            workspace_id (integer): ID of the workspace
            role_id (integer): ID of the role
            member_id (integer): User or Group Id
            show_warning: if True shows a warning if member is already in role
        Return:
            Workspace Role Membership (json) or None if the request fails.
        """

        addMemberToWorkspacePostData = {"id": str(member_id)}

        requestUrl = self.config()[
            "businessworkspaces"
        ] + "/{}/roles/{}/members".format(workspace_id, role_id)
        requestHeader = self.requestFormHeader()

        logger.info(
            "Check if user/group -> {} is already in role -> {} of workspace -> {}; calling -> {}".format(
                member_id, role_id, workspace_id, requestUrl
            )
        )

        workspaceMembershipResponse = requests.get(
            requestUrl, headers=requestHeader, cookies=self.cookie()
        )
        if not workspaceMembershipResponse.ok:
            logger.error(
                "Failed to get workspace members; status -> {}; error -> {}".format(
                    workspaceMembershipResponse.status_code,
                    workspaceMembershipResponse.text,
                )
            )
            return None

        workspace_members = self.parseRequestResponse(
            workspaceMembershipResponse)

        if self.existResultItem(workspace_members, "id", member_id):
            if show_warning:
                logger.warning(
                    "User -> {} is already a member of role -> {} of workspace -> {}".format(
                        member_id, role_id, workspace_id
                    )
                )
            return workspace_members

        logger.info(
            "Add user/group -> {} to role -> {} of workspace -> {}; calling -> {}".format(
                member_id, role_id, workspace_id, requestUrl
            )
        )

        workspaceMembershipResponse = requests.post(
            requestUrl,
            headers=requestHeader,
            data=addMemberToWorkspacePostData,
            cookies=self.cookie(),
        )

        if workspaceMembershipResponse.ok:
            return self.parseRequestResponse(workspaceMembershipResponse)
        else:
            logger.error(
                "Failed to add user/group -> {} to role -> {} of workspace -> {}; status -> {}; error -> {}".format(
                    member_id,
                    role_id,
                    workspace_id,
                    workspaceMembershipResponse.status_code,
                    workspaceMembershipResponse.text,
                )
            )
            return None

    # end method definition

    def removeMemberFromWorkspace(self, workspace_id: int, role_id: int, member_id: int, show_warning: bool = True):
        """Remove a member from a workspace role. Check that the user is currently a member.

        Args:
            workspace_id (integer): ID of the workspace
            role_id (integer): ID of the role
            member_id (integer): User or Group Id
            show_warning: if True shows a warning if member is not in role
        Return:
            Workspace Role Membership (json) or None if the request fails.
        """

        requestUrl = self.config()[
            "businessworkspaces"
        ] + "/{}/roles/{}/members".format(workspace_id, role_id)
        requestHeader = self.requestFormHeader()

        logger.info(
            "Check if user/group -> {} is in role -> {} of workspace -> {}; calling -> {}".format(
                member_id, role_id, workspace_id, requestUrl
            )
        )

        workspaceMembershipResponse = requests.get(
            requestUrl, headers=requestHeader, cookies=self.cookie()
        )
        if not workspaceMembershipResponse.ok:
            logger.error(
                "Failed to get workspace members; status -> {}; error -> {}".format(
                    workspaceMembershipResponse.status_code,
                    workspaceMembershipResponse.text,
                )
            )
            return None

        workspace_members = self.parseRequestResponse(
            workspaceMembershipResponse)

        if not self.existResultItem(workspace_members, "id", member_id):
            if show_warning:
                logger.warning(
                    "User -> {} is not a member of role -> {} of workspace -> {}".format(
                        member_id, role_id, workspace_id
                    )
                )
            return None

        requestUrl = self.config()[
            "businessworkspaces"
        ] + "/{}/roles/{}/members/{}".format(workspace_id, role_id, member_id)

        logger.info(
            "Removing user/group -> {} from role -> {} of workspace -> {}; calling -> {}".format(
                member_id, role_id, workspace_id, requestUrl
            )
        )

        workspaceMembershipResponse = requests.delete(
            requestUrl,
            headers=requestHeader,
            cookies=self.cookie(),
        )

        if workspaceMembershipResponse.ok:
            return self.parseRequestResponse(workspaceMembershipResponse)
        else:
            logger.error(
                "Failed to remove user/group -> {} to role -> {} of workspace -> {}; status -> {}; error -> {}".format(
                    member_id,
                    role_id,
                    workspace_id,
                    workspaceMembershipResponse.status_code,
                    workspaceMembershipResponse.text,
                )
            )
            return None

    # end method definition

    def assignWorkspacePermissions(
        self, workspace_id: int, role_id: int, permissions: list, apply_to: int = 2
    ):
        """Update permissions of a workspace role
        Args:
            workspace_id (integer): ID of the workspace
            role_id (integer): ID of the role
            permissions (list): list of permissions - potential elements:
                                "see"
                                "see_contents"
                                "modify"
                                "edit_attributes"
                                "add_items"
                                "reserve"
                                "add_major_version"
                                "delete_versions"
                                "delete"
                                "edit_permissions"
            apply_to (integer):  0 = this item
                                 1 = sub-items
                                 2 = This item and sub-items
                                 3 = This item and immediate sub-items
        Return:
            Workspace Role Membership (json) or None if the request fails.
        """

        requestUrl = self.config()["businessworkspaces"] + "/{}/roles/{}".format(
            workspace_id, role_id
        )

        requestHeader = self.requestFormHeader()

        logger.info(
            "Updating Permissions of role -> {} of workspace -> {} with permissions -> {}; calling -> {}".format(
                role_id, workspace_id, permissions, requestUrl
            )
        )

        permissionPostData = {
            "permissions": permissions,
            "apply_to": apply_to,
        }

        retries = 0
        while True:
            workspacePermissionResponse = requests.put(
                requestUrl,
                headers=requestHeader,
                data={"body": json.dumps(permissionPostData)},
                cookies=self.cookie(),
            )
            if workspacePermissionResponse.ok:
                return self.parseRequestResponse(workspacePermissionResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif workspacePermissionResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to update permissions for role -> {} of workspace -> {}; status -> {}; error -> {}".format(
                        role_id,
                        workspace_id,
                        workspacePermissionResponse.status_code,
                        workspacePermissionResponse.text,
                    )
                )
                return None

    # end method definition

    def createItem(
        self,
        parent_id: int,
        item_type: str,
        item_name: str,
        item_description: str = "",
        url: str = "",
        original_id: int = 0,
    ):
        """Create an Extended ECM item. This REST call is somewhat limited. It cannot set favortie (featured item) or hidden item.
           It does also not accept owner group information.

        Args:
            parent_id (integer): node ID of the parent
            item_type (string): type of the item (e.g. 0 = foler, 140 = URL)
            item_name (string): name of the item
            item_description (string): description of the item
            url (string): address of the URL item (if it is an URL item type)
            original_id (integer)
        Return:
            Response (json) of the created item or None if the REST call has failed.
        """

        createItemPostData = {
            "parent_id": parent_id,
            "type": item_type,
            "name": item_name,
            "description": item_description,
        }

        if url:
            createItemPostData["url"] = url
        if original_id > 0:
            createItemPostData["original_id"] = original_id

        requestUrl = self.config()["nodesUrlv2"]
        requestHeader = self.requestFormHeader()

        logger.info(
            "Create item -> {} (type -> {}) under parent -> {}; calling -> {}".format(
                item_name, item_type, parent_id, requestUrl
            )
        )

        retries = 0
        while True:
            # This REST API needs a special treatment: we encapsulate the payload as JSON into a "body" tag.
            createItemResponse = requests.post(
                requestUrl,
                data={"body": json.dumps(createItemPostData)},
                headers=requestHeader,
                cookies=self.cookie(),
            )
            if createItemResponse.ok:
                return self.parseRequestResponse(createItemResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif createItemResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to create item -> {}; status -> {}; error -> {}".format(
                        item_name,
                        createItemResponse.status_code,
                        createItemResponse.text,
                    )
                )
                return None

    # end method definition

    def updateItem(
        self,
        node_id: int,
        parent_id: int = 0,
        item_name: str = "",
        item_description: str = "",
    ):
        """Update an Extended ECM item (parent, name, description). Changing the parent ID is
           a move operation. If parent ID = 0 the item will not be moved.

        Args:
            node_id (integer): ID of the node
            parent_id (integer): node ID of the new parent (move operation)
            item_name (string): new name of the item
            item_description (string): new description of the item
        Return:
            Response (json) of the created item or None if the REST call has failed.
        """

        updateItemPutData = {
            "name": item_name,
            "description": item_description,
        }

        if parent_id:
            # this is a move operation
            updateItemPutData["parent_id"] = parent_id

        requestUrl = self.config()["nodesUrlv2"] + "/" + str(node_id)
        requestHeader = self.requestFormHeader()

        logger.info(
            "Update item -> {} with data -> {}; calling -> {}".format(
                item_name, updateItemPutData, requestUrl
            )
        )

        retries = 0
        while True:
            # This REST API needs a special treatment: we encapsulate the payload as JSON into a "body" tag.
            updateItemResponse = requests.put(
                requestUrl,
                data={"body": json.dumps(updateItemPutData)},
                headers=requestHeader,
                cookies=self.cookie(),
            )
            if updateItemResponse.ok:
                return self.parseRequestResponse(updateItemResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif updateItemResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to update item -> {}; status -> {}; error -> {}".format(
                        item_name,
                        updateItemResponse.status_code,
                        updateItemResponse.text,
                    )
                )
                return None

    # end method definition

    def getWebReportParameters(self, nickname: str):
        """Get parameters of a Web Report in Extended ECM. These are defined on the Web Report node
            (Properties --> Parameters)

        Args:
            nickname (str): nickname of the Web Reports node.
        Return:
            Response: list of Web Report parameters. Each list item is a dict describing the parameter.
            Structure of the list items:
            {
                "type": "string",
                "parm_name": "string",
                "display_text": "string",
                "prompt": true,
                "prompt_order": 0,
                "default_value": null,
                "description": "string",
                "mandatory": true
            }
            None if the REST call has failed.
        """

        requestUrl = self.config()["webReportsUrl"] + \
            "/" + nickname + "/parameters"
        requestHeader = self.requestFormHeader()

        logger.info(
            "Retrieving parameters of Web Report with nickname -> {}; calling -> {}".format(
                nickname, requestUrl
            )
        )
        retries = 0
        while True:
            runWebReportResponse = requests.get(
                requestUrl, headers=requestHeader, cookies=self.cookie()
            )
            if runWebReportResponse.ok:
                # Return the "data" element which is a list of dict items:
                result_dict = self.parseRequestResponse(runWebReportResponse)
                logger.debug(
                    "Web Report parameters result -> {}".format(result_dict))
                if not result_dict.get("data"):
                    return None
                return result_dict["data"]
            # Check if Session has expired - then re-authenticate and try once more
            elif runWebReportResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to retrieve parameters of Web Report with nickname -> {}; status -> {}; error -> {}".format(
                        nickname,
                        runWebReportResponse.status_code,
                        runWebReportResponse.text,
                    )
                )
                return None

    # end method definition

    def runWebReport(self, nickname: str, web_report_parameters: dict = {}):
        """Run a Web Report that is identified by its nick name.

        Args:
            nickname (str): nickname of the Web Reports node.
            web_report_parameters (dict): Parameters of the Web Report (names + value pairs)
        Return:
            Response (json) or None if the Web Report execution has failed.
        """

        requestUrl = self.config()["webReportsUrl"] + "/" + nickname
        requestHeader = self.requestFormHeader()

        logger.info(
            "Running Web Report with nickname -> {}; calling -> {}".format(
                nickname, requestUrl
            )
        )

        retries = 0
        while True:
            runWebReportResponse = requests.post(
                requestUrl,
                data=web_report_parameters,
                headers=requestHeader,
                cookies=self.cookie(),
            )
            if runWebReportResponse.ok:
                return self.parseRequestResponse(runWebReportResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif runWebReportResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to run web report with nickname -> {}; status -> {}; error -> {}".format(
                        nickname,
                        runWebReportResponse.status_code,
                        runWebReportResponse.text,
                    )
                )
                return None

    # end method definition

    def installCSApplication(self, application_name: str):
        """Install a CS Application (based on WebReports)

        Args:
            application_name (string): name of the application (e.g. OTPOReports, OTRMReports, OTRMSecReports)
        Return:
            Response (json) or None if the installation of the CS Application has failed.
        """

        installCSApplicationPostData = {"appName": application_name}

        requestUrl = self.config()["csApplicationsUrl"] + "/install"
        requestHeader = self.requestFormHeader()

        logger.info(
            "Install CS Application -> {}; calling -> {}".format(
                application_name, requestUrl
            )
        )

        retries = 0
        while True:
            installCSApplicationResponse = requests.post(
                requestUrl,
                data=installCSApplicationPostData,
                headers=requestHeader,
                cookies=self.cookie(),
            )
            if installCSApplicationResponse.ok:
                return self.parseRequestResponse(installCSApplicationResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif installCSApplicationResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to install CS Application -> {}; status -> {}; error -> {}".format(
                        application_name,
                        installCSApplicationResponse.status_code,
                        installCSApplicationResponse.text,
                    )
                )
                return None

    # end method definition

    def assignItemToUserGroup(
        self, node_id: int, subject: str, instruction: str, assignees: list
    ):
        """Assign an Extended ECM item to users and groups. This is a function used by
           Extended ECM for Government.

        Args:
            node_id (integer): node ID of the Extended ECM item (e.g. a workspace or a document)
            subject (string): title / subject of the assignment
            instructions (string): more detailed description or instructions for the assignment
            assignees (list): list of IDs of users or groups
        Return:
            Response (json) or None if the assignment has failed.
        """

        assignmentPostData = {
            "subject": subject,
            "instruction": instruction,
            "assignees": assignees,
        }

        requestUrl = (
            self.config()["nodesUrlv2"] + "/" +
            str(node_id) + "/xgovassignments"
        )

        requestHeader = self.requestFormHeader()

        logger.info(
            "Assign item with ID -> {} to assignees -> {} (subject -> {}); calling -> {}".format(
                node_id, assignees, subject, requestUrl
            )
        )

        retries = 0
        while True:
            # This REST API needs a special treatment: we encapsulate the payload as JSON into a "add_assignment" tag.
            assignmentResponse = requests.post(
                requestUrl,
                data={"add_assignment": json.dumps(assignmentPostData)},
                headers=requestHeader,
                cookies=self.cookie(),
            )
            if assignmentResponse.ok:
                return self.parseRequestResponse(assignmentResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif assignmentResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to assign item with ID -> {} to assignees -> {} (subject -> {}); status -> {}; error -> {}".format(
                        node_id,
                        assignees,
                        subject,
                        assignmentResponse.status_code,
                        assignmentResponse.text,
                    )
                )
                return None

    # end method definition

    def convertPermissionStringToPermissionValue(self, permissions: list) -> int:
        """Converts a list of permission names (strongs) to a bit-mask.

        Args:
            permissions (list): List of permission names - see conversion variable below.

        Return: bit-encoded permission value (integer) 
        """

        conversion = {
            "see": 130,  # Bits 2 and 8
            "see_contents": 36865,  # Bit 17
            "modify": 65536,  # Bit 18
            "edit_attributes": 131072,  # Bit 19
            "add_items": 4,  # Bit 3
            "reserve": 8192,  # Bit 14
            "add_major_version": 4194304,  # Bit 23
            "delete_versions": 16384,  # Bit 15
            "delete": 8,  # Bit 4
            "edit_permissions": 16,  # Bit 5
        }

        permission_value = 0

        for permission in permissions:
            if not conversion.get(permission):
                logger.error(
                    "Illegal permission value -> {}".format(permission))
                return 0
            permission_value += conversion[permission]

        return permission_value

    # end method definition

    def convertPermissionValueToPermissionString(self, permission_value: int) -> list:
        """Converts a bit-encoded permission value to a list of permission names (strings).

        Args:
            permission_value (integer): bit-encoded permission value

        Return: list of permission names
        """

        conversion = {
            "see": 130,  # Bits 2 and 8
            "see_contents": 36865,  # Bit 17
            "modify": 65536,  # Bit 18
            "edit_attributes": 131072,  # Bit 19
            "add_items": 4,  # Bit 3
            "reserve": 8192,  # Bit 14
            "add_major_version": 4194304,  # Bit 23
            "delete_versions": 16384,  # Bit 15
            "delete": 8,  # Bit 4
            "edit_permissions": 16,  # Bit 5
        }

        permissions = []

        for key, value in conversion.items():
            if permission_value & value:  # binary and
                permissions.append(key)

        return permissions

    # end method definition

    def assignPermission(
        self,
        node_id: int,
        assignee_type: str,
        assignee: int,
        permissions: list,
        apply_to: int = 0,
    ):
        """Assign permissions for Extended ECM item to a user or group.

        Args:
            node_id (integer): node ID of the Extended ECM item
            assignee_type (string): this can be either "owner", "group" (for owner group),
                                    "public", or "custom" (assigned access)
            assignee (integer): ID of user or group ("right ID"). If 0 and assigneeType
                                is "owner" or "group" then it is assumed that the owner and
                                owner group should not be changed.
            permissions (list): list of permissions - potential elements:
                                "see"
                                "see_contents"
                                "modify"
                                "edit_attributes"
                                "add_items"
                                "reserve"
                                "add_major_version"
                                "delete_versions"
                                "delete"
                                "edit_permissions"
            apply_to (integer):  0 = this item
                                 1 = sub-items
                                 2 = This item and sub-items
                                 3 = This item and immediate sub-items
        Return:
            Response (json) or None if the assignment of permissions has failed.
        """

        if not assignee_type or not assignee_type in [
            "owner",
            "group",
            "public",
            "custom",
        ]:
            logger.error(
                "Missing or wrong assignee type. Needs to be owner, group, public or custom!"
            )
            return None
        if assignee_type == "custom" and not assignee:
            logger.error("Missing permission assignee!")
            return None

        permissionPostData = {
            "permissions": permissions,
            "apply_to": apply_to,
        }

        # Assignees can be specified for owner and group and must be specified for custom:
        #
        if assignee:
            permissionPostData["right_id"] = assignee

        requestUrl = (
            self.config()["nodesUrlv2"]
            + "/"
            + str(node_id)
            + "/permissions/"
            + assignee_type
        )

        requestHeader = self.requestFormHeader()

        logger.info(
            "Assign permissions -> {} to item with ID -> {}; assignee type -> {}; calling -> {}".format(
                permissions, node_id, assignee_type, requestUrl
            )
        )

        retries = 0
        while True:
            # This REST API needs a special treatment: we encapsulate the payload as JSON into a "body" tag.
            if assignee_type == "custom":
                # Custom also has a REST POST - we prefer this one as to
                # also allows to add a new assigned permission (user or group):
                permissionResponse = requests.post(
                    requestUrl,
                    data={"body": json.dumps(permissionPostData)},
                    headers=requestHeader,
                    cookies=self.cookie(),
                )
            else:
                # Owner, Owner Group and Public require REST PUT:
                permissionResponse = requests.put(
                    requestUrl,
                    data={"body": json.dumps(permissionPostData)},
                    headers=requestHeader,
                    cookies=self.cookie(),
                )
            if permissionResponse.ok:
                return self.parseRequestResponse(permissionResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif permissionResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to assign permissions -> {} to item with ID -> {}; status -> {}; error -> {}".format(
                        permissions,
                        node_id,
                        permissionResponse.status_code,
                        permissionResponse.text,
                    )
                )
                return None

    # end method definition

    def assignClassification(
        self, node_id: int, classifications: list, apply_to_sub_items: bool = False
    ):
        """Assign one or multiple classifications to an Extended ECM item
        Args:
            node_id (integer): node ID of the Extended ECM item
            classifications (list): list of classification item IDs
            apply_to_sub_items (boolean): if True the classification is applied to the item and all its sub-items
                                          if False the classification is only applied to the item
        Return:
            Response (json) or None if the assignment of the classification has failed.
        """

        # the REST API expects a list of dict elements with "id" and the actual IDs
        classification_list = []
        for classification in classifications:
            classification_list.append({"id": classification})

        classificationPostData = {
            "class_id": classification_list,
            "apply_to_sub_items": apply_to_sub_items,
        }

        requestUrl = self.config()["nodesUrl"] + \
            "/" + str(node_id) + "/classifications"

        requestHeader = self.requestFormHeader()

        logger.info(
            "Assign classifications with IDs -> {} to item with ID -> {}; calling -> {}".format(
                classifications, node_id, requestUrl
            )
        )

        retries = 0
        while True:
            classificationResponse = requests.post(
                requestUrl,
                data=classificationPostData,
                headers=requestHeader,
                cookies=self.cookie(),
            )
            if classificationResponse.ok:
                return self.parseRequestResponse(classificationResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif classificationResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to assign classifications with IDs -> {} to item with ID -> {}; status -> {}; error -> {}".format(
                        classifications,
                        node_id,
                        classificationResponse.status_code,
                        classificationResponse.text,
                    )
                )
                return None

    # end method definition

    def assignRMClassification(
        self, node_id: int, rm_classification: int, apply_to_sub_items: bool = False
    ):
        """Assign a RM classification to an Extended ECM item
        Args:
            node_id (integer): node ID of the Extended ECM item
            rm_classification (integer): Records Management classification ID
            apply_to_sub_items (boolean): if True the RM classification is applied to the item and all its sub-items
                                          if False the RM classification is only applied to the item
        Return:
            Response (json) or None if the assignment of the RM classification has failed.
        """

        rmClassificationPostData = {
            "class_id": rm_classification,
            "apply_to_sub_items": apply_to_sub_items,
        }

        requestUrl = (
            self.config()["nodesUrl"] + "/" +
            str(node_id) + "/rmclassifications"
        )

        requestHeader = self.requestFormHeader()

        logger.info(
            "Assign RM classifications with ID -> {} to item with ID -> {}; calling -> {}".format(
                rm_classification, node_id, requestUrl
            )
        )

        retries = 0
        while True:
            classificationResponse = requests.post(
                requestUrl,
                data=rmClassificationPostData,
                headers=requestHeader,
                cookies=self.cookie(),
            )
            if classificationResponse.ok:
                return self.parseRequestResponse(classificationResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif classificationResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to assign RM classifications with ID -> {} to item with ID -> {}; status -> {}; error -> {}".format(
                        rm_classification,
                        node_id,
                        classificationResponse.status_code,
                        classificationResponse.text,
                    )
                )
                return None

    # end method definition

    def registerWorkspaceTemplate(self, node_id: int):
        """Register a workspace template as project template for Extended ECM for Engineering
        Args:
            node_id (integer): node ID of the Extended ECM workspace template
        Return:
            Response (json) or None if the registration of the workspace template has failed.
        """

        registrationPostData = {"ids": "{{ {} }}".format(node_id)}

        requestUrl = self.config()["xEngProjectTemplateUrl"]

        requestHeader = self.requestFormHeader()

        logger.info(
            "Register workspace template with ID -> {}; calling -> {}".format(
                node_id, requestUrl
            )
        )

        retries = 0
        while True:
            registrationResponse = requests.post(
                requestUrl,
                data=registrationPostData,
                headers=requestHeader,
                cookies=self.cookie(),
            )
            if registrationResponse.ok:
                return self.parseRequestResponse(registrationResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif registrationResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to register Workspace Template with ID -> {}; status -> {}; error -> {}".format(
                        node_id,
                        registrationResponse.status_code,
                        registrationResponse.text,
                    )
                )
                return None

    # end method definition

    def getRecordsManagementRSIs(self, limit: int = 100):
        """Get all Records management RSIs togther with their RSI Schedules.

        Args:
            limit (integer): max elements to return
        Return:
            List of Records Management RSIs or None if the request fails.
            Each RSI list element is a dict with this structure:
            {
                "RSIID": 0,
                "RSI": "string",
                "Title": "string",
                "Subject": "string",
                "Description": "string",
                "CreateDate": "string",
                "RSIStatus": "string",
                "StatusDate": "string",
                "DiscontFlag": 0,
                "DiscontDate": "string",
                "DiscontComment": "string",
                "Active": 0,
                "DispControl": 0,
                "RSIScheduleID": 0,
                "RetStage": "string",
                "RecordType": 0,
                "EventType": 0,
                "RSIRuleCode": "string",
                "DateToUse": "string",
                "YearEndMonth": 0,
                "YearEndDay": 0,
                "RetYears": 0,
                "RetMonths": 0,
                "RetDays": 0,
                "RetIntervals": 0,
                "EventRuleDate": "string",
                "EventRule": "string",
                "EventComment": "string",
                "StageAction": "string",
                "FixedRet": 0,
                "ActionCode": "string",
                "ActionDescription": "string",
                "Disposition": "string",
                "ApprovalFlag": 0,
                "MaximumRet": 0,
                "ObjectType": "LIV"
            }
        """

        requestUrl = self.config()["rsisUrl"] + "?limit=" + str(limit)
        requestHeader = self.requestFormHeader()

        logger.info(
            "Get list of Records Management RSIs; calling -> {}".format(
                requestUrl)
        )

        retries = 0
        while True:
            rsisResponse = requests.get(
                requestUrl, headers=requestHeader, cookies=self.cookie()
            )
            if rsisResponse.ok:
                rsi_dict = self.parseRequestResponse(rsisResponse)
                return rsi_dict["results"]["data"]["rsis"]
            # Check if Session has expired - then re-authenticate and try once more
            elif rsisResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to get list of Records Management RSIs; status -> {}; error -> {}".format(
                        rsisResponse.status_code, rsisResponse.text
                    )
                )
                return None

    # end method definition

    def getRecordsManagementCodes(self):
        """Get Records Management Codes. These are the most basic data types of
           the Records Management configuration and required to create RSIs and
           other higher-level Records Management configurations

        Args: None
        Return:
            RSI data (json) or None if the request fails.
        """

        requestUrl = self.config()["recordsManagementUrlv2"] + "/rmcodes"
        requestHeader = self.requestFormHeader()

        logger.info(
            "Get list of Records Management codes; calling -> {}".format(
                requestUrl)
        )

        retries = 0
        while True:
            rmCodesResponse = requests.get(
                requestUrl, headers=requestHeader, cookies=self.cookie()
            )
            if rmCodesResponse.ok:
                rm_codes_dict = self.parseRequestResponse(rmCodesResponse)
                return rm_codes_dict["results"]["data"]
            # Check if Session has expired - then re-authenticate and try once more
            elif rmCodesResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to get list of Records Management codes; status -> {}; error -> {}".format(
                        rmCodesResponse.status_code, rmCodesResponse.text
                    )
                )
                return None

    # end method definition

    # This is not yet working. REST API endpoint seems not to be in 22.4. Retest with 23.1
    def updateRecordsManagementCodes(self, rm_codes: dict):
        """Update Records Management Codes. These are the most basic data types of
           the Records Management configuration and required to create RSIs and
           other higher-level Records Management configurations

        Args:
            rm_codes: dict with the updated codes
        Return:
            RSI data (json) or None if the request fails.
        """

        updateRMCodesPostData = {}

        requestUrl = self.config()["recordsManagementUrl"] + "/rmcodes"
        requestHeader = self.requestFormHeader()

        logger.info(
            "Update Records Management codes; calling -> {}".format(requestUrl))

        retries = 0
        while True:
            rmCodesResponse = requests.post(
                requestUrl,
                headers=requestHeader,
                data=updateRMCodesPostData,
                cookies=self.cookie(),
            )
            if rmCodesResponse.ok:
                rm_codes_dict = self.parseRequestResponse(rmCodesResponse)
                return rm_codes_dict["results"]["data"]
            # Check if Session has expired - then re-authenticate and try once more
            elif rmCodesResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to update Records Management codes; status -> {}; error -> {}".format(
                        rmCodesResponse.status_code, rmCodesResponse.text
                    )
                )
                return None

    # end method definition

    def createRecordsManagementRSI(
        self,
        name: str,
        status: str,
        status_date: str,
        description: str,
        subject: str,
        title: str,
        dispcontrol: bool,
    ):
        """Create a new Records Management RSI.

        Args:
            name (string): name of the RSI
            status (string): status of the RSI
            status_date (string): statusDate of the RSI YYYY-MM-DDTHH:mm:ss
            description (string): description of the RSI
            subject (string): status of the RSI
            title (string): status of the RSI
            dispcontrol (boolean): status of the RSI
        Return:
            RSI data (json) or None if the request fails.
        """

        if statusDate == "":
            now = datetime.now()
            statusDate = now.strftime("%Y-%m-%dT%H:%M:%S")

        createRSIPostData = {
            "name": name,
            "status": status,
            "statusDate": status_date,
            "description": description,
            "subject": subject,
            "title": title,
            "dispcontrol": dispcontrol,
        }

        requestUrl = self.config()["rsiSchedulesUrl"]

        requestHeader = self.requestFormHeader()

        logger.info(
            "Create Records Management RSI -> {}; calling -> {}".format(
                name, requestUrl
            )
        )

        retries = 0
        while True:
            rsiResponse = requests.post(
                requestUrl,
                headers=requestHeader,
                data=createRSIPostData,
                cookies=self.cookie(),
            )
            if rsiResponse.ok:
                return self.parseRequestResponse(rsiResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif rsiResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to create Records Management RSI -> {}; status -> {}; error -> {}".format(
                        name,
                        rsiResponse.status_code,
                        rsiResponse.text,
                    )
                )
                return None

    # end method definition

    def createRecordsManagementRSISchedule(
        self,
        rsi_id: int,
        stage: str,
        event_type: int = 1,
        object_type: str = "LIV",
        rule_code: str = "",
        rule_comment: str = "",
        date_to_use: int = 91,
        retention_years: int = 0,
        retention_months: int = 0,
        retention_days: int = 0,
        category_id: int = 0,
        attribute_id: int = 0,
        year_end_month: int = 12,
        year_end_day: int = 31,
        retention_intervals: int = 1,
        fixed_retention: bool = True,
        maximum_retention: bool = True,
        fixed_date: str = "",
        event_condition: str = "",
        disposition: str = "",
        action_code: int = 0,
        description: str = "",
        new_status: str = "",
        min_num_versions_to_keep: int = 1,
        purge_superseded: bool = False,
        purge_majors: bool = False,
        mark_official_rendition: bool = False,
    ):
        """Create a new Records Management RSI Schedule for an existing RSI.

        Args:
            rsi_id (integer): ID of an existing RSI the schedule should be created for
            object_type (string): either "LIV" - Classified Objects (default) or "LRM" - RM Classifications
            stage: retention stage - this is the key parameter to define multiple stages (stages are basically schedules)
            event_type: 1 Calculated Date, 2 Calendar Calculation, 3 Event Based, 4 Fixed Date, 5 Permanent
            rule_code: rule code - this value must be defined upfront
            rule_comment: comment for the rule
            date_to_use: 91 Create Date, 92 Reserved Data, 93 Modification Date, 94 Status Date, 95 Records Date
            retention_years: years to wait before disposition
            retention_months: month to wait before disposition
            retention_days: days to wait before disposition
            category_id (integer): ID of the category
            attribute_id (integer): ID of the category attribute
            year_end_month (integer): month the year ends (normally 12)
            year_end_day (integer): day the year ends (normally 31)
            retention_intervals (integer): retention intervals
            fixed_retention (boolean): fixedRetention
            maximum_retention: maximumRetention
            fixed_date(string): fixed date format : YYYY-MM-DDTHH:mm:ss
            event_condition (string): eventCondition
            disposition: disposition
            action_code (integer): 0 None, 1 Change Status, 7 Close, 8 Finalize Record, 9 Mark Official, 10 Export, 11 Update Storage Provider, 12 Delete Electronic Format, 15 Purge Versions, 16 Make Rendition, 32 Destroy
            description (string): description
            new_status (string): new status
            min_num_versions_to_keep (integer): minimum document versions to keep
            purge_superseded (boolean): purge superseded
            purge_majors (boolean): purge majors
            mark_official_rendition (boolean): mark official rendition
        Return:
            RSI Schedule data (json) or None if the request fails.
        """

        if fixedDate == "":
            now = datetime.now()
            fixedDate = now.strftime("%Y-%m-%dT%H:%M:%S")

        createRSISchedulePostData = {
            "objectType": object_type,
            "stage": stage,
            "eventType": event_type,
            "ruleCode": rule_code,
            "ruleComment": rule_comment,
            "dateToUse": date_to_use,
            "retentionYears": retention_years,
            "retentionMonths": retention_months,
            "retentionDays": retention_days,
            "categoryId": category_id,
            "attributeId": attribute_id,
            "yearEndMonth": year_end_month,
            "yearEndDay": year_end_day,
            "retentionIntervals": retention_intervals,
            "fixedRetention": fixed_retention,
            "maximumRetention": maximum_retention,
            "fixedDate": fixed_date,
            "eventCondition": event_condition,
            "disposition": disposition,
            "actionCode": action_code,
            "description": description,
            "newStatus": new_status,
            "minNumVersionsToKeep": min_num_versions_to_keep,
            "purgeSuperseded": purge_superseded,
            "purgeMajors": purge_majors,
            "markOfficialRendition": mark_official_rendition,
        }

        requestUrl = self.config()["rsiSchedulesUrl"] + \
            "/" + str(rsi_id) + "/stages"

        requestHeader = self.requestFormHeader()

        logger.info(
            "Create Records Management RSI Schedule -> {} for RSI -> {}; calling -> {}".format(
                stage, rsi_id, requestUrl
            )
        )

        retries = 0
        while True:
            rsiScheduleResponse = requests.post(
                requestUrl,
                headers=requestHeader,
                data=createRSISchedulePostData,
                cookies=self.cookie(),
            )
            if rsiScheduleResponse.ok:
                return self.parseRequestResponse(rsiScheduleResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif rsiScheduleResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to create Records Management RSI Schedule -> {}; status -> {}; error -> {}".format(
                        stage,
                        rsiScheduleResponse.status_code,
                        rsiScheduleResponse.text,
                    )
                )
                return None

    # end method definition

    def createRecordsManagementHold(
        self,
        hold_type: str,
        name: str,
        comment: str,
        alternate_id: str = "",
        parent_id: int = 0,
        date_applied: str = "",
        date_to_remove: str = "",
    ):
        """Create a new Records Management Hold.

        Args:
            parent_id (integer): ID of the parent node. If no parent is 0 the item will be created right under "Hold Management" (top level item)
            type (string): type of the Hold
            name (string): name of the RSI
            comment (string): comment
            alternate_id (string): alternate hold ID
            date_applied (string): create date of the Hold in this format: YYYY-MM-DDTHH:mm:ss
            date_to_remove (string): suspend date of the Hold in this format: YYYY-MM-DDTHH:mm:ss
        Return:
            Hold data (json) or None if the request fails. The JSon structure is this: {'holdID': <ID>}
        """

        if date_applied == "":
            now = datetime.now()
            date_applied = now.strftime("%Y-%m-%dT%H:%M:%S")

        createHoldPostData = {
            "type": hold_type,
            "name": name,
            "comment": comment,
            "date_applied": date_applied,
            "date_to_remove": date_to_remove,
            "alternate_id": alternate_id,
        }

        if parent_id > 0:
            createHoldPostData["parent_id"] = parent_id

        requestUrl = self.config()["holdsUrl"]

        requestHeader = self.requestFormHeader()

        logger.info(
            "Create Records Management Hold -> {}; calling -> {}".format(
                name, requestUrl
            )
        )

        retries = 0
        while True:
            holdsResponse = requests.post(
                requestUrl,
                headers=requestHeader,
                data=createHoldPostData,
                cookies=self.cookie(),
            )
            if holdsResponse.ok:
                return self.parseRequestResponse(holdsResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif holdsResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to create Records Management Hold -> {}; status -> {}; error -> {}".format(
                        name,
                        holdsResponse.status_code,
                        holdsResponse.text,
                    )
                )
                return None

    # end method definition

    def getRecordsManagementHolds(self):
        """Get a list of all Records Management Holds in the system. Even though there are folders
           in the holds management area in RM these are not real folders - they cannot be retrieved
           with getNodeByParentAndName() thus we need this method to get them all.

           Args: None
           Return: response with list of holds:
            "results": {
                "data": {
                    "holds": [
                        {
                            "HoldID": 0,
                            "HoldName": "string",
                            "ActiveHold": 0,
                            "OBJECT": 0,
                            "ApplyPatron": "string",
                            "DateApplied": "string",
                            "HoldComment": "string",
                            "HoldType": "string",
                            "DateToRemove": "string",
                            "DateRemoved": "string",
                            "RemovalPatron": "string",
                            "RemovalComment": "string",
                            "EditDate": "string",
                            "EditPatron": "string",
                            "AlternateHoldID": 0,
                            "ParentID": 0
                        }
                    ]
                }
            }
        """

        requestUrl = self.config()["holdsUrlv2"]

        requestHeader = self.requestFormHeader()

        logger.info(
            "Get list of Records Management Holds; calling -> {}".format(
                requestUrl
            )
        )

        retries = 0
        while True:
            holdsResponse = requests.get(
                requestUrl,
                headers=requestHeader,
                cookies=self.cookie(),
            )
            if holdsResponse.ok:
                return self.parseRequestResponse(holdsResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif holdsResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to get list of Records Management Holds; status -> {}; error -> {}".format(
                        holdsResponse.status_code,
                        holdsResponse.text,
                    )
                )
                return None

    # end method definition

    def importRecordsManagementSettings(self, file_path: str):
        """Import Records Management settings from a file that is uploaded from the python pod
        Args:
            file_path (string): path + filename of config file in Python container filesystem
        Return:
            True if if the REST call succeeds or False otherwise.
        """

        requestUrl = self.config()["recordsManagementUrl"] + "/importSettings"

        requestHeader = (
            self.cookie()
        )  # for some reason we have to omit the other header parts here - otherwise we get a 400 response

        logger.info(
            "Importing Records Management Settings from file -> {}; calling -> {}".format(
                file_path, requestUrl
            )
        )

        filename = os.path.basename(file_path)
        if not os.path.exists(file_path):
            logger.error(
                "The file -> {} does not exist in path -> {}!".format(
                    filename, os.path.dirname(file_path)
                )
            )
            return False
        settingsPostFile = {"file": (filename, open(file_path), "text/xml")}

        retries = 0
        while True:
            settingsResponse = requests.post(
                requestUrl,
                files=settingsPostFile,
                headers=requestHeader,
                cookies=self.cookie(),
            )
            if settingsResponse.ok:
                return True
            # Check if Session has expired - then re-authenticate and try once more
            elif settingsResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to import Records Management Settings from file -> {}; status -> {}; error -> {}".format(
                        file_path,
                        settingsResponse.status_code,
                        settingsResponse.text,
                    )
                )
                return False

    # end method definition

    def importRecordsManagementCodes(
        self, file_path: str, update_existing_codes: bool = True
    ):
        """Import RM Codes from a file that is uploaded from the python pod
        Args:
            file_path (string): path + filename of settings file in Python container filesystem
            update_existing_codes (boolean): Flag that controls whether existing table maintenance codes
                                             should be updated.
        Return:
            True if if the REST call succeeds or False otherwise.
        """

        requestUrl = self.config()["recordsManagementUrl"] + "/importCodes"

        requestHeader = (
            self.cookie()
        )  # for some reason we have to omit the other header parts here - otherwise we get a 400 response

        logger.info(
            "Importing Records Management Codes from file -> {}; calling -> {}".format(
                file_path, requestUrl
            )
        )

        settingsPostData = {"updateExistingCodes": update_existing_codes}

        filename = os.path.basename(file_path)
        if not os.path.exists(file_path):
            logger.error(
                "The file -> {} does not exist in path -> {}!".format(
                    filename, os.path.dirname(file_path)
                )
            )
            return False
        settingsPostFile = {"file": (filename, open(file_path), "text/xml")}

        retries = 0
        while True:
            settingsResponse = requests.post(
                requestUrl,
                data=settingsPostData,
                files=settingsPostFile,
                headers=requestHeader,
                cookies=self.cookie(),
            )
            if settingsResponse.ok:
                return True
            # Check if Session has expired - then re-authenticate and try once more
            elif settingsResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to import Records Management Codes from file -> {}; status -> {}; error -> {}".format(
                        file_path,
                        settingsResponse.status_code,
                        settingsResponse.text,
                    )
                )
                return False

    # end method definition

    def importRecordsManagementRSIs(
        self,
        file_path: str,
        update_existing_rsis: bool = True,
        delete_schedules: bool = False,
    ):
        """Import RM RSIs from a config file that is uploaded from the Python pod
        Args:
            file_path (string): path + filename of config file in Python container filesystem
            update_existing_rsis (boolean): whether or not existing RSIs should be updated (or ignored)
            delete_schedules (boolean): whether RSI Schedules should be deleted
        Return:
            True if if the REST call succeeds or False otherwise.
        """

        requestUrl = self.config()["recordsManagementUrl"] + "/importRSIs"

        requestHeader = (
            self.cookie()
        )  # for some reason we have to omit the other header parts here - otherwise we get a 400 response

        logger.info(
            "Importing Records Management RSIs from file -> {}; calling -> {}".format(
                file_path, requestUrl
            )
        )

        settingsPostData = {
            "updateExistingRSIs": update_existing_rsis,
            "deleteSchedules": delete_schedules,
        }

        filename = os.path.basename(file_path)
        if not os.path.exists(file_path):
            logger.error(
                "The file -> {} does not exist in path -> {}!".format(
                    filename, os.path.dirname(file_path)
                )
            )
            return False
        settingsPostFile = {"file": (filename, open(file_path), "text/xml")}

        retries = 0
        while True:
            settingsResponse = requests.post(
                requestUrl,
                data=settingsPostData,
                files=settingsPostFile,
                headers=requestHeader,
                cookies=self.cookie(),
            )
            if settingsResponse.ok:
                return True
            # Check if Session has expired - then re-authenticate and try once more
            elif settingsResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to import Records Management RSIs from file -> {}; status -> {}; error -> {}".format(
                        file_path,
                        settingsResponse.status_code,
                        settingsResponse.text,
                    )
                )
                return False

    # end method definition

    def importPhysicalObjectsSettings(self, file_path: str):
        """Import Physical Objects settings from a config file that is uploaded from the python pod
        Args:
            file_path (string): path + filename of config file in Python container filesystem
        Return:
            True if if the REST call succeeds or False otherwise.
        """

        requestUrl = self.config()["physicalObjectsUrl"] + "/importSettings"

        requestHeader = (
            self.cookie()
        )  # for some reason we have to omit the other header parts here - otherwise we get a 400 response

        logger.info(
            "Importing Physical Objects Settings from server file -> {}; calling -> {}".format(
                file_path, requestUrl
            )
        )

        filename = os.path.basename(file_path)
        if not os.path.exists(file_path):
            logger.error(
                "The file -> {} does not exist in path -> {}!".format(
                    filename, os.path.dirname(file_path)
                )
            )
            return False
        settingsPostFile = {"file": (filename, open(file_path), "text/xml")}

        retries = 0
        while True:
            settingsResponse = requests.post(
                requestUrl,
                files=settingsPostFile,
                headers=requestHeader,
                cookies=self.cookie(),
            )
            if settingsResponse.ok:
                return True
            # Check if Session has expired - then re-authenticate and try once more
            elif settingsResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to import Physical Objects settings from file -> {}; status -> {}; error -> {}".format(
                        file_path,
                        settingsResponse.status_code,
                        settingsResponse.text,
                    )
                )
                return False

    # end method definition

    def importPhysicalObjectsCodes(
        self, file_path: str, update_existing_codes: bool = True
    ):
        """Import Physical Objects codes from a config file that is uploaded from the Python pod
        Args:
            file_path (string): path + filename of config file in Python container filesystem
            update_existing_codes (boolean): whether or not existing codes should be updated (default = True)
        Return:
            True if if the REST call succeeds or False otherwise.
        """

        requestUrl = self.config()["physicalObjectsUrl"] + "/importCodes"

        requestHeader = (
            self.cookie()
        )  # for some reason we have to omit the other header parts here - otherwise we get a 400 response

        logger.info(
            "Importing Physical Objects Codes from file -> {}; calling -> {}".format(
                file_path, requestUrl
            )
        )

        settingsPostData = {"updateExistingCodes": update_existing_codes}

        filename = os.path.basename(file_path)
        if not os.path.exists(file_path):
            logger.error(
                "The file -> {} does not exist in path -> {}!".format(
                    filename, os.path.dirname(file_path)
                )
            )
            return False
        settingsPostFile = {"file": (filename, open(file_path), "text/xml")}

        retries = 0
        while True:
            settingsResponse = requests.post(
                requestUrl,
                data=settingsPostData,
                files=settingsPostFile,
                headers=requestHeader,
                cookies=self.cookie(),
            )
            if settingsResponse.ok:
                return True
            # Check if Session has expired - then re-authenticate and try once more
            elif settingsResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to import Physical Objects Codes from file -> {}; status -> {}; error -> {}".format(
                        file_path,
                        settingsResponse.status_code,
                        settingsResponse.text,
                    )
                )
                return False

    # end method definition

    def importPhysicalObjectsLocators(self, file_path: str):
        """Import Physical Objects locators from a config file that is uploaded from the python pod
        Args:
            file_path (string): path + filename of config file in Python container filesystem
        Return:
            True if if the REST call succeeds or False otherwise.
        """

        requestUrl = self.config()["physicalObjectsUrl"] + "/importLocators"

        requestHeader = (
            self.cookie()
        )  # for some reason we have to omit the other header parts here - otherwise we get a 400 response

        logger.info(
            "Importing Physical Objects Locators from file -> {}; calling -> {}".format(
                file_path, requestUrl
            )
        )

        filename = os.path.basename(file_path)
        if not os.path.exists(file_path):
            logger.error(
                "The file -> {} does not exist in path -> {}!".format(
                    filename, os.path.dirname(file_path)
                )
            )
            return False
        settingsPostFile = {"file": (filename, open(file_path), "text/xml")}

        retries = 0
        while True:
            settingsResponse = requests.post(
                requestUrl,
                files=settingsPostFile,
                headers=requestHeader,
                cookies=self.cookie(),
            )
            if settingsResponse.ok:
                return True
            # Check if Session has expired - then re-authenticate and try once more
            elif settingsResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to import Physical Objects Locators from file -> {}; status -> {}; error -> {}".format(
                        file_path,
                        settingsResponse.status_code,
                        settingsResponse.text,
                    )
                )
                return False

    # end method definition

    def importSecurityClearanceCodes(self, file_path: str, include_users: bool = False):
        """Import Security Clearance codes from a config file that is uploaded from the python pod
        Args:
            file_path (string): path + filename of config file in Python container filesystem
            include_users (boolean): defines if users should be included or not
        Return:
            True if if the REST call succeeds or False otherwise.
        """

        requestUrl = self.config()["securityClearancesUrl"] + "/importCodes"

        requestHeader = (
            self.cookie()
        )  # for some reason we have to omit the other header parts here - otherwise we get a 400 response

        logger.info(
            "Importing Security Clearance Codes from file -> {}; calling -> {}".format(
                file_path, requestUrl
            )
        )

        settingsPostData = {"includeusers": include_users}

        filename = os.path.basename(file_path)
        if not os.path.exists(file_path):
            logger.error(
                "The file -> {} does not exist in path -> {}!".format(
                    filename, os.path.dirname(file_path)
                )
            )
            return False
        settingsPostFile = {"file": (filename, open(file_path), "text/xml")}

        retries = 0
        while True:
            settingsResponse = requests.post(
                requestUrl,
                data=settingsPostData,
                files=settingsPostFile,
                headers=requestHeader,
                cookies=self.cookie(),
            )
            if settingsResponse.ok:
                return True
            # Check if Session has expired - then re-authenticate and try once more
            elif settingsResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to import Security Clearance Codes from file -> {}; status -> {}; error -> {}".format(
                        file_path,
                        settingsResponse.status_code,
                        settingsResponse.text,
                    )
                )
                return False

    # end method definition

    def assignUserSecurityClearance(self, user_id: int, security_clearance: int):
        """Assign a Security Clearance level to an Extended ECM user

        Args:
            user_id: ID of the user
            security_clearance: security clearance level to be set
        Return:
            REST response or None if the REST call fails.
        """

        assignUserSecurityClearancePostData = {
            "securityLevel": security_clearance,
        }

        requestUrl = self.config()[
            "userSecurityUrl"
        ] + "/{}/securityclearancelevel".format(user_id)
        requestHeader = self.requestFormHeader()

        logger.info(
            "Assign security clearance -> {} to user ID -> {}; calling -> {}".format(
                security_clearance, user_id, requestUrl
            )
        )

        retries = 0
        while True:
            securityClearanceResponse = requests.post(
                requestUrl,
                headers=requestHeader,
                data=assignUserSecurityClearancePostData,
                cookies=self.cookie(),
            )
            if securityClearanceResponse.ok:
                return self.parseRequestResponse(securityClearanceResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif securityClearanceResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to assign security clearance -> {} to user -> {}; status -> {}; error -> {}".format(
                        user_id,
                        security_clearance,
                        securityClearanceResponse.status_code,
                        securityClearanceResponse.text,
                    )
                )
                return None

    # end method definition

    def assignUserSupplementalMarkings(self, user_id: int, supplemental_markings: list):
        """Assign a list of Supplemental Markings to a user


        Args:
            user_id (integer): ID of the user
            supplemental_markings (list of strings): list of Supplemental Markings to be set
        Return:
            REST response or None if the REST call fails.
        """

        assignUserSupplementalMarkingsPostData = {
            "suppMarks": supplemental_markings,
        }

        requestUrl = self.config()[
            "userSecurityUrl"
        ] + "/{}/supplementalmarkings".format(user_id)
        requestHeader = self.requestFormHeader()

        logger.info(
            "Assign supplemental markings -> {} to user ID -> {}; calling -> {}".format(
                supplemental_markings, user_id, requestUrl
            )
        )

        retries = 0
        while True:
            supplementalMarkingsResponse = requests.post(
                requestUrl,
                headers=requestHeader,
                data=assignUserSupplementalMarkingsPostData,
                cookies=self.cookie(),
            )
            if supplementalMarkingsResponse.ok:
                return self.parseRequestResponse(supplementalMarkingsResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif supplementalMarkingsResponse.status_code == 401 and retries == 0:
                logger.warning(
                    "Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to assign supplemental markings -> {} to user -> {}; status -> {}; error -> {}".format(
                        user_id,
                        supplemental_markings,
                        supplementalMarkingsResponse.status_code,
                        supplementalMarkingsResponse.text,
                    )
                )
                return None

    # end method definition

    def volumeTranslator(self, current_node_id: int, translator: object, languages: list):

        # Get current node based on the ID:
        current_node = self.getNode(current_node_id)
        current_node_id = self.getResultValue(current_node, "id")

        name = self.getResultValue(current_node, "name")
        description = self.getResultValue(current_node, "description")
        names_multilingual = self.getResultValue(current_node, "name_multilingual")
        descriptions_multilingual = self.getResultValue(current_node, "description_multilingual")

        for language in languages:
            if language == "en":
                continue
            # Does the language not exist as metadata language or is it already translated?
            # Then we skip this language:
            if language in names_multilingual and names_multilingual["en"] and not names_multilingual[language]:
                names_multilingual[language] = translator.translate("en", language, names_multilingual["en"])
            if language in descriptions_multilingual and descriptions_multilingual["en"] and not descriptions_multilingual[language]:
                descriptions_multilingual[language] = translator.translate("en", language, descriptions_multilingual["en"])

        # Rename node multi-lingual:
        response = self.renameNode(current_node_id, name, description, names_multilingual, descriptions_multilingual)

        # Get children nodes of the current node:
        results = self.getSubnodes(current_node_id, limit=200)["results"]

        for result in results:
            self.volumeTranslator(result["data"]["properties"]["id"], translator, languages)
