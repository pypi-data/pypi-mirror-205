from pyxecm.otds import *


if __name__ == "__main__":
    # some test code

    # Configure logging output
    logging.basicConfig(
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        datefmt="%d-%b-%Y %H:%M:%S",
        level=logging.DEBUG,
    )
    logger = logging.getLogger(os.path.basename(__file__))

    otds = OTDS("https", "otds.qa.terrarium.cloud", 443, "admin", "Opentext1!")

    cookie = otds.authenticate()
    logger.info("Cookie -> {}".format(cookie))

    response = otds.getGroup("Sales")
    print(response)

    # response = otds.getUser("Content Server Members", "nwheeler")
    # print(response)

    # response = otds.updateUser(
    #     "Content Server Members", "nwheeler", "displayName", "Nick Wheeler")
    # print(response)

    # result = otds.getOauthClient("salesforce")

    # print(result)

    # logger.info(
    #     "password -> {}, user -> {}, hostname -> {}".format(
    #         otds.config()["password"],
    #         otds.config()["username"],
    #         otds.config()["publicHostname"],
    #     )
    # )

    # logger.info(
    #     "otdsCredentialUrl -> {}, otdsOauthClientUrl -> {}".format(
    #         otds.credentialUrl(), otds.oauthClientUrl()
    #     )
    # )

    # response = otds.updateUser(
    #     "Content Server Members",
    #     "nwheeler",
    #     "oTExtraAttr0",
    #     "nwheeler_terrarium01@opentext.com",
    # )

    # print(response)

    # response = otds.getOauthClient("SalesforceManual")
    # print(response)

    # response = otds.addOauthClient(
    #     client_id="salesforce",
    #     description="Salesforce OAuth client",
    #     redirectURLs=["https://heise.de"],
    #     allowImpersonation=True,
    #     confidential=True,
    #     authScopes=None,  # empty string = "Global"
    #     allowedScopes=["full"],  # in OTDS UI: Permissible scopes
    #     defaultScopes=["full"],
    # )

    # print(response)

    # response = otds.addAuthHandlerOAuth(
    #     name="Salesforce",
    #     description="Salesforce OAuth Handler",
    #     provider_name="Salesforce",
    #     client_id="1234567890",
    #     client_secret="abcdefghijklmnopqrstuvwxyz",
    #     activeByDefault=False,
    #     authorizationEndpoint="https://idea02-dev-ed.my.salesforce.com/services/oauth2/authorize",
    #     tokenEndpoint="https://idea02-dev-ed.my.salesforce.com/services/oauth2/token",
    # )

    # print(response)

    # if cookie:
    #     result = otds.updateAccessRoleAttributes(
    #         "Access to awp", [{"name": "pushAllGroups", "values": ["True"]}]
    #     )

    #     print(result)

    # if cookie:
    #     response = otds.addAuthHandlerSAP("TM7", "Test", "/tmp/TM6_Sandbox.pse", "")

    #     print(response)
