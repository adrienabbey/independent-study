# Learning Objectives

This is an initial list of learning objectives I will use to jump-start my independent studies and give some direction.  It's not intended to be exhaustive or complete, as I expect that my research will expand to new topics as I learn of them.

**Containerization Learning Objectives:**
> Learning objectives for containerization typically include understanding the basics of containers, creating and managing container images, implementing best practices for container design, and deploying containers using platforms like Docker and Kubernetes. Additionally, learners should be able to evaluate container strategies and understand the lifecycle of containers.  - **DuckDuckGo DuckAssist**

**Kubernetes Learning Objectives:**
> Kubernetes learning objectives typically include understanding container orchestration, deploying and managing containerized applications, scaling deployments, and troubleshooting issues within a Kubernetes cluster. Additionally, learners often focus on mastering key components like control planes and nodes, as well as evaluating when to use Kubernetes for specific workloads. - **DuckDuckGo DuckAssist**

## Containers

- Compare different container technology options (Docker, LXC, etc.)
- Select one (or more) container technology to use with Kubernetes.
- Learn how to create and deploy containers.
- Learn how to automate container updates, builds and distribution (CI/CD).
- Learn about containerization best practices.
- Apply: build containers based on current VMs for personal use using all the above.

## Kubernetes

- Compare the different Kubernetes distributions (MicroK8s, etc.)
- Select a Kubernetes distribution to use (most likely MicroK8s).
- Learn the basics of Kubernetes (intentionally vague here).
  - Container orchestration (load balancing, maintaining uptime, etc.)
  - Managing deployment and updating of containers.
  - Understanding control planes and nodes.
  - Secure communications between containers.
  - Proxy services (accessing scaled container deployments)
  - Secret management.
  - Logging and alerts.
  - Best practices.
  - Surely more,
- Create a Kubernetes cluster using my personal Raspberry Pi cluster.
  - Consider also deploying a second Kubernetes cluster across VMs for testing.
- Begin deploying containers created earlier across the Kubernetes cluster.
  - Apply all the relevant methods researched earlier.
