"""
OTDS Module to implement functions to read / write OTDS objects
such as Ressources, Users, Groups, Licenses, Trusted Sites, ...

Important: userIDs consists of login name + "@" + partition name 

Class: OTDS
Methods:

__init__ : class initializer
config : returns config data set
cookie : returns cookie information
credentials: returns set of username and password

baseUrl : returns OTDS base URL
restUrl : returns OTDS REST base URL
credentialUrl : returns the OTDS Credentials REST URL
authHandlerUrl : returns the OTDS Authentication Handler REST URL
partitionUrl : returns OTDS Aartition REST URL
accessRoleUrl : returns OTDS Access Role REST URL
oauthClientUrl : returns OTDS OAuth Client REST URL
resourceUrl : returns OTDS Resource REST URL
licenseUrl : returns OTDS License REST URL
tokenUrl : returns OTDS Token REST URL
usersUrl : returns OTDS Users REST URL
groupsUrl : returns OTDS Groups REST URL
systemConfigUrl : returns OTDS System Config REST URL

authenticate : authenticates at OTDS server

addLicenseToResource : adds (or updates) a product license to OTDS
getLicensesForResource : get list of licenses for a resource
deleteLicenseFromResource : deletes a license from a resource
assignUserToLicense : assign a user to a license for a resource

addPartition : add an OTDS partition
getPartition : get a partition with a specific name
addUser : add a user to a partion
getUser : get a user with a specific user ID (= login name @ partition)
updateUser : update attributes of on OTDS user
deleteUser : delete a user with a specific ID in a specific partition
resetUserPassword : reset a password of a specific user ID
addGroup: add an OTDS group
getGroup: get a OTDS group by its name
addUserToGroup : add an OTDS user to a OTDS group
addGroupToParentGroup : add on OTDS group to a parent group

addResource : add a new resource to OTDS
getResource : get an OTDS resource with a specific name
activateResource : activate an OTDS resource

getAccessRoles : get all OTDS Access Roles
getAccessRole: get an OTDS Access Role with a specific name
addPartitionToAccessRole : add an OTDS Partition to to an OTDS Access Role
addUserToAccessRole : add an OTDS user to to an OTDS Access Role
addGroupToAccessRole : add an OTDS group to to an OTDS Access Role
updateAccessRoleAttributes: update attributes of an existing access role

addSystemAttribute : add an OTDS System Attribute

getTrustedSites : get OTDS Trusted Sites
addTrustedSite : add a new trusted site to OTDS

addOauthClient : add a new OAuth client to OTDS
getOauthClient : get an OAuth client with a specific client ID
updateOauthClient : update an OAuth client
addOauthClientsToAccessRole : add an OTDS OAuth Client to an OTDS Access Role
getAccessToken : get an OTDS Access Token

addAuthHandlerSAML: add an authentication handler for SAML (e.g. for SuccessFactors)
addAuthHandlerSAP: add an authentication handler for SAP
addAuthHandlerOAuth: add an authentication handler for OAuth (used for Salesforce)

consolidate: consolidate an OTDS resource
impersonateResource: Configure impersonation for an OTDS resource
impersonateOauth: Configure impersonation for an OTDS OAuth Client

"""

__author__ = "Dr. Marc Diefenbruch"
__copyright__ = "Copyright 2023, OpenText"
__credits__ = ["Kai-Philip Gatzweiler", "Jim Bennett"]
__maintainer__ = "Dr. Marc Diefenbruch"
__email__ = "mdiefenb@opentext.com"

import os
import logging
import requests
import json
import base64

logger = logging.getLogger(os.path.basename(__file__))

requestHeaders = {
    "accept": "application/json;charset=utf-8",
    "Content-Type": "application/json",
}

requestFormHeaders = {
    "accept": "application/json;charset=utf-8",
    "Content-Type": "application/x-www-form-urlencoded",
}


class OTDS:
    """Used to automate stettings in OpenText Directory Services (OTDS)."""

    _config = None
    _cookie = None

    def __init__(
        self, protocol: str, hostname: str, port: int, username: str, password: str
    ):
        """Initialize the OTDS object

        Args:
            protocol (string): either http or https
            hostname (string): hostname of otds
            port (integer): port number - typically 80 or 443
            username (type): otds user name
            password (type): otds password
        """

        # Initialize otdsConfig as an empty dictionary
        otdsConfig = {}

        if hostname:
            otdsConfig["publicHostname"] = hostname
        else:
            otdsConfig["publicHostname"] = "otds"

        if protocol:
            otdsConfig["protocol"] = protocol
        else:
            otdsConfig["protocol"] = "http"

        if port:
            otdsConfig["port"] = port
        else:
            otdsConfig["port"] = 80

        if username:
            otdsConfig["username"] = username
        else:
            otdsConfig["username"] = "admin"

        if password:
            otdsConfig["password"] = password
        else:
            otdsConfig["password"] = ""

        otdsBaseUrl = protocol + "://" + otdsConfig["publicHostname"]
        if str(port) not in ["80", "443"]:
            otdsBaseUrl += ":{}".format(port)
        otdsBaseUrl += "/otdsws"
        otdsConfig["baseUrl"] = otdsBaseUrl

        otdsRestUrl = otdsBaseUrl + "/rest"
        otdsConfig["restUrl"] = otdsRestUrl

        otdsConfig["partitionUrl"] = otdsRestUrl + "/partitions"
        otdsConfig["accessRoleUrl"] = otdsRestUrl + "/accessroles"
        otdsConfig["credentialUrl"] = otdsRestUrl + "/authentication/credentials"
        otdsConfig["oauthClientUrl"] = otdsRestUrl + "/oauthclients"
        otdsConfig["tokenUrl"] = otdsBaseUrl + "/oauth2/token"
        otdsConfig["resourceUrl"] = otdsRestUrl + "/resources"
        otdsConfig["licenseUrl"] = otdsRestUrl + "/licensemanagement/licenses"
        otdsConfig["usersUrl"] = otdsRestUrl + "/users"
        otdsConfig["groupsUrl"] = otdsRestUrl + "/groups"
        otdsConfig["systemConfigUrl"] = otdsRestUrl + "/systemconfig"
        otdsConfig["authHandlerUrl"] = otdsRestUrl + "/authhandlers"
        otdsConfig["consolidationUrl"] = otdsRestUrl + "/consolidation"

        self._config = otdsConfig

    def config(self):
        return self._config

    def cookie(self):
        return self._cookie

    def credentials(self):
        return {
            "userName": self.config()["username"],
            "password": self.config()["password"],
        }

    def baseUrl(self):
        return self.config()["baseUrl"]

    def restUrl(self):
        return self.config()["restUrl"]

    def credentialUrl(self):
        return self.config()["credentialUrl"]

    def authHandlerUrl(self):
        return self.config()["authHandlerUrl"]

    def partitionUrl(self):
        return self.config()["partitionUrl"]

    def accessRoleUrl(self):
        return self.config()["accessRoleUrl"]

    def oauthClientUrl(self):
        return self.config()["oauthClientUrl"]

    def resourceUrl(self):
        return self.config()["resourceUrl"]

    def licenseUrl(self):
        return self.config()["licenseUrl"]

    def tokenUrl(self):
        return self.config()["tokenUrl"]

    def usersUrl(self):
        return self.config()["usersUrl"]

    def groupsUrl(self):
        return self.config()["groupsUrl"]

    def systemConfigUrl(self):
        return self.config()["systemConfigUrl"]

    def consolidationUrl(self):
        return self.config()["consolidationUrl"]

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
                message = "Cannot decode response as JSon; error -> {}".format(e)
            if show_error:
                logger.error(message)
            else:
                logger.warning(message)
            return None
        else:
            return dict_object

    def authenticate(self, revalidate: bool = False):
        """Authenticate at Directory Services and retrieve OTCS Ticket.

        Args:
            revalidate (bool): determine if a re-athentication is enforced
                               (e.g. if session has timed out with 401 error)
        Return: Cookie information. Also stores cookie information in self._cookie
        """

        # Already authenticated and session still valid?
        if self._cookie and not revalidate:
            return self._cookie

        otds_ticket = "NotSet"

        logger.info("Requesting OTDS ticket from {}".format(self.credentialUrl()))

        authenticateResponse = None
        try:
            authenticateResponse = requests.post(
                self.credentialUrl(), json=self.credentials(), headers=requestHeaders
            )
        except Exception as e:
            logger.warning(
                "Unable to connect to -> {} : {}".format(self.credentialUrl(), e)
            )
            logger.warning("OTDS service may not be ready yet.")
            return None

        if authenticateResponse.ok:
            authenticate_dict = self.parseRequestResponse(authenticateResponse)
            if not authenticate_dict:
                return None
            else:
                otds_ticket = authenticate_dict["ticket"]
                logger.info("Ticket -> {}".format(otds_ticket))
        else:
            logger.error(
                "Failed to request an OTDS ticket; error -> {}".format(
                    authenticateResponse.text
                )
            )
            return None

        self._cookie = {"OTDSTicket": otds_ticket}
        return self._cookie

    # end method definition

    def addLicenseToResource(
        self,
        path_to_license_file: str,
        product_name: str,
        product_description: str,
        resource_id: str,
        update: bool = True,
    ):
        """Adds a product license to OTDS.

        Args:
            pathToLicenseFile (string): fully qualified filename of the license file
            productName (string): product name
            productDescription (string): product description
            resource_id (string): OTDS resource ID (this is ID not the resource name!)
            update (boolean): whether or not an existing license should be updated
        Return: Request response (json) or None if the REST call fails
        """

        logger.info("Reading license file -> {}...".format(path_to_license_file))
        try:
            with open(path_to_license_file) as licenseFile:
                license_content = licenseFile.read()
        except IOError as e:
            logger.error(
                "Error opening license file -> {}; error -> {}".format(
                    path_to_license_file, e.strerror
                )
            )
            return None

        licensePostBodyJson = {
            "description": product_description,
            "name": product_name,
            "values": [
                {"name": "oTLicenseFile", "values": license_content},
                {"name": "oTLicenseResource", "values": resource_id},
                {"name": "oTLicenseFingerprintGenerator", "values": [None]},
            ],
        }

        requestUrl = self.licenseUrl()
        # Check if we want to update an existing license:
        if update:
            existing_license = self.getLicensesForResource(resource_id)
            if existing_license:
                requestUrl += "/" + existing_license[0]["id"]
            else:
                logger.info(
                    "No existing license for resource -> {} found - adding a new license...".format(
                        resource_id
                    )
                )
                # change strategy to create a new license:
                update = False

        logger.info(
            "Adding product license -> {} for product -> {} to resource -> {}; calling -> {}".format(
                path_to_license_file, product_description, resource_id, requestUrl
            )
        )

        retries = 0
        while True:
            if update:
                # Do a REST PUT call for update an existing license:
                uploadLicenseResponse = requests.put(
                    requestUrl,
                    json=licensePostBodyJson,
                    headers=requestHeaders,
                    cookies=self.cookie(),
                )
            else:
                # Do a REST POST call for creation of a new license:
                uploadLicenseResponse = requests.post(
                    requestUrl,
                    json=licensePostBodyJson,
                    headers=requestHeaders,
                    cookies=self.cookie(),
                )
            if uploadLicenseResponse.ok:
                return self.parseRequestResponse(uploadLicenseResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif uploadLicenseResponse.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to add product license -> {} for product -> {}; error -> {}".format(
                        path_to_license_file,
                        product_description,
                        uploadLicenseResponse.text,
                    )
                )
                return None

    # end method definition

    def getLicensesForResource(self, resource_id: str):
        """Get a product license for a resource in OTDS.

        Args:
            resource_id (string): OTDS resource ID (this is ID not the resource name!)
        Return: Licenses for a resource or None if the REST call fails
        """

        requestUrl = (
            self.licenseUrl()
            + "/assignedlicenses?resourceID="
            + resource_id
            + "&validOnly=false"
        )

        logger.info(
            "Get license for resource -> {}; calling -> {}".format(
                resource_id, requestUrl
            )
        )

        retries = 0
        while True:
            licenseResponse = requests.get(
                requestUrl, headers=requestHeaders, cookies=self.cookie()
            )
            if licenseResponse.ok:
                response_dict = self.parseRequestResponse(licenseResponse)
                if not response_dict:
                    return None
                return response_dict["licenseObjects"]["_licenses"]
            # Check if Session has expired - then re-authenticate and try once more
            elif licenseResponse.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to get license for resource -> {}; error -> {}".format(
                        resource_id, licenseResponse.text
                    )
                )
                return None

    # end method definition

    def deleteLicenseFromResource(self, resource_id: str, license_id: str):
        """Delete a product license for a resource in OTDS.

        Args:
            resource_id (string): OTDS resource ID (this is ID not the resource name!)
            licenseId (string): OTDS license ID (this is the ID not the license name!)
        Return: True if successful or False if the REST call fails
        """

        requestUrl = "{}/{}".format(self.licenseUrl(), license_id)

        logger.info(
            "Deleting product license -> {} from resource -> {}; calling -> {}".format(
                license_id, resource_id, requestUrl
            )
        )

        retries = 0
        while True:
            deleteResponse = requests.delete(
                requestUrl, headers=requestHeaders, cookies=self.cookie()
            )
            if deleteResponse.ok:
                return True
            # Check if Session has expired - then re-authenticate and try once more
            elif deleteResponse.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to delete license -> {} for resource -> {}; error -> {}".format(
                        license_id, resource_id, deleteResponse.text
                    )
                )
                return None

    # end method definition

    def assignUserToLicense(
        self,
        partition: str,
        user_id: str,
        resource_id: str,
        license_feature: str,
        license_name: str,
        license_type: str = "Full",
    ):
        """Assign a product license (feature) to a user in OTDS.

        Args:
            partition (string): user partition in OTDS, e.g. "Content Server Members"
            user_id (string): ID of the user (= login name)
            resource_id (string): OTDS resource ID (this is ID not the resource name!)
            license_feature (string): name of the license feature
            license_name (string): name of the license to assign
            license_type (string, optional): deault is "Full", Extended ECM also has "Occasional"
        Return: True if successful or False if the REST call fails
        """

        licenses = self.getLicensesForResource(resource_id)

        for lic in licenses:
            if lic["_oTLicenseProduct"] == license_name:
                licenseLocation = lic["id"]

        try:
            licenseLocation
        except UnboundLocalError:
            logger.error(
                "Cannot find license for resource -> {} for {}".format(
                    license_name, resource_id
                )
            )
            return None

        user = self.getUser(partition, user_id)
        if user:
            userLocation = user["location"]
        else:
            logger.error("Cannot find location for user -> {}".format(user_id))
            return None

        licensePostBodyJson = {
            "_oTLicenseType": license_type,
            "_oTLicenseProduct": "users",
            "name": userLocation,
            "values": [{"name": "counter", "values": [license_feature]}],
        }

        requestUrl = self.licenseUrl() + "/object/" + licenseLocation

        logger.info(
            "Assign license feature -> {} of license -> {} associated with resource -> {} to user -> {}; calling -> {}".format(
                license_feature, licenseLocation, resource_id, user_id, requestUrl
            )
        )

        retries = 0
        while True:
            addLicenseResponse = requests.post(
                requestUrl,
                json=licensePostBodyJson,
                headers=requestHeaders,
                cookies=self.cookie(),
            )
            if addLicenseResponse.ok:
                logger.info(
                    "Added license feature -> {} for user -> {}".format(
                        license_feature, user_id
                    )
                )
                return True
            # Check if Session has expired - then re-authenticate and try once more
            elif addLicenseResponse.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to add license feature -> {} associated with resource -> {} for user -> {}; status code -> {}".format(
                        license_feature,
                        resource_id,
                        user_id,
                        addLicenseResponse.status_code,
                    )
                )
                return False

    # end method definition

    def addPartition(self, name: str, description: str):
        """Add a new user partition to OTDS

        Args:
            name (string): name of the new partition
        Return:
            Request response (json) or None if the creation fails.
        """

        partitionPostBodyJson = {"name": name, "description": description}

        requestUrl = self.partitionUrl()

        logger.info(
            "Adding user partition -> {} ({}); calling -> {}".format(
                name, description, requestUrl
            )
        )

        retries = 0
        while True:
            partitionResponse = requests.post(
                requestUrl,
                json=partitionPostBodyJson,
                headers=requestHeaders,
                cookies=self.cookie(),
            )
            if partitionResponse.ok:
                return self.parseRequestResponse(partitionResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif partitionResponse.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to add user partition -> {}; error -> {}".format(
                        name, partitionResponse.text
                    )
                )
                return None

    # end method definition

    def getPartition(self, name: str, show_error: bool = True):
        """Get an existing user partition from OTDS

        Args:
            name (string): name of the partition to retrieve
            show_error (boolean): whether or not we want to log an error if partion is not found
        Return:
            Request response (json) or None if the creation fails.
        """

        requestUrl = "{}/{}".format(self.config()["partitionUrl"], name)

        logger.info(
            "Getting user partition -> {}; calling -> {}".format(name, requestUrl)
        )

        retries = 0
        while True:
            partitionResponse = requests.get(
                requestUrl, headers=requestHeaders, cookies=self.cookie()
            )
            if partitionResponse.ok:
                return self.parseRequestResponse(partitionResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif partitionResponse.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                if show_error:
                    logger.error(
                        "Failed to get partition -> {}; warning -> {}".format(
                            name, partitionResponse.text
                        )
                    )
                return None

    # end method definition

    def addUser(
        self,
        partition: str,
        name: str,
        description: str = "",
        first_name: str = "",
        last_name: str = "",
        email: str = "",
    ):
        """Add a new user to a user partition in OTDS

        Args:
            partition (string): name of the OTDS user partition (needs to exist)
            name (string): login name of the new user
            description (string): description of the new user
            first_name (string): first name of the new user
            last_name (string): last name of the new user
            email (string): email address of the new user
        Return:
            Request response (json) or None if the creation fails.
        """

        userPostBodyJson = {
            "userPartitionID": partition,
            "values": [
                {"name": "sn", "values": [last_name]},
                {"name": "givenName", "values": [first_name]},
                {"name": "mail", "values": [email]},
            ],
            "name": name,
            "description": description,
        }

        requestUrl = self.usersUrl()

        logger.info(
            "Adding user -> {} to partition -> {}; calling -> {}".format(
                name, partition, requestUrl
            )
        )
        logger.debug("User Attributes -> {}".format(userPostBodyJson))

        retries = 0
        while True:
            userResponse = requests.post(
                requestUrl,
                json=userPostBodyJson,
                headers=requestHeaders,
                cookies=self.cookie(),
            )
            if userResponse.ok:
                return self.parseRequestResponse(userResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif userResponse.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to add user -> {}; error -> {}".format(
                        name, userResponse.text
                    )
                )
                return None

    # end method definition

    def getUser(self, partition: str, user_id: str):
        """Get a user by its partition and user ID

        Args:
            partition (string): name of the partition
            user_id (string): ID of the user (= login name)
        Return:
            Request response (json) or None if the creation fails.
        """

        requestUrl = self.usersUrl() + "/" + user_id + "@" + partition

        logger.info(
            "Get user -> {} in partition -> {}; calling -> {}".format(
                user_id, partition, requestUrl
            )
        )

        retries = 0
        while True:
            userResponse = requests.get(
                requestUrl, headers=requestHeaders, cookies=self.cookie()
            )
            if userResponse.ok:
                return self.parseRequestResponse(userResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif userResponse.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to get user -> {}; error -> {}".format(
                        user_id, userResponse.text
                    )
                )
                return None

    # end method definition

    def updateUser(
        self, partition: str, user_id: str, attribute_name: str, attribute_value: str
    ):
        """Update a user attribute with a new value

        Args:
            partition (string): name of the partition
            user_id (string): ID of the user (= login name)
            attribute_name (string): name of the attribute
            attribute_value (string):new value of the attribute
        Return:
            Request response (json) or None if the creation fails.
        """

        userPatchBodyJson = {
            "userPartitionID": partition,
            "values": [{"name": attribute_name, "values": [attribute_value]}],
        }

        requestUrl = self.usersUrl() + "/" + user_id

        logger.info(
            "Update user -> {} attribute -> {} to value -> {}; calling -> {}".format(
                user_id, attribute_name, attribute_value, requestUrl
            )
        )

        retries = 0
        while True:
            userResponse = requests.patch(
                requestUrl,
                json=userPatchBodyJson,
                headers=requestHeaders,
                cookies=self.cookie(),
            )
            if userResponse.ok:
                return self.parseRequestResponse(userResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif userResponse.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to update user -> {}; error -> {}".format(
                        user_id, userResponse.text
                    )
                )
                return None

    # end method definition

    def deleteUser(self, partition: str, user_id: str):
        """Delete an existing user

        Args:
            partition (string): name of the partition
            user_id (string): Id (= login name) of the user
        Return:
            Request response (json) or None if the reset fails.
        """

        requestUrl = self.usersUrl() + "/" + user_id + "@" + partition

        logger.info(
            "Delete user -> {} in partition -> {}; calling -> {}".format(
                user_id, partition, requestUrl
            )
        )

        retries = 0
        while True:
            userResponse = requests.delete(
                requestUrl, headers=requestHeaders, cookies=self.cookie()
            )
            if userResponse.ok:
                return True
            # Check if Session has expired - then re-authenticate and try once more
            elif userResponse.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to delete user -> {}; error -> {}".format(
                        user_id, userResponse.text
                    )
                )
                return False

    # end method definition

    def resetUserPassword(self, user_id: str, password: str):
        """Reset a password of an existing user

        Args:
            user_id (string): Id (= login name) of the user
            password (string): new password of the user
        Return:
            Request response (json) or None if the reset fails.
        """

        userPostBodyJson = {"newPassword": password}

        requestUrl = "{}/{}/password".format(self.usersUrl(), user_id)

        logger.info(
            "Resetting password for user -> {}; calling -> {}".format(
                user_id, requestUrl
            )
        )

        retries = 0
        while True:
            userResponse = requests.put(
                requestUrl,
                json=userPostBodyJson,
                headers=requestHeaders,
                cookies=self.cookie(),
            )
            if userResponse.ok:
                return userResponse.ok
            # Check if Session has expired - then re-authenticate and try once more
            elif userResponse.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to reset password for user -> {}; error -> {}".format(
                        user_id, userResponse.text
                    )
                )
                return userResponse.ok

    # end method definition

    def addGroup(self, partition: str, name: str, description: str):
        """Add a new user group to a user partition in OTDS

        Args:
            partition (string): name of the OTDS user partition (needs to exist)
            name (string): name of the new group
            description (string): description of the new group
        Return:
            Request response (json) or None if the creation fails.
        """

        groupPostBodyJson = {
            "userPartitionID": partition,
            "name": name,
            "description": description,
        }

        requestUrl = self.groupsUrl()

        logger.info(
            "Adding group -> {} to partition -> {}; calling -> {}".format(
                name, partition, requestUrl
            )
        )
        logger.info("Group Attributes -> {}".format(groupPostBodyJson))

        retries = 0
        while True:
            groupResponse = requests.post(
                requestUrl,
                json=groupPostBodyJson,
                headers=requestHeaders,
                cookies=self.cookie(),
            )
            if groupResponse.ok:
                return self.parseRequestResponse(groupResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif groupResponse.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to add group -> {}; error -> {}".format(
                        name, groupResponse.text
                    )
                )
                return None

    # end method definition

    def getGroup(self, group: str):
        """Get a group by its group name

        Args:
            group_id (string): ID of the group (= group name)
        Return:
            Request response (json) or None if the group was not found.
            Example values:
            {
                'numMembers': 7,
                'userPartitionID': 'Content Server Members',
                'name': 'Sales',
                'location': 'oTGroup=3f921294-b92a-4c9e-bf7c-b50df16bb937,orgunit=groups,partition=Content Server Members,dc=identity,dc=opentext,dc=net',
                'id': 'Sales@Content Server Members',
                'values': [{...}, {...}, {...}, {...}, {...}, {...}, {...}, {...}, {...}, ...],
                'description': None,
                'uuid': '3f921294-b92a-4c9e-bf7c-b50df16bb937',
                'objectClass': 'oTGroup',
                'customAttributes': None,
                'originUUID': None,
                'urlId': 'Sales@Content Server Members',
                'urlLocation': 'oTGroup=3f921294-b92a-4c9e-bf7c-b50df16bb937,orgunit=groups,partition=Content Server Members,dc=identity,dc=opentext,dc=net'
            }
        """

        requestUrl = self.groupsUrl() + "/" + group

        logger.info("Get group -> {}; calling -> {}".format(group, requestUrl))

        retries = 0
        while True:
            groupResponse = requests.get(
                requestUrl, headers=requestHeaders, cookies=self.cookie()
            )
            if groupResponse.ok:
                return self.parseRequestResponse(groupResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif groupResponse.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to get group -> {}; error -> {}".format(
                        group, groupResponse.text
                    )
                )
                return None

    # end method definition

    def addUserToGroup(self, user: str, group: str):
        """Add an existing user to an existing group in OTDS

        Args:
            user (string): name of the OTDS user (needs to exist)
            group (string): name of the OTDS group (needs to exist)
        Return:
            Request return code.
        """

        userToGroupPostBodyJson = {"stringList": [group]}

        requestUrl = self.usersUrl() + "/" + user + "/memberof"

        logger.info(
            "Adding user -> {} to group -> {}; calling -> {}".format(
                user, group, requestUrl
            )
        )

        retries = 0
        while True:
            userToGroupResponse = requests.post(
                requestUrl,
                json=userToGroupPostBodyJson,
                headers=requestHeaders,
                cookies=self.cookie(),
            )
            if userToGroupResponse.ok:
                return True
            # Check if Session has expired - then re-authenticate and try once more
            elif userToGroupResponse.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to add user -> {} to group -> {}; error -> {}".format(
                        user, group, userToGroupResponse.text
                    )
                )
                return False

    # end method definition

    def addGroupToParentGroup(self, group: str, parent_group: str):
        """Add an existing group to an existing parent group in OTDS

        Args:
            group (string): name of the OTDS group (needs to exist)
            parent_group (string): name of the OTDS parent group (needs to exist)
        Return:
            Request return code.
        """

        groupToParentGroupPostBodyJson = {"stringList": [parent_group]}

        requestUrl = self.groupsUrl() + "/" + group + "/memberof"

        logger.info(
            "Adding group -> {} to parent group -> {}; calling -> {}".format(
                group, parent_group, requestUrl
            )
        )

        retries = 0
        while True:
            groupToParentGroupResponse = requests.post(
                requestUrl,
                json=groupToParentGroupPostBodyJson,
                headers=requestHeaders,
                cookies=self.cookie(),
            )

            if groupToParentGroupResponse.ok:
                return True
            # Check if Session has expired - then re-authenticate and try once more
            elif groupToParentGroupResponse.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to add group -> {} to parent group -> {}; error -> {}".format(
                        group, parent_group, groupToParentGroupResponse.text
                    )
                )
                return False

    # end method definition

    def addResource(
        self,
        name: str,
        description: str,
        display_name: str,
        additional_payload: dict = {},
    ):
        """Add an OTDS resource

        Args:
            name (string): name of the new OTDS resource
            description (string): description of the new OTDS resource
            display_name (string): display name of the OTDS resource
            additional_payload (list): additional values for the json payload
        Return:
            Request response (json) or None if the REST call fails.
        """

        resourcePostBodyJson = {
            "resourceName": name,
            "description": description,
            "displayName": display_name,
        }

        # Check if there's additional payload for the body provided to handle special cases:
        if additional_payload:
            # Merge additional payload:
            resourcePostBodyJson.update(additional_payload)

        requestUrl = self.config()["resourceUrl"]

        logger.info(
            "Adding resource -> {} ({}); calling -> {}".format(
                name, description, requestUrl
            )
        )

        retries = 0
        while True:
            resourceResponse = requests.post(
                requestUrl,
                json=resourcePostBodyJson,
                headers=requestHeaders,
                cookies=self.cookie(),
            )
            if resourceResponse.ok:
                return self.parseRequestResponse(resourceResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif resourceResponse.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to add resource -> {}; error -> {}".format(
                        name, resourceResponse.text
                    )
                )
                return None

    # end method definition

    def getResource(self, name: str, show_error: bool = False):
        """Get an existing OTDS resource

        Args:
            name (string): name of the new OTDS resource
            show_error (boolean): treat as error if resource is not found
        Return:
            Request response (json) or None if the REST call fails.
        """

        requestUrl = "{}/{}".format(self.config()["resourceUrl"], name)

        logger.info("Retrieving resource -> {}; calling -> {}".format(name, requestUrl))

        retries = 0
        while True:
            resourceResponse = requests.get(
                requestUrl, headers=requestHeaders, cookies=self.cookie()
            )
            if resourceResponse.ok:
                return self.parseRequestResponse(resourceResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif resourceResponse.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                # We don't necessarily want to log an error as this function
                # is also used in wait loops:
                if show_error:
                    logger.warning(
                        "Failed to retrieve resource -> {}; warning -> {}".format(
                            name, resourceResponse.text
                        )
                    )
                else:
                    logger.info("Resource -> {} not found.".format(name))
                return None

    # end method definition

    def updateResource(self, name: str, resource: object, show_error: bool = True):
        """Update an existing OTDS resource

        Args:
            name (string): name of the new OTDS resource
            resource (object): updated resource object of getResource called before
            show_error (boolean): treat as error if resource is not found
        Return:
            Request response (json) or None if the REST call fails.
        """

        requestUrl = "{}/{}".format(self.config()["resourceUrl"], name)

        logger.info("Updating resource -> {}; calling -> {}".format(name, requestUrl))

        retries = 0
        while True:
            resourceResponse = requests.put(
                requestUrl, json=resource, headers=requestHeaders, cookies=self.cookie()
            )
            if resourceResponse.ok:
                return self.parseRequestResponse(resourceResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif resourceResponse.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                # We don't necessarily want to log an error as this function
                # is also used in wait loops:
                if show_error:
                    logger.warning(
                        "Failed to retrieve resource -> {}; warning -> {}".format(
                            name, resourceResponse.text
                        )
                    )
                else:
                    logger.info("Resource -> {} not found.".format(name))
                return None

    # end method definition

    def activateResource(self, resource_id):
        """Activate an OTDS resource

        Args:
            resource_id (string): ID of the OTDS resource
        Return:
            Request response (json) or None if the REST call fails.
        """

        resourcePostBodyJson = {}

        requestUrl = "{}/{}/activate".format(self.config()["resourceUrl"], resource_id)

        logger.info(
            "Activating resource -> {}; calling -> {}".format(resource_id, requestUrl)
        )

        retries = 0
        while True:
            resourceResponse = requests.post(
                requestUrl,
                json=resourcePostBodyJson,
                headers=requestHeaders,
                cookies=self.cookie(),
            )
            if resourceResponse.ok:
                return self.parseRequestResponse(resourceResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif resourceResponse.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to activate resource -> {}; error -> {}".format(
                        resource_id, resourceResponse.text
                    )
                )
                return None

    # end method definition

    def getAccessRoles(self):
        """Get a list of all OTDS access roles

        Args: None
        Return:
            Request response (json) or None if the REST call fails.
        """

        requestUrl = self.config()["accessRoleUrl"]

        logger.info("Retrieving access roles; calling -> {}".format(requestUrl))

        retries = 0
        while True:
            accessRolesResponse = requests.get(
                requestUrl, headers=requestHeaders, cookies=self.cookie()
            )
            if accessRolesResponse.ok:
                return self.parseRequestResponse(accessRolesResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif accessRolesResponse.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to retrieve access roles; error -> {}".format(
                        accessRolesResponse.text
                    )
                )
                return None

    # end method definition

    def getAccessRole(self, name: str):
        """Get an OTDS access role

        Args:
            name (string): name of the access role
        Return:
            Request response (json) or None if the REST call fails.
        """

        requestUrl = self.config()["accessRoleUrl"] + "/" + name

        logger.info(
            "Retrieving access role -> {}; calling -> {}".format(name, requestUrl)
        )

        retries = 0
        while True:
            accessRolesResponse = requests.get(
                requestUrl, headers=requestHeaders, cookies=self.cookie()
            )
            if accessRolesResponse.ok:
                return self.parseRequestResponse(accessRolesResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif accessRolesResponse.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to retrieve access role -> {}; error -> {}".format(
                        name, accessRolesResponse.text
                    )
                )
                return None

    # end method definition

    def addPartitionToAccessRole(
        self, access_role: str, partition: str, location: str = ""
    ):
        """Add an OTDS partition to an OTDS access role

        Args:
            access_role (string): name of the OTDS access role
            partition (string): name of the partition
            location (string): this is kind of a unique identifier DN (Distinguished Name)
                               most of the times you will want to keep it to empty string ("")
        Return:
            Request response (json) or None if the REST call fails.
        """

        accessRolePostBodyJson = {
            "userPartitions": [{"name": partition, "location": location}]
        }

        requestUrl = "{}/{}/members".format(self.config()["accessRoleUrl"], access_role)

        logger.info(
            "Add user partition -> {} to access role -> {}; calling -> {}".format(
                partition, access_role, requestUrl
            )
        )

        retries = 0
        while True:
            accessRoleResponse = requests.post(
                requestUrl,
                json=accessRolePostBodyJson,
                headers=requestHeaders,
                cookies=self.cookie(),
            )
            if accessRoleResponse.ok:
                return True
            elif accessRoleResponse.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to add partition -> {} to access role -> {}; error -> {}".format(
                        partition, access_role, accessRoleResponse.text
                    )
                )
                return False

    # end method definition

    def addUserToAccessRole(self, access_role: str, user_id: str, location: str = ""):
        """Add an OTDS user to an OTDS access role

        Args:
            access_role (string): name of the OTDS access role
            user_id (string): ID of the user (= login name)
            location (string): this is kind of a unique identifier DN (Distinguished Name)
                               most of the times you will want to keep it to empty string ("")
        Return:
            Request response (json) or None if the REST call fails.
        """

        # get existing members to check if user is already a member:
        accessRolesGetResponse = self.getAccessRole(access_role)

        if not accessRolesGetResponse:
            return False

        # Checking if user already added to access role
        accessRoleUsers = accessRolesGetResponse["accessRoleMembers"]["users"]
        for user in accessRoleUsers:
            if user["displayName"] == user_id:
                logger.info(
                    "User -> {} already added to access role -> {}".format(
                        user_id, access_role
                    )
                )
                return True

        logger.info(
            "User -> {} is not yet in access role -> {} - adding...".format(
                user_id, access_role
            )
        )

        # create payload for REST call:
        accessRolePostBodyJson = {"users": [{"name": user_id, "location": location}]}

        requestUrl = "{}/{}/members".format(self.config()["accessRoleUrl"], access_role)

        logger.info(
            "Add user -> {} to access role -> {}; calling -> {}".format(
                user_id, access_role, requestUrl
            )
        )

        retries = 0
        while True:
            accessRoleResponse = requests.post(
                requestUrl,
                json=accessRolePostBodyJson,
                headers=requestHeaders,
                cookies=self.cookie(),
            )
            if accessRoleResponse.ok:
                return True
            elif accessRoleResponse.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to add user -> {} to access role -> {}; error -> {}".format(
                        user_id, access_role, accessRoleResponse.text
                    )
                )
                return False

    # end method definition

    def addGroupToAccessRole(self, access_role: str, group: str, location: str = ""):
        """Add an OTDS user to an OTDS access role

        Args:
            access_role (string): name of the OTDS access role
            group (string): name of the group
            location (string): this is kind of a unique identifier DN (Distinguished Name)
                               most of the times you will want to keep it to empty string ("")
        Return:
            Request response (json) or None if the REST call fails.
        """

        # get existing members to check if user is already a member:
        accessRolesGetResponse = self.getAccessRole(access_role)

        if not accessRolesGetResponse:
            return False

        # Checking if group already added to access role
        accessRoleGroups = accessRolesGetResponse["accessRoleMembers"]["groups"]
        for accessRoleGroup in accessRoleGroups:
            if accessRoleGroup["name"] == group:
                logger.info(
                    "Group -> {} already added to access role -> {}".format(
                        group, access_role
                    )
                )
                return True

        logger.info(
            "Group -> {} is not yet in access role -> {} - adding...".format(
                group, access_role
            )
        )

        # create payload for REST call:
        accessRolePostBodyJson = {"groups": [{"name": group, "location": location}]}

        requestUrl = "{}/{}/members".format(self.config()["accessRoleUrl"], access_role)

        logger.info(
            "Add group -> {} to access role -> {}; calling -> {}".format(
                group, access_role, requestUrl
            )
        )

        retries = 0
        while True:
            accessRoleResponse = requests.post(
                requestUrl,
                json=accessRolePostBodyJson,
                headers=requestHeaders,
                cookies=self.cookie(),
            )
            if accessRoleResponse.ok:
                return True
            elif accessRoleResponse.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to add group -> {} to access role -> {}; error -> {}".format(
                        group, access_role, accessRoleResponse.text
                    )
                )
                return False

    # end method definition

    def updateAccessRoleAttributes(self, name: str, attributeList: list):
        """Update some attributes of an existing OTDS Access Role

        Args:
            name (string): name of the existing access role
            attributeList (list): list of attribute name and attribute value pairs
                                  The values need to be a list as well. Example:
                                  [{name: "pushAllGroups", values: ["True"]}]
        Return:
            Request response (json) or None if the REST call fails.
        """

        # Return if list is empty:
        if not attributeList:
            return None

        # create payload for REST call:
        access_role = self.getAccessRole(name)
        if not access_role:
            logger.error("Failed to get access role -> {}".format(name))
            return None

        accessRolePutBodyJson = {"attributes": attributeList}

        requestUrl = "{}/{}/attributes".format(self.config()["accessRoleUrl"], name)

        logger.info(
            "Update access role -> {} with attributes -> {}; calling -> {}".format(
                name, accessRolePutBodyJson, requestUrl
            )
        )

        retries = 0
        while True:
            accessRoleResponse = requests.put(
                requestUrl,
                json=accessRolePutBodyJson,
                headers=requestHeaders,
                cookies=self.cookie(),
            )
            if accessRoleResponse.ok:
                return self.parseRequestResponse(accessRoleResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif accessRoleResponse.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to update access role -> {}; error -> {}".format(
                        name, accessRoleResponse.text
                    )
                )
                return None

    # end method definition

    def addSystemAttribute(self, name: str, value: str, description: str = ""):
        """Add a new system attribute to OTDS

        Args:
            name (string): name of the new system attribute
            value (string): value of the system attribute
            description (string): optional description of the system attribute
        Return:
            Request response (json) or None if the REST call fails.
        """

        systemAttributePostBodyJson = {
            "name": name,
            "value": value,
            "friendlyName": description,
        }

        requestUrl = "{}/system_attributes".format(self.config()["systemConfigUrl"])

        if description:
            logger.info(
                "Add system attribute -> {} ({}) with value -> {}; calling -> {}".format(
                    name, description, value, requestUrl
                )
            )
        else:
            logger.info(
                "Add system attribute -> {} with value -> {}; calling -> {}".format(
                    name, value, requestUrl
                )
            )

        retries = 0
        while True:
            systemAttributeResponse = requests.post(
                requestUrl,
                json=systemAttributePostBodyJson,
                headers=requestHeaders,
                cookies=self.cookie(),
            )
            if systemAttributeResponse.ok:
                return self.parseRequestResponse(systemAttributeResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif systemAttributeResponse.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to add system attribute -> {} with value -> {}; error -> {}".format(
                        name, value, systemAttributeResponse.text
                    )
                )
                return None

    # end method definition

    def getTrustedSites(self):
        """get all configured OTDS trusted sites

        Args: None
        Return:
            Request response (json) or None if the REST call fails.
        """

        requestUrl = "{}/whitelist".format(self.config()["systemConfigUrl"])

        logger.info("Retrieving trusted sites; calling -> {}".format(requestUrl))

        retries = 0
        while True:
            trustedSitesResponse = requests.get(
                requestUrl, headers=requestHeaders, cookies=self.cookie()
            )
            if trustedSitesResponse.ok:
                return self.parseRequestResponse(trustedSitesResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif trustedSitesResponse.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to retrieve trusted sites; error -> {}".format(
                        trustedSitesResponse.text
                    )
                )
                return None

    # end method definition

    def addTrustedSite(self, trusted_site: str):
        """Add a new OTDS trusted site

        Args:
            trustedSite (string): name of the new trusted site
        Return:
            Request response (json) or None if the REST call fails.
        """

        trustedSitePostBodyJson = {"stringList": [trusted_site]}

        # we need to first retrieve the existing sites and then
        # append the new one:
        existingTrustedSites = self.getTrustedSites()

        if existingTrustedSites:
            trustedSitePostBodyJson["stringList"].extend(
                existingTrustedSites["stringList"]
            )

        requestUrl = "{}/whitelist".format(self.config()["systemConfigUrl"])

        logger.info(
            "Add trusted site -> {}; calling -> {}".format(trusted_site, requestUrl)
        )

        trustedSiteResponse = requests.put(
            requestUrl,
            json=trustedSitePostBodyJson,
            headers=requestHeaders,
            cookies=self.cookie(),
        )
        if not trustedSiteResponse.ok:
            logger.error(
                "Failed to add trusted site -> {}; error -> {}".format(
                    trusted_site, trustedSiteResponse.text
                )
            )
        return trustedSiteResponse

    # end method definition

    def enableAudit(self):
        """enable Audit

        Args:
            -
        Return:
            Request response (json) or None if the REST call fails.
        """

        auditPutBodyJson = {
            "daysToKeep": "7",
            "enabled": "true",
            "auditTo": "DATABASE",
            "eventIDs": [
                "User Create",
                "Group Create",
                "User Delete",
                "Group Delete",
                "User Modify",
                "Group Modify",
                "Initial authentication successful",
                "Initial authentication failed",
                "Impersonation",
                "Import Finished",
                "Access Denied",
                "Authentication code incorrect",
                "Authentication code required",
                "User locked out",
                "Consolidate Partition with identity provider",
                "Recycle Bin User Deleted",
                "Recycle Bin Group Deleted",
                "User Moved to Recycle Bin",
                "Group Moved to Recycle Bin",
                "User Restored from Recycle Bin",
                "Group Restored from Recycle Bin",
                "Scheduled Cleanup",
                "Consolidation finished",
                "Monitoring session finished",
                "User Rename",
                "Group Rename",
                "Role Create",
                "Role Delete",
                "Role Modify",
                "Role Rename",
                "Recycle Bin Role Deleted",
                "Role Moved to Recycle Bin",
                "Role Restored from Recycle Bin",
                "Set group members",
                "Set group members for moved in objects",
                "User logout",
                "Password change successful",
                "Password change failed",
                "Add Parent Object",
                "Remove Parent Object",
                "OAuth Client Create",
                "OAuth Client Delete",
                "OAuth Client Modify",
                "Tenant Create",
                "Tenant Delete",
                "Tenant Modify",
                "Migration",
            ],
        }

        requestUrl = "{}/audit".format(self.config()["systemConfigUrl"])

        logger.info("Enable audit; calling -> {}".format(requestUrl))

        auditResponse = requests.put(
            requestUrl,
            json=auditPutBodyJson,
            headers=requestHeaders,
            cookies=self.cookie(),
        )
        if not auditResponse.ok:
            logger.error(
                "Failed to enable audit; error -> {}".format(auditResponse.text)
            )
        return auditResponse

    # end method definition

    def addOauthClient(
        self,
        client_id: str,
        description: str,
        redirect_urls: list = [],
        allow_impersonation: bool = True,
        confidential: bool = True,
        auth_scopes: list = [],  # empty string = "Global"
        allowed_scopes: list = [],  # in OTDS UI: Permissible scopes
        default_scopes: list = [],  # in OTDS UI: Default scopes
    ):
        """Add a new OAuth client to OTDS

        Args:
            client_id (string): name of the new OAuth client (should not have blanks)
            description (string): description of the OAuth client
            redirect_urls (list): list of redirect URLs (strings)
            allow_impersonation (boolean)
            confidential (boolean)
            auth_scope: str = "",  # empty string = "Global"
            allowed_scopes: list = [],  # in OTDS UI: Permissible scopes
            default_scopes: list = [],  # in OTDS UI: Default scopes
        Return:
            Request response (json) or None if the creation fails.
        """

        oauthClientPostBodyJson = {
            "id": client_id,
            "description": description,
            "redirectURLs": redirect_urls,
            "accessTokenLifeTime": 1000,
            "refreshTokenLifeTime": 20000,
            "authCodeLifeTime": 20000,
            "allowRefreshToken": True,
            "allowImpersonation": allow_impersonation,
            "useSessionRefreshTokenLifeTime": True,
            "confidential": confidential,
            "authScopes": auth_scopes,
            "allowedScopes": allowed_scopes,
            "defaultScopes": default_scopes,
        }

        requestUrl = self.oauthClientUrl()

        logger.info(
            "Adding oauth client -> {} ({}); calling -> {}".format(
                description, client_id, requestUrl
            )
        )

        retries = 0
        while True:
            oauthClientResponse = requests.post(
                requestUrl,
                json=oauthClientPostBodyJson,
                headers=requestHeaders,
                cookies=self.cookie(),
            )
            if oauthClientResponse.ok:
                return self.parseRequestResponse(oauthClientResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif oauthClientResponse.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to add OAuth client -> {}; error -> {}".format(
                        client_id, oauthClientResponse.text
                    )
                )
                return None

    # end method definition

    def getOauthClient(self, client_id, show_error: bool = True):
        """Get an existing OAuth client from OTDS

        Args:
            client_id (string): name (= ID) of the OAuth client to retrieve
            show_error (boolean): whether or not we want to log an error if partion is not found
        Return:
            Request response (json) or None if the client is not found.
        """

        requestUrl = "{}/{}".format(self.oauthClientUrl(), client_id)

        logger.info(
            "Get oauth client -> {}; calling -> {}".format(client_id, requestUrl)
        )

        retries = 0
        while True:
            oauthClientResponse = requests.get(
                requestUrl, headers=requestHeaders, cookies=self.cookie()
            )
            if oauthClientResponse.ok:
                return self.parseRequestResponse(oauthClientResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif oauthClientResponse.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                if show_error:
                    logger.error(
                        "Failed to get oauth client -> {}; error -> {}".format(
                            client_id, oauthClientResponse.text
                        )
                    )
                return None

    # end method definition

    def updateOauthClient(self, client_id, updates: dict):
        oauthClientPatchBodyJson = updates

        requestUrl = "{}/{}".format(self.oauthClientUrl(), client_id)

        logger.info(
            "Update OAuth client -> {} with -> {}; calling -> {}".format(
                client_id, updates, requestUrl
            )
        )

        retries = 0
        while True:
            oauthClientResponse = requests.patch(
                requestUrl,
                json=oauthClientPatchBodyJson,
                headers=requestHeaders,
                cookies=self.cookie(),
            )
            if oauthClientResponse.ok:
                return self.parseRequestResponse(oauthClientResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif oauthClientResponse.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to update OAuth client -> {}; error -> {}".format(
                        client_id, oauthClientResponse.text
                    )
                )
                return None

    # end method definition

    def addOauthClientsToAccessRole(self, access_role_name: str):
        """Add Oauth clients user partion to an OTDS Access Role

        Args:
            access_role_name (string): name of the OTDS Access Role

        Return: response of REST call or None in case of an error
        """

        accessRolesUrl = self.config()["accessRoleUrl"] + "/" + access_role_name

        logger.info(
            "Get access role -> {}; calling -> {}".format(
                access_role_name, accessRolesUrl
            )
        )

        retries = 0
        while True:
            accessRolesGetResponse = requests.get(
                accessRolesUrl, headers=requestHeaders, cookies=self.cookie()
            )
            if accessRolesGetResponse.ok:
                accessRolesJson = self.parseRequestResponse(accessRolesGetResponse)
                break
            # Check if Session has expired - then re-authenticate and try once more
            elif accessRolesGetResponse.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to retrieve role -> {}; url -> {} : error -> {}".format(
                        access_role_name, accessRolesUrl, accessRolesGetResponse.text
                    )
                )
                return None

        # Checking if OAuthClients partition already added to access role
        userPartitions = accessRolesJson["accessRoleMembers"]["userPartitions"]
        for userPartition in userPartitions:
            if userPartition["userPartition"] == "OAuthClients":
                logger.error(
                    "OAuthClients partition already added to role -> {}".format(
                        access_role_name
                    )
                )
                return None

        # Getting location info for the OAuthClients partition
        # so it can be added to access roles json
        oauthPartitionsUrl = self.config()["partitionsUrl"] + "/OAuthClients"
        partitionsResponse = requests.get(
            oauthPartitionsUrl, headers=requestHeaders, cookies=self.cookie()
        )
        if partitionsResponse.ok:
            response_dict = self.parseRequestResponse(partitionsResponse)
            if not response_dict:
                return None
            oauthClientLocation = response_dict["location"]
        else:
            logger.error(
                "Failed to get partition info for OAuthClients; url -> {} : error -> {}".format(
                    oauthPartitionsUrl, partitionsResponse.text
                )
            )
            return None

        # adding OAuthClients info to acess roles organizational units
        oauthClientsOuBlock = {
            "location": oauthClientLocation,
            "name": oauthClientLocation,
            "userPartition": None,
        }
        accessRolesJson["accessRoleMembers"]["organizationalUnits"].append(
            oauthClientsOuBlock
        )

        updateAccessRoleResponse = requests.put(
            accessRolesUrl,
            json=accessRolesJson,
            headers=requestHeaders,
            cookies=self.cookie(),
        )

        if updateAccessRoleResponse.ok:
            logger.info(
                "OauthClients partition successfully added to access role -> {}".format(
                    access_role_name
                )
            )
        else:
            logger.warning(
                "Status code of {} returned attempting to add OAuthClients to access role {}: error -> {}".format(
                    updateAccessRoleResponse.status_code,
                    access_role_name,
                    updateAccessRoleResponse.text,
                )
            )
        return updateAccessRoleResponse

    # end method definition

    def getAccessToken(self, client_id, client_secret):
        encodedClientSecret = "{}:{}".format(client_id, client_secret).encode("utf-8")
        accessTokenRequestHeaders = {
            "Authorization": "Basic "
            + base64.b64encode(encodedClientSecret).decode("utf-8"),
            "Content-Type": "application/x-www-form-urlencoded",
        }

        requestUrl = self.tokenUrl()

        accessTokenResponse = requests.post(
            requestUrl,
            data={"grant_type": "client_credentials"},
            headers=accessTokenRequestHeaders,
        )

        accessToken = None
        if accessTokenResponse.ok:
            accessTokenJson = self.parseRequestResponse(accessTokenResponse)

            if "access_token" in accessTokenJson:
                accessToken = accessTokenJson["access_token"]

        return accessToken

    # end method definition

    def addAuthHandlerSAML(
        self,
        name: str,
        description: str,
        provider_name: str,
        saml_url: str,
        otds_url: str,
    ):
        """Add a new SAML authentication handler

        Args:
            name (string): name of the new authentication handler
            description (string): description of the new authentication handler
            provider_name (string): description of the new authentication handler
            saml_url (string): SAML URL
            otds_url (string): the external(!) service provider URL of OTDS
        Return:
            Request response (json) or None if the REST call fails.
        """

        authHandlerPostBodyJson = {
            "_name": name,
            "_description": description,
            "_class": "com.opentext.otds.as.drivers.saml.SAML2Handler",
            "_enabled": "true",
            "_priority": "5",
            "_authPrincipalAttrNames": ["oTExternalID1", "oTUserID1"],
            "_properties": [
                {
                    "_key": "com.opentext.otds.as.drivers.saml.provider_name",
                    "_name": "Identity Provider (IdP) Name",
                    "_description": "The name of the identity provider. This should be a single word since it will be part of the metadata URL.",
                    "_value": provider_name,
                },
                {
                    "_key": "com.opentext.otds.as.drivers.saml.provider_metadata_description",
                    "_name": "IdP Metadata URL",
                    "_description": "The URL for the IdP's federation metadata. The metadata will be automatically updated by OTDS daily at midnight.",
                    "_value": saml_url,
                },
                {
                    "_key": "com.opentext.otds.as.drivers.saml.provider_nameid_format",
                    "_name": "IdP NameID Format",
                    "_description": "Specifies which NameID format supported by the identity provider contains the desired user identifier. The value in this identifier must correspond to the value of the user attribute specified for the authentication principal attribute. This value is usually set to urn:oasis:names:tc:SAML:2.0:nameid-format:persistent or urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress. Please ensure this is consistent with the identity provider's configuration.",
                    "_value": "urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified",
                },
                {
                    "_key": "com.opentext.otds.as.drivers.saml._impersonator_claim",
                    "_name": "Claim for impersonating user",
                    "_description": "A claim that contains the ID of the actor/impersonator for the user identified by NameID. It must be in the same format as NameID.",
                    "_value": "loggedinuserid",
                },
                {
                    "_key": "com.opentext.otds.as.drivers.saml.sp_url",
                    "_name": "OTDS SP Endpoint",
                    "_description": "Specifies the service provider URL that will be used to identify OTDS to the identity provider. If not specified, the URL will be taken from the request. This generally needs to be configured for environments in which OTDS is behind a reverse-proxy.",
                    "_value": otds_url,
                },
                {
                    "_key": "com.opentext.otds.as.drivers.saml.enable_sp_sso",
                    "_name": "Active By Default",
                    "_description": "Whether to activate this handler for any request to the OTDS login page. If true, any login request to the OTDS login page will be redirected to the IdP. If false, the user has to select the provider on the login page.",
                    "_value": "false",
                },
                {
                    "_key": "com.opentext.otds.as.drivers.saml._signature_alg",
                    "_name": "XML Signature Algorithm",
                    "_description": "Only relevant when certificate and private key are configured. Default is http://www.w3.org/2000/09/xmldsig#rsa-sha1. Valid values are defined at http://www.w3.org/TR/xmldsig-core1/#sec-AlgID.",
                    "_value": "http://www.w3.org/2001/04/xmldsig-more#rsa-sha256",
                },
                {
                    "_key": "com.opentext.otds.as.drivers.saml.use_acs_url",
                    "_name": "Use AssertionConsumerServiceURL",
                    "_description": "Set to true to have the SAML AuthnRequest use AssertionConsumerServiceURL instead of AssertionConsumerServiceIndex",
                    "_value": "true",
                },
                {
                    "_key": "com.opentext.otds.as.drivers.saml.grace_period",
                    "_name": "Grace Period",
                    "_description": 'Specifies the number of minutes to allow for "NotBefore" and "NotOnOrAfter" fields when validating assertions in order to account for time difference between the identity provider and this service provider.',
                    "_value": "5",
                },
                {
                    "_key": "com.opentext.otds.as.drivers.saml.auth_request_binding",
                    "_name": "Auth Request Binding",
                    "_description": "Specifies the preferred SAML binding to use for sending the AuthnRequest, provided it is supported by the identity provider.",
                    "_value": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST",
                },
                {
                    "_key": "com.opentext.otds.as.drivers.saml.auth_response_binding",
                    "_name": "Auth Response Binding",
                    "_description": "Specifies the SAML binding to use for the response to an AuthnRequest",
                    "_value": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST",
                },
            ],
        }

        requestUrl = self.authHandlerUrl()

        logger.info(
            "Adding SAML auth handler -> {} ({}); calling -> {}".format(
                name, description, requestUrl
            )
        )

        retries = 0
        while True:
            authHandlerResponse = requests.post(
                requestUrl,
                json=authHandlerPostBodyJson,
                headers=requestHeaders,
                cookies=self.cookie(),
            )
            if authHandlerResponse.ok:
                return self.parseRequestResponse(authHandlerResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif authHandlerResponse.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to add SAML auth handler -> {}; error -> {}".format(
                        name, authHandlerResponse.text
                    )
                )
                return None

    # end method definition

    def addAuthHandlerSAP(
        self,
        name: str,
        description: str,
        certificate_file: str,
        certificate_password: str,
    ):
        """Add a new SAP authentication handler

        Args:
            name (string): name of the new authentication handler
            description (string): description of the new authentication handler
            certificate_file (string): fully qualified file name (with path) to the certificate file
            certificate_password (string): password of the certificate
        Return:
            Request response (json) or None if the REST call fails.
        """

        # 1. Prepare the body for the AuthHandler REST call:
        authHandlerPostBodyJson = {
            "_name": name,
            "_description": description,
            "_class": "com.opentext.otds.as.drivers.sapssoext.SAPSSOEXTAuthHandler",
            "_enabled": "true",
            "_priority": "10",
            "_authPrincipalAttrNames": ["oTExternalID1"],
            "_scope": None,
            "_properties": [
                {
                    "_key": "com.opentext.otds.as.drivers.sapssoext.certificate_description1",
                    "_name": "SAP Certificate 1 Description",
                    "_description": "Specifies a custom description for the corresponding certificate.",
                    "_required": False,
                    "_fileBased": False,
                    "_fileName": False,
                    "_fileExtensions": None,
                    "_value": os.path.basename(
                        certificate_file
                    ),  # "TM6_Sandbox.pse" - file name only
                    "_allowedValues": None,
                    "_confidential": False,
                    "_keepOriginal": False,
                },
                {
                    "_key": "com.opentext.otds.as.drivers.sapssoext.certificate1",
                    "_name": "SAP Certificate (PSE) 1",
                    "_description": "Specifies a certificate (.pse file) to use to decode SAP tokens. Note: The selected file does not need to reside on the server since only its contents will be stored on the server. Clear the string in this field in order to delete the certificate stored on the server.",
                    "_required": False,
                    "_fileBased": True,
                    "_fileName": False,
                    "_fileExtensions": ["pse"],
                    "_value": None,
                    "_allowedValues": None,
                    "_confidential": False,
                    "_keepOriginal": False,
                },
                {
                    "_key": "com.opentext.otds.as.drivers.sapssoext.certificate_pass1",
                    "_name": "SAP Certificate 1 Password",
                    "_description": "Specifies the password for the corresponding .pse file.",
                    "_required": False,
                    "_fileBased": False,
                    "_fileName": False,
                    "_fileExtensions": None,
                    "_value": certificate_password,
                    "_allowedValues": None,
                    "_confidential": True,
                    "_keepOriginal": False,
                },
            ],
        }

        # 2. Create the auth handler in OTDS
        requestUrl = self.authHandlerUrl()

        logger.info(
            "Adding SAP auth handler -> {} ({}); calling -> {}".format(
                name, description, requestUrl
            )
        )

        authHandlerResponse = requests.post(
            requestUrl,
            json=authHandlerPostBodyJson,
            headers=requestHeaders,
            cookies=self.cookie(),
        )
        if not authHandlerResponse.ok:
            logger.error(
                "Failed to add SAP auth handler -> {}; error -> {}".format(
                    name, authHandlerResponse.text
                )
            )
            return None

        # 3. Upload the certificate file:

        # Check that the certificate (PSE) file is readable:
        logger.info("Reading certificate file -> {}...".format(certificate_file))
        try:
            # PSE files are binary - so we need to open with "rb":
            with open(certificate_file, "rb") as certFile:
                certContent = certFile.read()
                if not certContent:
                    logger.error(
                        "No data in certificate file -> {}".format(certificate_file)
                    )
                    return None
        except IOError as e:
            logger.error(
                "Error opening file -> {}; error -> {}".format(
                    certificate_file, e.strerror
                )
            )
            return None

        # Check that we have the binary certificate file - this is what OTDS expects. If the file content is
        # base64 encoded we will decode it and write it back into the same file
        try:
            # If file is not base64 encoded the next statement will throw an exception
            # (this is good)
            certContentDecoded = base64.b64decode(certContent, validate=True)
            certContentEncoded = base64.b64encode(certContentDecoded).decode("utf-8")
            if certContentEncoded == certContent.decode("utf-8"):
                logger.info(
                    "Certificate file -> {} is base64 encoded".format(certificate_file)
                )
                cert_file_encoded = True
            else:
                cert_file_encoded = False
        except:
            logger.info(
                "Certificate file -> {} is not base64 encoded".format(certificate_file)
            )
            cert_file_encoded = False

        if cert_file_encoded:
            certificate_file = "/tmp/" + os.path.basename(certificate_file)
            logger.info(
                "Writing decoded certificate file -> {}...".format(certificate_file)
            )
            try:
                # PSE files need to be binary - so we need to open with "wb":
                with open(certificate_file, "wb") as certFile:
                    certFile.write(base64.b64decode(certContent))
            except IOError as e:
                logger.error(
                    "Failed writing to file -> {}; error -> {}".format(
                        certificate_file, e.strerror
                    )
                )
                return None

        authHandlerPostData = {
            "file1_property": "com.opentext.otds.as.drivers.sapssoext.certificate1"
        }

        # It is important to send the file pointer and not the actual file content
        # otherwise the file is send base64 encoded which we don't want:
        authHandlerPostFiles = {
            "file1": (
                os.path.basename(certificate_file),
                open(certificate_file, "rb"),
                "application/octet-stream",
            )
        }

        requestUrl = self.authHandlerUrl() + "/" + name + "/files"

        logger.info(
            "Uploading certificate file -> {} for SAP auth handler -> {} ({}); calling -> {}".format(
                certificate_file, name, description, requestUrl
            )
        )

        # it is important to NOT pass the headers parameter here!
        # Basically, if you specify a files parameter (a dictionary),
        # then requests will send a multipart/form-data POST automatically:
        authHandlerResponse = requests.post(
            requestUrl,
            data=authHandlerPostData,
            files=authHandlerPostFiles,
            cookies=self.cookie(),
        )
        if not authHandlerResponse.ok:
            logger.error(
                "Failed to upload certificate file -> {} for SAP auth handler -> {}; error -> {}".format(
                    certificate_file, name, authHandlerResponse.text
                )
            )
            return None

        return authHandlerResponse

    # end method definition

    def addAuthHandlerOAuth(
        self,
        name: str,
        description: str,
        provider_name: str,
        client_id: str,
        client_secret: str,
        active_by_default: bool = False,
        authorization_endpoint: str = "",
        token_endpoint: str = "",
        scope_string: str = "",
    ):
        """Add a new OAuth authentication handler

        Args:
            name (string): name of the new authentication handler
            description (string): description of the new authentication handler
            provider_name (string): the name of the authentication provider. This name is displayed on the login page.
            client_id (string): the client ID
            client_secret (string): the client secret
            active_by_default (boolean): Whether to activate this handler for any request to the OTDS login page.
                                         If true, any login request to the OTDS login page will be redirected to this OAuth provider.
                                         If false, the user has to select the provider on the login page.
            authorization_endpoint (string): The URL to redirect the browser to for authentication.
                                             It is used to retrieve the authorization code or an OIDC id_token.
            token_endpoint (string): The URL from which to retrieve the access token.
                                     Not strictly required with OpenID Connect if using the implicit flow.
            scope_string (string): Space delimited scope values to send. Include 'openid' to use OpenID Connect.
        Return:
            Request response (json) or None if the REST call fails.
        """

        # 1. Prepare the body for the AuthHandler REST call:
        authHandlerPostBodyJson = {
            "_name": name,
            "_description": description,
            "_class": "com.opentext.otds.as.drivers.http.OAuth2Handler",
            "_enabled": "true",
            "_priority": "10",
            "_authPrincipalAttrNames": ["oTExtraAttr0"],
            "_scope": None,
            "_properties": [
                {
                    "_key": "com.opentext.otds.as.drivers.http.oauth2.provider_name",
                    "_name": "Provider Name",
                    "_description": "The name of the authentication provider. This name is displayed on the login page.",
                    "_required": True,
                    "_fileBased": False,
                    "_fileName": False,
                    "_fileExtensions": None,
                    "_value": provider_name,
                    "_allowedValues": None,
                    "_confidential": False,
                    "_keepOriginal": False,
                },
                {
                    "_key": "com.opentext.otds.as.drivers.http.oauth2.active_by_default",
                    "_name": "Active By Default",
                    "_description": "Whether to activate this handler for any request to the OTDS login page. If true, any login request to the OTDS login page will be redirected to this OAuth provider. If false, the user has to select the provider on the login page.",
                    "_required": False,
                    "_fileBased": False,
                    "_fileName": False,
                    "_fileExtensions": None,
                    "_value": active_by_default,
                    "_allowedValues": ["true", "false"],
                    "_confidential": False,
                    "_keepOriginal": False,
                },
                {
                    "_key": "com.opentext.otds.as.drivers.http.oauth2.client_id",
                    "_name": "Client ID",
                    "_description": "The Client ID",
                    "_required": True,
                    "_fileBased": False,
                    "_fileName": False,
                    "_fileExtensions": None,
                    "_value": client_id,
                    "_allowedValues": None,
                    "_confidential": False,
                    "_keepOriginal": False,
                },
                {
                    "_key": "com.opentext.otds.as.drivers.http.oauth2.client_secret",
                    "_name": "Client Secret",
                    "_description": "The Client Secret",
                    "_required": True,
                    "_fileBased": False,
                    "_fileName": False,
                    "_fileExtensions": None,
                    "_value": client_secret,
                    "_allowedValues": None,
                    "_confidential": True,
                    "_keepOriginal": False,
                },
                {
                    "_key": "com.opentext.otds.as.drivers.http.oauth2.scope_string",
                    "_name": "Scope String",
                    "_description": "Space delimited scope values to send. Include 'openid' to use OpenID Connect.",
                    "_required": False,
                    "_fileBased": False,
                    "_fileName": False,
                    "_fileExtensions": None,
                    "_value": scope_string,
                    "_allowedValues": None,
                    "_confidential": False,
                    "_keepOriginal": False,
                },
                {
                    "_key": "com.opentext.otds.as.drivers.http.oauth2.get_code_url",
                    "_name": "Authorization Endpoint",
                    "_description": "The URL to redirect the browser to for authentication. It is used to retrieve the authorization code or an OIDC id_token.",
                    "_required": False,
                    "_fileBased": False,
                    "_fileName": False,
                    "_fileExtensions": None,
                    "_value": authorization_endpoint,
                    "_allowedValues": None,
                    "_confidential": False,
                    "_keepOriginal": False,
                },
                {
                    "_key": "com.opentext.otds.as.drivers.http.oauth2.get_access_token_url",
                    "_name": "Token Endpoint",
                    "_description": "The URL from which to retrieve the access token. Not strictly required with OpenID Connect if using the implicit flow.",
                    "_required": False,
                    "_fileBased": False,
                    "_fileName": False,
                    "_fileExtensions": None,
                    "_value": token_endpoint,
                    "_allowedValues": None,
                    "_confidential": False,
                    "_keepOriginal": False,
                },
                {
                    "_key": "com.opentext.otds.as.drivers.http.oauth2.get_user_info_url",
                    "_name": "User Info Endpoint",
                    "_description": "The URL from which to retrieve the JSON object representing the authorized user",
                    "_required": False,
                    "_fileBased": False,
                    "_fileName": False,
                    "_fileExtensions": None,
                    "_value": "{id}",
                    "_allowedValues": None,
                    "_confidential": False,
                    "_keepOriginal": False,
                },
                {
                    "_key": "com.opentext.otds.as.drivers.http.oauth2.user_identifier",
                    "_name": "User Identifier Field",
                    "_description": "The field corresponding to the user's unique ID at this provider",
                    "_required": True,
                    "_fileBased": False,
                    "_fileName": False,
                    "_fileExtensions": None,
                    "_value": "username",
                    "_allowedValues": None,
                    "_confidential": False,
                    "_keepOriginal": False,
                },
                {
                    "_key": "com.opentext.otds.as.drivers.http.oauth2.field1",
                    "_name": "Response Field 1",
                    "_description": "A field in the JSON response that should be mapped to an OTDS attribute. This value is case sensitive. Mapped fields are only relevant for auto-provisioned accounts.",
                    "_required": False,
                    "_fileBased": False,
                    "_fileName": False,
                    "_fileExtensions": None,
                    "_value": "email",
                    "_allowedValues": None,
                    "_confidential": False,
                    "_keepOriginal": False,
                },
                {
                    "_key": "com.opentext.otds.as.drivers.http.oauth2.attribute1",
                    "_name": "OTDS Attribute 1",
                    "_description": "OTDS user attribute to which the response field should be mapped.",
                    "_required": False,
                    "_fileBased": False,
                    "_fileName": False,
                    "_fileExtensions": None,
                    "_value": "mail",
                    "_allowedValues": None,
                    "_confidential": False,
                    "_keepOriginal": False,
                },
                {
                    "_key": "com.opentext.otds.as.drivers.http.oauth2.field2",
                    "_name": "Response Field 2",
                    "_description": "",
                    "_required": False,
                    "_fileBased": False,
                    "_fileName": False,
                    "_fileExtensions": None,
                    "_value": "first_name",
                    "_allowedValues": None,
                    "_confidential": False,
                    "_keepOriginal": False,
                },
                {
                    "_key": "com.opentext.otds.as.drivers.http.oauth2.attribute2",
                    "_name": "OTDS Attribute 2",
                    "_description": None,
                    "_required": False,
                    "_fileBased": False,
                    "_fileName": False,
                    "_fileExtensions": None,
                    "_value": "givenName",
                    "_allowedValues": None,
                    "_confidential": False,
                    "_keepOriginal": False,
                },
                {
                    "_key": "com.opentext.otds.as.drivers.http.oauth2.field3",
                    "_name": "Response Field 3",
                    "_description": "",
                    "_required": False,
                    "_fileBased": False,
                    "_fileName": False,
                    "_fileExtensions": None,
                    "_value": "last_name",
                    "_allowedValues": None,
                    "_confidential": False,
                    "_keepOriginal": False,
                },
                {
                    "_key": "com.opentext.otds.as.drivers.http.oauth2.attribute3",
                    "_name": "OTDS Attribute 3",
                    "_description": None,
                    "_required": False,
                    "_fileBased": False,
                    "_fileName": False,
                    "_fileExtensions": None,
                    "_value": "sn",
                    "_allowedValues": None,
                    "_confidential": False,
                    "_keepOriginal": False,
                },
                {
                    "_key": "com.opentext.otds.as.drivers.http.oauth2.attribute4",
                    "_name": "OTDS Attribute 4",
                    "_description": None,
                    "_required": False,
                    "_fileBased": False,
                    "_fileName": False,
                    "_fileExtensions": None,
                    "_value": "displayName",
                    "_allowedValues": None,
                    "_confidential": False,
                    "_keepOriginal": False,
                },
                {
                    "_key": "com.opentext.otds.as.drivers.http.oauth2.attribute5",
                    "_name": "OTDS Attribute 5",
                    "_description": None,
                    "_required": False,
                    "_fileBased": False,
                    "_fileName": False,
                    "_fileExtensions": None,
                    "_value": "oTStreetAddress",
                    "_allowedValues": None,
                    "_confidential": False,
                    "_keepOriginal": False,
                },
                {
                    "_key": "com.opentext.otds.as.drivers.http.oauth2.attribute6",
                    "_name": "OTDS Attribute 6",
                    "_description": None,
                    "_required": False,
                    "_fileBased": False,
                    "_fileName": False,
                    "_fileExtensions": None,
                    "_value": "l",
                    "_allowedValues": None,
                    "_confidential": False,
                    "_keepOriginal": False,
                },
                {
                    "_key": "com.opentext.otds.as.drivers.http.oauth2.attribute7",
                    "_name": "OTDS Attribute 7",
                    "_description": None,
                    "_required": False,
                    "_fileBased": False,
                    "_fileName": False,
                    "_fileExtensions": None,
                    "_value": "st",
                    "_allowedValues": None,
                    "_confidential": False,
                    "_keepOriginal": False,
                },
                {
                    "_key": "com.opentext.otds.as.drivers.http.oauth2.attribute8",
                    "_name": "OTDS Attribute 8",
                    "_description": None,
                    "_required": False,
                    "_fileBased": False,
                    "_fileName": False,
                    "_fileExtensions": None,
                    "_value": "postalCode",
                    "_allowedValues": None,
                    "_confidential": False,
                    "_keepOriginal": False,
                },
                {
                    "_key": "com.opentext.otds.as.drivers.http.oauth2.attribute9",
                    "_name": "OTDS Attribute 9",
                    "_description": None,
                    "_required": False,
                    "_fileBased": False,
                    "_fileName": False,
                    "_fileExtensions": None,
                    "_value": "countryName",
                    "_allowedValues": None,
                    "_confidential": False,
                    "_keepOriginal": False,
                },
                {
                    "_key": "com.opentext.otds.as.drivers.http.oauth2.attribute10",
                    "_name": "OTDS Attribute 10",
                    "_description": None,
                    "_required": False,
                    "_fileBased": False,
                    "_fileName": False,
                    "_fileExtensions": None,
                    "_value": "oTTelephoneNumber",
                    "_allowedValues": None,
                    "_confidential": False,
                    "_keepOriginal": False,
                },
                {
                    "_key": "com.opentext.otds.as.drivers.http.oauth2.attribute11",
                    "_name": "OTDS Attribute 11",
                    "_description": None,
                    "_required": False,
                    "_fileBased": False,
                    "_fileName": False,
                    "_fileExtensions": None,
                    "_value": "oTMemberOf",
                    "_allowedValues": None,
                    "_confidential": False,
                    "_keepOriginal": False,
                },
                {
                    "_key": "com.opentext.otds.as.drivers.http.oauth2.attribute12",
                    "_name": "OTDS Attribute 12",
                    "_description": None,
                    "_required": False,
                    "_fileBased": False,
                    "_fileName": False,
                    "_fileExtensions": None,
                    "_value": "oTDepartment",
                    "_allowedValues": None,
                    "_confidential": False,
                    "_keepOriginal": False,
                },
                {
                    "_key": "com.opentext.otds.as.drivers.http.oauth2.attribute13",
                    "_name": "OTDS Attribute 13",
                    "_description": None,
                    "_required": False,
                    "_fileBased": False,
                    "_fileName": False,
                    "_fileExtensions": None,
                    "_value": "title",
                    "_allowedValues": None,
                    "_confidential": False,
                    "_keepOriginal": False,
                },
            ],
        }

        requestUrl = self.authHandlerUrl()

        logger.info(
            "Adding OAuth auth handler -> {} ({}); calling -> {}".format(
                name, description, requestUrl
            )
        )

        retries = 0
        while True:
            authHandlerResponse = requests.post(
                requestUrl,
                json=authHandlerPostBodyJson,
                headers=requestHeaders,
                cookies=self.cookie(),
            )
            if authHandlerResponse.ok:
                return self.parseRequestResponse(authHandlerResponse)
            # Check if Session has expired - then re-authenticate and try once more
            elif authHandlerResponse.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to add OAuth auth handler -> {}; error -> {}".format(
                        name, authHandlerResponse.text
                    )
                )
                return None

        # end method definition

    def consolidate(self, resource_name: str):
        """Consolidate an OTDS resource

        Args:
            resource_name (string): resource to be consolidated
        Return:
            True if the consolidation succeeded or False if it failed.
        """

        resource = self.getResource(resource_name)
        if not resource:
            logger.error(
                "Resource -> {} not found - cannot consolidate; error -> {}".format(
                    resource_name
                )
            )
            return False

        resourceDN = resource["resourceDN"]
        if not resourceDN:
            logger.error("Resource DN is empty - cannot consolidate")
            return False

        consolidationPostBodyJson = {
            "cleanupUsersInResource": False,
            "cleanupGroupsInResource": False,
            "resourceList": [resourceDN],
            "objectToConsolidate": resourceDN,
        }

        requestUrl = "{}".format(self.consolidationUrl())

        logger.info(
            "Consolidation of resource -> {}; calling -> {}".format(
                resourceDN, requestUrl
            )
        )

        retries = 0
        while True:
            consolidationResponse = requests.post(
                requestUrl,
                json=consolidationPostBodyJson,
                headers=requestHeaders,
                cookies=self.cookie(),
            )
            if consolidationResponse.ok:
                return True
            # Check if Session has expired - then re-authenticate and try once more
            elif consolidationResponse.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to consolidate; error -> {}".format(
                        consolidationResponse.text
                    )
                )
                return False

    # end method definition

    def impersonateResource(
        self,
        resource_name: str,
        allow_impersonation: bool = True,
        impersonation_list: list = [],
    ):
        """Configure impersonation for an OTDS resource

        Args:
            resource_name (string): resource to be configure impersonation for
            allow_impersonation (boolean): optional; wether to turn on or off impersonation
            impersonation_list (list): optional; list of users to restrict it to; empty list = all users
        Return:
            True if the impersonation setting succeeded or False if it failed.
        """

        impersonationPutBodyJson = {
            "allowImpersonation": allow_impersonation,
            "impersonateList": impersonation_list,
        }

        requestUrl = "{}/{}/impersonation".format(self.resourceUrl(), resource_name)

        logger.info(
            "Impersonation settings for resource -> {}; calling -> {}".format(
                resource_name, requestUrl
            )
        )

        retries = 0
        while True:
            impersonationResponse = requests.put(
                requestUrl,
                json=impersonationPutBodyJson,
                headers=requestHeaders,
                cookies=self.cookie(),
            )
            if impersonationResponse.ok:
                return True
            # Check if Session has expired - then re-authenticate and try once more
            elif impersonationResponse.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to set impersonation for resource -> {}; error -> {}".format(
                        resource_name, impersonationResponse.text
                    )
                )
                return False

    # end method definition

    def impersonateOauthClient(
        self,
        client_id: str,
        allow_impersonation: bool = True,
        impersonation_list: list = [],
    ):
        """Configure impersonation for an OTDS OAuth Client

        Args:
            client_id (string): OAuth Client to be configure impersonation for
            allow_impersonation (boolean): optional; wether to turn on or off impersonation
            impersonation_list (list): optional; list of users to restrict it to; empty list = all users
        Return:
            True if the impersonation setting succeeded or False if it failed.
        """

        impersonationPutBodyJson = {
            "allowImpersonation": allow_impersonation,
            "impersonateList": impersonation_list,
        }

        requestUrl = "{}/{}/impersonation".format(self.oauthClientUrl(), client_id)

        logger.info(
            "Impersonation settings for OAuth Client -> {}; calling -> {}".format(
                client_id, requestUrl
            )
        )

        retries = 0
        while True:
            impersonationResponse = requests.put(
                requestUrl,
                json=impersonationPutBodyJson,
                headers=requestHeaders,
                cookies=self.cookie(),
            )
            if impersonationResponse.ok:
                return True
            # Check if Session has expired - then re-authenticate and try once more
            elif impersonationResponse.status_code == 401 and retries == 0:
                logger.warning("Session has expired - try to re-authenticate...")
                self.authenticate(True)
                retries += 1
            else:
                logger.error(
                    "Failed to set impersonation for OAuth Client -> {}; error -> {}".format(
                        client_id, impersonationResponse.text
                    )
                )
                return False

    # end method definition