# Networking Documentation

## Time and RTC

- Based on the project's requirements, the sender side cluster must be functional without Internet access.
- Because Raspberry Pis do not have hardware real-time clocks, time is lost when power is disconnected.
- Kubernetes requires time synchronization to function.
- As a short-term fix, the cluster will be powered on while connected to the Internet so time may be synchronized using NTP.
  - The Internet connection will be removed after each node has had time to boot & sync.

## DHCP and Static IPs

- Without a DHCP server (which routers usually provide), network connectivity is not usable out of the box.
- To solve this issue, each node will be assigned a static IP.
  - For Ubuntu 24.04, this involves configuring Netplan.
- Additionally, the `/etc/hosts` file will be edited to record each node's hostname and IP.
  - This removes the need for DHCP.
- For reliability and continuity, the static IPs will be the same as assigned by the DHCP server.

### Example `/etc/netplan/00-installer-config.yaml` File

```yaml
network:
  version: 2
  ethernets:
    eth0:
      dhcp4: no
      addresses:
        - 192.168.1.200/24
```

### Example `/etc/hosts` File

```text
127.0.0.1       localhost
127.0.1.1       raspi1

192.168.1.200  raspi1
192.168.1.100  raspi2
192.168.1.146  raspi3
```
