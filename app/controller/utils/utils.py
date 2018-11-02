import json
import base64
from .kube_interface import KubeInterface


def assign_cluster_policy(dsm, policy_name):
    ids = dshosts_that_map_to_kubenodes(dsm)
    profile = dsm.get_security_profile_by_name(policy_name)

    for id in ids:
        dsm.security_profile_assign_to_host(profile['ID'], id)

    dsm.host_update_now(ids)


def dshosts_that_map_to_kubenodes(dsm):
    ids = []
    kube_interface = KubeInterface()
    ds_hosts = dsm.host_retrieve_all()
    kube_nodes = kube_interface.get_nodes()

    for node in kube_nodes:
        for address in node.addresses:
            exists = [x for x in ds_hosts if x['displayName'] == address or x['name'] == address]

            if exists and exists[0]:
                ids.append(exists[0]['ID'])

    return ids

def get_ds_password(kube_api):
    secrets = kube_api.list_secret_for_all_namespaces().items
    password = None
    for secret in secrets:
        if secret.metadata.name == 'deepsecurity-password':
            password = base64.b64decode(secret.data['password']).decode('utf-8')

    return password