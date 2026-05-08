# Homelab Infrastructure (Docker GitOps)

This repository contains the Infrastructure as Code (IaC) for my personal home server. It is built entirely on Docker Compose and deployed using a pull-based GitOps pipeline via Portainer. 

The primary objective of this architecture is disaster recovery (DR) and environment reproducibility, while maintaining strict isolation and secret management.

## Architecture & Hardware

* **Hardware:** Raspberry Pi 5 
* **Storage:** External SSD (Container Data) + HDD (Media/Backups)
* **Container Engine:** Docker
* **Deployment Pipeline:** Portainer (Repository polling)
* **Reverse Proxy & WAF:** NPMPlus with integrated CrowdSec deep-packet inspection

## Security Implementation

This environment is treated as a production server. To ensure the repository remains sanitized, the following principles are enforced in the code:

* **Secret Management:** No credentials, API keys, or identifiable domain names are hardcoded in the YAML files. All sensitive data is abstracted into localized `.env` files and injected at deployment. (Reference the `.env.sample` files for expected variables).
* **Network Isolation:** All containers exposing web interfaces are bound strictly to the host's loopback interface (`127.0.0.1`). They cannot be accessed directly via the local LAN and route exclusively through the reverse proxy.
* **Service Accounts:** Where applicable, containers are run under specific PUID/PGID parameters (`1000:1000`) rather than root.

## Infrastructure Highlights

The stack handles routing, media management, document OCR, and local version control. Notable configurations include:

* `nextcloud-aio/`: Configured for reverse-proxy compatibility avoiding internal buffering timeouts.
* `vaultwarden/`: Includes an automated Alpine sidecar container executing daily, non-corrupting SQLite backups.
* `matrix/`: Configured for external federation via `.well-known` signpost delegation.
* `gitea/`: Self-hosted Git service with customized SSH port bindings to deflect automated bot traffic.
* `arr-stack/`: Complex multi-container deployment demonstrating shared volume mapping and internal service dependencies.

---
*Deployment Note: Cloning this repository requires the manual provisioning of local `.env` files for the stacks to execute.*