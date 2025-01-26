# Containers and Kubernetes

## What is a Container?

- Containers are a specialized variation of a lightweight virtual machine (VM) that allows for running applications in an isolated environment without the same overhead that a normal VM would require.
- This is because containers don't actually virtualize the hardware and an entire OS like a VM would.  Instead it creates an isolated environment that allows applications to make use of resources within the host kernel without the typical risk of those applications being able to escape isolation and affect the host operating system.
- Kubernetes supports several different *container runtimes*, the component which containers use to interface with the host to run.  These container runtimes all use a standardized *container runtime interface* (CRI), making it possible to switch these out easily.
- Docker is a popular containerization platform.  While it still remains popular, most of the key technologies behind Docker have become open standards, opening the door to supporting alternative containerization platforms within Kubernetes.
- Originally I believed I needed to do some deep research into figuring out alternatives to Docker, as I read that Kubernetes was depreciating Docker support.  It turns out that containers created by Docker will continue to run on Kubernetes without issue in the majority of cases:
  - <https://kubernetes.io/blog/2020/12/02/dont-panic-kubernetes-and-docker/>

## What is Kubernetes?

- Kubernetes is a container orchestrator.  Kubernetes makes it possible to manage and monitor containers running on many different servers.
- This makes it easy to do things like load-balancing very heavy loads across many different containers and systems, create redundancy and fault-tolerance with containers, manage the life-cycle of containers (like automatic rolling updates without loss of service), etc.
- MicroK8s is a light-weight version of Kubernetes made by Canonical (the people behind Ubuntu) that was designed to run on low-power devices like the Raspberry Pi.  This will be what I'll be using for this project.

## Why Study Containers and Kubernetes?

- For several years now, I've been running VMs on a server at home.  These VMs run everything from Nextcloud (synchronizing file, calendar, tasks, contacts, etc. across all my devices) to test beds for exploring new technologies (like containers and Kubernetes!).
- While I've been very happy with my VMs, the hardware required to run them is expensive and requires significant power draw to run 24/7.  When considering alternatives, I realized I could get similar benefits at a much lower cost if I were to migrate to containers running on a Kubernetes cluster across multiple Raspberry Pis.
- Perhaps more crucially, I needed two more 4000-level credit hours, and this became a great opportunity to finally get the motivation to learn.  So here we are.
