k8s-deepsecurity-initializer
====

Status: Experimental [Simple Example]    
  
A very simple example of setting up a Kubernetes Initialization Controller in Python.  
Big shout out to Jesse Kinkead as this example leverages his Initializer framework.  
https://github.com/allenai/kubernetes-initializer-python  

The purpose of this example is to demonstrate basic Dynamic Admission Control integration  
with Deep Security. In this example we intercept all pod deployments with a label of "jeffsbooks".  
From here we extract the deepsecurity-policy label value assigned to the deployment and then  
assign that DS policy to the single cluster node in this example.  

Note: The computer name or display name in Deep Security must match the node name returned by   
kubectl get nodes  

For testing you can run the controller outside of the cluster i.e your laptop. To support this  
just change running_in_cluster = False in ds_initializer.py

## Pre Installation Deployment
1. kubectl apply -f cluster_role.yml  #sets up service account for initializer
2. kubectl apply -f secret.yaml       #sets up DSaaS password as kubernets secret
3. update ds_initializer.py with your DSaaS username and tenant

## Installation
1. Build docker image from included Dockerfile and push to your registry of choice   
2. Update deployment/ds-initializer-deployment with the name of your docker image
3. See pre install deployment above. Deploy manifests in deployments directory. Do   
   not deploy ds-initializer.yaml until ds-initializer-deployment.yaml is up and working.  
   This sets up the admission registration.  
4. review deploment/sample-pod-deployment.yaml. The controller intercepts all deployments  
   with the name jeffsbooks and with a label of deepsecurity-policy.
   
   
## Demo Video

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/1abdcVlTJFU/0.jpg)](https://www.youtube.com/watch?v=1abdcVlTJFU)
