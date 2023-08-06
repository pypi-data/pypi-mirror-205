"""
Kubernetes Module to implement functions to read / write Kubernetes objects
such as Pods, Stateful Sets, Config Maps, ...

https://github.com/kubernetes-client/python/blob/master/kubernetes/README.md
https://github.com/kubernetes-client/python/tree/master/examples

Class: K8s
Methods:

__init__ : class initializer
getCoreV1Api : get Kubernetes API object for Core APIs
getAppsV1Api : get Kubernetes API object for Applications (e.g. Stateful Sets)
getNetworkingV1Api : get Kubernetes API object for Networking (e.g. Ingress)

getNamespace : get the Kubernetes Namespace the K8s object is configured for

getPod : get a Kubernetes Pod based on its name
listPods : get a list of Kubernetes Pods based on field and label selectors
execPodCommand : execute a list of commands in a Kubernetes Pod
execPodCommendInteractive: write commands to stdin and wait for response
deletePod: delete a running pod (e.g. to make Kubernetes restart it)

getConfigMap : get a Kubernetes Config Map based on its name
listConfigMaps : get a list of Kubernetes Config Maps based on field and label selectors
findConfigMap : find a Kubernetes Config Map based on its name
replaceConfigMap : replace the data body of a Kubernetes Config Map

getStatefulSet : get a Kubernetes Stateful Set based on its name
getStatefulSetScale : get the number of replicas for a Kubernetes Stateful Set
patchStatefulSet : update the specification of a Kubernetes Stateful Set
scaleStatefulSet : change number of replicas for a Kubernetes Stateful Set

getService : get a Kubernetes Service based on its name
listServices : get a list of Kubernetes Services based on field and label selectors
patchService : update the specification of a Kubernetes Service

getIngress : get a Kubernetes Ingress based on its name
patchIngress : update the specification of a Kubernetes Ingress
updateIngressBackendServices: replace the backend service and port for an ingress host

"""

__author__ = "Dr. Marc Diefenbruch"
__copyright__ = "Copyright 2023, OpenText"
__credits__ = ["Kai-Philip Gatzweiler"]
__maintainer__ = "Dr. Marc Diefenbruch"
__email__ = "mdiefenb@opentext.com"

import os
import logging
import time
from kubernetes import client, config
from kubernetes.stream import stream
from kubernetes.client.exceptions import ApiException, ApiValueError

# Configure Kubernetes API authentication to use pod serviceAccount
# config.load_incluster_config()

logger = logging.getLogger(os.path.basename(__file__))


class K8s(object):
    """Used to automate stettings in Kubernetes."""

    _core_v1_api = None
    _apps_v1_api = None
    _networking_v1_api = None
    _namespace = None

    def __init__(self, inCluster: bool = True, namespace: str = ""):
        """Initialize the Kubernetes object."""

        # Configure Kubernetes API authentication to use pod serviceAccount
        if inCluster:
            config.load_incluster_config()
        else:
            config.load_kube_config()

        self._core_v1_api = client.CoreV1Api()
        self._apps_v1_api = client.AppsV1Api()
        self._networking_v1_api = client.NetworkingV1Api()
        if namespace:
            self._namespace = namespace
        else:
            # Read current namespace
            with open(
                "/var/run/secrets/kubernetes.io/serviceaccount/namespace", "r"
            ) as f:
                self._namespace = f.read()

    def getCoreV1Api(self):
        return self._core_v1_api

    def getAppsV1Api(self):
        return self._apps_v1_api

    def getNetworkingV1Api(self):
        return self._networking_v1_api

    def getNamespace(self):
        return self._namespace

    def getPod(self, podName: str):
        """getPod: get a pod in the configured namespace (the namespace is defined in the class constructor).
        Args:
            podName (string): name of the Kubernetes pod in the current namespace
        Return: V1Pod (object):
                api_version='v1',
                kind='Pod',
                metadata=V1ObjectMeta(...),
                spec=V1PodSpec(...),
                status=V1PodStatus(...)
        """

        try:
            response = self.getCoreV1Api().read_namespaced_pod(
                name=podName, namespace=self.getNamespace()
            )
        except ApiException as e:
            logger.error("Failed to get Pod -> {}; error -> {}".format(podName, str(e)))
            return None

        return response

    def listPods(self, fieldSelector: str = "", labelSelector: str = ""):
        """listPods: list all Kubernetes pods in a given namespace. The list can be further restricted
                     by specifying a field or label selector.
        Args:
            podName (string): name of the Kubernetes pod in the current namespace
            conditionName (string): name of the condition, e.g. "Ready"
        Return: V1PodList (object):
                api_version: The Kubernetes API version.
                items: A list of V1Pod objects, each representing a pod. You can access the fields of a
                       V1Pod object using dot notation, for example, pod.metadata.name to access the name of the pod
                kind: The Kubernetes object kind, which is always "PodList".
                metadata: Additional metadata about the pod list, such as the resource version.
        """

        try:
            response = self.getCoreV1Api().list_namespaced_pod(
                field_selector=fieldSelector,
                label_selector=labelSelector,
                namespace=self.getNamespace(),
            )
        except ApiException as e:
            logger.error(
                "Failed to list Pods with field_selector -> {} and label_selector -> {}; error -> {}".format(
                    fieldSelector, labelSelector, str(e)
                )
            )
            return None

        return response

    def waitPodCondition(self, podName: str, conditionName: str):
        """waitPodCondition: wait for the pod to reach a defined condition (e.g. "Ready").
        Args:
            podName (string): name of the Kubernetes pod in the current namespace
            conditionName (string): name of the condition, e.g. "Ready"
        Return: True once the pod reaches the condition - otherwise wait forever
        """

        ready = False
        while not ready:
            try:
                pod_status = self.getCoreV1Api().read_namespaced_pod_status(
                    podName, self.getNamespace()
                )

                # Check if the pod has reached the defined condition:
                for cond in pod_status.status.conditions:
                    if cond.type == conditionName and cond.status == "True":
                        logger.info(
                            "Pod -> {} is in state -> {}!".format(
                                podName, conditionName
                            )
                        )
                        ready = True
                        break
                else:
                    logger.info(
                        "Pod -> {} is not yet in state -> {}. Waiting...".format(
                            podName, conditionName
                        )
                    )
                    time.sleep(30)
                    continue

            except ApiException as e:
                logger.error(
                    "Failed to wait for pod -> {}; error -> {}".format(podName, str(e))
                )

    # end method definition

    def execPodCommand(self, podName: str, command: list):
        """execPodCommand: execute a command inside a Kubernetes pod (similar to kubectl exec on command line).
        Args:
            podName (string): name of the Kubernetes pod in the current namespace
            command (list): list of command and its parameters, e.g. ["/bin/bash", "-c", "pwd"]
                            The "-c" is required to make the shell executing the command.
        Return: response of the command or None if the call fails
        """

        pod = self.getPod(podName)
        if not pod:
            logger.error("Pod -> {} does not exist".format(podName))

        logger.info(
            "Execute command -> {} in pod -> {}".format(command, podName))

        try:
            response = stream(
                self.getCoreV1Api().connect_get_namespaced_pod_exec,
                podName,
                self.getNamespace(),
                command=command,
                stderr=True,
                stdin=False,
                stdout=True,
                tty=False,
            )
        except ApiException as e:
            logger.error(
                "Failed to execute command -> {} in pod -> {}; error -> {}".format(
                    command, podName, str(e)
                )
            )
            return None

        return response

    # end method definition

    # Some commands like the OTAC spawner need to run interactive - otherwise the command "hangs"
    def execPodCommandInteractive(self, podName: str, commands: list, timeout: int = 30, writeStderrToErrorLog: bool = True):
        """execPodCommandInteractive: execute a command inside a Kubernetes pod (similar to kubectl exec on command line).
                                      Other than execPodCommand() method above this is an interactive execution using
                                      stdin and reading the output from stdout and stderr. This is required for longer
                                      running commands. It is currently used for restarting the spawner of Archive Center.
                                      The output of the command is pushed into the logging.
        Args:
            podName (string): name of the Kubernetes pod in the current namespace
            commands (list): list of command and its parameters, e.g. ["/bin/bash", "/etc/init.d/spawner restart"]
                             Here we should NOT have a "-c" parameter!
            timeout (integer): timeout duration that is waited for any response. 
                               Each time a resonse is found in stdout or stderr we wait another timeout duration
                               to make sure we get the full output of the command.
            writeStderrToErrorLog (boolean): flag to control if output in stderr should be written to info or error log stream.
                                             Default is write to error log (True)
        Return: response of the connect_get_namespaced_pod_exec() or None if the call fails
        """

        pod = self.getPod(podName)
        if not pod:
            logger.error("Pod -> {} does not exist".format(podName))

        if not commands:
            return None

        # Get first command - this should be the shell:
        command = commands.pop(0)

        try:
            response = stream(
                self.getCoreV1Api().connect_get_namespaced_pod_exec,
                podName,
                self.getNamespace(),
                command=command,
                stderr=True,
                stdin=True,  # This is important!
                stdout=True,
                tty=False,
                _preload_content=False  # This is important!
            )
        except ApiException as e:
            logger.error(
                "Failed to execute command -> {} in pod -> {}; error -> {}".format(
                    command, podName, str(e)
                )
            )
            return None

        while response.is_open():
            got_response = False
            response.update(timeout=timeout)
            if response.peek_stdout():
                logger.info(response.read_stdout().replace("\n", " "))
                got_response = True
            if response.peek_stderr():
                if writeStderrToErrorLog:
                    logger.error(response.read_stderr().replace("\n", " "))
                else:
                    logger.info(response.read_stderr().replace("\n", " "))
                got_response = True
            if commands:
                command = commands.pop(0)
                logger.info(
                    "Execute command -> {} in pod -> {}".format(command, podName))
                response.write_stdin(command + "\n")
            else:
                # We continue as long as we get some response during timeout period
                if not got_response:
                    break

        response.close()

        return response

    # end method definition

    def deletePod(self, podName: str):
        """deletePod: delete a pod in the configured namespace (the namespace is defined in the class constructor).
        Args:
            podName (string): name of the Kubernetes pod in the current namespace
        Return: V1Status (object):
                api_version: The Kubernetes API version.
                kind: The Kubernetes object kind, which is always "Status".
                metadata: Additional metadata about the status object, such as the resource version.
                status: The status of the operation, which is either "Success" or an error status.
                message: A human-readable message explaining the status.
                reason: A short string that describes the reason for the status.
                code: An HTTP status code that corresponds to the status.
        """

        pod = self.getPod(podName)
        if not pod:
            logger.error("Pod -> {} does not exist".format(podName))

        try:
            response = self.getCoreV1Api().delete_namespaced_pod(
                podName, namespace=self.getNamespace()
            )
        except ApiException as e:
            logger.error(
                "Failed to delete Pod -> {}; error -> {}".format(podName, str(e))
            )
            return None

        return response

    # end method definition

    def getConfigMap(self, configMapName: str):
        """getConfigMap: get a config map in the configured namespace (the namespace is defined in the class constructor).
        Args:
            configMapName (string): name of the Kubernetes config map in the current namespace
        Return: V1ConfigMap (object) that includes these fields:
                api_version: The Kubernetes API version.
                metadata: A V1ObjectMeta object representing metadata about the V1ConfigMap object,
                          such as its name, labels, and annotations.
                data: A dictionary containing the non-binary data stored in the ConfigMap,
                      where the keys represent the keys of the data items and the values represent
                      the values of the data items.
                binary_data: A dictionary containing the binary data stored in the ConfigMap,
                             where the keys represent the keys of the binary data items and the values
                             represent the values of the binary data items. Binary data is encoded as base64
                             strings in the dictionary values.
        """

        try:
            response = self.getCoreV1Api().read_namespaced_config_map(
                name=configMapName, namespace=self.getNamespace()
            )
        except ApiException as e:
            logger.error("Failed to get Config Map -> {}; error -> {}".format(str(e)))
            return None

        return response

    # end method definition

    def listConfigMaps(self, fieldSelector: str = "", labelSelector: str = ""):
        try:
            response = self.getCoreV1Api().list_namespaced_config_map(
                field_selector=fieldSelector,
                label_selector=labelSelector,
                namespace=self.getNamespace(),
            )
        except ApiException as e:
            logger.error(
                "Failed to list Config Maps with field_selector -> {} and label_selector -> {}; error -> {}".format(
                    fieldSelector, labelSelector, str(e)
                )
            )
            return None

        return response

    # end method definition

    def findConfigMap(self, configMapName: str):
        try:
            response = self.listConfigMaps(
                fieldSelector="metadata.name={}".format(configMapName)
            )
        except ApiException as e:
            logger.error(
                "Failed to find Config Map -> {}; error -> {}".format(
                    configMapName, str(e)
                )
            )
            return None

        return response

    # end method definition

    def replaceConfigMap(self, configMapName: str, configMapData: dict):
        try:
            response = self.getCoreV1Api().replace_namespaced_config_map(
                name=configMapName,
                namespace=self.getNamespace(),
                body=client.V1ConfigMap(
                    metadata=client.V1ObjectMeta(
                        name=configMapName,
                    ),
                    data=configMapData,
                ),
            )
        except ApiException as e:
            logger.error(
                "Failed to replace Config Map -> {}; error -> {}".format(
                    configMapName, str(e)
                )
            )
            return None

        return response

    # end method definition

    def getStatefulSet(self, stsName: str):
        try:
            response = self.getAppsV1Api().read_namespaced_stateful_set(
                name=stsName, namespace=self.getNamespace()
            )
        except ApiException as e:
            logger.error(
                "Failed to get Stateful Set -> {}; error -> {}".format(stsName, str(e))
            )
            return None

        return response

    # end method definition

    def getStatefulSetScale(self, stsName: str):
        try:
            response = self.getAppsV1Api().read_namespaced_stateful_set_scale(
                name=stsName, namespace=self.getNamespace()
            )
        except ApiException as e:
            logger.error(
                "Failed to get scaling (replicas) of Stateful Set -> {}; error -> {}".format(
                    stsName, str(e)
                )
            )
            return None

        return response

    # end method definition

    def patchStatefulSet(self, stsName: str, stsBody: dict):
        """patchStatefulSet: patch a Stateful set with new values
        Args:
            stsName (string): name of the Kubernetes stateful set in the current namespace
            stsBody (string): patch string
        Return: response of the Kubernetes patch command or None if the call fails
        """

        try:
            response = self.getAppsV1Api().patch_namespaced_stateful_set(
                name=stsName, namespace=self.getNamespace(), body=stsBody
            )
        except ApiException as e:
            logger.error(
                "Failed to patch Stateful Set -> {} with -> {}; error -> {}".format(
                    stsName, stsBody, str(e)
                )
            )
            return None

        return response

    # end method definition

    def scaleStatefulSet(self, stsName: str, scale: int):
        """scaleStatefulSet: scale a stateful set to a specific number of replicas. It uses the class method patchStatefulSet() above.
        Args:
            stsName (string): name of the Kubernetes stateful set in the current namespace
        Return: response of the Kubernetes patch command or None if the call fails
        """

        try:
            response = self.patchStatefulSet(
                stsName, stsBody={"spec": {"replicas": scale}}
            )
        except ApiException as e:
            logger.error(
                "Failed to scale Stateful Set -> {} to -> {} replicas; error -> {}".format(
                    stsName, scale, str(e)
                )
            )
            return None

        return response

    # end method definition

    def getService(self, serviceName: str):
        """getService: gets a Kubernetes service with a defined name in the
        current namespace
        Args:
            serviceName (string): name of the Kubernetes service in the current namespace
        Return: <class 'kubernetes.client.models.v1_service.V1Service'> or None if the call fails
                This is NOT a dict but an object - the you have to use the "." syntax to access to returned elements
        """

        try:
            response = self.getCoreV1Api().read_namespaced_service(
                name=serviceName, namespace=self.getNamespace()
            )
        except ApiException as e:
            logger.error(
                "Failed to get Service -> {}; error -> {}".format(serviceName, str(e))
            )
            return None

        return response

    def listServices(self, fieldSelector: str = "", labelSelector: str = ""):
        """listServices: lists all Kubernetes Service in the current namespace.
                         The list can be filtered by providing field selectors and
                        label selectors.
        Args:
            fieldSelector (string): filter result based on fields
            labelSelector (string): filter result based on labels
        Return: Object of <class 'kubernetes.client.models.v1_service_list.V1ServiceList'> or None if the call fails
                This is NOT a dict but an object - you have to use the "." syntax to access to returned elements
        """
        try:
            response = self.getCoreV1Api().list_namespaced_service(
                field_selector=fieldSelector,
                label_selector=labelSelector,
                namespace=self.getNamespace(),
            )
        except ApiException as e:
            logger.error(
                "Failed to list Services with field_selector -> {} and label_selector -> {}; error -> {}".format(
                    fieldSelector, labelSelector, str(e)
                )
            )
            return None

        return response

    # end method definition

    def patchService(self, serviceName: str, serviceBody: dict):
        """patchService: patches a Kubernetes Service with an updated spec
        Args:
            serviceName (string): name of the Kubernetes Ingress in the current namespace
            serviceBody (dict): new / updated Service body spec (will be merged with existing values)
        Return: Object of <class 'kubernetes.client.models.v1_service.V1Service'> or None if the call fails
                This is NOT a dict but an object - you have to use the "." syntax to access to returned elements
        """

        try:
            response = self.getCoreV1Api().patch_namespaced_service(
                name=serviceName, namespace=self.getNamespace(), body=serviceBody
            )
        except ApiException as e:
            logger.error(
                "Failed to patch Service -> {} with -> {}; error -> {}".format(
                    serviceName, serviceBody, str(e)
                )
            )
            return None

        return response

    # end method definition

    def getIngress(self, ingressName: str):
        """getIngress: gets a Kubernetes Ingress with a defined name in the
        current namespace
        Args:
            ingressName (string): name of the Kubernetes Ingress in the current namespace
        Return: Object of <class 'kubernetes.client.models.v1_ingress.V1Ingress'> or None if the call fails
                This is NOT a dict but an object - the you have to use the "." syntax to access to returned elements
        """

        try:
            response = self.getNetworkingV1Api().read_namespaced_ingress(
                name=ingressName, namespace=self.getNamespace()
            )
        except ApiException as e:
            logger.error(
                "Failed to get Ingress -> {}; error -> {}".format(ingressName, str(e))
            )
            return None

        return response

    # end method definition

    def patchIngress(self, ingressName: str, ingressBody: dict):
        """patchIngress: patches a Kubernetes Ingress with a updated spec
        Args:
            ingressName (string): name of the Kubernetes Ingress in the current namespace
            ingressBody (dict): new / updated ingress body spec (will be merged with existing values)
        Return: Object of <class 'kubernetes.client.models.v1_ingress.V1Ingress'> or None if the call fails
                This is NOT a dict but an object - you have to use the "." syntax to access to returned elements
        """

        try:
            response = self.getNetworkingV1Api().patch_namespaced_ingress(
                name=ingressName,
                namespace=self.getNamespace(),
                body=ingressBody,
            )
        except ApiException as e:
            logger.error(
                "Failed to patch Ingress -> {} with -> {}; error -> {}".format(
                    ingressName, ingressBody, str(e)
                )
            )
            return None

        return response

    # end method definition

    def updateIngressBackendServices(
        self, ingressName: str, hostname: str, serviceName: str, servicePort: int
    ):
        """updateIngressBackendService: updates a backend service and port of an Kubernetes Ingress

        "spec": {
            "rules": [
                {
                    "host": host,
                    "http": {
                        "paths": [
                            {
                                "path": "/",
                                "pathType": "Prefix",
                                "backend": {
                                    "service": {
                                        "name": <serviceName>,
                                        "port": {
                                            "name": None,
                                            "number": <servicePort>,
                                        },
                                    },
                                },
                            }
                        ]
                    },
                }
            ]
        }

        Args:
            ingressName (string): name of the Kubernetes Ingress in the current namespace
            hostname (string): hostname that should get an updated backend service / port
            serviceName (string): new backend service name
            servicePort (int): new backend service port
        Return: Object of <class 'kubernetes.client.models.v1_ingress.V1Ingress'> or None if the call fails
                This is NOT a dict but an object - you have to use the "." syntax to access to returned elements
        """

        ingress = self.getIngress(ingressName)
        if not ingress:
            return None

        host = ""
        rules = ingress.spec.rules
        rule_index = 0
        for rule in rules:
            if hostname in rule.host:
                host = rule.host
                path = rule.http.paths[0]
                backend = path.backend
                service = backend.service

                logger.info(
                    "Replace backend service -> {} ({}) with new backend service -> {} ({})".format(
                        service.name, service.port.number, serviceName, servicePort
                    )
                )

                service.name = serviceName
                service.port.number = servicePort
                break
            else:
                rule_index += 1

        if not host:
            logger.error("Cannot find host -> {}.")
            return None

        body = [
            {
                "op": "replace",
                "path": "/spec/rules/{}/http/paths/0/backend/service/name".format(
                    rule_index
                ),
                "value": serviceName,
            },
            {
                "op": "replace",
                "path": "/spec/rules/{}/http/paths/0/backend/service/port/number".format(
                    rule_index
                ),
                "value": servicePort,
            },
        ]

        return self.patchIngress(ingressName, body)

    # end method definition
