from pyxecm.otcs import *
from pyxecm.translate import *

if __name__ == "__main__":

    # some test code ...

    # Configure logging output
    logging.basicConfig(
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        datefmt="%d-%b-%Y %H:%M:%S",
        level=logging.DEBUG,
    )
    logger = logging.getLogger(os.path.basename(__file__))

    logger.info("Executing OTCS test code...")

    otcs = OTCS("https", "otcs.qa.terrarium.cloud",
                443, "admin", "Opentext1!")

    # we change the otcs credentials to the user:
    #otcs.setCredentials("admin", "Opentext1!")

    cookie = otcs.authenticate()
    assert cookie, f"Authentication failed - exit"

    google_translator = Translator(api_key="AIzaSyD9I5qEcuqMakYcOBKSOdCUpMtxKNahhP4", project_key="846626430249")

    root_node = otcs.getVolume(198)
    root_node_id = otcs.getResultValue(root_node, "id")

    otcs.volumeTranslator(root_node_id, google_translator, languages=["de", "fr", "it", "ja"])

    # response = otcs.downloadConfigFile("/cs/cs?func=officegroups.DownloadTeamsPackage", "/tmp/test.zip")

    # if otcs.isProxy("kurt"):
    #     logger.info("Existing proxy")
    # else:
    #     logger.info("New proxy")

    # if otcs.downloadDocument(6315, "/tmp/adam_minton.png"):
    #     logger.info("Success")
    # else:
    #     logger.info("Failure")

    # result = otcs.addDocumentVersion(35192, "/tmp/customizing.log", "customizing.log", "plain/txt", "additional python log")
    # logger.info(result)

    # response = otcs.createWorkspaceRelationship(4711, 815)
    # if response == None:
    #     logger.error("Failed to create workspace relationship.")
    # else:
    #     logger.info("Successfully created workspace relationship.")

    # response = otcs.getNodeByParentAndName(
    #     14097, "customizing.log")
    # logger.info(response)
    # node_id = otcs.getResultItem(response, "id")
    # logger.info(node_id)
    # name = otcs.getResultItem(response, "name")
    # logger.info(name)

    # if result and result["results"] and result["results"][0]:
    #     node_id = result["results"][0]["data"]["properties"]["id"]
    #     logger.info("Node ID -> {}".format(node_id))

    # response = otcs.deployTransport(
    #     "https://terrarium.blob.core.windows.net/transports-dev/Terrarium-040-Facets-Columns-Folders.zip",
    #     "Terrarium 040 Facets & Columns & Folders.zip",
    #     "Terrarium Top level folders, facets and custom columns",
    # )
    # response = otcs.importRecordsManagementSettings(
    #     "/tmp/RecordsManagementSystemSettings.xml"
    # )
    # print(response)

    # response = otcs.importRecordsManagementCodes(
    #     "/tmp/RecordsManagementCodes.xml", update_existing_codes=True
    # )
    # print(response)

    # response = otcs.importRecordsManagementRSIs(
    #     "/tmp/RecordsManagementRSIs.xml",
    #     update_existing_rsis=True,
    #     delete_schedules=False,
    # )
    # print(response)

    # response = otcs.importPhysicalObjectsSettings(
    #     "/tmp/PhysicalObjectsSystemSettings.xml"
    # )
    # print(response)

    # response = otcs.importPhysicalObjectsCodes(
    #     "/tmp/PhysicalObjectsCodes.xml", update_existing_codes=True
    # )
    # print(response)

    # response = otcs.importPhysicalObjectsLocators("/tmp/RecordsManagementRSIs.xml")
    # print(response)

    # response = otcs.importSecurityClearanceCodes("/tmp/SecurityClearanceCodes.xml")
    # print(response)

    # response = otcs.getNodeByParentAndName(2122, "Test Hold Group", False)

    # if response and response["results"]:
    #     parent_id = response["results"][0]["data"]["properties"]["id"]
    # else:
    #     result = otcs.createItem(2122, "833", "Test Hold Group")
    #     parent_id = result["results"]["data"]["properties"]["id"]

    # print(parent_id)
    # response = otcs.importRecordsManagementSettings(
    #     "/tmp/TerrariumRecordsManagementSystemSettings.xml"
    # )

    # response = otcs.importPhysicalObjectsSettings(
    #     "/opt/opentext/cs/appData/supportasset/Settings/PhysicalObjectsSystemSettings.xml"
    # )

    # response = otcs.createRecordsManagementHold(
    #     "LEGAL",
    #     "Test Hold",
    #     "This is a comment",
    #     "4711",
    #     dateToRemove="2028-12-12T00:00:00",
    # )

    # result = otcs.search(searchTerm="pump")

    # print(result)

    # result = otcs.assignPermission(
    #     2109,
    #     "custom",
    #     6361,
    #     [
    #         "see",
    #         "see_contents",
    #         # "modify",
    #         # "edit_attributes",
    #         # "add_items",
    #         # "reserve",
    #         # "add_major_version",
    #         # "delete_versions",
    #         # "delete",
    #         # "edit_permissions",
    #     ],
    #     2,
    # )

    # print(result)

    # node = otcs.getNodeByVolumeAndPath(141, ["Case Management"])

    # print(node)

    # url_item = otcs.createItem(
    #     29114, 140, "Test2", "Test Description", "https://heise.de"
    # )

    # print(url_item)

    # folder_item = otcs.createItem(
    #     parentId=2000,
    #     itemType=0,
    #     itemName="Test7",
    #     itemDescription="Description",
    #     itemFavorite=True,
    #     itemHidden=False,
    # )

    # print(folder_item)

    # shortcut_item = otcs.createItem(
    #     29114, 1, "Test Marc Shortcut", "Test Description", originalId=14266
    # )

    # print(shortcut_item)

    # user = otcs.addUser(
    #     name="mdiefenb",
    #     password="Opentext1!",
    #     firstName="Marc",
    #     lastName="Diefenbruch",
    #     email="mdiefenb@opentext.com",
    #     baseGroup=9971,
    # )

    # print(user)

    # user_id = user["id"]

    # response = otcs.addGroupMember(user_id, 9971)

    # print(response)

    # rsi_list = otcs.getRSIs()

    # now = datetime.now()

    # rsi = otcs.createRecordsManagementRSI(
    #     name="Test RSI Name",
    #     status="ACTIVE",
    #     statusDate=now.strftime("%Y-%m-%dT%H:%M:%S"),  # YYYY-MM-DDTHH:mm:ss
    #     description="Test RSI Description",
    #     subject="Test RSI Subject",
    #     title="Test RSI Title",
    #     dispcontrol=True,
    # )

    # rsi_id = rsi["results"]["id"]
    # response = otcs.createRecordsManagementRSISchedule(rsiID=rsi_id, stage="MARC-1")

    # print(response)

    # workspace_template_id = 16521

    # response = otcs.getWorkspaceRoles(workspace_template_id)

    # for roles in response["results"]:
    #     role_name = roles["data"]["properties"]["name"]
    #     role_id = roles["data"]["properties"]["id"]
    #     permissions = roles["data"]["properties"]["perms"]
    #     permission_string_list = otcs.convertPermissionValueToPermissionString(
    #         permissions
    #     )
    #     print(
    #         "Role = {}; Role ID = {}; Permissions = {}; Permission String = {}".format(
    #             role_name, role_id, permissions, permission_string_list
    #         )
    #     )

    #     permissions = otcs.convertPermissionStringToPermissionValue(
    #         permission_string_list
    #     )
    #     print(
    #         "Role = {}; Role ID = {}; Permissions = {}; Permission String = {}".format(
    #             role_name, role_id, permissions, permission_string_list
    #         )
    #     )

    #     response = otcs.assignWorkspacePermissions(
    #         workspace_template_id,
    #         role_id,
    #         permission_string_list,
    #         2,
    #     )

    # otcs.updateUserProxy(18355)

    # otcs.getWorkspaceNode(20845)

    # path = [
    #     "RM Classifications",
    #     "Case Management",
    #     "Building Authorities",
    #     "01.Buildings",
    #     "01.Building applications",
    #     "02.Alteration and repair",
    # ]
    # rm_class_node = otcs.getNodeByVolumeAndPath(198, path)

    # if rm_class_node:
    #     rm_class_node_id = rm_class_node["results"][0]["data"]["properties"]["id"]

    #     response = otcs.assignRMClassification(20365, rm_class_node_id, False)

    #     print(response)

    # response = otcs.applyConfig("./settings/CoreShareSettings.xml")

    # logger.info("Config response -> {}.".format(response))

    # response = otcs.searchUser("dfoxhoven")
    # userId = response["results"][0]["data"]["properties"]["id"]
    # response = otcs.updateUser(userId, "password", "Opentext1!")

    # otcs.setCredentials("dfoxhoven", "Opentext1!")
    # cookie = otcs.authenticate()
    # assert cookie, (f"Authentication failed - exit")

    # response = otcs.addFavorite(14715)

    # logger.info("Added favorite for node ID -> {}.".format(14715))

    # otcs.getWorkspaceTypes()

    # category_payload = {"categories": { "7081": {"7081_28": "50031", "7081_38": "0000050031", "7081_29": "Global Trade AG", "7081_30": "Gutleutstraße 53", "7081_34": "Frankfurt", "7081_31": "Germany", "7081_32": "60329", "7081_37": "Retail", "7081_33": "1000", "7081_25": "Customer", "7081_1": {"version_number": 1}}}}

    # otcs.createWorkspace(11840, "Test", "Description", 17, category_payload)

    # package_path = os.path.abspath( os.path.dirname( __file__ ) )+'/package'
    # all_packages =  os.listdir(package_path)
    # all_packages.sort()
    # logger.info("Deploying transport packages -> {}".format(all_packages))
    # for package in all_packages:
    #    otcs.deployTransportPackage(package_path+"/"+package)

    # for file in admin_settings_files:
    #     apply = otcs.applyConfig(file)
