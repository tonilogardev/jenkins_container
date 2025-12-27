# Terraform Infrastructure

## Index

1. [Overview](#1-overview)
2. [File Structure](#2-file-structure)
3. [Variables](#3-variables)
4. [Usage via Jenkins](#4-usage-via-jenkins)
5. [Manual Usage](#5-manual-usage)
6. [Next steps](#6-next-steps)

---

## 1 Overview

Terraform is installed in the Jenkins container (v1.9.0) and is used to provision infrastructure on Hetzner Cloud.

The configuration creates:
- SSH Key in Hetzner
- VPS Server (Ubuntu 22.04)
- DNS Zone (Hetzner Cloud DNS)

[←Index](#index)

## 2 File Structure

```
002_terraform/
├── providers.tf    # Hetzner provider configuration
├── variables.tf    # Input variable declarations
├── main.tf         # Server and SSH key resources
└── outputs.tf      # Output values (server IP)
```

[←Index](#index)

## 3 Variables

Variables are defined in `002_terraform/variables.tf` and can be overridden via environment or CLI.

| Variable | Description | Default |
|----------|-------------|---------|
| `hcloud_token` | Hetzner Cloud API Token (sensitive) | - |
| `domain_name` | Domain name for the server | - |
| `location` | Hetzner location | `nbg1` |
| `server_type` | Server type | `cax11` |
| `ssh_public_key` | SSH public key content | - |

Environment variables are loaded from [env.development](../env.development):

```bash
TF_VAR_domain_name="tonilogar.com"
TF_VAR_location="nbg1"
TF_VAR_server_type="cax11"
```

> Note: `hcloud_token` is stored securely in Jenkins credentials, not in env files.

[←Index](#index)

## 4 Usage via Jenkins

The **Deploy-Infrastructure** pipeline provides a parameterized interface:

1. Go to Jenkins → **Deploy-Infrastructure**
2. Click **Build with Parameters**
3. Select **ACTION**:
   - `plan`: Preview changes (safe, no modifications)
   - `apply`: Create/update infrastructure
   - `destroy`: Delete all managed resources
4. Check **CONFIRM** (required for `apply` and `destroy`)
5. Click **Build**

### Example Workflow

1. Run with `ACTION=plan` to review changes
2. If plan looks good, run with `ACTION=apply` + `CONFIRM=true`
3. When done, run with `ACTION=destroy` + `CONFIRM=true` to avoid costs

[←Index](#index)

## 5 Manual Usage

If you need to run Terraform manually inside the container:

```bash
# Enter the container
docker exec -it jenkins bash

# Navigate to terraform directory
cd /home/a.lopez.g/Documents/trabajos/jenkins_container/terraform

# Load environment variables
set -a
. ../env.development
set +a

# Run Terraform commands
terraform init
terraform plan -var="hcloud_token=YOUR_TOKEN" -var="ssh_public_key=$(cat ~/.ssh/id_rsa.pub)"
terraform apply -auto-approve -var="hcloud_token=YOUR_TOKEN" -var="ssh_public_key=$(cat ~/.ssh/id_rsa.pub)"
```

[←Index](#index)

## 6 Next steps

- [005_deploy_production](./005_deploy_production.md) *(pending)*
