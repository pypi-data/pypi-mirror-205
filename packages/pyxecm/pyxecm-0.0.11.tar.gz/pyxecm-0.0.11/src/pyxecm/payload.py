"""
Payload Module to implement functions to process Terrarium payload

This code processes a YAML payload file that includes various settings:
* WebHooks (URLs) to call (e.g. to start-up external services or applications)
* OTDS partitions and OAuth clients
* OTDS trusted sites and system attributes
* OTDS licenses
* Extended ECM users and groups
* Extended ECM Admin Settings (LLConfig)
* Extended ECM External System Connections (SAP, SuccessFactors, ...)
* Extended ECM Transport Packages (scenarios and demo content)
* Extended ECM CS Applications (typically based on Web Reports)
* Extended ECM Web Reports to run
* Extended ECM Workspaces to create (incl. members, workspace relationships)
* Extended ECM user photos, user favorites and user settings
* Extended ECM items to create and permissions to apply
* Extended ECM items to rename
* Extended ECM assignments (used e.g. for Government scenario)
* Extended ECM Records Management settings, Security Clearance, Supplemental Markings, and Holds
* SAP RFCs (Remote Function Calls)
* Commands to execute in Kubernetes Pods

This code typically runs in a container as part of the cloud automation.

Class: Payload
Methods:

__init__ : class initializer
replacePlaceholders: replace placeholder in admin config files
initPayload: load and initialize the YAML payload
getPayloadSection: delivers a section of the payload as a list of settings

processPayload: process payload (main method)
processWebHooks: process list of web hooks
processPartitions: process the OTDS partitions
processOAuthClients: process the OTDS OAuth clients
processTrustedSites: process the OTDS trusted sites
processSystemAttributes: process the OTDS system attributes
processGroups: process Extended ECM user groups
processGroupsM365: process M365 user groups
processUsers: process Extended ECM users
processUsersM365: process M365 users
processAdminSettings: process Extended ECM administration settings (LLConfig)
processExternalSystems: process Extended ECM external systems
processTransportPackages: process Extended ECM transport packages
processUserPhotos: process Extended ECM user photos (user profile)
processWorkspaceTypes: process Extended ECM workspace types (needs to run after processTransportPackages)
processWorkspaceTemplateRegistrations: register workspace templates as projects for Extended ECM for Engineering (deprecated)
processWorkspaces: process Extended ECM workspace instances
processWorkspaceRelationships: process Extended ECM workspace relationships
processWorkspaceMembers: process Extended ECM workspace members (users and groups)
processWebReports: process Extended ECM Web Reports (starts them with parameters)
processCSApplications: process Extended ECM CS Applications
processUserFavoritesAndSettings: process Extended ECM user favorites and user settings
processSecurityClearances: process Security Clearance for users
processSupplementalMarkings: process Supplemental Markings for users
processUserSecurity: process Security Clearance and Supplemental Markings for users
processRecordsManagementSettings: process Records Management settings by applying settings files
processHolds: process Records Management Holds
processAdditionalGroupMembers: process additional OTDS group memberships
processAdditionalAccessRoleMembers: process additional OTDS group memberships
processRenamings: process Extended ECM node renamings
processItems: process Extended ECM items (nodes) to create
processPermissions: process permission changes for alist of Extended ECM items or volumes
processAssignments: process assignments of workspaces / documents to users / groups
processUserLicenses: process and apply licenses to all Extended ECM users (used for OTIV)
processExecPodCommands: process Kubernetes pod commands
initSAP: initalize SAP object for RFC communication
processSAPRFCs: process SAP Remote Function Calls (RFC) to trigger automation in SAP S/4HANA

getPayload: return the payload data structure
getUsers: return list of users
getGroups: return list of groups
getWorkspaces: return list of workspaces
getOTCSFrontend: return OTCS object for OTCS frontend
getOTCSBackend: return OTCS object for OTCS backend
getOTDS: return OTDS object
getK8S: return the Kubernetes object

"""

__author__ = "Dr. Marc Diefenbruch"
__copyright__ = "Copyright 2023, OpenText"
__credits__ = ["Kai-Philip Gatzweiler"]
__maintainer__ = "Dr. Marc Diefenbruch"
__email__ = "mdiefenb@opentext.com"

import os
import logging
import yaml
import hcl2
import re

from urllib.parse import urlparse


logger = logging.getLogger(os.path.basename(__file__))

# OpenText specific modules:
from pyxecm import web

try:
  from pyxecm import sap
except ImportError as e:
  logger.error(f"Loading SAP failed -> {e}")  



class Payload(object):
    """Used to process Terrarium payload."""

    # _debug controls whether or not transport processing is
    # stopped if one transport fails:
    _debug = False
    _otcs = None
    _otcs_backend = None
    _otcs_frontend = None
    _otds = None
    _otiv = None
    _k8s = None
    _web = None
    _m365 = None
    _custom_settings_dir = ""

    # _payload_source (string): This is either path + filename of the yaml payload
    # or an path + filename of the Terraform HCL payload
    _payload_source = ""
    # _payload is a dict of the complete payload file.
    # It is initialized by the initPayload() method:
    _payload = {}
    # _payload_sections is a list of dicts:
    _payload_sections = []

    # Initialize payload section variables. They are all liust of dicts:
    _webhooks = []
    _webhooks_post = []
    _partitions = []
    _oauth_clients = []
    _trusted_sites = []
    _system_attributes = []
    _groups = []
    # users: List of users. List items are dicts with "id", "name" (= login),
    # "password", "firstname", "lastname", and "email"
    _users = []
    _admin_settings = []
    # exec_pod_commands: list of commands to be executed in the pods
    # list elements need to be dicts with pod name, command, etc.
    _exec_pod_commands = []
    # external_systems (list): List of external systems. Each list element is a dict with
    # "description", "external_system_name", "connection_type",
    # "as_url", "base_url", "username", and "password". Depending
    # on the connection type there may be additional dict values.
    _external_systems = []
    # transport_packages (list): List of transport packages systems. Each list element is a
    # dict with "url", "name", and "description" keys.
    _transport_packages = []
    _workspace_types = []
    _workspaces = []
    _sap_rfcs = []
    _web_reports = []
    _web_reports_post = []
    _cs_applications = []
    _admin_settings_post = []
    # additional_group_members: List of memberships to establish. Each element
    # is a dict with these keys:
    # - parent_group (string)
    # - user_name (string)
    # - group_name (string)
    _additional_group_members = []
    # additional_access_role_members: List of memberships to establish. Each element
    # is a dict with these keys:
    # - access_role (string)
    # - user_name (string)
    # - group_name (string)
    # - partition_name (string)
    _additional_access_role_members = []
    _renamings = []
    _content_transport_packages = []
    _items = []
    _items_post = []
    _permissions = []
    _permissions_post = []
    # assignments: List of assignments. Each element is a dict with these keys:
    # - subject (string)
    # - instruction (string)
    # - workspace (string)
    # - nickname (string)
    # - groups (list)
    # - users (list)
    _assignments = []
    _workspace_template_registrations = []
    _security_clearances = []
    _supplemental_markings = []
    _records_management_settings = []
    _holds = []

    _placeholder_values = {}

    def __init__(self, payload_source: str,
                 custom_settings_dir: str,
                 k8s_object: object,
                 otds_object: object,
                 otcs_backend_object: object,
                 otcs_frontend_object: object,
                 otiv_object: object,
                 m365_object: object,
                 placeholder_values: dict = {},
                 stop_on_error: bool = False):
        """Initialize the Payload object

        Args:
            payload_source (string): path or URL to payload source file
            k8s_object (object): Kubernetes object
            otds_object (object): OTDS object
            otcs_backend_object (object): OTCS backend object
            otcs_frontend_object (object): OTCS frontend object
            otiv_object (object): OTIV object
            m365_object (object): M365 object to talk to Microsoft Graph API
            placeholder_values (dict): dictionary of placeholder values to be replaced in admin settings
            stop_on_error (bool): controls if transport deployment should stop if one transport fails
        """

        self._stop_on_error = stop_on_error
        self._payload_source = payload_source
        self._k8s = k8s_object
        self._otds = otds_object
        self._otcs = otcs_backend_object
        self._otcs_backend = otcs_backend_object
        self._otcs_frontend = otcs_frontend_object
        self._otiv = otiv_object
        self._m365 = m365_object
        self._custom_settings_dir = custom_settings_dir
        self._placeholder_values = placeholder_values

        self._http_object = web.HTTP()

       # end method definition

    def replacePlaceholders(self, content: str):

        # https://stackoverflow.com/questions/63502218/replacing-placeholders-in-a-text-file-with-python
        return re.sub(
            r"%%(\w+?)%%", lambda match: self._placeholder_values[match.group(
                1)], content
        )

        # end method definition

    def initPayload(self):
        """Read the YAML or Terraform HCL payload file.

        Args: None
        Return:
            payload as a Python dict. Elements are the different payload sections.
            None in case the file couldn't be found or read.
        """

        if not os.path.exists(self._payload_source):
            logger.error(
                "Cannot access payload file -> {}".format(self._payload_source))
            return None

        # Is it a YAML file?
        if self._payload_source.endswith(".yaml"):
            logger.info(
                "Open payload from YAML file -> {}".format(self._payload_source))
            try:
                with open(self._payload_source, "r") as stream:
                    payload_data = stream.read()
                self._payload = yaml.safe_load(payload_data)
            except yaml.YAMLError as exc:
                logger.error(
                    "Error while reading YAML payload file -> {}; error -> {}".format(
                        self._payload_source, exc
                    )
                )
                self._payload = None
        # Or is it a Terraform HCL file?
        elif self._payload_source.endswith(".tf"):
            logger.info(
                "Open payload from Terraform HCL file -> {}".format(self._payload_source))
            try:
                with open(self._payload_source, "r") as stream:
                    self._payload = hcl2.load(stream)
                # If payload is wrapped into "external_payload" we unwrap it:
                if self._payload.get("external_payload"):
                    self._payload = self._payload["external_payload"]
            except Exception as exc:
                logger.error(
                    "Error while reading Terraform HCL payload file -> {}; error -> {}".format(
                        self._payload_source, exc
                    )
                )
                self._payload = None
        # If not, it is an unsupported type:
        else:
            logger.error(
                "File -> {} has unsupported file type; error -> {}".format(
                    self._payload_source)
            )
            self._payload = None

        self._payload_sections = self._payload["payloadSections"]
        if not self._payload_sections:
            logger.error(
                "Sections for payload -> {} are undefined - skipping...".format(
                    self._payload_source
                )
            )
            return None

        # Retrieve all the payload sections and store them in lists:
        self._webhooks = self.getPayloadSection("webHooks")
        self._webhooks_post = self.getPayloadSection("webHooksPost")
        self._partitions = self.getPayloadSection("partitions")
        self._oauth_clients = self.getPayloadSection("oauthClients")
        self._trusted_sites = self.getPayloadSection("trustedSites")
        self._system_attributes = self.getPayloadSection("systemAttributes")
        self._groups = self.getPayloadSection("groups")
        self._users = self.getPayloadSection("users")
        self._admin_settings = self.getPayloadSection("adminSettings")
        self._exec_pod_commands = self.getPayloadSection("execPodCommands")
        self._external_systems = self.getPayloadSection("externalSystems")
        self._transport_packages = self.getPayloadSection("transportPackages")
        self._workspaces = self.getPayloadSection("workspaces")
        self._sap_rfcs = self.getPayloadSection("sapRFCs")
        self._web_reports = self.getPayloadSection("webReports")
        self._web_reports_post = self.getPayloadSection("webReportsPost")
        self._cs_applications = self.getPayloadSection("csApplications")
        self._admin_settings_post = self.getPayloadSection("adminSettingsPost")
        self._additional_group_members = self.getPayloadSection(
            "additionalGroupMemberships")
        self._additional_access_role_members = self.getPayloadSection(
            "additionalAccessRoleMemberships")
        self._renamings = self.getPayloadSection("renamings")
        self._content_transport_packages = self.getPayloadSection(
            "contentTransportPackages")
        self._items = self.getPayloadSection("items")
        self._items_post = self.getPayloadSection("itemsPost")
        self._permissions = self.getPayloadSection("permissions")
        self._permissions_post = self.getPayloadSection("permissionsPost")
        self._assignments = self.getPayloadSection("assignments")
        self._workspace_template_registrations = self.getPayloadSection(
            "workspaceTemplateRegistrations",
        )
        self._security_clearances = self.getPayloadSection(
            "securityClearances")
        self._supplemental_markings = self.getPayloadSection(
            "supplementalMarkings")
        self._records_management_settings = self.getPayloadSection(
            "recordsManagementSettings")
        self._holds = self.getPayloadSection("holds")

        return self._payload
        # end method definition

    def getPayloadSection(self, payload_section_name: str):
        """Get a defined section of the payload. The section is delivered as a list of settings.
        It deliveres an empty list if this payload section is disabled by the corresponding
        payload switch (this is read from the payloadSections dictionary of the payload)

        Args:
            payload (dict): payload data structure (converted to dict from YAML file)
            payload_section_name (string): name of the dict element in the payload structure
        Return:
            section of the payload as a Python list. Empty list if section does not exist
            or section is disabled by the corresponding payload switch.
        """

        # if the secton is not in the payload we return an empty list:
        if not self._payload.get(payload_section_name):
            return []

        # Check if the payload section is either enabled
        # or the struct for payloadSection enabling is not in the payload:
        sections = self._payload.get("payloadSections")
        if sections:
            section = next(
                (item for item in sections if item["name"]
                 == payload_section_name),
                None,
            )
            if not section or not section["enabled"]:
                return []

        return self._payload[payload_section_name]

        # end method definition

    def processPayload(self):
        """Main method to process a payload file.

        Returns: None
        """

        if not self._payload_sections:
            return None

        for payload_section in self._payload_sections:
            match payload_section["name"]:
                case "webHooks":
                    logger.info(
                        "========== Process Web Hooks ==========================="
                    )
                    self.processWebHooks(self._webhooks)
                case "webHooksPost":
                    logger.info(
                        "========== Process Web Hooks (post) ===================="
                    )
                    self.processWebHooks(self._webhooks_post)
                case "partitions":
                    logger.info(
                        "========== Process OTDS Partitions ====================="
                    )
                    self.processPartitions()
                case "oauthClients":
                    logger.info(
                        "========== Process OTDS OAuth Clients =================="
                    )
                    self.processOAuthClients()
                case "trustedSites":
                    logger.info(
                        "========== Process OTDS Trusted Sites =================="
                    )
                    self.processTrustedSites()
                case "systemAttributes":
                    logger.info(
                        "========== Process OTDS System Attributes =============="
                    )
                    self.processSystemAttributes()
                case "groups":
                    logger.info(
                        "========== Process OTCS Groups ========================="
                    )
                    self.processGroups()
                    if self._m365:
                        logger.info(
                            "========== Process M365 Groups ========================="
                        )
                        self.processGroupsM365()
                case "users":
                    logger.info(
                        "========== Process OTCS Users =========================="
                    )
                    self.processUsers()
                    logger.info("========== Assign OTCS Licenses to Users ===============")
                    self.processUserLicenses(
                        self._otcs.config()["resource"],
                        self._otcs.config()["license"],
                        "EXTENDED_ECM",
                        user_specific_payload_field="license"
                    )
                    logger.info("========== Assign OTIV Licenses to Users ===============")
                    self.processUserLicenses(
                        self._otiv.config()["resource"],
                        self._otiv.config()["license"],
                        "INTELLIGENT_VIEWING",
                        user_specific_payload_field=""
                    )
                    if self._m365:
                        logger.info(
                            "========== Process M365 Users =========================="
                        )
                        self.processUsersM365()
                        logger.info(
                            "========== Process M365 Teams =========================="
                        )
                        self.processTeamsM365()
                case "adminSettings":
                    logger.info(
                        "========== Process OTCS LLConfig Settings (1) =========="
                    )
                    self.processAdminSettings(self._admin_settings)
                case "adminSettingsPost":
                    logger.info(
                        "========== Process OTCS LLConfig Settings (2) =========="
                    )
                    self.processAdminSettings(self._admin_settings_post)
                case "execPodCommands":
                    logger.info(
                        "========== Process Pod Commands ========================"
                    )
                    self.processExecPodCommands()
                case "csApplications":
                    logger.info(
                        "========== Process CS Apps (backend) ==================="
                    )
                    self.processCSApplications()
                    logger.info(
                        "========== Process CS Apps (frontend) =================="
                    )
                    self.processCSApplications(self._otcs_frontend)
                case "externalSystems":
                    logger.info(
                        "========== Process External System Connections ========="
                    )
                    self.processExternalSystems()
                case "transportPackages":
                    logger.info(
                        "========== Process Transport Packages =================="
                    )
                    self.processTransportPackages(self._transport_packages)
                    # right after the transport that create the workspace types
                    # we extract them and put them in a generated payload list:
                    logger.info(
                        "========== Process Workspace Types ====================="
                    )
                    workspace_types = self.processWorkspaceTypes()
                case "workspaceTemplateRegistrations":
                    logger.info(
                        "========== Register Workspace Templates ================"
                    )
                    self.processWorkspaceTemplateRegistrations()
                case "workspaces":
                    logger.info(
                        "========== Process Workspaces =========================="
                    )
                    self.processWorkspaces()
                    logger.info(
                        "========== Process Workspace Relationships ============="
                    )
                    self.processWorkspaceRelationships()
                    logger.info(
                        "========== Process Workspace Memberships ==============="
                    )
                    self.processWorkspaceMembers()
                case "sapRFCs":
                    logger.info(
                        "========== Process SAP RFCs ============================"
                    )

                    if self._external_systems:
                        sap_external_system = next(
                            (
                                item
                                for item in self._external_systems
                                if item["external_system_type"] == "SAP"
                            ),
                            None,
                        )
                    if not sap_external_system:
                        logger.warning(
                            "SAP RFC in payload but SAP external system is configured. RFCs will not be processed."
                        )
                    elif not sap_external_system.get("enabled"):
                        logger.warning(
                            "SAP RFC in payload but SAP external system is disabled. RFCs will not be processed."
                        )
                    elif not sap_external_system.get("reachable"):
                        logger.warning(
                            "SAP RFC in payload but SAP external system is not reachable. RFCs will not be processed."
                        )
                    else:
                        sap = self.initSAP(sap_external_system)
                        if sap:
                            self.processSAPRFCs(sap)
                case "webReports":
                    logger.info(
                        "========== Process Web Reports ========================="
                    )
                    self.processWebReports(self._web_reports)
                case "webReportsPost":
                    logger.info(
                        "========== Process Web Reports (post) =================="
                    )
                    self.processWebReports(self._web_reports_post)
                case "additionalGroupMemberships":
                    logger.info(
                        "========== Process additional group members for OTDS ==="
                    )
                    self.processAdditionalGroupMembers()
                case "additionalAccessRoleMemberships":
                    logger.info(
                        "==== Process additional access role members for OTDS ==="
                    )
                    self.processAdditionalAccessRoleMembers()
                case "renamings":
                    logger.info(
                        "========== Process Custom Node Renamings ==============="
                    )
                    self.processRenamings()
                case "contentTransportPackages":
                    logger.info(
                        "========== Process Content Transport Packages =========="
                    )
                    self.processTransportPackages(
                        self._content_transport_packages)
                case "items":
                    logger.info(
                        "========== Process Items ==============================="
                    )
                    self.processItems(self._items)
                case "itemsPost":
                    logger.info(
                        "========== Process Items (post) ========================"
                    )
                    self.processItems(self._items_post)
                case "permissions":
                    logger.info(
                        "========== Process Permissions ========================="
                    )
                    self.processPermissions(self._permissions)
                case "permissionsPost":
                    logger.info(
                        "========== Process Permissions (post) =================="
                    )
                    self.processPermissions(self._permissions_post)
                case "assignments":
                    logger.info(
                        "========== Process Assignments ========================="
                    )
                    self.processAssignments()
                case "securityClearances":
                    logger.info(
                        "========== Process Security Clearances ================="
                    )
                    self.processSecurityClearances()
                case "supplementalMarkings":
                    logger.info(
                        "========== Process Supplemental Markings ==============="
                    )
                    self.processSupplementalMarkings()
                case "recordsManagementSettings":
                    logger.info(
                        "========== Process Records Management Settings ========="
                    )
                    self.processRecordsManagementSettings()
                case "holds":
                    logger.info(
                        "========== Process Records Management Holds ============"
                    )
                    self.processHolds()
                case other:
                    logger.error(
                        "Illegal payload section name -> {} in payloadSections!".format(
                            payload_section["name"]
                        )
                    )

        if self._users:
            logger.info(
                "========== Process User Profile Photos =================")
            self.processUserPhotos()
            if self._m365:
                logger.info(
                    "========== Process M365 User Profile Photos ============")
                self.processUserPhotosM365()
            logger.info(
                "========== Process User Favorites and Settings =========")
            self.processUserFavoritesAndSettings()
            logger.info(
                "========== Process User Security =======================")
            self.processUserSecurity()

        # end method definition

    def processWebHooks(self, webhooks: list):
        """Process Web Hooks in payload and do HTTP requests.

        Args: None
        Return: None
        """

        if not webhooks:
            return None

        for webhook in webhooks:

            url = webhook.get("url")
            if not url:
                logger.info("Web Hook does not have a url - skipping...")
                continue

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in webhook and not webhook["enabled"]:
                logger.info(
                    "Payload for Web Hook -> {} is disabled. Skipping...".format(
                        url
                    )
                )
                continue

            description = webhook.get("description")

            method = webhook.get("method", "POST")

            payload = webhook.get("payload", {})

            headers = webhook.get("headers", {})

            if description:
                logger.info(
                    "Calling Web Hook -> {}: {} ({})".format(method, url, description))
            else:
                logger.info(
                    "Calling Web Hook -> {}: {}".format(method, url))

            self._http_object.httpRequest(url, method, payload, headers)

        # end method definition

    def processPartitions(self):
        """Process OTDS partitions in payload and create them in OTDS.

        Args: None
        Return: None
        """

        for partition in self._partitions:

            partition_name = partition.get("name")
            if not partition_name:
                logger.error("Partition does not have a name - skipping...")
                continue

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in partition and not partition["enabled"]:
                logger.info(
                    "Payload for Partition -> {} is disabled. Skipping...".format(
                        partition_name
                    )
                )
                continue

            partition_description = partition.get("description")

            # Check if Partition does already exist
            # (in an attempt to make the code idem-potent)
            logger.info(
                "Check if OTDS partition -> {} does already exist...".format(partition_name))
            response = self._otds.getPartition(
                partition_name, show_error=False)
            if response:
                logger.info(
                    "Partition -> {} does already exist. Skipping...".format(partition_name))
                continue
            else:
                logger.info(
                    "Partition -> {} does not exist. Creating...".format(partition_name))

            response = self._otds.addPartition(
                partition_name, partition_description)
            if response:
                logger.info(
                    "Added OTDS partition -> {}".format(partition_name))
            else:
                logger.error(
                    "Failed to add OTDS partition -> {}".format(partition_name))
                continue

            access_role = partition.get("access_role")
            if access_role:
                response = self._otds.addPartitionToAccessRole(
                    access_role, partition_name)
                if response:
                    logger.info(
                        "Added OTDS partition -> {} to access role -> {}".format(
                            partition_name, access_role
                        )
                    )
                else:
                    logger.error(
                        "Failed to add OTDS partition -> {} to access role -> {}".format(
                            partition_name, access_role
                        )
                    )
                    continue

        # end method definition

    def processOAuthClients(self):
        """Process OTDS OAuth clients in payload and create them in OTDS.

        Args: None
        Return: None
        """

        for oauth_client in self._oauth_clients:

            client_name = oauth_client.get("name")
            if not client_name:
                logger.error("OAuth client does not have a name - skipping...")
                continue

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in oauth_client and not oauth_client["enabled"]:
                logger.info(
                    "Payload for OAuthClient -> {} is disabled. Skipping...".format(
                        client_name
                    )
                )
                continue

            client_description = oauth_client.get("description")
            client_confidential = oauth_client.get("confidential")
            client_partition = oauth_client.get("partition")
            if client_partition == "Global":
                client_partition = None
            client_redirect_urls = oauth_client.get("redirect_urls")
            client_permission_scopes = oauth_client.get("permission_scopes")
            client_default_scopes = oauth_client.get("default_scopes")
            client_allow_impersonation = oauth_client.get(
                "allow_impersonation")

            # Check if OAuth client does already exist
            # (in an attempt to make the code idem-potent)
            logger.info(
                "Check if OTDS OAuth Client -> {} does already exist...".format(client_name))
            response = self._otds.getOauthClient(
                client_name, show_error=False)
            if response:
                logger.info(
                    "OAuth Client -> {} does already exist. Skipping...".format(client_name))
                continue
            else:
                logger.info(
                    "OAuth Client -> {} does not exist. Creating...".format(client_name))

            response = self._otds.addOauthClient(
                client_id=client_name,
                description=client_description,
                redirect_urls=client_redirect_urls,
                allow_impersonation=client_allow_impersonation,
                confidential=client_confidential,
                auth_scopes=client_partition,
                allowed_scopes=client_permission_scopes,
                default_scopes=client_default_scopes,
            )
            if response:
                logger.info(
                    "Added OTDS OAuth client -> {}".format(client_name))
            else:
                logger.error(
                    "Failed to add OTDS OAuth client -> {}".format(client_name))
                continue

            client_secret = response.get("secret")
            if not client_secret:
                logger.error(
                    "OAuth client -> {} does not have a secret!".format(
                        client_name)
                )
                continue

            client_description += " Client Secret Key: " + str(client_secret)
            response = self._otds.updateOauthClient(
                client_name, {"description": client_description}
            )

    #        self._otds.addOauthClientsToAccessRole()

    # end method definition

    def processTrustedSites(self):
        """Process OTDS trusted sites in payload and create them in OTDS.

        Args: None
        Return: None
        """

        for trusted_site in self._trusted_sites:
            self._otds.addTrustedSite(trusted_site)
            logger.info("Added OTDS trusted site -> {}".format(trusted_site))

        # end method definition

    def processSystemAttributes(self):
        """Process OTDS system attributes in payload and create them in OTDS.

        Args: None
        Return: None
        """

        for system_attribute in self._system_attributes:
            # Check if there's a matching formal parameter defined on the Web Report node:
            if not system_attribute.get("name"):
                logger.error("OTDS System Attribute needs a name. Skipping...")
                continue
            attribute_name = system_attribute["name"]

            if "enabled" in system_attribute and not system_attribute["enabled"]:
                logger.info(
                    "Payload for OTDS System Attribute -> {} is disabled. Skipping...".format(
                        attribute_name
                    )
                )
                continue

            if not system_attribute.get("value"):
                logger.error(
                    "OTDS System Attribute needs a value. Skipping...")
                continue

            attribute_value = system_attribute["value"]
            attribute_description = system_attribute.get("description")
            self._otds.addSystemAttribute(
                attribute_name, attribute_value, attribute_description)
            logger.info(
                "Added OTDS system attribute -> {} with value -> {}".format(
                    attribute_name, attribute_value
                )
            )

        # end method definition

    def processGroups(self):
        """Process groups in payload and create them in Extended ECM.

        Args: None
        Return: None
        Side Effects:
            the group items are modified by adding an "id" dict element that
            includes the technical ID of the group in Extended ECM
        """

        # First run through groups: create all groups in payload
        # and store the IDs of the created groups:
        for group in self._groups:

            if not "name" in group:
                logger.error("Group needs a name. Skipping...")
                continue
            group_name = group["name"]

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in group and not group["enabled"]:
                logger.info(
                    "Payload for Group -> {} is disabled. Skipping...".format(
                        group_name)
                )
                continue

            # Check if the group does already exist (e.g. if job is restarted)
            # as this is a pattern search it could return multiple groups:
            existing_groups = self._otcs.getGroup(group_name)
            if existing_groups and existing_groups["data"]:
                logger.debug(
                    "Found existing groups -> {}".format(existing_groups["data"]))
                # Get list of all matching groups:
                existing_groups_list = existing_groups["data"]
                # Find the group with the exact match of the name:
                existing_group = next(
                    (item for item in existing_groups_list if item["name"] == group_name),
                    None,
                )
                # Have we found an exact match?
                if existing_group is not None:
                    logger.info(
                        "Found existing group -> {} ({}) - skipping to next group...".format(
                            existing_group["name"], existing_group["id"]
                        )
                    )
                    group["id"] = existing_group["id"]

                    # Add Group with its ID to the class dict _placeholder_values:
                    self._placeholder_values[
                        "OTCS_GROUP_ID_{}".format(
                            group_name.upper().replace(" & ", "_").replace(" ", "_")
                        )
                    ] = str(group["id"])
                    continue
                else:
                    logger.info(
                        "Did not find an exact match for the group - creating a new group..."
                    )
            else:
                logger.info(
                    "Did not find any matching group - creating a new group...")
            # Now we know it is a new group...
            new_group = self._otcs.addGroup(group_name)
            if new_group is not None:
                logger.debug("New group -> {}".format(new_group))
                group["id"] = new_group["id"]

            # Add Group with its ID to the global dict with placeholder values:
            self._placeholder_values[
                "OTCS_GROUP_ID_{}".format(
                    group_name.upper().replace(" & ", "_").replace(" ", "_")
                )
            ] = str(group["id"])

        logger.debug("Groups = {}".format(self._groups))

        logger.debug(
            "Placeholder values after group processing = {}".format(
                self._placeholder_values)
        )

        # Second run through groups: create all group memberships
        # (nested groups) based on the IDs created in first run:
        for group in self._groups:
            if not "id" in group:
                logger.error(
                    "Group -> {} does not have an ID.".format(group["name"]))
                continue
            parent_group_names = group["parent_groups"]
            for parent_group_name in parent_group_names:
                # First, try to find parent group in payload by parent group name:
                parent_group = next(
                    (item for item in self._groups if item["name"]
                     == parent_group_name), None
                )
                if parent_group is None:
                    # If this didn't work, try to get the parent group from OTCS. This covers
                    # cases where the parent group is system generated or part
                    # of a former payload processing:
                    parent_group = self._otcs.getGroup(
                        parent_group_name)
                    if not parent_group:
                        logger.error(
                            "Parent Group -> {} not found. Skipping...".format(
                                parent_group_name
                            )
                        )
                        continue
                    parent_group = parent_group["data"][0]
                elif not "id" in parent_group:
                    logger.error(
                        "Parent Group -> {} does not have an ID. Skipping...".format(
                            parent_group["name"]
                        )
                    )
                    continue

                # retrieve all members of the parent group (1 = get only groups)
                members = self._otcs.getGroupMembers(
                    parent_group["id"], 1)
                if self._otcs.existResultItem(members, "id", group["id"]):
                    #                if existing_member:
                    logger.info(
                        "Group -> {} ({}) is already a member of parent group -> {} ({}) - skipping to next parent group...".format(
                            group["name"],
                            group["id"],
                            parent_group["name"],
                            parent_group["id"],
                        )
                    )
                else:
                    logger.info(
                        "Add group -> {} ({}) to parent group -> {} ({})".format(
                            group["name"],
                            group["id"],
                            parent_group["name"],
                            parent_group["id"],
                        )
                    )
                    self._otcs.addGroupMember(
                        group["id"], parent_group["id"])

        # end method definition

    def processGroupsM365(self):
        """Process groups in payload and create them in Microsoft 365.

        Args: None
        Return: None
        """

        # First run through groups: create all groups in payload
        # and store the IDs of the created groups:
        for group in self._groups:

            if not "name" in group:
                logger.error("Group needs a name. Skipping...")
                continue
            group_name = group["name"]

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in group and not group["enabled"]:
                logger.info(
                    "Payload for Group -> {} is disabled. Skipping...".format(
                        group_name)
                )
                continue
            if not "enable_o365" in group or not group["enable_o365"]:
                logger.info(
                    "Office 365 is not enabled in payload for Group -> {}. Skipping...".format(
                        group_name)
                )
                continue

            # Check if the group does already exist (e.g. if job is restarted)
            # as this is a pattern search it could return multiple groups:
            existing_groups = self._m365.getGroup(group_name)
            if existing_groups and existing_groups["value"]:
                logger.debug(
                    "Found existing Azure AD groups -> {}".format(existing_groups["value"]))
                # Get list of all matching groups:
                existing_groups_list = existing_groups["value"]
                # Find the group with the exact match of the name:
                existing_group = next(
                    (item for item in existing_groups_list if item["displayName"] == group_name),
                    None,
                )
                # Have we found an exact match?
                if existing_group is not None:
                    logger.info(
                        "Found existing Azure AD group -> {} ({}) - skip creation of group...".format(
                            existing_group["displayName"], existing_group["id"]
                        )
                    )
                    group["m365_id"] = existing_group["id"]
                    continue
                else:
                    logger.info(
                        "Did not find an exact match for the group - creating a new Azure AD group..."
                    )
            else:
                logger.info(
                    "Did not find any matching group - creating a new Azure AD group...")

            # Now we know it is a new group...
            new_group = self._m365.addGroup(group_name)
            if new_group is not None:
                # Store the Microsoft 365 group ID in payload:
                group["m365_id"] = new_group["id"]
                logger.info(
                    "New Azure AD group -> {} with ID -> {} has been created".format(
                        group_name, group["m365_id"]
                    )
                )

        # end method definition

    def processUsers(self):
        """Process users in payload and create them in Extended ECM.

        Args: None
        Return: None
        Side Effects:
            the user items are modified by adding an "id" dict element that
            includes the technical ID of the user in Extended ECM
        """

        # Add all users in payload and establish membership in
        # specified groups:
        for user in self._users:

            # Sanity checks:
            if not "name" in user:
                logger.error(
                    "User is missing a login - skipping to next user...")
                continue
            user_name = user["name"]

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in user and not user["enabled"]:
                logger.info(
                    "Payload for User -> {} is disabled. Skipping...".format(
                        user_name)
                )
                continue

            # Sanity checks:
            if not "password" in user:
                logger.error(
                    "User -> {} is missing a password - skipping to next user...".format(
                        user_name
                    )
                )
                continue

            # Sanity checks:
            if not "base_group" in user:
                logger.warning(
                    "User -> {} is missing a base group - setting to default group".format(
                        user_name
                    )
                )
                user["base_group"] = "DefaultGroup"

            # Check if the user does already exist (e.g. if job is restarted)
            # As this is a pattern search it could return multiple users:
            existing_users = self._otcs.getUser(user_name)
            if existing_users and existing_users["data"]:
                logger.debug(
                    "Found existing users -> {}".format(existing_users["data"]))
                # Get list of all matching users:
                existing_users_list = existing_users["data"]
                # Find the user with the exact match of the name:
                existing_user = next(
                    (item for item in existing_users_list if item["name"] == user_name),
                    None,
                )
                # Have we found an exact match?
                if existing_user is not None:
                    logger.info(
                        "Found existing user -> {} ({}) - skipping to next user...".format(
                            existing_user["name"], existing_user["id"]
                        )
                    )
                    user["id"] = existing_user["id"]
                    continue
                else:
                    logger.info(
                        "Did not find an exact match for the user - creating a new user..."
                    )
            else:
                logger.info(
                    "Did not find any matching user - creating a new user...")

            # Find the base group of the user. Assume 'Default Group' (= 1001) if not found:
            base_group = next(
                (item["id"]
                 for item in self._groups if item["name"] == user["base_group"]),
                1001,
            )

            # Now we know it is a new user...
            new_user = self._otcs.addUser(
                name=user_name,
                password=user["password"],
                # be careful - can be empty
                first_name=user.get("firstname", ""),
                # be careful - can be empty
                last_name=user.get("lastname", ""),
                email=user.get("email", ""),  # be careful - can be empty
                base_group=base_group,
                privileges=user.get("privileges", ["Login", "Public Access"]),
            )

            # Process group memberships of new user:
            if new_user is not None:
                logger.info(
                    "New user -> {} with ID -> {} has been created".format(
                        user_name, new_user["id"]
                    )
                )
                user["id"] = new_user["id"]
                group_names = user["groups"]
                for group_name in group_names:
                    # Find the group dictionary item to the parent group name:
                    group = next(
                        (item for item in self._groups if item["name"]
                         == group_name), None
                    )
                    if group is None:
                        # if group is not in payload try to find group in OTCS
                        # in case it is a pre-existing group:
                        group = self._otcs.getGroup(group_name)
                        if group is None:
                            logger.error(
                                "Group -> {} not found. Skipping...".format(
                                    group_name)
                            )
                            continue
                        group = group["data"][0]

                    if group["id"] is None:
                        logger.error(
                            "Group -> {} does not have an ID. Skipping...".format(
                                group["name"]
                            )
                        )
                        continue

                    logger.info(
                        "Add user -> {} ({}) to group -> {} ({})".format(
                            user["name"], user["id"], group["name"], group["id"]
                        )
                    )
                    self._otcs.addGroupMember(user["id"], group["id"])
                # for some unclear reason the user is not added to its base group in OTDS
                # so we do this explicitly:
                self._otds.addUserToGroup(
                    user["name"], user["base_group"])

                # Extra OTDS attributes for the user can be provided in "extra_attributes"
                # as part of the user payload.
                if "extra_attributes" in user:
                    extra_attributes = user["extra_attributes"]
                    for extra_attribute in extra_attributes:
                        attribute_name = extra_attribute.get("name")
                        attribute_value = extra_attribute.get("value")
                        if not attribute_name or not attribute_value:
                            logger.error(
                                "User attribute is missing a name or value. Skipping..."
                            )
                            continue
                        logger.info(
                            "Set user attribute -> {} to -> {}".format(
                                attribute_name, attribute_value
                            )
                        )
                        user_partition = self._otcs.config()[
                            "partition"]
                        if not user_partition:
                            logger.error(
                                "User partition not found!"
                            )
                        self._otds.updateUser(
                            user_partition,
                            user["name"],
                            attribute_name,
                            attribute_value,
                        )

        # end method definition

    def processUsersM365(self):
        """Process users in payload and create them in Microsoft 365 via MS Graph API.

        Args: None
        Return: None
        """

        # Add all users in payload and establish membership in
        # specified groups:
        for user in self._users:

            # Sanity checks:
            if not "name" in user:
                logger.error(
                    "User is missing a login - skipping to next user...")
                continue
            user_name = user["name"]

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in user and not user["enabled"]:
                logger.info(
                    "Payload for User -> {} is disabled. Skipping...".format(
                        user_name)
                )
                continue
            if not "enable_o365" in user or not user["enable_o365"]:
                logger.info(
                    "Office 365 is not enabled in payload for User -> {}. Skipping...".format(
                        user_name)
                )
                continue

            # Sanity checks:
            if not "password" in user:
                logger.error(
                    "User -> {} is missing a password - skipping to next user...".format(
                        user_name
                    )
                )
                continue
            user_password = user["password"]
            # be careful with the following fields - they could be empty
            user_department = user.get("base_group", "")
            user_first_name = user.get("firstname", "")
            user_last_name = user.get("lastname", "")

            # Check if the user does already exist (e.g. if job is restarted)
            # As this is a pattern search it could return multiple users:
            user_name = user_name + "@" + self._m365.config()["domain"]
            existing_user = self._m365.getUser(user_name)
            if existing_user:
                logger.info(
                    "Found existing Azure AD user -> {} ({}) with ID -> {}".format(
                        existing_user["displayName"], existing_user["userPrincipalName"], existing_user["id"]
                    )
                )
                user["m365_id"] = existing_user["id"]
            else:
                logger.info(
                    "Did not find existing user - creating a new Azure AD user...")

                # Now we know it is a new user...
                new_user = self._m365.addUser(email=user_name,
                                              password=user_password,
                                              first_name=user_first_name,
                                              last_name=user_last_name,
                                              location="US",
                                              department=user_department)
                if new_user is not None:
                    # Store the Microsoft 365 user ID in payload:
                    user["m365_id"] = new_user["id"]
                    logger.info(
                        "New Azure AD user -> {} with ID -> {} has been created".format(
                            user_name, user["m365_id"]
                        )
                    )
                else:
                    logger.error(
                        "Failed to create new Azure AD user -> {}".format(user_name))
                    continue

            # Now we assign a license to the new Azure AD user:
            sku_id = self._m365.config()["skuId"]
            if sku_id and not "m365_sku" in user:
                response = self._m365.assignLicenseToUser(
                    user["m365_id"], sku_id)
                if not response:
                    logger.error(
                        "Failed to assign license -> {} to Azure AD user -> {}".format(sku_id, user_name))
                else:
                    user["m365_sku"] = sku_id
                    logger.info(
                        "License -> {} has been assigned to Azure AD user -> {}".format(sku_id, user_name))

            # Process Microsoft 365 group memberships of new user:
            if "m365_id" in user:
                user_id = user["m365_id"]
                # don't forget the base group (department) !
                group_names = user["groups"]
                if user_department:
                    group_names.append(user_department)
                logger.info(
                    "User -> {} has these groups in payload -> {} (including base group -> {}). Checking if they are Azure AD Groups...".format(user_name, group_names, user_department))
                for group_name in group_names:

                    # Find the group dictionary item to the parent group name:
                    group = next(
                        (item for item in self._groups if item["name"]
                         == group_name), None
                    )
                    if group is None or not "enable_o365" in group or not group["enable_o365"]:
                        # if group is not in payload then this membership
                        # is not relevant for Microsoft 365.
                        # If Office 365 is not enabled for this group in
                        # the payload we can also skip:
                        logger.info(
                            "Payload Group -> {} is not enabled for M365. Skipping...".format(
                                group_name)
                        )
                    else:
                        response = self._m365.getGroup(group_name)
                        if response is None or not "value" in response or not response["value"]:
                            logger.error(
                                "Azure AD Group -> {} not found. Skipping...".format(
                                    group_name)
                            )
                        else:
                            group_id = response["value"][0]["id"]

                            # Check if user is already a member. We don't want
                            # to throw an error if the user is not found as a member:
                            if self._m365.isMember(group_id, user_id, show_error=False):
                                logger.info(
                                    "Azure AD user -> {} ({}) is already in Azure AD group -> {} ({})".format(
                                        user["name"], user_id, group_name, group_id
                                    ))
                            else:
                                logger.info(
                                    "Add Azure AD user -> {} ({}) to Azure AD group -> {} ({})".format(
                                        user["name"], user_id, group_name, group_id
                                    )
                                )
                                self._m365.addGroupMember(group_id, user_id)
                                # As each group should have at least one owner in M365
                                # we set all users also as owners for now. Later we
                                # may want to configure this via payload:
                                logger.info(
                                    "Make Azure AD user -> {} ({}) owner of Azure AD group -> {} ({})".format(
                                        user["name"], user_id, group_name, group_id
                                    )
                                )
                                self._m365.addGroupOwner(group_id, user_id)

                    # As M365 groups are flat (not nested) we also add the
                    # user as member to the parent groups of the current group:
                    parent_group_names = group.get("parent_groups")
                    logger.info("Group -> {} has the following parent groups -> {}".format(group_name, parent_group_names))
                    for parent_group_name in parent_group_names:
                        # Find the group dictionary item to the parent group name:
                        parent_group = next(
                            (item for item in self._groups if item["name"]
                             == parent_group_name), None
                        )
                        if parent_group is None or not "enable_o365" in parent_group or not parent_group["enable_o365"]:
                            # if parent group is not in payload then this membership
                            # is not relevant for Microsoft 365.
                            # If Office 365 is not enabled for this parent group in
                            # the payload we can also skip:
                            logger.info(
                                "Parent Group -> {} is not enabled for M365. Skipping...".format(
                                    group_name)
                            )
                            continue

                        response = self._m365.getGroup(parent_group_name)
                        if response is None or not "value" in response or not response["value"]:
                            logger.error(
                                "Azure AD Group -> {} not found. Skipping...".format(
                                    group_name)
                            )
                            continue
                        parent_group_id = response["value"][0]["id"]

                        # Check if user is already a member. We don't want
                        # to throw an error if the user is not found as a member:
                        if self._m365.isMember(parent_group_id, user_id, show_error=False):
                            logger.info(
                                "Azure AD user -> {} ({}) is already in Azure AD group -> {} ({})".format(
                                    user["name"], user_id, parent_group_name, parent_group_id
                                ))
                            continue

                        logger.info(
                            "Add Azure AD user -> {} ({}) to Azure AD group -> {} ({})".format(
                                user["name"], user_id, parent_group_name, parent_group_id
                            )
                        )
                        self._m365.addGroupMember(parent_group_id, user_id)

        # end method definition

    def processTeamsM365(self):
        """Process groups in payload and create matching Teams in Microsoft 365.
           We need to do this after the creation of the M365 users as wie require
           Group Owners to create teams.

        Args: None
        Return: None
        """

        for group in self._groups:

            if not "name" in group:
                logger.error("Team needs a name. Skipping...")
                continue
            group_name = group["name"]

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in group and not group["enabled"]:
                logger.info(
                    "Payload for Group -> {} is disabled. Skipping...".format(
                        group_name)
                )
                continue
            if not "enable_o365" in group or not group["enable_o365"]:
                logger.info(
                    "Office 365 is not enabled in payload for Group -> {}. Skipping...".format(
                        group_name)
                )
                continue

            # Check if the M365 group does not exist (this should actually never happen at this point)
            if not "m365_id" in group:
                # The "m365_id" value is set by the method processGroupsM365()
                logger.error(
                    "No M365 Group exist for group -> {} (M365 Group creation may have failed). Skipping...".format(
                        group_name)
                )
                continue

            if not self._m365.hasTeam(group_name):
                logger.info(
                    "Create M365 Team -> {} or existing M365 Group -> {}...".format(group_name, group_name))
                # Now "upgrading" this group to a MS Team:
                new_team = self._m365.addTeam(group_name)
            else:
                logger.info(
                    "M365 group -> {} already has an MS Team connected. Skipping...".format(group_name))

        # end method definition

    def processAdminSettings(self, admin_settings: list) -> bool:
        """Process admin settings in payload and import them to Extended ECM.

        Args:
            admin_settings (list): list of admin settings. We need this parameter
                                   as we process two different lists.
        Return:
            True if a restart of the OTCS pods is required. False otherwise.
        """

        restart_required = False

        for admin_setting in admin_settings:

            # Sanity checks:
            if not "filename" in admin_setting:
                logger.error(
                    "Filename is missing - skipping to next admin setting...")
                continue
            filename = admin_setting["filename"]

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in admin_setting and not admin_setting["enabled"]:
                logger.info(
                    "Payload for setting file -> {} is disabled. Skipping...".format(
                        filename)
                )
                continue

            settings_file = self._custom_settings_dir + filename
            if os.path.exists(settings_file):

                description = admin_setting.get("description")
                if description:
                    logger.info(description)

                # Read the config file:
                with open(settings_file, "r") as file:
                    file_content = file.read()

                logger.debug(
                    "Replace Placeholder -> {} in file -> {}".format(
                        self._placeholder_values, file_content
                    )
                )

                file_content = self.replacePlaceholders(
                    file_content)

                # Write the updated config file:
                tmpfile = "/tmp/" + os.path.basename(settings_file)
                with open(tmpfile, "w") as file:
                    file.write(file_content)

                response = self._otcs.applyConfig(tmpfile)
                if response and response["results"]["data"]["restart"]:
                    logger.info(
                        "A restart of Extended ECM service is required.")
                    restart_required = True
            else:
                logger.error(
                    "Admin settings file -> {} not found.".format(settings_file))

        return restart_required

        # end method definition

    def processExternalSystems(self):
        """Process external systems in payload and create them in Extended ECM.

        Args: None
        Return: None
        Side Effects:
            - based on system_type different other settings in the dict are set
            - reachability is tested and a flag is set in the dict are set
        """

        for external_system in self._external_systems:
            #
            # 1: Do sanity checks for the payload:
            #
            if not "external_system_name" in external_system:
                logger.error(
                    "External System connection needs a logical system name! Skipping to next external system..."
                )
                continue
            system_name = external_system["external_system_name"]

            if not "external_system_type" in external_system:
                logger.error(
                    "External System connection -> {} needs a type (SAP, Salesfoce, SuccessFactors, AppWorks Platform)! Skipping to next external system...".format(
                        system_name
                    )
                )
                continue
            system_type = external_system["external_system_type"]

            if "enabled" in external_system and not external_system["enabled"]:
                logger.info(
                    "Payload for External System -> {} ({}) is disabled. Skipping...".format(
                        system_name, system_type
                    )
                )
                continue

            description = (
                external_system["description"] if external_system.get(
                    "description") else ""
            )

            # Set the default settings for the different system types:
            match system_type:
                # Check if we have a SuccessFactors system:
                case "SuccessFactors":
                    connection_type = "SFInstance"
                    auth_method = "OAUTH"
                    provider_name = system_type
                    username = None
                    password = None
                case "SAP":
                    connection_type = "HTTP"
                    auth_method = "BASIC"
                    provider_name = ""
                    oauth_client_id = None
                    oauth_client_secret = None
                case "Salesforce":
                    connection_type = "SF"
                    auth_method = "OAUTH"
                    provider_name = system_type
                    username = None
                    password = None
                case "AppWorks Platform":
                    connection_type = "HTTP"
                    auth_method = "BASIC"
                    provider_name = ""
                    oauth_client_id = None
                    oauth_client_secret = None

            if not "base_url" in external_system:
                base_url = ""  # baseUrl is optional
            else:
                base_url = external_system["base_url"]

            if not "as_url" in external_system:
                logger.warning(
                    "External System connection -> {} needs an Application Server URL! Skipping to next external system...".format(
                        system_name
                    )
                )
                continue
            as_url = external_system["as_url"]

            # Extract the hostname:
            external_system_hostname = urlparse(as_url).hostname
            # Write this information back into the data structure:
            external_system["external_system_hostname"] = external_system_hostname
            # Extract the port:
            external_system_port = urlparse(
                as_url).port if urlparse(as_url).port else 80
            # Write this information back into the data structure:
            external_system["external_system_port"] = external_system_port

            if self._http_object.checkHostReachable(external_system_hostname, external_system_port):
                logger.info(
                    "Mark external system -> {} as reachable for later workspace creation...".format(
                        system_name
                    )
                )
                external_system["reachable"] = True
            else:
                external_system["reachable"] = False

            # Read either username/password (BASIC) or client ID / secret (OAuth)
            match auth_method:
                case "BASIC":
                    if not "username" in external_system:
                        logger.warning(
                            "External System connection -> {} needs a user name for BASIC authentication! Skipping to next external system...".format(
                                system_name
                            )
                        )
                        continue
                    if not "password" in external_system:
                        logger.warning(
                            "External System connection -> {} needs a password for BASIC authentication! Skipping to next external system...".format(
                                system_name
                            )
                        )
                        continue
                    username = external_system["username"]
                    password = external_system["password"]
                case "OAUTH":
                    if not "oauth_client_id" in external_system:
                        logger.error(
                            "External System connection -> {} is missing OAuth client ID! Skipping to next external system...".format(
                                system_name
                            )
                        )
                        continue
                    if not "oauth_client_secret" in external_system:
                        logger.error(
                            "External System connection -> {} is missing OAuth client secret! Skipping to next external system...".format(
                                system_name
                            )
                        )
                        continue
                    oauth_client_id = external_system["oauth_client_id"]
                    oauth_client_secret = external_system["oauth_client_secret"]
                    # For backward compatibility we also read username/password
                    # with OAuth settings:
                    username = (
                        external_system["username"]
                        if external_system.get("username")
                        else None
                    )
                    password = (
                        external_system["password"]
                        if external_system.get("password")
                        else None
                    )

            # We do this existance test late in this function to make sure the payload
            # datastructure is properly updated for debugging purposes.
            logger.info(
                "Test if external system -> {} does already exist...".format(
                    system_name)
            )
            if self._otcs.getExternalSystemConnection(system_name):
                logger.info(
                    "External System connection -> {} already exists! Skipping to next external system...".format(
                        system_name
                    )
                )
                continue

            #
            # 2: Create External System:
            #
            logger.info(
                "Create external system -> {}; type -> {}".format(
                    system_name, connection_type
                )
            )
            response = self._otcs.addExternalSystemConnection(
                system_name,
                connection_type,
                as_url,
                base_url,
                username,
                password,
                auth_method,
                oauth_client_id,
                oauth_client_secret,
            )
            if response == None:
                logger.error(
                    "Failed to create external system -> {}; type -> {}".format(
                        system_name, connection_type
                    )
                )
            else:
                logger.info(
                    "Successfully created external system -> {}".format(
                        system_name)
                )

            #
            # 3: Create Authentication Handler for external system:
            #

            match system_type:
                case "SuccessFactors":
                    # Configure a SAML authentication handler:
                    if not "saml_url" in external_system:
                        logger.error(
                            "SuccessFactors system -> {} ({}) is missing the SAML URL!".format(
                                system_name,
                                connection_type,
                            )
                        )
                        continue
                    saml_url = external_system["saml_url"]
                    if not "otds_sp_endpoint" in external_system:
                        logger.error(
                            "SuccessFactors system -> {} ({}) is missing the OTDS endpoint!".format(
                                system_name,
                                connection_type,
                            )
                        )
                        continue
                    otds_sp_endpoint = external_system["otds_sp_endpoint"]

                    response = self._otds.addAuthHandlerSAML(
                        name=system_name,
                        description=description,
                        provider_name=provider_name,
                        saml_url=saml_url,
                        otds_url=otds_sp_endpoint,
                    )
                    if response:
                        logger.info(
                            "Successfully added SAML authentication handler.")
                    else:
                        logger.error(
                            "Failed to add SAML authentication handler.")
                case "SAP":
                    # Configure a certificate-based SAP authentication handler:
                    if not "certificate_file" in external_system:
                        logger.error(
                            "External system -> {}; type -> {}; has a certificate file -> {} but it is missing the certificate password!".format(
                                system_name,
                                system_type,
                                external_system["certificate_file"],
                            )
                        )
                        continue
                    if not "certificate_password" in external_system:
                        logger.error(
                            "External system -> {}; type -> {}; has a certificate file -> {} but it is missing the certificate password!".format(
                                system_name,
                                connection_type,
                                external_system["certificate_file"],
                            )
                        )
                        continue
                    certificate_file = external_system["certificate_file"]
                    certificate_password = external_system["certificate_password"]
                    certificate_description = external_system["description"]
                    response = self._otds.addAuthHandlerSAP(
                        name=system_name,
                        description=certificate_description,
                        certificate_file=certificate_file,
                        certificate_password=certificate_password,
                    )
                    if response:
                        logger.info(
                            "Successfully added SAP authentication handler.")
                    else:
                        logger.error(
                            "Failed to add SAP authentication handler.")
                case "Salesforce":
                    # Configure an OAuth-based authentication handler:
                    if not "authorization_endpoint" in external_system:
                        logger.error(
                            "Salesforce system -> {} ({}) is missing the authorization endpoint!".format(
                                system_name,
                                connection_type,
                            )
                        )
                        continue
                    authorization_endpoint = external_system["authorization_endpoint"]
                    if not "token_endpoint" in external_system:
                        logger.error(
                            "Salesforce system -> {} ({}) is missing the token endpoint!".format(
                                system_name,
                                connection_type,
                            )
                        )
                        continue
                    token_endpoint = external_system["token_endpoint"]
                    response = self._otds.addAuthHandlerOAuth(
                        name=system_name,
                        description=description,
                        provider_name=provider_name,
                        client_id=oauth_client_id,
                        client_secret=oauth_client_secret,
                        active_by_default=False,
                        authorization_endpoint=authorization_endpoint,
                        token_endpoint=token_endpoint,
                        scope_string="id",
                    )
                    if response:
                        logger.info(
                            "Successfully added OAuth authentication handler.")
                    else:
                        logger.error(
                            "Failed to add OAuth authentication handler.")

        # end method definition

    def processTransportPackages(self, transport_packages: list):
        """Process transport packages in payload and import them to Extended ECM.

        Args:
            transport_packages (list): list of transport packages. As we
                                       have two different lists (transport and
                                       content_transport) we need a parameter
        Return: None
        """

        for transport_package in transport_packages:
            if not "name" in transport_package:
                logger.error(
                    "Transport Package needs a name! Skipping to next transport..."
                )
                continue
            name = transport_package["name"]

            if "enabled" in transport_package and not transport_package["enabled"]:
                logger.info(
                    "Payload for Transport Package -> {} is disabled. Skipping...".format(
                        name
                    )
                )
                continue

            if not "url" in transport_package:
                logger.error(
                    "Transport Package -> {} needs a URL! Skipping to next transport...".format(
                        name
                    )
                )
                continue
            if not "description" in transport_package:
                logger.warning(
                    "Transport Package -> {} is missing a description".format(
                        name)
                )
            url = transport_package["url"]
            description = transport_package["description"]

            # For some transports there can be string replacements
            # configured:
            if "replacements" in transport_package:
                replacements = transport_package["replacements"]
                logger.info(
                    "Deploy transport -> {} with replacements -> {}; URL -> {}".format(description, url, replacements))
                response = self._otcs.deployTransport(url, name, description, replacements)
            else:            
                logger.info(
                    "Deploy transport -> {}; URL -> {}".format(description, url))
                response = self._otcs.deployTransport(url, name, description)
            if response == None:
                logger.error(
                    "Failed to deploy transport -> {}; URL -> {}".format(
                        name, url)
                )
                if self._stop_on_error:
                    return
            else:
                logger.info(
                    "Successfully deployed transport -> {}".format(name))

        # end method definition

    def processUserPhotos(self):
        """Process user photos in payload and assign them to Extended ECM users.

        Args: None
        Return: None
        """

        # we assume the nickname of the photo item equals the login name of the user
        # we also assume that the photos have been uploaded / transported into the target system
        for user in self._users:
            user_name = user["name"]
            if not "id" in user:
                logger.error(
                    "User -> {} does not have an ID. The user creation may have failed before. Skipping...".format(
                        user_name
                    )
                )
                continue
            user_id = user["id"]

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in user and not user["enabled"]:
                logger.info(
                    "Payload for User -> {} is disabled. Skipping...".format(
                        user_name)
                )
                continue

            response = self._otcs.getNodeFromNickname(user_name)
            if response == None:
                logger.warning(
                    "Missing photo for user -> {} - nickname not found. Skipping...".format(
                        user_name
                    )
                )
                continue
            photo_id = self._otcs.getResultValue(response, "id")
            response = self._otcs.updateUserPhoto(user_id, photo_id)
            if response == None:
                logger.warning(
                    "Failed to add photo for user -> {}".format(user_name))
            else:
                logger.info(
                    "Successfully added photo for user -> {}".format(user_name))

        # Check if Admin has a photo as well (nickname needs to be "admin"):
        response = self._otcs.getNodeFromNickname("admin")
        if response == None:
            logger.warning(
                "Missing photo for admin - nickname not found. Skipping...")
            return
        photo_id = self._otcs.getResultValue(response, "id")
        response = self._otcs.updateUserPhoto(1000, photo_id)
        if response == None:
            logger.warning(
                "Failed to add photo for admin")
        else:
            logger.info(
                "Successfully added photo for admin")

        # end method definition

    def processUserPhotosM365(self):
        """Process user photos in payload and assign them to Azure AD users.

        Args: None
        Return: None
        """

        # we assume the nickname of the photo item equals the login name of the user
        # we also assume that the photos have been uploaded / transported into the target system
        for user in self._users:
            user_name = user["name"]
            if not "id" in user:
                logger.error(
                    "User -> {} does not have an ID. The user creation may have failed before. Skipping...".format(
                        user_name
                    )
                )
                continue
            user_id = user["id"]

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in user and not user["enabled"]:
                logger.info(
                    "Payload for User -> {} is disabled. Skipping...".format(
                        user_name)
                )
                continue
            if not "enable_o365" in user or not user["enable_o365"]:
                logger.info(
                    "Office 365 is not enabled in payload for User -> {}. Skipping...".format(
                        user_name)
                )
                continue
            if not "m365_id" in user:
                logger.error(
                    "Office 365 user -> {} has not been created. Skipping...".format(
                        user_name)
                )
                continue

            user_m365_id = user["m365_id"]

            response = self._otcs.getNodeFromNickname(user_name)
            if response == None:
                logger.warning(
                    "Missing photo for user -> {} - nickname not found. Skipping...".format(
                        user_name
                    )
                )
                continue
            photo_id = self._otcs.getResultValue(response, "id")
            photo_name = self._otcs.getResultValue(response, "name")
            photo_path = "/tmp/" + photo_name
            response = self._otcs.downloadDocument(photo_id, photo_path)
            if response == None:
                logger.warning(
                    "Failed to download photo for user -> {} from Extended ECM".format(user_name))
            else:
                logger.info(
                    "Successfully downloaded photo for user -> {} from Extended ECM to file -> {}".format(user_name, photo_path))

            # Upload photo to M365:
            response = self._m365.updateUserPhoto(user_m365_id, photo_path)
            if response == None:
                logger.error(
                    "Failed to upload photo for user -> {} to Microsoft 365".format(user_name))
            else:
                logger.info(
                    "Successfully uploaded photo for user -> {} to Microsoft 365".format(user_name))

        # end method definition

    def processWorkspaceTypes(self):
        """Create a data structure for all workspace types in the Extended ECM system.

        Args: None
        Return: list of workspace types. Each list element is a dict with these values:
                - id (string)
                - name (string)
                - templates (list)
                    + name
                    + id
        """

        # get all workspace types (these have been created by the transports and are not in the payload!):
        response = self._otcs.getWorkspaceTypes()
        if response == None:
            logger.error("No workspace types found!")
            self._workspace_types = []
        else:
            self._workspace_types = response["results"]

        # now we enrich the workspace_type list elments (which are dicts)
        # with additional dict elements for further processing:
        for workspace_type in self._workspace_types:
            workspace_type_id = workspace_type["data"]["properties"]["wksp_type_id"]
            logger.info("Workspace Types ID -> {}".format(workspace_type_id))
            workspace_type["id"] = workspace_type_id
            workspace_type_name = workspace_type["data"]["properties"]["wksp_type_name"]
            logger.info(
                "Workspace Types Name -> {}".format(workspace_type_name))
            workspace_type["name"] = workspace_type_name
            workspace_templates = workspace_type["data"]["properties"]["templates"]
            # Create empty lists of dicts with template names and node IDs:
            workspace_type["templates"] = []
            if workspace_templates:
                # Determine available templates per workspace type (there can be multiple!)
                for workspace_template in workspace_templates:
                    workspace_template_id = workspace_template["id"]
                    workspace_template_name = workspace_template["name"]
                    logger.info(
                        "Found template with name -> {} and ID -> {}".format(
                            workspace_template_name, workspace_template_id
                        )
                    )
                    template = {
                        "name": workspace_template_name,
                        "id": workspace_template_id,
                    }
                    workspace_type["templates"].append(template)

                    # Workaround for problem with workspace role inheritance
                    # which may be related to Transport or REST API: to work-around this we
                    # push down the workspace roles to the workspace folders explicitly:
                    response = self._otcs.getWorkspaceRoles(
                        workspace_template_id)

                    for roles in response["results"]:
                        role_name = roles["data"]["properties"]["name"]
                        role_id = roles["data"]["properties"]["id"]
                        permissions = roles["data"]["properties"]["perms"]
                        # as getWorkspaceRoles() delivers permissions as a value (bit encoded)
                        # we need to convert it to a permissions string list:
                        permission_string_list = (
                            self._otcs.convertPermissionValueToPermissionString(
                                permissions)
                        )

                        logger.info(
                            "Inherit permissions of workspace template -> {} and role -> {} to workspace folders...".format(
                                workspace_template_name, role_name
                            )
                        )

                        # Inherit permissions to folders of workspace template:
                        response = self._otcs.assignWorkspacePermissions(
                            workspace_template_id,
                            role_id,
                            permission_string_list,
                            1,  # Only sub items - workspace node itself is OK
                        )

            else:
                logger.warning(
                    "Workspace Types Name -> {} has no templates!".format(
                        workspace_type_name
                    )
                )
                continue

        return self._workspace_types

        # end method definition

    def processWorkspaceTemplateRegistrations(self):
        """Process workspace template registrations for Extended ECM for Engineering.
        This has been a work-around for a transport issue in 22.4. This code is not required
        for 23.1 or newer. Right now we just disabled the payload. We may consider to remove
        the code in future versions.

        Args: None
        Return: None
        """

        # loop through the workspace template registrations in the payload:
        for workspace_template_registration in self._workspace_template_registrations:
            # Do some sanity checks first and read the workspace type name
            # and workspace template name from the payload:
            if not "workspace_type_name" in workspace_template_registration:
                logger.error(
                    "Workspace template registration needs a workspace type name! Skipping to next workspace template registration..."
                )
                continue
            type_name = workspace_template_registration["workspace_type_name"]

            if (
                "enabled" in workspace_template_registration
                and not workspace_template_registration["enabled"]
            ):
                logger.info(
                    "Payload for Workspace Template Registration for Workspace Type -> {} is disabled. Skipping...".format(
                        type_name
                    )
                )
                continue

            if not "workspace_template_name" in workspace_template_registration:
                logger.error(
                    "Workspace template registration needs a workspace template name! Skipping to next workspace template registration..."
                )
                continue
            template_name = workspace_template_registration["workspace_template_name"]

            # now we have the template type name and the template name from the
            # payload. We can now proceed to find these items in the workspace types
            # data structure. First we lookup the workspace type:
            workspace_type = next(
                (item for item in self._workspace_types if item["name"]
                 == type_name), None
            )
            if workspace_type is None:
                logger.error(
                    "Workspace Type with name -> {} not found.".format(type_name))
                continue

            # now we use the template list in the workspace type datastructure
            # to find the workspace template:
            workspace_template_list = workspace_type["templates"]
            if workspace_template_list is []:
                logger.error(
                    "Workspace Type with name -> {} has no templates.".format(
                        type_name)
                )
                continue

            workspace_template = next(
                (item for item in workspace_template_list if item["name"] == template_name),
                None,
            )
            if workspace_template is None:
                logger.error(
                    "Workspace Type with name -> {} has no Template with name -> {}.".format(
                        type_name, template_name
                    )
                )
                continue
            workspace_template_id = workspace_template["id"]

            logger.info(
                "Register workspace template -> {} ({}) with workspace type -> {}".format(
                    template_name, workspace_template_id, type_name
                )
            )

            response = self._otcs.registerWorkspaceTemplate(
                workspace_template_id)
            if response == None:
                logger.error(
                    "Failed to register workspace template -> {} with workspace type -> {}".format(
                        template_name, type_name
                    )
                )
                continue

        # end method definition

    def processWorkspaces(self):
        """Process workspaces in payload and create them in Extended ECM.

        Args: None
        Return: None 
        Side Effects:
            Set workspace["nodeId] to the node ID of the created workspace
        """

        for workspace in self._workspaces:
            # Read name from payload:
            if not "name" in workspace:
                logger.error(
                    "Workspace needs a name! Skipping to next workspace...")
                continue
            name = workspace["name"]

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in workspace and not workspace["enabled"]:
                logger.info(
                    "Payload for Workspace -> {} is disabled. Skipping...".format(
                        name)
                )
                continue

            # Read Type Name from payload:
            if not "type_name" in workspace:
                logger.error(
                    "Workspace -> {} needs a type name! Skipping to next workspace...".format(
                        name
                    )
                )
                continue
            type_name = workspace["type_name"]

            # check if the workspace has been created before (effort to make the customizing code idem-potent)
            logger.info(
                "Check if workspace -> {} of type -> {} does already exist...".format(
                    name, type_name
                )
            )
            response = self._otcs.getWorkspaceByNameAndType(
                name, type_name)
            logger.debug(
                "Search for existing workspace delivered -> {}".format(response))
            workspace_id = self._otcs.getResultValue(response, "id")
            if workspace_id:
                # we still want to set the nodeId as other parts of the payload depend on it:
                workspace["nodeId"] = workspace_id
                logger.info(
                    "Workspace -> {} of type -> {} does already exist and has ID -> {}! Skipping to next workspace...".format(
                        name, type_name, workspace_id
                    )
                )
                continue

            logger.info(
                "Creating new Workspace -> {}; Workspace Type -> {}...".format(
                    name, type_name
                )
            )

            # Read optional description from payload:
            if not "description" in workspace:
                description = ""
            else:
                description = workspace["description"]

            # Parent ID is optional and only required if workspace type does not specify a create location.
            # This is typically the case if it is a nested workspace or workspaces of the same type can be created
            # in different locations in the Enterprise Workspace:
            parent_id = workspace["parent_id"] if workspace.get(
                "parent_id") else None

            if parent_id is not None:
                parent_workspace = next(
                    (item for item in self._workspaces if item["id"]
                     == parent_id), None
                )
                if parent_workspace is None:
                    logger.error(
                        "Parent Workspace with logical ID -> {} not found.".format(
                            parent_id
                        )
                    )
                    continue

                if not "nodeId" in parent_workspace:
                    logger.warning(
                        "Parent Workspace without node ID (parent workspace creation may have failed) - skipping to next workspace..."
                    )
                    continue
                # now determine the actual node IDs of the parent workspace (should have been created before):
                parent_workspace_node_id = parent_workspace["nodeId"]
                logger.info(
                    "Parent Workspace with logical ID -> {} has node ID -> {}".format(
                        parent_id, parent_workspace_node_id
                    )
                )
            else:
                # if no parent_id is specified the workspace location is determined by the workspace type definition
                # and we pass None as parent ID to the getWorkspaceCreateForm and createWorkspace methods below:
                parent_workspace_node_id = None

            # Find the workspace type with the name given in the payload:
            workspace_type = next(
                (item for item in self._workspace_types if item["name"]
                 == type_name), None
            )
            if workspace_type is None:
                logger.error(
                    "Workspace Type -> {} not found. Skipping to next workspace.".format(
                        type_name
                    )
                )
                continue
            elif workspace_type["templates"] == []:
                logger.error(
                    "Workspace Type -> {} does not have templates. Skipping to next workspace.".format(
                        type_name
                    )
                )
                continue

            # check if the template to be used is specified in the payload:
            if "template_name" in workspace:
                template_name = workspace["template_name"]
                workspace_template = next(
                    (
                        item
                        for item in workspace_type["templates"]
                        if item["name"] == template_name
                    ),
                    None,
                )
                if workspace_template:  # does this template exist?
                    logger.info(
                        "Workspace Template -> {} has been specified in payload and it does exist.".format(
                            template_name
                        )
                    )
                else:
                    logger.error(
                        "Workspace Template -> {} has been specified in payload but it doesn't exist!".format(
                            template_name
                        )
                    )
                    logger.error(
                        "Workspace Type -> {} has only these templates -> {}".format(
                            type_name, workspace_type["templates"]
                        )
                    )
                    continue
            # template to be used is NOT specified in the payload - then we just take the first one:
            else:
                workspace_template = workspace_type["templates"][0]
                logger.info(
                    "Workspace Template has not been specified in payload - we just take the first one".format(
                        workspace_template
                    )
                )

            template_id = workspace_template["id"]
            template_name = workspace_template["name"]
            workspace_type_id = workspace_type["id"]

            logger.info(
                "Create Workspace -> {} (type -> {}) from workspace template -> {} (ID -> {})".format(
                    name, type_name, template_name, template_id
                )
            )

            # Read business object data from workspace payload:
            ext_system_id = None
            bo_type = None
            bo_id = None
            # Check if business objects are in workspace payload and list is not empty:
            if "business_objects" in workspace and workspace["business_objects"]:
                # Currently we can only process one business object (workspaces connected to multiple leading systems are not support yet)
                business_object_data = workspace["business_objects"][0]
                # business_object_data is a dict with 3 elements:
                if "external_system" in business_object_data:
                    ext_system_id = business_object_data["external_system"]
                if "bo_type" in business_object_data:
                    bo_type = business_object_data["bo_type"]
                if "bo_id" in business_object_data:
                    bo_id = business_object_data["bo_id"]
                logger.info(
                    "Workspace -> {} has business object information -> ({}, {}, {})".format(
                        name, ext_system_id, bo_type, bo_id
                    )
                )

                # Check if external system has been declared in payload:
                external_system = next(
                    (
                        item
                        for item in self._external_systems
                        if (item["external_system_name"] == ext_system_id)
                    ),
                    None,
                )
                if not external_system:
                    logger.warning(
                        "External System -> {} does not exist. Cannot connect workspace -> {} to -> {}. Create workspace without connection.".format(
                            ext_system_id, name, ext_system_id
                        )
                    )
                    # we remove the Business Object information to avoid communication
                    # errors during workspace create form and workspace creation
                    ext_system_id = None
                    bo_type = None
                    bo_id = None
                elif not external_system.get("reachable"):
                    logger.warning(
                        "External System -> {} is not reachable. Cannot connect workspace -> {} to -> {}. Create workspace without connection.".format(
                            ext_system_id, name, ext_system_id
                        )
                    )
                    # we remove the Business Object information to avoid communication
                    # errors during workspace create form and workspace creation
                    ext_system_id = None
                    bo_type = None
                    bo_id = None
                else:
                    logger.info(
                        "Workspace -> {} will be connected with external system -> {} ({}, {})".format(
                            name, ext_system_id, bo_type, bo_id
                        )
                    )

            # Read categories from payload:
            if not "categories" in workspace:
                logger.info(
                    "Workspace payload has no category data! Will leave category attributes empty..."
                )
                category_create_data = {}
            else:
                categories = workspace["categories"]
                category_create_data = {"categories": {}}

                response = self._otcs.getWorkspaceCreateForm(
                    template_id, ext_system_id, bo_type, bo_id, parent_workspace_node_id
                )
                if response == None:
                    logger.error(
                        "Failed to retrieve create information for template -> {}".format(
                            template_id
                        )
                    )
                    continue
                else:
                    logger.info(
                        "Successfully retrieved create information for template -> {}".format(
                            template_id
                        )
                    )

                # Process category information
                forms = response["forms"]

                categories_form = None
                classification_form = None
                system_attributes_form = None

                # Typically the the create workspace form delivers 3 forms:
                # 1. Form for System Attributes (has no role name)
                # 2. Form for Category Data (role name = "categories")
                # 3. Form for Classifications (role name = "classifications")
                # First we extract these 3 forms:
                for form in forms:
                    if "role_name" in form and form["role_name"] == "categories":
                        categories_form = form
                        logger.debug(
                            "Found Categories form -> {}".format(form))
                        continue
                    if "role_name" in form and form["role_name"] == "classifications":
                        classifications_form = form
                        logger.debug(
                            "Found Classification form -> {}".format(form))
                        continue
                    # the remaining option is that this form is the system attributes form:
                    system_attributes_form = form
                    logger.debug(
                        "Found System Attributes form -> {}".format(form))

                # We are just interested in the single category data set (role_name = "categories"):
                data = categories_form["data"]
                logger.debug("Categories data found -> {}".format(data))
                schema = categories_form["schema"]["properties"]
                logger.debug("Categories schema found -> {}".format(schema))
                # parallel loop over category data and schema
                for cat_data, cat_schema in zip(data, schema):
                    logger.info("Category ID -> {}".format(cat_data))
                    data_attributes = data[cat_data]
                    logger.debug(
                        "Data Attributes -> {}".format(data_attributes))
                    schema_attributes = schema[cat_schema]["properties"]
                    logger.debug(
                        "Schema Attributes -> {}".format(schema_attributes))
                    cat_name = schema[cat_schema]["title"]
                    logger.info("Category name -> {}".format(cat_name))
                    # parallel loop over attribute data and schema
                    # Sets with one (fixed) row have type = object
                    # Multi-value Sets with (multiple) rows have type = array and "properties" in "items" schema
                    # Multi-value attributes have also type = array but NO "properties" in "items" schema
                    for attr_data, attr_schema in zip(data_attributes, schema_attributes):
                        logger.debug("Attribute ID -> {}".format(attr_data))
                        logger.debug(
                            "Attribute Data -> {}".format(
                                data_attributes[attr_data])
                        )
                        logger.debug(
                            "Attribute Schema -> {}".format(
                                schema_attributes[attr_schema])
                        )
                        attr_type = schema_attributes[attr_schema]["type"]
                        logger.debug("Attribute Type -> {}".format(attr_type))
                        if not "title" in schema_attributes[attr_schema]:
                            logger.debug("Attribute has no title - skipping")
                            continue
                        # Check if it is an multi-line set:
                        if attr_type == "array" and (
                            "properties" in schema_attributes[attr_schema]["items"]
                        ):
                            set_name = schema_attributes[attr_schema]["title"]
                            logger.info(
                                "Multi-line Set -> {}".format(set_name))
                            set_data_attributes = data_attributes[
                                attr_data
                            ]  # this is a list []
                            logger.debug(
                                "Set Data Attributes -> {}".format(
                                    set_data_attributes)
                            )
                            set_schema_attributes = schema_attributes[attr_schema]["items"][
                                "properties"
                            ]
                            logger.debug(
                                "Set Schema Attributes -> {}".format(
                                    set_schema_attributes)
                            )
                            set_schema_max_rows = schema_attributes[attr_schema]["items"][
                                "maxItems"
                            ]
                            logger.debug(
                                "Set Schema Max Rows -> {}".format(
                                    set_schema_max_rows)
                            )
                            set_data_max_rows = len(set_data_attributes)
                            logger.debug(
                                "Set Data Max Rows -> {}".format(
                                    set_data_max_rows)
                            )
                            row = 1
                            # it can happen that the payload contains more rows than the
                            # initial rows in the set data structure. In this case we use
                            # a copy of the data structure from row 0 as template...
                            first_row = dict(set_data_attributes[0])
                            # We don't know upfront how many rows of data we will find in payload
                            # but we at max process the maxItems specified in the schema:
                            while row <= set_schema_max_rows:
                                # Test if we have any payload for this row:
                                attribute = next(
                                    (
                                        item
                                        for item in categories
                                        if (
                                            item["name"] == cat_name
                                            and item["set"] == set_name
                                            and "row" in item
                                            and item["row"] == row
                                        )
                                    ),
                                    None,
                                )
                                # stop if there's no payload for the row:
                                if attribute is None:
                                    logger.info(
                                        "No payload found for set -> {}, row -> {}".format(
                                            set_name, row
                                        )
                                    )
                                    # we assume that if there's no payload for row n there will be no payload for rows > n
                                    # and break the while loop:
                                    break
                                # do we need to create a new row in the data set?
                                elif row > set_data_max_rows:
                                    # use the row we stored above to create a new empty row:
                                    logger.info(
                                        "Found payload for row -> {}, we need a new data row for it".format(
                                            row
                                        )
                                    )
                                    logger.info(
                                        "Adding an additional row -> {} to set data -> {}".format(
                                            row, set_name
                                        )
                                    )
                                    # add the empty dict to the list:
                                    set_data_attributes.append(dict(first_row))
                                    set_data_max_rows += 1
                                else:
                                    logger.info(
                                        "Found payload for row -> {} we can store in existing data row".format(
                                            row, set_name
                                        )
                                    )
                                # traverse all attributes in a single row:
                                for set_attr_schema in set_schema_attributes:
                                    logger.debug(
                                        "Set Attribute ID -> {} (row -> {})".format(
                                            set_attr_schema, row
                                        )
                                    )
                                    logger.debug(
                                        "Set Attribute Schema -> {} (row -> {})".format(
                                            set_schema_attributes[set_attr_schema], row
                                        )
                                    )
                                    set_attr_type = set_schema_attributes[set_attr_schema][
                                        "type"
                                    ]
                                    logger.debug(
                                        "Set Attribute Type -> {} (row -> {})".format(
                                            set_attr_type, row
                                        )
                                    )
                                    set_attr_name = set_schema_attributes[set_attr_schema][
                                        "title"
                                    ]
                                    logger.debug(
                                        "Set Attribute Name -> {} (row -> {})".format(
                                            set_attr_name, row
                                        )
                                    )
                                    # Lookup the attribute with the right category, set, attribute name, and row number in payload:
                                    attribute = next(
                                        (
                                            item
                                            for item in categories
                                            if (
                                                item["name"] == cat_name
                                                and item["set"] == set_name
                                                and item["attribute"] == set_attr_name
                                                and "row" in item
                                                and item["row"] == row
                                            )
                                        ),
                                        None,
                                    )
                                    if attribute is None:
                                        logger.warning(
                                            "Set -> {}, Attribute -> {}, Row -> {} not found in payload.".format(
                                                set_name, set_attr_name, row
                                            )
                                        )
                                        # need to use row - 1 as index starts with 0 but payload rows start with 1
                                        set_data_attributes[row -
                                                            1][set_attr_schema] = ""
                                    else:
                                        logger.info(
                                            "Set -> {}, Attribute -> {}, Row -> {} found in payload, value -> {}".format(
                                                set_name,
                                                set_attr_name,
                                                row,
                                                attribute["value"],
                                            )
                                        )
                                        # Put the value from the payload into data structure
                                        # need to use row - 1 as index starts with 0 but payload rows start with 1
                                        set_data_attributes[row - 1][
                                            set_attr_schema
                                        ] = attribute["value"]
                                row += 1  # continue the while loop with the next row
                        # Check if it is single-line set:
                        elif attr_type == "object":
                            set_name = schema_attributes[attr_schema]["title"]
                            logger.info(
                                "Single-line Set -> {}".format(set_name))
                            set_data_attributes = data_attributes[attr_data]
                            logger.debug(
                                "Set Data Attributes -> {}".format(
                                    set_data_attributes)
                            )
                            set_schema_attributes = schema_attributes[attr_schema][
                                "properties"
                            ]
                            logger.debug(
                                "Set Schema Attributes -> {}".format(
                                    set_schema_attributes)
                            )
                            for set_attr_data, set_attr_schema in zip(
                                set_data_attributes, set_schema_attributes
                            ):
                                logger.debug(
                                    "Set Attribute ID -> {}".format(set_attr_data))
                                logger.debug(
                                    "Set Attribute Data -> {}".format(
                                        set_data_attributes[set_attr_data]
                                    )
                                )
                                logger.debug(
                                    "Set Attribute Schema -> {}".format(
                                        set_schema_attributes[set_attr_schema]
                                    )
                                )
                                set_attr_type = set_schema_attributes[set_attr_schema][
                                    "type"
                                ]
                                logger.debug(
                                    "Set Attribute Type -> {}".format(
                                        set_attr_type)
                                )
                                set_attr_name = set_schema_attributes[set_attr_schema][
                                    "title"
                                ]
                                logger.debug(
                                    "Set Attribute Name -> {}".format(
                                        set_attr_name)
                                )
                                # Lookup the attribute with the right category, set and attribute name in payload:
                                attribute = next(
                                    (
                                        item
                                        for item in categories
                                        if (
                                            item["name"] == cat_name
                                            and item["set"] == set_name
                                            and item["attribute"] == set_attr_name
                                        )
                                    ),
                                    None,
                                )
                                if attribute is None:
                                    logger.warning(
                                        "Set -> {}, Attribute -> {} not found in payload.".format(
                                            set_name, set_attr_name
                                        )
                                    )
                                    set_data_attributes[set_attr_data] = ""
                                else:
                                    logger.info(
                                        "Set -> {}, Attribute -> {} found in payload, value -> {}".format(
                                            set_name, set_attr_name, attribute["value"]
                                        )
                                    )
                                    # Put the value from the payload into data structure
                                    set_data_attributes[set_attr_data] = attribute["value"]
                        # It is a plain attribute (not inside a set) or it is a multi-value attribute (not inside a set):
                        else:
                            attr_name = schema_attributes[attr_schema]["title"]
                            logger.debug(
                                "Attribute Name -> {}".format(attr_name))
                            # Lookup the attribute with the right category and attribute name in payload:
                            attribute = next(
                                (
                                    item
                                    for item in categories
                                    if (
                                        item["name"] == cat_name
                                        and item["attribute"] == attr_name
                                    )
                                ),
                                None,
                            )
                            if attribute is None:
                                logger.warning(
                                    "Attribute -> {} not found in payload.".format(
                                        attr_name
                                    )
                                )
                                data_attributes[attr_data] = ""
                            else:
                                logger.info(
                                    "Attribute -> {} found in payload, value -> {}".format(
                                        attr_name, attribute["value"]
                                    )
                                )
                                # We need to handle a very special case here for Extended ECM for Government
                                # which has an attribute type "Organizational Unit" (OU). This is referring to a group ID
                                # which is not stable across deployments. So we need to lookup the Group ID and add it
                                # to the data structure. This expects that the payload has the Group Name and not the Group ID
                                if attr_type == str(11480):
                                    logger.info(
                                        "Attribute -> {} is is of type -> Organizational Unit ({}). Looking up group ID for group name -> {}".format(
                                            attr_name, attr_type, attribute["value"]
                                        )
                                    )
                                    response = self._otcs.getGroup(
                                        attribute["value"])
                                    # retrieve the list of matching group names - should just be 1
                                    group_list = response["data"]
                                    # Make sure we have an exact match:
                                    group = next(
                                        (
                                            item
                                            for item in group_list
                                            if item["name"] == attribute["value"]
                                        ),
                                        None,
                                    )
                                    if group:
                                        # Group has been found - determine ID:
                                        group_id = group["id"]
                                        logger.info(
                                            "Group for Organizational Unit -> {} has ID -> {}".format(
                                                attribute["value"], group_id
                                            )
                                        )
                                        # Put the group ID into data structure
                                        data_attributes[attr_data] = str(
                                            group_id)
                                    else:
                                        logger.error(
                                            "Group for Organizational Unit -> {} does not exist!".format(
                                                attribute["value"]
                                            )
                                        )
                                        # Clear the value to avoid workspace create failure
                                        data_attributes[attr_data] = ""
                                # handle special case where attribute type is a user picker.
                                # we expect that the payload includes the login name for this
                                # (as user IDs are not stable across systems) but then we need
                                # to lookup the real user ID here:
                                elif attr_type == "otcs_user_picker":
                                    logger.info(
                                        "Attribute -> {} is is of type -> User Picker ({}). Looking up user ID for user login name -> {}".format(
                                            attr_name, attr_type, attribute["value"]
                                        )
                                    )
                                    response = self._otcs.getUser(
                                        attribute["value"])
                                    # retrieve the list of matching group names - should just be 1
                                    user_list = response["data"]
                                    # Make sure we have an exact match:
                                    user = next(
                                        (
                                            item
                                            for item in user_list
                                            if item["name"] == attribute["value"]
                                        ),
                                        None,
                                    )
                                    if user:
                                        # User has been found - determine ID:
                                        user_id = user["id"]
                                        logger.info(
                                            "User -> {} has ID -> {}".format(
                                                attribute["value"], user_id
                                            )
                                        )
                                        # Put the user ID into data structure
                                        data_attributes[attr_data] = str(
                                            user_id)
                                    else:
                                        logger.error(
                                            "User with login name -> {} does not exist!".format(
                                                attribute["value"]
                                            )
                                        )
                                        # Clear the value to avoid workspace create failure
                                        data_attributes[attr_data] = ""

                                else:
                                    # Put the value from the payload into data structure
                                    data_attributes[attr_data] = attribute["value"]
                    category_create_data["categories"][cat_data] = data_attributes

            logger.debug(
                "Category Create Data -> {}".format(category_create_data))

            # Create the workspace with all provided information:
            response = self._otcs.createWorkspace(
                template_id,
                name,
                description,
                workspace_type_id,
                category_create_data,
                ext_system_id,
                bo_type,
                bo_id,
                parent_workspace_node_id,
            )
            if response == None:
                logger.error("Failed to create workspace -> {}".format(name))
                continue

            # Now we add the node ID of the new workspace to the payload data structure
            # This will be reused when creating the workspace relationships!
            workspace["nodeId"] = self._otcs.getResultValue(response, "id")

            # We also get the name the workspace was finally created with.
            # This can be different form the namein the payload as additional
            # naming conventions from the Workspace Type definitions may apply.
            # This is important to make the python container idem-potent.
            response = self._otcs.getWorkspace(workspace["nodeId"])
            workspace["name"] = self._otcs.getResultValue(response, "name")

            logger.info(
                "Successfully created workspace with final name -> {} and node ID -> {}".format(
                    workspace["name"], workspace["nodeId"]
                )
            )

            # Check if an RM classification is specified for the workspace:
            # RM Classification is specified as list of path elements (top-down)
            if (
                "rm_classification_path" in workspace
                and workspace["rm_classification_path"] != []
            ):
                rm_class_node = self._otcs.getNodeByVolumeAndPath(
                    198, workspace["rm_classification_path"]
                )
                rm_class_node_id = self._otcs.getResultValue(
                    rm_class_node, "id")
                if rm_class_node_id:
                    response = self._otcs.assignRMClassification(
                        workspace["nodeId"], rm_class_node_id, False
                    )
                    if response == None:
                        logger.error(
                            "Failed to assign RM classification -> {} ({}) to workspace -> {}".format(
                                workspace["rm_classification_path"][-1],
                                rm_class_node_id,
                                name,
                            )
                        )
                    else:
                        logger.info(
                            "Assigned RM Classification -> {} to workspace -> {}".format(
                                workspace["rm_classification_path"][-1], name
                            )
                        )
            # Check if one or multiple classifications are specified for the workspace
            # Classifications are specified as list of path elements (top-down)
            if (
                "classification_pathes" in workspace
                and workspace["classification_pathes"] != []
            ):
                for classification_path in workspace["classification_pathes"]:
                    class_node = self._otcs.getNodeByVolumeAndPath(
                        198, classification_path)
                    class_node_id = self._otcs.getResultValue(class_node, "id")
                    if class_node_id:
                        response = self._otcs.assignClassification(
                            workspace["nodeId"], class_node_id, False
                        )
                        if response == None:
                            logger.error(
                                "Failed to assign classification -> {} to workspace -> {}".format(
                                    class_node_id, name
                                )
                            )
                        else:
                            logger.info(
                                "Assigned Classification -> {} to workspace -> {}".format(
                                    classification_path[-1], name
                                )
                            )

        # end method definition

    def processWorkspaceRelationships(self):
        """Process workspaces relationships in payload and create them in Extended ECM.

        Relationships can only be created if all workspaces have been created before.
        Once a workspace got created, the node ID of that workspaces has been added
        to the payload["workspaces"] data structure (see processWorkspaces())
        Relationships are created between the node IDs of two business workspaces
        (and not the logical IDs in the inital payload specification)

        Args: None
        Return: None
        """

        for workspace in self._workspaces:
            # Read name from payload:
            if not "name" in workspace:
                continue
            name = workspace["name"]

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in workspace and not workspace["enabled"]:
                logger.info(
                    "Payload for Workspace -> {} is disabled. Skipping...".format(
                        name)
                )
                continue

            # Read relationships from payload:
            if not "relationships" in workspace:
                logger.info(
                    "Workspace -> {} has no relationships - skipping to next workspace...".format(
                        name
                    )
                )
                continue

            # Check that workspaces actually have a logical ID -
            # otherwise we cannot establish the relationship:
            if not "id" in workspace:
                logger.warning(
                    "Workspace without ID cannot have a relationship - skipping to next workspace..."
                )
                continue

            workspace_id = workspace["id"]
            logger.info(
                "Workspace -> {} has relationships - creating...".format(name))

            if not "nodeId" in workspace:
                logger.warning(
                    "Workspace without node ID cannot have a relationship (workspace creation may have failed) - skipping to next workspace..."
                )
                continue
            # now determine the actual node IDs of the workspaces (have been created above):
            workspace_node_id = workspace["nodeId"]
            logger.info(
                "Workspace with logical ID -> {} has node ID -> {}".format(
                    workspace_id, workspace_node_id
                )
            )

            for related_workspace_id in workspace["relationships"]:
                # Find the workspace type with the name given in the payload:
                related_workspace = next(
                    (item for item in self._workspaces if item["id"]
                     == related_workspace_id),
                    None,
                )
                if related_workspace is None:
                    logger.error(
                        "Related Workspace with logical ID -> {} not found.".format(
                            related_workspace_id
                        )
                    )
                    continue

                if "enabled" in related_workspace and not related_workspace["enabled"]:
                    logger.info(
                        "Payload for Related Workspace -> {} is disabled. Skipping...".format(
                            related_workspace["name"]
                        )
                    )
                    continue

                if not "nodeId" in related_workspace:
                    logger.warning(
                        "Related Workspace without node ID (workspaces creation may have failed) - skipping to next workspace..."
                    )
                    continue
                # now determine the actual node IDs of the related workspace (should have been created above):
                related_workspace_node_id = related_workspace["nodeId"]
                logger.info(
                    "Related Workspace with logical ID -> {} has node ID -> {}".format(
                        related_workspace_id, related_workspace_node_id
                    )
                )

                logger.info(
                    "Create Workspace Relationship between workspace node ID -> {} and workspace node ID -> {}".format(
                        workspace_node_id, related_workspace_node_id
                    )
                )

                # Check if relationship does already exists:
                response = self._otcs.getWorkspaceRelationships(
                    workspace_node_id)

                existing_workspace_relationship = self._otcs.existResultItem(
                    response, "id", related_workspace_node_id)
                if existing_workspace_relationship:
                    logger.info(
                        "Workspace relationship between workspace ID -> {} and related workspace ID -> {} does already exist. Skipping...".format(workspace_node_id, related_workspace_node_id))
                    continue

                response = self._otcs.createWorkspaceRelationship(
                    workspace_node_id, related_workspace_node_id
                )
                if response == None:
                    logger.error("Failed to create workspace relationship.")
                else:
                    logger.info("Successfully created workspace relationship.")

        # end method definition

    def processWorkspaceMembers(self):
        """Process workspaces members in payload and create them in Extended ECM.

        Args: None
        Return: None
        """

        for workspace in self._workspaces:
            # Read name from payload (just for logging):
            if not "name" in workspace:
                continue
            workspace_name = workspace["name"]

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in workspace and not workspace["enabled"]:
                logger.info(
                    "Payload for Workspace -> {} is disabled. Skipping...".format(
                        workspace_name
                    )
                )
                continue

            # Read members from payload:
            if not "members" in workspace:
                logger.info(
                    "Workspace -> {} has no members in payload - skipping to next workspace...".format(
                        workspace_name
                    )
                )
                continue
            members = workspace["members"]

            workspace_id = workspace["id"]
            logger.info(
                "Workspace -> {} has memberships in payload - establishing...".format(
                    workspace_name
                )
            )

            if not "nodeId" in workspace:
                logger.warning(
                    "Workspace without node ID cannot have a members (workspaces creation may have failed) - skipping to next workspace..."
                )
                continue

            # now determine the actual node IDs of the workspaces (have been created by processWorkspaces()):
            workspace_node_id = workspace["nodeId"]
            logger.info(
                "Adding members to workspace with ID -> {} and node Id -> {}".format(
                    workspace_id, workspace_node_id
                )
            )

            workspace_roles = self._otcs.getWorkspaceRoles(
                workspace_node_id)
            if workspace_roles == None:
                logger.info(
                    "Workspace with ID -> {} and node Id -> {} has no roles - skipping to next workspace...".format(
                        workspace_id, workspace_node_id
                    )
                )
                continue

            for member in members:
                # read user list and role name from payload:
                member_users = (
                    member["users"] if member.get("users") else []
                )  # be careful to avoid key errors as users are optional
                member_groups = (
                    member["groups"] if member.get("groups") else []
                )  # be careful to avoid key errors as groups are optional
                member_role_name = member["role"]

                if member_role_name == "":  # role name is required
                    logger.error(
                        "Members of workspace -> {} is missing the role name.".format(
                            workspace_name
                        )
                    )
                    continue
                if (
                    member_users == [] and member_groups == []
                ):  # we either need users or groups (or both)
                    logger.warning(
                        "Role -> {} of workspace -> {} does not have any members (no users nor groups).".format(
                            member_role_name, workspace_name
                        )
                    )
                    continue

                role_id = self._otcs.lookupResultValue(
                    workspace_roles, "name", member_role_name, "id")
                if role_id is None:
                    #    if member_role is None:
                    logger.error(
                        "Workspace -> {} does not have a role with name -> {}".format(
                            workspace_name, member_role_name
                        )
                    )
                    continue
                logger.info(
                    "Role -> {} has ID -> {}".format(member_role_name, role_id))

                # Process users as workspaces members:
                for member_user in member_users:
                    # find member user in current payload:
                    member_user_id = next(
                        (item for item in self._users if item["name"]
                         == member_user), None
                    )
                    if member_user_id:
                        user_id = member_user_id["id"]
                    else:
                        # If this didn't work, try to get the member user from OTCS. This covers
                        # cases where the user is system generated or part
                        # of a former payload processing (thus not in the current payload):
                        logger.info(
                            "Member -> {} not found in current payload - check if it exists in OTCS already...".format(
                                member_user
                            )
                        )
                        existing_user = self._otcs.getUser(member_user)
                        user_id = self._otcs.getResultValue(
                            existing_user, "id")
                        if not user_id:
                            logger.error(
                                "Cannot find member user with login -> {}. Skipping...".format(
                                    member_user
                                )
                            )
                            continue

                    # Add member if it does not yet exists - suppress warning
                    # message if user is already in role:
                    response = self._otcs.addMemberToWorkspace(
                        workspace_node_id, role_id, user_id, False)
                    if response == None:
                        logger.error(
                            "Failed to add user -> {} ({}) to role -> {} of workspace -> {}".format(
                                member_user_id["name"],
                                user_id,
                                member_role_name,
                                workspace_name,
                            )
                        )
                    else:
                        logger.info(
                            "Successfully added user -> {} ({}) to role -> {} of workspace -> {}".format(
                                member_user_id["name"],
                                user_id,
                                member_role_name,
                                workspace_name,
                            )
                        )

                # Process groups as workspaces members:
                for member_group in member_groups:
                    member_group_id = next(
                        (item for item in self._groups if item["name"]
                         == member_group), None
                    )
                    if member_group_id is None:
                        logger.error(
                            "Cannot find group with name -> {}".format(
                                member_group)
                        )
                        continue
                    group_id = member_group_id["id"]

                    response = self._otcs.addMemberToWorkspace(
                        workspace_node_id, role_id, group_id)
                    if response == None:
                        logger.error(
                            "Failed to add group -> {} ({}) to role -> {} of workspace -> {}".format(
                                member_group_id["name"],
                                group_id,
                                member_role_name,
                                workspace_name,
                            )
                        )
                    else:
                        logger.info(
                            "Successfully added group -> {} ({}) to role -> {} of workspace -> {}".format(
                                member_group_id["name"],
                                group_id,
                                member_role_name,
                                workspace_name,
                            )
                        )

                # We don't want Admin to be in the leader role
                # of workspaces - this can happen because the admin
                # user is the creator of the workspaces and the
                # creator gets added to the leader role automatically:
                leader_role_id = self._otcs.lookupResultValue(
                    workspace_roles, "leader", True, "id")

                if leader_role_id:
                    leader_role_name = self._otcs.lookupResultValue(
                        workspace_roles, "leader", True, "name")
                    response = self._otcs.removeMemberFromWorkspace(
                        workspace_node_id, leader_role_id, 1000, False
                    )
                    if response:
                        logger.info(
                            "Removed admin user (1000) from leader role -> {} ({}) of workspace -> {}".format(
                                leader_role_name,
                                leader_role_id,
                                workspace_name,
                            )
                        )

        # end method definition

    def processWebReports(self, web_reports: list):
        """Process web reports in payload and run them in Extended ECM.

        Args:
            web_reports (list): list of web reports. As we have two different list (pre and post)
                                we need to pass the actual list as parameter.
        Return: None
        """

        for web_report in web_reports:
            nick_name = web_report["nickname"]

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in web_report and not web_report["enabled"]:
                logger.info(
                    "Payload for Web Report -> {} is disabled. Skipping...".format(
                        nick_name
                    )
                )
                continue

            description = web_report["description"]

            if not self._otcs.getNodeFromNickname(nick_name):
                logger.error("Web Report with nickname -> {} does not exist! Skipping...".format(nick_name))
                continue
                    
            # be careful to avoid key errors as Web Report parameters are optional:
            actual_params = web_report["parameters"] if web_report.get(
                "parameters") else {}
            formal_params = self._otcs.getWebReportParameters(nick_name)
            if actual_params:
                logger.info(
                    "Running Web Report -> {} ({}) with parameters -> {} ...".format(
                        nick_name, description, actual_params
                    )
                )
                # Do some sanity checks to see if the formal and actual parameters are matching...
                # Check 1: are there formal parameters at all?
                if not formal_params:
                    logger.error(
                        "Web Report -> {} is called with actual parameters but it does not expect parameters! Skipping...".format(
                            nick_name
                        )
                    )
                    continue
                lets_continue = False
                # Check 2: Iterate through the actual parameters given in the payload
                # and see if there's a matching formal parameter expected by the Web Report:
                for key, value in actual_params.items():
                    # Check if there's a matching formal parameter defined on the Web Report node:
                    formal_param = next(
                        (item for item in formal_params if item["parm_name"] == key), None
                    )
                    if formal_param is None:
                        logger.error(
                            "Web Report -> {} is called with parameter -> {} that is not expected! Skipping...".format(
                                nick_name, key
                            )
                        )
                        lets_continue = True  # we cannot do a "continue" here directly as we are in an inner loop
                # Check 3: Iterate through the formal parameters and validate there's a matching
                # actual parameter defined in the payload for each mandatory formal parameter
                # that does not have a default value:
                for formal_param in formal_params:
                    if (
                        (formal_param["mandatory"] == True)
                        and (formal_param["default_value"] == None)
                        and not actual_params.get(formal_param["parm_name"])
                    ):
                        logger.error(
                            "Web Report -> {} is called without mandatory parameter -> {}! Skipping...".format(
                                nick_name, formal_param["parm_name"]
                            )
                        )
                        lets_continue = True  # we cannot do a "continue" here directly as we are in an inner loop
                # Did any of the checks fail?
                if lets_continue:
                    continue
                # Actual parameters are validated, we can run the Web Report:
                response = self._otcs.runWebReport(
                    nick_name, actual_params)
            else:
                logger.info(
                    "Running Web Report -> {} ({}) without parameters...".format(
                        nick_name, description
                    )
                )
                # Check if there's a formal parameter that is mandatory but
                # does not have a default value:
                if formal_params:
                    required_param = next(
                        (
                            item
                            for item in formal_params
                            if (item["mandatory"] == True) and (not item["default_value"])
                        ),
                        None,
                    )
                    if required_param:
                        logger.error(
                            "Web Report -> {} is called without parameters but has a mandatory parameter -> {} without a default value! Skipping...".format(
                                nick_name, required_param["parm_name"]
                            )
                        )
                        continue
                    else:  # we are good to proceed!
                        logger.debug(
                            "Web Report -> {} does not have a mandatory parameter without a default value!".format(
                                nick_name
                            )
                        )
                response = self._otcs.runWebReport(nick_name)
            if response == None:
                logger.error(
                    "Failed to run web report -> {}".format(nick_name))

        # end method definition

    def processCSApplications(self, otcs_object: object = None):
        """Process CS applications in payload and install them in Extended ECM.
        The CS Applications need to be installed in all frontend and backends.

        Args:
            otcs_object (object): this can either be the OTCS frontend or OTCS backend. If None
                                  then the otcs_backend is used.
        Return: None
        """

        # OTCS backend is the default:
        if not otcs_object:
            otcs_object = self._otcs_backend

        for cs_application in self._cs_applications:
            application_name = cs_application["name"]

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in cs_application and not cs_application["enabled"]:
                logger.info(
                    "Payload for CS Application -> {} is disabled. Skipping...".format(
                        application_name
                    )
                )
                continue

            application_description = cs_application["description"]

            logger.info(
                "Install CS Application -> {} ({})...".format(
                    application_name, application_description
                )
            )
            response = otcs_object.installCSApplication(application_name)
            if response == None:
                logger.error(
                    "Failed to install CS Application -> {}!".format(
                        application_name)
                )

        # end method definition

    def processUserFavoritesAndSettings(self):
        """Process user favorites and settings in payload and create them in Extended ECM.

        We can only set favorites if we impersonate / authenticate as the user.
        We also want to make sure that the user is not forced to change the password.
        The following code (for loop) will change the authenticated user - we need to
        switch it back to admin user later so we safe the admin credentials for this:

        Args: None
        Return: None
        """

        if self._users:
            # save admin credentials for later switch back to admin user:
            admin_credentials = self._otcs.credentials()

        for user in self._users:
            user_name = user["name"]

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in user and not user["enabled"]:
                logger.info(
                    "Payload for User -> {} is disabled. Skipping...".format(
                        user_name)
                )
                continue

            user_password = user["password"]

            user_partition = self._otcs.config()["partition"]
            if not user_partition:
                logger.error(
                    "User partition not found!"
                )

            # Set the OTDS display name. Extended ECM does not use this but
            # it makes AppWorks display users correctly (and it doesn't hurt)
            # We only set this if firstname _and_ last name are in the payload:
            if "firstname" in user and "lastname" in user:
                user_display_name = user["firstname"] + " " + user["lastname"]
                response = self._otds.updateUser(user_partition,
                                                 user_name,
                                                 "displayName",
                                                 user_display_name)
                if response:
                    logger.info(
                        "Display name for user -> {} has been updated to -> {}".format(
                            user_name, user_display_name)
                    )
                else:
                    logger.error(
                        "Display name for user -> {} could not be updated to -> {}".format(
                            user_name, user_display_name)
                    )

            # Don't enforce the user to reset password at first login (settings in OTDS):
            logger.info(
                "Don't enforce password change for user -> {}...".format(user_name))
            response = self._otds.updateUser(user_partition,
                                             user_name,
                                             "UserMustChangePasswordAtNextSignIn",
                                             "False")

            # we change the otcs credentials to the user:
            self._otcs.setCredentials(user_name, user_password)

            # we re-authenticate as the user:
            logger.info("Authenticate user -> {}...".format(user_name))
            # True = force new login with new user
            cookie = self._otcs.authenticate(True)
            if not cookie:
                logger.error(
                    "Couldn't authenticate user -> {}".format(user_name))
                continue

            # we update the user profile to activate navigation tree:
            response = self._otcs.updateUserProfile(
                "conwsNavigationTreeView", True)
            if response is None:
                logger.warning(
                    "Profile for user -> {} couldn't be updated!".format(
                        user_name)
                )
            else:
                logger.info(
                    "Profile for user -> {} has been updated to enable Workspace Navigation Tree.".format(
                        user_name
                    )
                )

            # we work through the list of favorites defined for the user:
            favorites = user["favorites"]
            for favorite in favorites:
                # check if favorite is a logical workspace name
                favorite_item = next(
                    (item for item in self._workspaces if item["id"]
                     == favorite), None
                )
                is_workspace = False
                if favorite_item is not None:
                    logger.info(
                        "Found favorite item (workspace) -> {}".format(
                            favorite_item["name"]
                        )
                    )
                    if "nodeId" in favorite_item:
                        favorite_id = favorite_item["nodeId"]
                    else:
                        logger.info(
                            "Favorite -> {} (workspace) does not have a nodeId - skipping to next favorite...".format(
                                favorite
                            )
                        )
                        continue
                    is_workspace = True
                else:
                    # alternatively try to find the item as a nickname:
                    favorite_item = self._otcs.getNodeFromNickname(
                        favorite)
                    favorite_id = self._otcs.getResultValue(
                        favorite_item, "id")
#                    if favorite_item is None:
                    if favorite_id is None:
                        logger.warning(
                            "Favorite -> {} neither found as workspace ID nor as nickname - skipping to next favorite...".format(
                                favorite
                            )
                        )
                        continue

                response = self._otcs.addFavorite(favorite_id)
                if response is None:
                    logger.warning(
                        "Favorite ID -> {} couldn't be added for user -> {}!".format(
                            favorite_id, user_name
                        )
                    )
                else:
                    logger.info(
                        "Added favorite for user -> {}, node ID -> {}.".format(
                            user_name, favorite_id
                        )
                    )
                    logger.info(
                        "Simulate user -> {} browsing node ID -> {}.".format(
                            user_name, favorite_id
                        )
                    )
                    # simulate a browse by the user to populate recently accessed items
                    if is_workspace:
                        response = self._otcs.getWorkspace(favorite_id)
                    else:
                        response = self._otcs.getNode(favorite_id)

            # we work through the list of proxies defined for the user
            # (we need to consider that not all users have the proxies element):
            proxies = user["proxies"] if user.get("proxies") else []

            for proxy in proxies:
                proxy_user = next(
                    (item for item in self._users if item["name"] == proxy),
                    None,
                )
                if not proxy_user or not "id" in proxy_user:
                    logger.error(
                        "The proxy -> {} for user -> {} does not exist! Skipping proxy...".format(
                            proxy, user_name
                        )
                    )
                    continue
                proxy_user_id = proxy_user["id"]

                # Check if the proxy is already set:
                if not self._otcs.isProxy(proxy):
                    logger.info(
                        "Set user -> {} ({}) as proxy for user -> {}.".format(
                            proxy, proxy_user_id, user_name
                        )
                    )
                    # set the user proxy - currently we don't support time based proxies in payload.
                    # The called method is ready to support this.
                    response = self._otcs.updateUserProxy(proxy_user_id)
                else:
                    logger.info(
                        "User -> {} ({}) is already proxy for user -> {}. Skipping...".format(
                            proxy, proxy_user_id, user_name
                        )
                    )
        if self._users:
            # Set back admin credentials:
            self._otcs.setCredentials(
                admin_credentials["username"], admin_credentials["password"]
            )

            # we re-authenticate as the admin user:
            logger.info(
                "Authenticate as admin user -> {}...".format(
                    admin_credentials["username"])
            )
            # True = force new login with new user
            cookie = self._otcs.authenticate(True)

        # end method definition

    def processSecurityClearances(self):
        """Process Security Clearances for Extended ECM.

        Args: None
        Return: None
        """

        for security_clearance in self._security_clearances:
            clearance_level = security_clearance.get("level")
            clearance_name = security_clearance.get("name")

            if "enabled" in security_clearance and not security_clearance["enabled"]:
                logger.info(
                    "Payload for Security Clearance -> {} is disabled. Skipping...".format(
                        clearance_name
                    )
                )
                continue

            clearance_description = security_clearance.get("description")
            if not clearance_description:
                clearance_description = ""
            if clearance_level and clearance_name:
                logger.info(
                    "Creating Security Clearance -> {} : {}".format(
                        clearance_level, clearance_name
                    )
                )
                self._otcs.runWebReport("web_report_security_clearance",
                                        security_clearance)
            else:
                logger.error(
                    "Cannot create Security Clearance - either level or name is missing!"
                )

        # end method definition

    def processSupplementalMarkings(self):
        """Process Supplemental Markings for Extended ECM.

        Args: None
        Return: None
        """

        for supplemental_marking in self._supplemental_markings:
            code = supplemental_marking.get("code")

            if "enabled" in supplemental_marking and not supplemental_marking["enabled"]:
                logger.info(
                    "Payload for Supplemental Marking -> {} is disabled. Skipping...".format(
                        code
                    )
                )
                continue

            description = supplemental_marking.get("description")
            if not description:
                description = ""
            if code:
                logger.info(
                    "Creating Supplemental Marking -> {} : {}".format(
                        code, description)
                )
                self._otcs.runWebReport(
                    "web_report_supplemental_marking", supplemental_marking)
            else:
                logger.error(
                    "Cannot create Supplemental Marking - either code or description is missing!"
                )

        # end method definition

    def processUserSecurity(self):
        """Process Security Clearance and Supplemental Markings for Extended ECM users.

        Args: None
        Return: None
        """

        for user in self._users:
            user_id = user.get("id")
            user_name = user.get("name")

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in user and not user["enabled"]:
                logger.info(
                    "Payload for User -> {} is disabled. Skipping...".format(
                        user_name)
                )
                continue

            # Read security clearance from user payload (it is optional!)
            user_security_clearance = user.get("security_clearance")
            if user_id and user_security_clearance:
                response = self._otcs.assignUserSecurityClearance(
                    user_id, user_security_clearance)

            # Read supplemental markings from user payload (it is optional!)
            user_supplemental_markings = user.get("supplemental_markings")
            if user_id and user_supplemental_markings:
                response = self._otcs.assignUserSupplementalMarkings(
                    user_id, user_supplemental_markings
                )

        # end method definition

    def processRecordsManagementSettings(self):
        """Process Records Management Settings for Extended ECM.
        The setting files need to be placed in the OTCS file system file via
        a transport into the Support Asset Volume.

        Args: None
        Return: None
        """

        if (
            "records_management_system_settings" in self._records_management_settings
            and self._records_management_settings["records_management_system_settings"] != ""
        ):
            filename = self._custom_settings_dir + \
                self._records_management_settings["records_management_system_settings"]
            self._otcs.importRecordsManagementSettings(filename)

        if (
            "records_management_codes" in self._records_management_settings
            and self._records_management_settings["records_management_codes"] != ""
        ):
            filename = self._custom_settings_dir + \
                self._records_management_settings["records_management_codes"]
            self._otcs.importRecordsManagementCodes(filename)

        if (
            "records_management_rsis" in self._records_management_settings
            and self._records_management_settings["records_management_rsis"] != ""
        ):
            filename = self._custom_settings_dir + \
                self._records_management_settings["records_management_rsis"]
            self._otcs.importRecordsManagementRSIs(filename)

        if (
            "physical_objects_system_settings" in self._records_management_settings
            and self._records_management_settings["physical_objects_system_settings"] != ""
        ):
            filename = self._custom_settings_dir + \
                self._records_management_settings["physical_objects_system_settings"]
            self._otcs.importPhysicalObjectsSettings(filename)

        if (
            "physical_objects_codes" in self._records_management_settings
            and self._records_management_settings["physical_objects_codes"] != ""
        ):
            filename = self._custom_settings_dir + \
                self._records_management_settings["physical_objects_codes"]
            self._otcs.importPhysicalObjectsCodes(filename)

        if (
            "physical_objects_locators" in self._records_management_settings
            and self._records_management_settings["physical_objects_locators"] != ""
        ):
            filename = self._custom_settings_dir + \
                self._records_management_settings["physical_objects_locators"]
            self._otcs.importPhysicalObjectsLocators(filename)

        if (
            "security_clearance_codes" in self._records_management_settings
            and self._records_management_settings["security_clearance_codes"] != ""
        ):
            filename = self._custom_settings_dir + \
                self._records_management_settings["security_clearance_codes"]
            self._otcs.importSecurityClearanceCodes(filename)

        # end method definition

    def processHolds(self):
        """Process Records Management Holds for Extended ECM users.

        Args: None
        Return: None
        """

        for hold in self._holds:
            if not "name" in hold:
                logger.error("Cannot create Hold without a name! Skipping...")
                continue
            hold_name = hold["name"]

            if not "type" in hold:
                logger.error(
                    "Cannot create Hold -> {} without a type! Skipping...".format(
                        hold_name)
                )
                continue
            hold_type = hold["type"]

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in hold and not hold["enabled"]:
                logger.info(
                    "Payload for Hold -> {} is disabled. Skipping...".format(
                        hold_name)
                )
                continue

            hold_group = hold.get("group")
            hold_comment = hold.get("comment")
            hold_alternate_id = hold.get("alternate_id")
            hold_date_applied = hold.get("date_applied")
            hold_date_suspend = hold.get("date_to_remove")

            if hold_group:
                # Check if the Hold Group (folder) does already exist.
                # 2122 is the ID of the "Hold Maintenance" top level
                # folder in Records Management area that (we hope) will remain
                # stable:
                response = self._otcs.getNodeByParentAndName(
                    2122, hold_group)
                parent_id = self._otcs.getResultValue(response, "id")
                if not parent_id:
                    response = self._otcs.createItem(
                        2122, "833", hold_group)
                    parent_id = self._otcs.getResultValue(response, "id")
            else:
                parent_id = 2122

            # Holds are special - they ahve folders that cannot be traversed
            # in the normal way - we need to get the whole list of holds and use
            # specialparameters for the existResultItems() method as the REST
            # API calls delivers a results->data->holds structure (not properties)
            response = self._otcs.getRecordsManagementHolds()
            if self._otcs.existResultItem(response, "HoldName", hold_name, property_name="holds"):
                logger.info(
                    "Hold -> {} does already exist. Skipping...".format(hold_name))
                continue

            hold = self._otcs.createRecordsManagementHold(
                hold_type,
                hold_name,
                hold_comment,
                hold_alternate_id,
                parent_id,
                hold_date_applied,
                hold_date_suspend,
            )

            if hold and hold["holdID"]:
                logger.info(
                    "Successfully created hold -> {} with ID -> {}".format(
                        hold_name, hold["holdID"]
                    )
                )

        # end method definition

    def processAdditionalGroupMembers(self):
        """Process additional groups memberships we want to have in OTDS.

        Args: None
        Return: None
        """

        for additional_group_member in self._additional_group_members:
            if not "parent_group" in additional_group_member:
                logger.error("Missing parent_group! Skipping...")
                continue
            parent_group = additional_group_member["parent_group"]

            if (
                "enabled" in additional_group_member
                and not additional_group_member["enabled"]
            ):
                logger.info(
                    "Payload for Additional Group Member with Parent Group -> {} is disabled. Skipping...".format(
                        parent_group
                    )
                )
                continue

            if (not "user_name" in additional_group_member) and (
                not "group_name" in additional_group_member
            ):
                logger.error(
                    "Either group_name or user_name need to be specified! Skipping..."
                )
                continue
            if "group_name" in additional_group_member:
                group_name = additional_group_member["group_name"]
                logger.info(
                    "Adding group -> {} to parent group -> {} in OTDS.".format(
                        group_name, parent_group
                    )
                )
                response = self._otds.addGroupToParentGroup(
                    group_name, parent_group)
                if not response:
                    logger.error(
                        "Failed to add group -> {} to parent group -> {} in OTDS.".format(
                            group_name, parent_group
                        )
                    )
            elif "user_name" in additional_group_member:
                user_name = additional_group_member["user_name"]
                logger.info(
                    "Adding user -> {} to group -> {} in OTDS.".format(
                        user_name, parent_group
                    )
                )
                response = self._otds.addUserToGroup(
                    user_name, parent_group)
                if not response:
                    logger.error(
                        "Failed to add user -> {} to group -> {} in OTDS.".format(
                            user_name, parent_group
                        )
                    )

        # end method definition

    def processAdditionalAccessRoleMembers(self):
        """Process additional access role memberships we want to have in OTDS.

        Args: None
        Return: None
        """

        for additional_access_role_member in self._additional_access_role_members:
            if not "access_role" in additional_access_role_member:
                logger.error("Missing access_role! Skipping...")
                continue
            access_role = additional_access_role_member["access_role"]

            if (
                "enabled" in additional_access_role_member
                and not additional_access_role_member["enabled"]
            ):
                logger.info(
                    "Payload for Additional Member for AccessRole -> {} is disabled. Skipping...".format(
                        access_role
                    )
                )
                continue

            if (
                (not "user_name" in additional_access_role_member)
                and (not "group_name" in additional_access_role_member)
                and (not "partition_name" in additional_access_role_member)
            ):
                logger.error(
                    "Either group_name or user_name need to be specified! Skipping..."
                )
                continue
            if "group_name" in additional_access_role_member:
                group_name = additional_access_role_member["group_name"]
                logger.info(
                    "Adding group -> {} to access role -> {} in OTDS.".format(
                        group_name, access_role
                    )
                )
                response = self._otds.addGroupToAccessRole(
                    access_role, group_name)
                if not response:
                    logger.error(
                        "Failed to add group -> {} to access role -> {} in OTDS.".format(
                            group_name, access_role
                        )
                    )
            elif "user_name" in additional_access_role_member:
                user_name = additional_access_role_member["user_name"]
                logger.info(
                    "Adding user -> {} to access role -> {} in OTDS.".format(
                        user_name, access_role
                    )
                )
                response = self._otds.addUserToAccessRole(
                    access_role, user_name)
                if not response:
                    logger.error(
                        "Failed to add user -> {} to access role -> {} in OTDS.".format(
                            user_name, access_role
                        )
                    )
            elif "partition_name" in additional_access_role_member:
                partition_name = additional_access_role_member["partition_name"]
                logger.info(
                    "Adding partition -> {} to access role -> {} in OTDS.".format(
                        partition_name, access_role
                    )
                )
                response = self._otds.addPartitionToAccessRole(
                    access_role, partition_name)
                if not response:
                    logger.error(
                        "Failed to add partition -> {} to access role -> {} in OTDS.".format(
                            partition_name, access_role
                        )
                    )

        # end method definition

    def processRenamings(self):
        """Process renamings specified in payload and rename existing Extended ECM items.

        Args: None
        Return: None
        """

        for renaming in self._renamings:
            if not "nodeid" in renaming:
                if not "volume" in renaming:
                    logger.error(
                        "Renamings require either a node ID or a volume! Skipping to next renaming..."
                    )
                    continue
                # Determine object ID of volume:
                volume = self._otcs.getVolume(renaming["volume"])
                node_id = self._otcs.getResultValue(volume, "id")
            else:
                node_id = renaming["nodeid"]

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in renaming and not renaming["enabled"]:
                logger.info("Payload for Renaming is disabled. Skipping...")
                continue

            response = self._otcs.renameNode(
                node_id, renaming["name"], renaming["description"])
            if not response:
                logger.error(
                    "Failed to rename node ID -> {} to new name -> {}.".format(
                        node_id, renaming["name"]
                    )
                )

        # end method definition

    def processItems(self, items: list):
        """Process items specified in payload and create them in Extended ECM.

        Args:
            otcs: OTCS object
            items: list of items to create (need this as parameter as we
                   have multiple lists)
        Return: None
        """

        for item in items:

            if not "name" in item:
                logger.error("Item needs a name. Skipping...")
                continue
            item_name = item["name"]

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in item and not item["enabled"]:
                logger.info(
                    "Payload for Item -> {} is disabled. Skipping...".format(
                        item_name)
                )
                continue

            if not "description" in item:
                item_description = ""
            else:
                item_description = item["description"]

            parent_nickname = item.get("parent_nickname")
            parent_path = item.get("parent_path")

            if parent_nickname:
                parent_node = self._otcs.getNodeFromNickname(
                    parent_nickname)
                parent_id = self._otcs.getResultValue(parent_node, "id")
                # if not parent_node:
                if not parent_id:
                    logger.error(
                        "Item -> {} has a parent nickname -> {} that does not exist. Skipping...".format(
                            item_name, parent_nickname
                        )
                    )
                    continue
            else:  # use parent_path and Enterprise Volume
                parent_node = self._otcs.getNodeByVolumeAndPath(
                    141, parent_path)
                parent_id = self._otcs.getResultValue(parent_node, "id")
                if not parent_id:
                    # if not parent_node:
                    logger.error(
                        "Item -> {} has a parent path that does not exist. Skipping...".format(
                            item_name
                        )
                    )
                    continue

            original_nickname = item.get("original_nickname")
            original_path = item.get("original_path")

            if original_nickname:
                original_node = self._otcs.getNodeFromNickname(
                    original_nickname)
                original_id = self._otcs.getResultValue(original_node, "id")
                if not original_id:
                    # if not original_node:
                    logger.error(
                        "Item -> {} has a original nickname -> {} that does not exist. Skipping...".format(
                            item_name, original_nickname
                        )
                    )
                    continue
            elif original_path:
                original_node = self._otcs.getNodeByVolumeAndPath(
                    141, original_path)
                original_id = self._otcs.getResultValue(original_node, "id")
                if not original_id:
                    # if not original_node:
                    logger.error(
                        "Item -> {} has a original path that does not exist. Skipping...".format(
                            item_name
                        )
                    )
                    continue
            else:
                original_id = 0

            if not "type" in item:
                logger.error(
                    "Item -> {} needs a type. Skipping...".format(item_name))
                continue

            item_type = item.get("type")
            item_url = item.get("url")

            # check that we have the required information
            # for the given item type:
            match item_type:
                case 140:  # URL
                    if item_url == "":
                        logger.error(
                            "Item -> {} has type URL but the URL is not in the payload. Skipping...".format(
                                item_name
                            )
                        )
                        continue
                case 1:  # Shortcut
                    if original_id == 0:
                        logger.error(
                            "Item -> {} has type Shortcut but the original item is not in the payload. Skipping...".format(
                                item_name
                            )
                        )
                        continue

            # Check if an item with the same name does already exist.
            # This can also be the case if the python container runs a 2nd time.
            # For this reason we are also not issuing an error but just an info (False):
            response = self._otcs.getNodeByParentAndName(
                parent_id, item_name, False)
            if self._otcs.getResultValue(response, "name") == item_name:
                logger.info(
                    "Item with name -> {} does already exist in parent folder with ID -> {}".format(
                        item_name, parent_id
                    )
                )
                continue
            response = self._otcs.createItem(
                parent_id, item_type, item_name, item_description, item_url, original_id
            )
            if not response:
                logger.error("Failed to create item -> {}.".format(item_name))

        # end method definition

    def processPermissions(self, permissions: list):
        """Process items specified in payload and upadate permissions.

        Args:
            permissions: list of items to apply permissions to. Each list item is a dict
                         with this structure:
                            {
                                nodeid = "..."
                                volume = "..."
                                nickname = "..."
                                public_access_permissions = ["see", "see_content", ...]
                                owner_permissions = []
                                owner_group_permissions = []
                                groups = [
                                {
                                    name = "..."
                                    permissions = []
                                }
                                ]
                                users = [
                                {
                                    name = "..."
                                    permissions = []
                                }
                                ]
                                apply_to = 2
                            }

        Return: None
        """

        for permission in permissions:

            if (
                not "path" in permission
                and not "volume" in permission
                and not "nickname" in permission
            ):
                logger.error(
                    "Item to change permission is not specified. Skipping...")
                continue

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in permission and not permission["enabled"]:
                logger.info("Payload for Permission is disabled. Skipping...")
                continue

            node_id = 0

            # Check if "volume" is in payload and not empty string:
            if "volume" in permission and permission["volume"]:
                volume_type = permission["volume"]
                logger.info(
                    "Found volume type -> {} in permission definition. Determine volume ID...".format(
                        volume_type
                    )
                )
                volume = self._otcs.getVolume(volume_type)
                node_id = self._otcs.getResultValue(volume, "id")
                if not node_id:
                    logger.error(
                        "Illegal volume -> {} in permission specification. Skipping...".format(
                            volume_type
                        )
                    )
                    continue

            # Check if "path" is in payload and not empty list
            # (path can be combined with volume so we need to take volume into account):
            if "path" in permission and permission["path"]:
                path = permission["path"]
                logger.info(
                    "Found path -> {} in permission definition. Determine node ID...".format(
                        path
                    )
                )
                node = self._otcs.getNodeByVolumeAndPath(
                    volume_type, path)
                node_id = self._otcs.getResultValue(node, "id")
                if not node_id:
                    logger.error(
                        "Path -> {} does not exist. Skipping...".format(path))
                    continue

            # Check if "nickname" is in payload and not empty string:
            if "nickname" in permission and permission["nickname"]:
                nickname = permission["nickname"]
                logger.info(
                    "Found nickname -> {} in permission definition. Determine node ID...".format(
                        nickname
                    )
                )
                node = self._otcs.getNodeFromNickname(nickname)
                node_id = self._otcs.getResultValue(node, "id")
                if not node_id:
                    logger.error("Nickname -> {} does not exist. Skipping...")
                    continue

            # Now we should have a value for node_id:
            if not node_id:
                logger.error("No node ID found! Skipping permission...")
                continue
            else:
                logger.info(
                    "Found node ID -> {} to apply permission to.".format(node_id))

            if "apply_to" in permission:
                apply_to = permission["apply_to"]
            else:
                apply_to = 2  # make item + sub-items the default

            # 1. Process Owner Permissions (list canbe empty!)
            if "owner_permissions" in permission:
                permissions = permission["owner_permissions"]
                logger.info(
                    "Update owner permissions for item -> {} to -> {}".format(
                        node_id, permissions
                    )
                )
                response = self._otcs.assignPermission(
                    node_id, "owner", 0, permissions, apply_to)
                if not response:
                    logger.error(
                        "Failed to update owner permissions for item -> {}.".format(
                            node_id)
                    )

            # 2. Process Owner Group Permissions
            if "owner_group_permissions" in permission:
                permissions = permission["owner_group_permissions"]
                logger.info(
                    "Update owner group permissions for item -> {} to -> {}".format(
                        node_id, permissions
                    )
                )
                response = self._otcs.assignPermission(
                    node_id, "group", 0, permissions, apply_to)
                if not response:
                    logger.error(
                        "Failed to update group permissions for item -> {}.".format(
                            node_id)
                    )

            # 3. Process Public Permissions
            if "public_permissions" in permission:
                permissions = permission["public_permissions"]
                logger.info(
                    "Update public permissions for item -> {} to -> {}".format(
                        node_id, permissions
                    )
                )
                response = self._otcs.assignPermission(
                    node_id, "public", 0, permissions, apply_to)
                if not response:
                    logger.error(
                        "Failed to update public permissions for item -> {}.".format(
                            node_id
                        )
                    )
                    continue

            # 3. Process Assigned User Permissions (if specified and not empty)
            if "users" in permission and permission["users"]:
                users = permission["users"]
                for user in users:
                    if not "name" in user or not "permissions" in user:
                        logger.error(
                            "Missing user name or permissions in user permission specificiation. Cannot set user permissions. Skipping..."
                        )
                        continue
                    user_name = user["name"]
                    permissions = user["permissions"]
                    otcs_user = self._otcs.getUser(user_name, True)
                    if not otcs_user or not otcs_user["data"]:
                        logger.error(
                            "Cannot find user with name -> {}; cannot set user permissions. Skipping user...".format(
                                user_name
                            )
                        )
                        continue
                    user_id = otcs_user["data"][0]["id"]
                    logger.info(
                        "Update user -> {} permissions for item -> {} to -> {}".format(
                            user_name, node_id, permissions
                        )
                    )
                    response = self._otcs.assignPermission(
                        node_id, "custom", user_id, permissions, apply_to
                    )
                    if not response:
                        logger.error(
                            "Failed to update assigned user permissions for item -> {}.".format(
                                node_id
                            )
                        )

            # 4. Process Assigned Group Permissions (if specified and not empty)
            if "groups" in permission and permission["groups"]:
                groups = permission["groups"]
                for group in groups:
                    if not "name" in group or not "permissions" in group:
                        logger.error(
                            "Missing group name or permissions in group permission specificiation. Cannot set group permissions. Skipping..."
                        )
                        continue
                    group_name = group["name"]
                    permissions = group["permissions"]
                    logger.info(
                        "Update group -> {} permissions for item -> {} to -> {}".format(
                            group_name, node_id, permissions
                        )
                    )
                    otcs_group = self._otcs.getGroup(group_name, True)
                    if not otcs_group or not otcs_group["data"]:
                        logger.error(
                            "Cannot find group with name -> {}; cannot set group permissions. Skipping group...".format(
                                group_name
                            )
                        )
                        continue
                    group_id = otcs_group["data"][0]["id"]
                    response = self._otcs.assignPermission(
                        node_id, "custom", group_id, permissions, apply_to
                    )
                    if not response:
                        logger.error(
                            "Failed to update assigned group permissions for item -> {}.".format(
                                node_id
                            )
                        )

        # end method definition

    def processAssignments(self):
        """Process assignments specified in payload and assign items (such as workspaces and
        items withnicknames) to users or groups.

        Args: None
        Return: None
        """

        for assignment in self._assignments:
            # Sanity check: we need a subject - it's mandatory:
            if not "subject" in assignment:
                logger.error(
                    "Assignment needs a subject! Skipping assignment...")
                continue
            subject = assignment["subject"]

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in assignment and not assignment["enabled"]:
                logger.info(
                    "Payload for Assignment -> {} is disabled. Skipping...".format(
                        subject)
                )
                continue

            # instruction is optional but we give a warning if they are missing:
            if not "instruction" in assignment:
                logger.warning(
                    "Assignment -> {} should have an instruction!".format(
                        subject)
                )
                instruction = ""
            else:
                instruction = assignment["instruction"]
            # Sanity check: we either need users or groups (or both):
            if not "groups" in assignment and not "users" in assignment:
                logger.error(
                    "Assignment -> {} needs groups or users! Skipping assignment...".format(
                        subject
                    )
                )
                continue
            # Check if a workspace is specified for the assignment and check it does exist:
            if "workspace" in assignment and assignment["workspace"]:
                workspace = next(
                    (item for item in self._workspaces if item["id"]
                     == assignment["workspace"]),
                    None,
                )
                if not workspace or not "nodeId" in workspace:
                    logger.error(
                        "Assignment -> {} has specified a not existing workspace -> {}! Skipping assignment...".format(
                            subject, assignment["workspace"]
                        )
                    )
                    continue
                node_id = workspace["nodeId"]
            # If we don't have a workspace then check if a nickname is specified for the assignment:
            elif "nickname" in assignment:
                response = self._otcs.getNodeFromNickname(
                    assignment["nickname"])
                node_id = self._otcs.getResultValue(response, "id")
                if not node_id:
                    # if response == None:
                    logger.error(
                        "Assignment item with nickname -> {} not found".format(
                            assignment["nickname"]
                        )
                    )
                    continue
            else:
                logger.error(
                    "Assignment -> {} needs a workspace or nickname! Skipping assignment...".format(
                        subject
                    )
                )
                continue

            assignees = []

            if "groups" in assignment:
                group_assignees = assignment["groups"]
                for group_assignee in group_assignees:
                    # find the group in the group list
                    group = next(
                        (item for item in self._groups if item["name"]
                         == group_assignee),
                        None,
                    )
                    if not group:
                        logger.error(
                            "Assignment group -> {} does not exist! Skipping group...".format(
                                group_assignee
                            )
                        )
                        continue
                    if not "id" in group:
                        logger.error(
                            "Assignment group -> {} does not have an ID. Skipping group...".format(
                                group_assignee
                            )
                        )
                        continue
                    group_id = group["id"]
                    # add the group ID to the assignee list:
                    assignees.append(group_id)

            if "users" in assignment:
                user_assignees = assignment["users"]
                for user_assignee in user_assignees:
                    # find the user in the user list
                    user = next(
                        (item for item in self._users if item["name"]
                         == user_assignee),
                        None,
                    )
                    if not user:
                        logger.error(
                            "Assignment user -> {} does not exist! Skipping user...".format(
                                user_assignee
                            )
                        )
                        continue
                    if not "id" in user:
                        logger.error(
                            "Assignment user -> {} does not have an ID. Skipping user...".format(
                                user_assignee
                            )
                        )
                        continue
                    user_id = user["id"]
                    # add the group ID to the assignee list:
                    assignees.append(user_id)

            if assignees == []:
                logger.error(
                    "Cannot add assignment -> {} for node ID -> {} because no assignee was found.".format(
                        subject, node_id
                    )
                )
                return

            response = self._otcs.assignItemToUserGroup(
                node_id, subject, instruction, assignees)
            if not response:
                logger.error(
                    "Failed to add assignment -> {} for node ID -> {} with assignees -> {}.".format(
                        subject, node_id, assignees
                    )
                )

        # end method definition

    def processUserLicenses(self, resource_name: str, license_feature: str, license_name: str ,user_specific_payload_field: str = "license"):
        """Assign a specific OTDS license feature to all Extended ECM users.

        Args:
            resource_name: name of the OTDS resource
            license_feature: license feature to assign to the user (product specific)
            license_name: Name of the license Key
            user_specific_payload_field: name of the user specific field in payload
                                         (if empty it will be ignored)
        Return: None
        """

        otds_resource = self._otds.getResource(resource_name)
        if not otds_resource:
            logger.error("OTDS Resource -> {} not found. Cannot assign licenses to users.")
            return

        user_partition = self._otcs.config()[
            "partition"]
        if not user_partition:
            logger.error(
                "OTCS user partition not found in OTDS!"
            )
            return

        for user in self._users:

            user_name = user["name"]

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in user and not user["enabled"]:
                logger.info(
                    "Payload for User -> {} is disabled. Skipping...".format(
                        user_name
                    )
                )
                continue

            if user_specific_payload_field and user_specific_payload_field in user:
                logger.info(
                    "Found specific license feature -> {} for User -> {}. Overwriting default license feature -> {}".format(
                        user[user_specific_payload_field], user_name, license_feature
                    )
                )
                user_license_feature = user[user_specific_payload_field]
            else: # use the default feature from the actual parameter
                user_license_feature = [license_feature]

            for lic_feature in user_license_feature:
                assigned_license = self._otds.assignUserToLicense(
                    user_partition,
                    user_name,  # we want the plain login name here
                    otds_resource["resourceID"],
                    lic_feature,
                    license_name
                )
                
            if not assigned_license:
                logger.error(
                    "Failed to assign license feature -> {} to user -> {}!".format(
                        license_feature, user["name"]
                    )
                )

        # end method definition

    def processExecPodCommands(self):
        """Process commands that should be executed in the Kubernetes pods.

        Args: None
        Return: None
        """

        for exec_pod_command in self._exec_pod_commands:
            if not "pod_name" in exec_pod_command:
                logger.error(
                    "To execute a command in a pod the pod name needs to be specified in the payload! Skipping to next pod command..."
                )
                continue
            pod_name = exec_pod_command["pod_name"]

            if not "command" in exec_pod_command or not exec_pod_command.get("command"):
                logger.error(
                    "Pod command is not specified for pod -> {}! It needs to be a non-empty list! Skipping to next pod command...".format(
                        pod_name)
                )
                continue
            command = exec_pod_command["command"]

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in exec_pod_command and not exec_pod_command["enabled"]:
                logger.info(
                    "Payload for Exec Pod Command in pod -> {} is disabled. Skipping...".format(pod_name))
                continue

            if not "description" in exec_pod_command:
                logger.info(
                    "Executing command -> {} in pod -> {}".format(command, pod_name))
            else:
                description = exec_pod_command["description"]
                logger.info(
                    "Executing command -> {} in pod -> {} ({})".format(command, pod_name, description))

            if not "interactive" in exec_pod_command or exec_pod_command["interactive"] == False:
                result = self._k8s.execPodCommand(pod_name, command)
            else:
                if not "timeout" in exec_pod_command:
                    result = self._k8s.execPodCommandInteractive(
                        pod_name, command)
                else:
                    timeout = exec_pod_command["timeout"]
                    result = self._k8s.execPodCommandInteractive(
                        pod_name, command, timeout)

            if result:
                logger.info(
                    "Execution of command -> {} in pod -> {} returned result -> {}".format(
                        command, pod_name, result
                    )
                )
            else:
                # It is not an error if no result is returned. It depends on the nature of the command
                # if a result is written to stdout or stderr.
                logger.info(
                    "Execution of command -> {} in pod -> {} did not return a result.".format(
                        command, pod_name, result
                    )
                )

        # end method definition

    def initSAP(self, sap_external_system: dict, direct_application_server_login: bool = True) -> object:
        """Initialize SAP object for RFC communication with SAP S/4HANA.

        Args:
            sap_external_system (dictionary): SAP external system created before
            direct_application_server_login (boolean): flag to control wether we comminicate directly with 
                                                       SAP application server or via a load balancer
        Return: sap_object
        """

        if not sap_external_system:
            return None

        username = sap_external_system["username"]
        password = sap_external_system["password"]
        # "external_system_hostname" is extracted from as_url in processExternalSystems()
        host = sap_external_system["external_system_hostname"]
        client = sap_external_system.get("client", "100")
        system_number = sap_external_system.get("external_system_number", "00")
        system_id = sap_external_system["external_system_name"]
        group = sap_external_system.get("group", "PUBLIC")
        destination = sap_external_system.get(
            "destination", "")

        logger.info("Connection parameters SAP:")
        logger.info("SAP Hostname             = " + host)
        logger.info("SAP Client               = " + client)
        logger.info("SAP System Number        = " + system_number)
        logger.info("SAP System ID            = " + system_id)
        logger.info("SAP User Name            = " + username)
        if not direct_application_server_login:
            logger.info("SAP Group Name (for RFC) = " + group)
        if destination:
            logger.info("SAP Destination          = " + destination)

        if direct_application_server_login:
            logger.info(
                "SAP Login                = Direct Application Server (ashost)")
            sap_object = sap.SAP(
                username=username,
                password=password,
                ashost=host,
                client=client,
                system_number=system_number,
                system_id=system_id,
                destination=destination
            )
        else:
            logger.info(
                "SAP Login                = Logon with load balancing (mshost)")
            sap_object = sap.SAP(
                username=username,
                password=password,
                mshost=host,
                group=group,
                client=client,
                system_number=system_number,
                system_id=system_id,
                destination=destination
            )

        return sap_object

        # end method definition

    def processSAPRFCs(self, sap_object: object):
        """Process SAP RFCs in payload and run them in SAP S/4HANA.

        Args:
            sap_object: SAP object
        Return: None
        """

        for sap_rfc in self._sap_rfcs:
            rfc_name = sap_rfc["name"]

            # Check if element has been disabled in payload (enabled = false).
            # In this case we skip the element:
            if "enabled" in sap_rfc and not sap_rfc["enabled"]:
                logger.info(
                    "Payload for SAP RFC -> {} is disabled. Skipping...".format(
                        rfc_name)
                )
                continue

            rfc_description = sap_rfc["description"] if sap_rfc.get(
                "description") else ""

            # be careful to avoid key errors as SAP RFC parameters are optional:
            rfc_params = sap_rfc["parameters"] if sap_rfc.get(
                "parameters") else {}
            if rfc_params:
                logger.info(
                    "Calling SAP RFC -> {} ({}) with parameters -> {} ...".format(
                        rfc_name, rfc_description, rfc_params
                    )
                )
            else:
                logger.info(
                    "Calling SAP RFC -> {} ({}) without parameters...".format(
                        rfc_name, rfc_description
                    )
                )

            # be careful to avoid key errors as SAP RFC parameters are optional:
            rfc_call_options = sap_rfc["call_options"] if sap_rfc.get(
                "call_options") else {}
            if rfc_call_options:
                logger.info(
                    "Using call options -> {} ...".format(
                        rfc_call_options
                    )
                )

            result = sap_object.call(rfc_name, rfc_call_options, rfc_params)
            if result == None:
                logger.error("Failed to call SAP RFC -> {}".format(rfc_name))
            else:
                logger.info(
                    "Successfully called RFC -> {}. Result -> {}".format(
                        rfc_name, result)
                )

        # end method definition

    def getPayload(self) -> dict:
        return self._payload

    def getUsers(self) -> list:
        return self._users

    def getGroups(self) -> list:
        return self._groups

    def getWorkspaces(self) -> list:
        return self._workspaces

    def getOTCSFrontend(self) -> object:
        return self._otcs_frontend

    def getOTCSBackend(self) -> object:
        return self._otcs_backend

    def getOTDS(self) -> object:
        return self._otds

    def getK8S(self) -> object:
        return self._k8s

    def getM365(self) -> object:
        return self._m365


