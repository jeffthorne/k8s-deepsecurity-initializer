"""
A very simple example of setting up a Kubernetes Initialization Controller in Python.
Big shout out to Jesse Kinkead as this example leverages his Initializer framework.
https://github.com/allenai/kubernetes-initializer-python

The purpose of this example is to demonstrate basic Dynamic Admission Control integration
with Deep Security. In this example we intercept all pod deployments with a label of "jeffsbooks".
From here we extract the deepsecurity-policy label value assigned to the deployment and then
assign that DS policy to the single cluster node in this example.

Note: The computer name or display name in Deep Security must match the node name returned by kubectl get nodes

"""

import kubernetes

from ai2.kubernetes.initializer import (InitializerController, ResourceHandler, SimpleResourceController, Rejection)
from dsp3.models.manager import Manager

from controller.utils import assign_cluster_policy
from controller.main_loop import main_loop
from controller import logger
from controller.utils import get_ds_password

running_in_cluster = True

if running_in_cluster:
    kubernetes.config.load_incluster_config()  # or load config in cluster
else:
    kubernetes.config.load_kube_config() # Load the Kubernetes configuration from your local kubeconfig file.


v1 = kubernetes.client.CoreV1Api()
password = get_ds_password(v1)   #password store as k8s secret. See deployment/secret.yaml
dsm = Manager(username="username", password=password, tenant='tenant')


def main():
    """
    Runs a controller that looks for pods with a label deepsecurity-policy then confirms that policy is assigned to
    cluster nodes.

    Note: this is only a simplistic demonstration of a basic initializer and was tested against DSaaS.
    """

    def handle_item(item):
        """
        Requires that the given item have a non-empty 'deepsecurity-policy' label.

        Args:
            item: A Kubernetes object with standard metadata attached.
        """

        if item.metadata.name == "jeffsbooks":
            if 'deepsecurity-policy' in item.metadata.labels:
                logger.info(item.metadata)
                policy_name = item.metadata.labels['deepsecurity-policy']
                assign_cluster_policy(dsm, policy_name, item)
            else:
                raise Rejection("Label 'deepsecurity-policy' missing from {}:{}".format(item.metadata.namespace, item.metadata.name), 'MissingPolicy')

        return item   #We aren't changing any data, so simply return the item.

    def build_initializer(api_client: kubernetes.client.api_client.ApiClient):
        """
        Creates a deployment interception controller. Interception action is spefified through custom item handler.

        :param api_client: kubernetes.client.api_client.ApiClient
        :return: ai2.kubernetes.initializer.initializer_controller.InitializerController
        """
        deployment_controller = SimpleResourceController(ResourceHandler.deployment_handler(api_client), handle_item)
        all_controllers = [deployment_controller]

        # The name here should match what you've configured in your InitializerConfiguration eg ds_initializer.yaml.
        return InitializerController('ds.required.example', all_controllers)

    try:
        main_loop(build_initializer)
    except Exception:
        main_loop(build_initializer)


if __name__ == '__main__':

    main()
