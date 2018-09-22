% Making Kubernetes Easy With Ansible
% Will Thames, Skedulo
%# October 2018

---

# Making Kubernetes Easy With Ansible
## Will Thames, Skedulo
### October 2018

<div class="image-left"><image src="images/ansible.png"></div>
<div class="image-right"><image src="images/kubernetes.png"></div>

---

# Contents

- Introduction
- About Kubernetes
- Managing Kubernetes with Ansible

---

# Motivation

---

FIXME: replace with Ansible's slide

# About me

- Ansible contributor since July 2012
- Author of ansible-lint, ansible-review, ansible-inventory-grapher
- Mostly AWS-related contributions but lately a lot of Kubernetes

---

# About Skedulo

- Skedulo is the platform for intelligent mobile workforce management
- Helps enterprises intelligently manage, schedule, dispatch, and track
  workers in the field
- Typical use-cases include healthcare, home services



---

# Live Demo

- Create a brand new Kubernetes cluster in AWS' Elastic Kubernetes Service
- Demonstrate some of the best practices for Kubernetes configuration management
- Starts now! (10+ minutes to fire up EKS)

---

# What's not in this talk

- explicit comparisons with other Kubernetes configuration management (e.g. Helm)
- explicit comparisons with other configuration management tools (chef, puppet, etc)
- Much about Kubernetes *cluster* management
- Add ons to Kubernetes
- Datastore management

<aside class="notes">
use GKE, AKS, EKS or something like kops
</aside>

---

# About Kubernetes

* Kubernetes is a management framework for distributed clusters
  of container instances
* Kubernetes continually runs a reconciliation loop to ensure
  the cluster is in the desired state and corrects it if possible
  if not

---

# Important Kubernetes resources

* Pod - unit of compute containing one or more containers,
  each running their own particular image version with their
  individual configuration
* Deployments - ensure that the right number of replicas of
  a Pod are running, and that upgrades from one Pod specification
  to a new one are handled correctly

<aside class="notes">
* e.g. environment variables, volume mounts
* e.g. rolling update, replace in place
</aside>

---

# Important Kubernetes resources

* ConfigMap - one or more configuration items in a dict. Useful
  for setting environment variables or declaring entire configuration
  files for a Pod
* Secret - similar to ConfigMap but better protected from casual view.
* Service - allows inbound traffic from other Pods
* Ingress - allows inbound traffic to a Service from outside the cluster

---

# Welcome to the bleeding edge

- A lot of the functionality used here is in Ansible 2.7
- Some of the functionality mentioned here won't be out until 2.8
- EKS communication relies on kubernetes python client 7.X FIXME
- Features from openshift 0.7.Y are also mentioned FIXME


---

# Ansible's Kubernetes strengths

- Templating
- Hierarchical inventory
- Secrets management
- Modules, lookup plugins, filter plugins

---

# Anti-pattern: using kubectl in playbooks

- `kubectl` is *awesome*
- But all the usual caveats to running commands apply<sup>&dagger;</sup>
- You have to do a template/kubectl/delete dance

<div class="footer">
<sup>&dagger;</sup><a href="http://willthames.github.io/2016/09/21/using-command-and-shell-in-ansible.html">
Using Ansible's `shell` and `command` modules properly</a>

<aside class="notes">
if it has a feature that the `k8s` module does not, that can
be considered a bug
</aside>

---

# Are there reasons to use kubectl?

- `kubectl` does validation (`k8s` should in 2.8)
- `kubectl` can append hashes to ConfigMaps and Secrets to make
  them immutable (`k8s` should have this in 2.8)
- ad-hoc tasks:
  ```
  kubectl get configmap -n some-namespace some-config-map
  ansible -m k8s_facts -a 'namespace=some-namespace kind=ConfigMap api_version=v1 name=some-config-map' localhost
  ```

---

# Reuse

- Our goal is to use as much common code for Kubernetes management
  as possible.
- A single Ansible role that takes a set of
  resource manifests and ensures that Kubernetes meets those expectations
- Ideally, one manifest template that works for most applications would be
  great, but harder.
- At the very least, manifests should be reusable across all environments.

---

# Templating

* Templates are super-powerful
* Use as few control structures as possible
  ```
  replicas = {% 5 if env == 'prod' else 1 %}
  ```
  vs
  ```
  replicas = {{ kube_deployment_replicas }}
  ```

---

# Templating dicts

Sometimes whole sections of manifests differ between environment
(e.g. if one environment needs annotations for certificates and one doesn't)

```
annotations:
  all_envs: have this annotation
  this_one: is only in some environments
```

```
metadata:
  annotations:
    {{ annotations | to_nice_yaml(indent=2) | indent=4 }}
```

---

# Hierarchical inventory

* Some variables are the same across many applications within an environment
* Some variables are the same across all environments for an application
* Some variables can be composed from other variables
* Some variables may need specific overrides for certain application/environment
  combinations
* All of these needs are met by inventory groups

<aside class="notes">
* e.g. the hostname of a particular database instance
* e.g. the name of a datastore within a database
* e.g. if you know the domain name for an environment, working out the fully qualified
  hostname can be easy
</aside>

---

# Avoiding `hosts: localhost`

* Typically people will use `hosts: localhost` to talk to Kubernetes
* This reduces the power of inventory and reuse:

FIXME: flat inventory vs structured inventory



# Using the runner pattern

* Runner pattern uses hosts declarations like `hosts: "{{ env }}-{{ app }}-runner"`
  with e.g. `-e env=test -e app=web`.
* Suitable inventory group hierarchies allow such hosts to gather their inventory
  from groups such as `test`, `web` and `test-web`, as well as the `runner` group
* Set `ansible_connection: local` and `ansible_python_interpreter: "{{ ansible_playbook_python }}"`
  in the `runner` group_vars file.


---

# Generating inventory

For every application/environment pair, you might want a group for the application,
a group for the environment and a group for the application-environment pair.

It is possible to define these using standard ansible inventory files but they quickly
explode as the number of applications and environments increase

Instead can use the `generator` inventory plugin to generate such group combinations
from a list of layers.

---

# Secrets


<ul class="tip">
<li>Use `ansible-vault encrypt_string` to encrypt each secret inline</li>
</ul>
<ul class="warn">
<li>Don't forget to use `echo -n $secret | ansible-vault encrypt_string` to
  avoid encrypting the newline!
</ul>

- We use `ansible-vault` for all of our secrets.
- Kubernetes expects secrets to be base64 encoded
- Use `no_log` with the `k8s` module when uploading  secrets
- Anti-pattern: vaulting whole secrets files - this causes huge
  diffs on change (the whole file changes for a single byte difference)

---

# Secrets in environment variables

- Use a Secret resource to store secret environment variables
- Use envFrom if you then want to include all the secrets from that resource

```
apiVersion: v1
kind: Secret
metadata:
  name: my-secret-env
  namespace: my-namespace
data:
  {{ my_secret_env | to_nice_yaml(indent=2) | indent(2) }}
---
kind: Deployment
spec:
  template:
    spec:
      containers:
      - envFrom:
          - secretKeyRef:
              name: my-secret-env
```

---

# Secrets in environment variables

```
key1: !vault |
  $ANSIBLE_VAULT;1.1;AES256
  61666162663666643939353165393833383331313664616234343739653937336337626263663538
  3335336263303963623332666639666364356166393462370a396465393637363938656562393936
  61663834376235613564303237313131396335303336636466326430353530613836356564343832
  6638393533663931640a663438313461616436393365346566313037613034323738646234363534
  3734
my_secret_env:
  KEY1: "{{ key1 | b64encode }}"
```
---

# Modules

* `k8s` - main module for managing Kubernetes resources.
* `k8s_facts` - useful for run-time querying of resources
* `aws_eks_cluster` - manages AWS Elastic Kubernetes Service clusters
* `azure_rm_aks` - manages Azure Kubernetes Service clusters
* `gcp_container_cluster` - manages Google Kubernetes Engine clusters
* `gcp_container_nodepool` - manages GKE node pools


---

# k8s module

- uses the same manifest definitions as kubectl
- can take inline resource `definition`s, or `src` from file
- inline definitions work well with `template` lookup
  `definition: "{{ lookup('template', 'path/to/resource.j2') | from_yaml }}"
- invoke once with a manifest containing a list of resources, or invoke
  in a `loop` over a list of resources
- copes with Custom Resource Definitions (2.7)

<aside class="notes">
Main difference is how `changed` behaves.


---

# Plugins

* `yaml` stdout callback plugin is great for having output match input
* `k8s` lookup plugin returns information about Kubernetes resources
* `from_yaml` and `from_yaml_all` (2.7) useful for feeding templates into
  modules
* `to_nice_yaml` and `indent` are helpful for outputting ansible data structures
  into kubernetes manifest form

---

# Upcoming features of the k8s module

* `append_hash` will enable immutable ConfigMaps and Secrets (likely 2.8)
* `validate` will return helpful warning and/or error messages if a resource manifest
  does not match the Kubernetes resource specification (likely 2.8)
* `wait` will allow you to wait until the Kubernetes resources are actually in the
  desired state (hopefully 2.8)
