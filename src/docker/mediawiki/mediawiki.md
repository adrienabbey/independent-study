# MediaWiki Deployment

Documentation for deploying MediaWiki across my Kubernetes cluster.

> Note: I used ChatGPT heavily to research and get configuration for most of this. I made an effort to manually review and adjust these files to my needs, and have a good general idea of what they do. I'm not aiming to learn the detailed syntax of these files, as that's not what I had in mind for my intended scope of this project.

## Goals

- Deploy a private MediaWiki site to my Kubernetes cluster.
- Use two containers: one for MariaDB, and another for Apache/MediaWiki.
- Use ~~Longhorn~~ OpenEBS for distributed persistent storage across the Kubernetes cluster.
- Use Kubernetes secrets to protect passwords and other sensitive information.
- ~~Host my Docker images on my GitLab CE container repository.~~
- Configure Ingress so I can access my MediaWiki.
- _Stretch Goal_: setup a CI/CD pipeline on GitLab CE to automatically update and deploy containers across the cluster.

## ~~Step 1: Setup GitLab CE~~

- I currently have a GitLab CE VM running, but it only has a basic Docker container repo.
- I want to configure it to automatically pull the latest images of containers from Docker Hub as needed.
- To do this, I need to configure the CI/CD pipeline, and create at least one GitLab Runner.
  - For fun, I want to create at least two GitLab runners, and have them on my MicroK8s cluster.

### ~~GitLab Runner~~

- I first need to enable Helm on MicroK8s.
  - Helm is a package manager for Kubernetes, bundling, installing and managing Kubernetes manifests (or Charts).
  - I'll be using it to deploy the GitLab runner and other applications to my cluster.
  - I created a `gitlab-runner-values.yaml` file on my GitLab instance to hold Helm values for the runner configuration.
- I'm going to create a `gitlab-runner` namespace on my MicroK8s cluster.
  - Namespaces allow for isolating resources. This means I can keep my gitlab runners and my project containers isolated from one another.
- Ran into issues with DNS within containers. Troubleshooting now.
  - Attempting to specify my local DNS server.
  - Turned out I was missing an essential Calico port. Calico is used to enable network communication between containers.
- While I fixed one problem, my GitLab runner is still failing, claiming DNS lookup failures.
  - If I open the container's shell, I can get results from an `nslookup` of my GitLab instance without error.
  - Apparently the runner spawns a helper container, and that might be failing.

### Compromises

- I never got the GitLab runner working. Time to change goals. I shouldn't waste multiple days troubleshooting something I don't need.

## Distributed Storage: OpenEBS

- I wanted a distributed file system for my cluster that would allow for files from a container on one node to be distributed and saved across the cluster. This not only ensures that I won't lose data if a node fails, but also ensures that I can launch a container on any node without concern about data integrity.
- I need to be mindful that I intend for this to eventually run on my Raspberry Pi cluster. That means official ARM support and lightweight requirements, while keeping the replication. Originally I was leaning towards Longhorn, but that would have been a tight fit on the Raspberry Pis.
- The solution is thus OpenEBS.
- I used Helm to install OpenEBS across my cluster using its official chart.

## Creating the Containers

- Start by creating a Kubernetes secrets file for the MariaDB passwords.
  - This file has secrets! I added it to `.gitignore` so I don't go spraying my undesirables all over the Internets.
- Created persistent OpenEBS volumes for each container: `mariadb-pvc.yaml` and `mediawiki-pvc.yaml`
  - I adjusted the ChatGPT recommendations down to 1 Gi each, which should be overkill for what I'm doing.
- Created a Kubernetes deployment and service file for MariaDB: `mariadb-deployment.yaml` and `mariadb-service.yaml`
  - The deployment file selects the official MariaDB container on Docker Hub, sets the users/passwords, and creates the database for MediaWiki using the Kubernetes secrets configured earlier. It also attaches the persistent volumes created in the previous step.
  - The service file opens the port on the container. I believe this is only accessible from the local machine and/or containers.
  - The deployment file did _not_ specify a port, unlike the one for MediaWiki. I believe this may restrict access further.
- Did the same for the MediaWiki container: `mediawiki-deployment.yaml` and `mediawiki-service.yaml`
  - This deployment file _does_ specify a port (80).
  - It also pulls the DB information from the MariaDB secrets from earlier.
  - Mounts the persistent storage too.
  - The service file specifies a `NodePort`. This instructs each node in the cluster to open this port so that the container can be externally accessed.
