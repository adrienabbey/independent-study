# Containers

## Learning Goals

### Phase 1

Learn how to properly and effectively use Docker to self-host MediaWiki:

- Create separate containers for each service: one to host the database (MariaDB) and another to host Apache/PHP.
- Create a network to allow the containers to communicate with each other.
- Create persistent storage to save the database and MediaWiki files.
- How to properly handle secrets (passwords) to limit exposure of sensitive information.

### Phase 2

Advanced features I may not immediately benefit from:

- Self-hosting a container repository
- Automatic updates and deployment of containers
- Additional best-practices as discovered while learning.

## Best Practices

- Combine commands in order to minimize image layer creation.
- Clean up temporary files when possible.
- Example of combining the two above practices:
  > `RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*`
- Run as non-root when possible.  This reduces the attack surface:
  > `RUN addgroup -S appgroup && adduser -S appuser -G appgroup`
  >
  > `USER appuser`
- Be mindful of properly handling secrets (such as passwords) in such a way that they never become part of the container image or the git repository.
  - Use `.dockerignore` and `.gitignore`
  - Use variables to pull passwords from local files:
    > `docker run -e "DB_USER=admin" -e "DB_PASS=$(cat secret_file)" myimage:latest`
  - Better option: use Kubernetes secrets (when I get to that)
- Clean up unused data regularly:
  > `docker system prune -a`

### Summary

- **Lightweight**: Fewer unnecessary dependencies, faster pull times.
- **Secure**: Minimal attack surface, no hard-coded secrets, regular patching.
- **Maintainable**: Clear Dockerfiles, logical layering, consistent builds.
- **Stable**: Predictable, versioned images.

## Feb. 16 Update

- I need to decide how much of Docker's proprietary features I'm willing to use for the container portion of my independent study.
  - Docker Compose can be used in place of Kubernetes for multi-container systems.
  - Docker Volumes can be used for persistent storage.
  - Docker has proprietary networking features.
  - Docker secrets to secure passwords.
- Given the above, and my desire to transition to Kubernetes, I'll focus on using features that will be easily replaced.
  - Namely, I'll use Docker networks and volumes for now, but avoid Compose.
- I need to create or define persistent storage.
  - This can be a filesystem directory, or a Docker Volume.
- I need to define a network to allow containers to communicate with each other.
- I've discovered that I should be using the official MariaDB docker image rather than make my own.
  - Making my own would require a lot more effort.  I'd have to make a bash script to initialize the database, configure everything, etc.
  - By comparison, using the official image would require only a single terminal command to launch.
    - This command would include all the relevant details, such as user/pass, persistent storage, etc.
- I feel like I'm going in circles here, as I'm trying to use tools in ways they weren't intended as a result of my current learning plan.
  - I might do better if I try learning containers *while* also implementing them with Kubernetes.
