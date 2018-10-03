Instructions for EKS are in roles/eks/README.md

You may want to add an overrides.yml file. Mine looks a bit like

```
eks_kubeconfig_env:
  - name: AWS_PROFILE
    value: my_profile
kube_domain_name: a.domain.name.in.route53
```

The `kube_domain_name` is used to point the two applications at
the ELB created by the nginx ingress controller


Example commands are shown in [demo.txt](demo.txt)
