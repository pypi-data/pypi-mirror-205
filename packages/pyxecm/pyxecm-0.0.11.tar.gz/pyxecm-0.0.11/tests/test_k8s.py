from pyxecm.k8s import *


if __name__ == "__main__":

    # Test code is follwing...

    # Configure logging output
    logging.basicConfig(
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        datefmt="%d-%b-%Y %H:%M:%S",
        level=logging.INFO,
    )
    logger = logging.getLogger(os.path.basename(__file__))

    logger.info("Executing K8s test code...")

    k8s_object = K8s(inCluster=False, namespace="qa")

    response = k8s_object.execPodCommand(
        "otcs-admin-0", ["/bin/bash", "-c", "touch /tmp/python_was_here"])

    # response = k8s_object.execPodCommandInteractive(
    #     "otac-0", ["/bin/bash", "/etc/init.d/spawner restart"], 30
    # )

    # result = k8s.getIngress("otxecm-ingress")
    # print(result)

    # result = k8s.updateIngressBackendServices(
    #     "otxecm-ingress", "otcs", "maintenance", 80
    # )
    # print(result)

    # result = k8s.updateIngressBackendServices(
    #     "otxecm-ingress", "otcs", "otcs-frontend", 80
    # )
    # print(result)

    # otcs_frontend_service = k8s.getService("otcs-frontend")

    # otxecm_selector = otcs_frontend_service.spec.selector
    # otxecm_spec = {"spec": {"selector": otxecm_selector}}

    # maintenance_selector = {
    #     "app.kubernetes.io/component": "maintenance",
    #     "app.kubernetes.io/instance": "otxecm",
    # }
    # maintenance_spec = {"spec": {"selector": maintenance_selector}}

    # k8s.patchService("otcs-frontend", maintenance_spec)

    # print("Maintenance Mode!")

    # k8s.patchService("otcs-frontend", otxecm_spec)

    # print("Back in Production Mode!")

    # pods = k8s.listPods(
    #     labelSelector="app.kubernetes.io/component={}".format("otcs-admin")
    # )

    # print(pods)
    # config_map = k8s.getConfigMap("appworks-config-ymls")

    # sts = k8s.getStatefulSetScale("appworks")
    # replicas = sts.spec.replicas
    # logger.info("Scale -> {} to -> {} replicas".format("appworks", replicas + 1))
    # result = k8s.scaleStatefulSet("appworks", replicas + 1)
    # logger.info("Scale -> {} to -> {} replicas".format("appworks", replicas))
    # result = k8s.scaleStatefulSet("appworks", replicas)

    # logger.info("Stop OTCS Service...")

    #    result = k8s.execPodCommand(
    #        "otcs-admin-0", ["/bin/sh", "-c", "/opt/opentext/cs/stop_csserver"]
    #    )

    # logger.info("Start OTCS Service...")

    # result = k8s.execPodCommand(
    #     "otcs-admin-0", ["/bin/sh", "-c", "/opt/opentext/cs/start_csserver"]
    # )
