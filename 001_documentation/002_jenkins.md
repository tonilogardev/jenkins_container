# Jenkins Container

## Index

1. [Structure](#1-structure)
2. [Deployment](#2-deployment)
3. [Automated Pipelines](#3-automated-pipelines)
4. [Credential Management](#4-credential-management)
5. [Important Notes](#5-important-notes)
6. [Next steps](#6-next-steps)

---

## 1 Structure

- **Dockerfile**: Custom image based on `jenkins/jenkins:lts`. Installs Docker CLI, Docker Compose, and Terraform.
- **plugins.txt**: List of plugins installed automatically.
- **jenkins.yaml**: JCasC configuration. Defines users and pipelines.
- **docker-compose.yml**: Orchestration. Mounts Docker socket and host workspace.

[←Index](#index)

## 2 Deployment

1. **Start Jenkins**:
   ```bash
   ./run_jenkins.sh
   ```
   This script cleans up Docker, builds the image, and starts Jenkins with logs visible.  
   Press `Ctrl+C` to stop.

2. **Access**: [http://localhost:8080](http://localhost:8080)
   - User: `admin`
   - Password: `admin`

[←Index](#index)

## 3 Automated Pipelines

### Deploy-App
Deploys the web application (Vite + TS) located in `003_app`.
- Executes: `docker compose -p 003_app up -d --build`
- App port: `3001`

### Stop-App
Stops and removes the `003_app` application.
- Executes: `docker compose -p 003_app down`

### Deploy-Infrastructure
Terraform pipeline with parameters for infrastructure management.
- **ACTION**: `plan`, `apply`, or `destroy`
- **CONFIRM**: Required for `apply` and `destroy` actions

[←Index](#index)

## 4 Credential Management

Credentials (SSH Key and Hetzner Token) are stored in **Jenkins' internal encrypted storage**.

- **Persistence**: Saved in the `jenkins_home` volume.
- **Local Files**: The `secrets/` folder is no longer needed on the host.
- **Management**: Update them via "Manage Jenkins" → "Credentials".

### Configured IDs
- `ssh-credentials`: SSH private key.
- `hcloud-token`: Hetzner Cloud API Token (Terraform).
- `hetzner-dns-token`: Hetzner DNS API Token (Traefik/Let's Encrypt).

### Adding Credentials Manually

1. Go to **Manage Jenkins** → **Credentials**.
2. Click **(global)** under the "System" domain.
3. Click **Add Credentials**.

#### For Hetzner Cloud Token (Terraform):
- **Kind**: Secret text
- **Secret**: Paste your Hetzner Cloud API token.
- **ID**: `hcloud-token`
- **Description**: "Hetzner Cloud API Token"

#### For Hetzner DNS Token (Traefik/SSL):
- **Kind**: Secret text
- **Secret**: Paste your Hetzner DNS API token.
- **ID**: `hetzner-dns-token`
- **Description**: "Hetzner DNS API Token for Traefik/Let's Encrypt"

> This token is passed to Traefik during production deployment to validate wildcard SSL certificates via DNS challenge.

#### For SSH Keys:
- **Kind**: SSH Username with private key
- **ID**: `ssh-credentials`
- **Username**: `jenkins`
- **Private Key**: Select **Enter directly** and paste your private key content.
- **Passphrase**: Leave empty if your key has no passphrase.

> [!IMPORTANT]
> **Security**: Once credentials are configured in Jenkins, **delete local files** (such as `secrets/` folder or token files). Jenkins stores this data encrypted. Keeping them in plain text on your machine is an unnecessary security risk.

### Private Repository Access (GitHub Deploy Key)

For pipelines that need to access a **private GitHub repository** (e.g., `Deploy-Production`), you must configure a **Deploy Key** in GitHub.

1. **Verify your SSH Key**: Ensure the public key corresponding to the `ssh-credentials` ID in Jenkins is available.
2. **Go to GitHub**: Navigate to your repository -> **Settings** -> **Deploy keys**.
3. **Add Deploy Key**: 
   - Click **Add deploy key**.
   - **Title**: Give it a recognizable name (e.g., "Jenkins Production").
   - **Key**: Paste the **Public SSH Key**.
   - **Allow write access**: **Unchecked** (unless you specifically need Jenkins to push tags or commits back to the repo). For standard deployment (checkout only), read-only is sufficient and safer.
4. **Update Pipeline**: Ensure your pipeline uses the SSH URL (`git@github.com:...`) and references the `ssh-credentials` ID.


[←Index](#index)

## 5 Important Notes

- **Volumes**: The host's working directory is mounted at the same path inside the Jenkins container. This allows Jenkins to execute Docker commands referencing host files without path issues.
- **Project Name**: Use `-p container_01` in Docker Compose commands for consistency and to avoid name conflicts.

[←Index](#index)

## 6 Next steps

- [003_hetzner_login_domain_API_tokens](./003_hetzner_login_domain_API_tokens.md)
