# MediaWiki Deployment

Documentation for deploying MediaWiki across my Kubernetes cluster.

## Goals

- Deploy a private MediaWiki site to my Kubernetes cluster.
- Use two containers: one for MariaDB, and another for Apache/MediaWiki.
- Use persistent storage, preferably one that is synchronized across the Kubernetes cluster.
- Use Kubernetes secrets to protect passwords and other sensitive information.
- Host my Docker images on my GitLab CE container repository.
- _Stretch goal_: setup a CI/CD pipeline on GitLab CE to automatically update and deploy containers across the cluster.

## Step 1: Setup GitLab CE

- I currently have a GitLab CE VM running, but it only has a basic Docker container repo.
- I want to configure it to automatically pull the latest images of containers from Docker Hub as needed.
- To do this, I need to configure the CI/CD pipeline, and create at least one GitLab Runner.
  - For fun, I want to create at least two GitLab runners, and have them on my MicroK8s cluster.

### GitLab Runner

- I first need to enable Helm on MicroK8s.
  - Helm is a package manager for Kubernetes, bundling, installing and managing Kubernetes manifests (or Charts).
  - I'll be using it to deploy the GitLab runner and other applications to my cluster.
  - I created a `gitlab-runner-values.yaml` file on my GitLab instance to hold Helm values for the runner configuration.
- I'm going to create a `gitlab-runner` namespace on my MicroK8s cluster.
  - Namespaces allow for isolating resources. This means I can keep my gitlab runners and my project containers isolated from one another.
- Ran into issues with DNS within containers. Troubleshooting now.
  - Attempting to specify my local DNS server.
