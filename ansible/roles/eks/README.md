# eks

The eks role creates an EKS cluster with associated worker nodes

## Prerequisites

### Linked service role

Currently there is no way to create service linked roles with Ansible

```
aws iam create-service-linked-role --aws-service-name=eks.amazonaws.com
```

### key pair

Reasonable defaults are set for most values but in particular, the file
`~/.ssh/{{ eks_key_file }}.pub` must exist. `eks_key_file` defaults to
the value of `eks_cluster_name`, by default `ansiblefest2018`. Either create
an ssh key pair to match these defaults or change the value of `eks_key_file`
to match an existing key. This file is then used to create a key called
`eks_key_name`, which defaults to the value of `eks_key_file`.

### botocore

botocore must be 1.10.32 or above. Upgrading AWS CLI or boto3 will both
upgrade botocore.

### kubectl

kubectl must be 1.10.0+ to work with aws-iam-authenticator

### aws-iam-authenticator

Install the aws-iam-authenticator using the instructions at
https://docs.aws.amazon.com/eks/latest/userguide/getting-started.html#eks-prereqs

### openshift library

Very very bleeding edge right now (should be fixed soonish)
* openshift from https://github.com/openshift/openshift-restclient-python/pull/196
* kubernetes python client with base updated to https://github.com/kubernetes-client/python-base/pull/75/files
