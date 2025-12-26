resource "hcloud_ssh_key" "default" {
  name       = "jenkins-terraform-key"
  public_key = var.ssh_public_key
}

resource "hcloud_server" "web" {
  name        = "vps-${var.domain_name}"
  image       = "ubuntu-22.04"
  server_type = var.server_type
  location    = var.location
  ssh_keys    = [hcloud_ssh_key.default.id]

  public_net {
    ipv4_enabled = true
    ipv6_enabled = true
  }

  labels = {
    environment = "production"
    managed_by  = "terraform"
  }

  user_data = <<-EOF
    #!/bin/bash
    set -e

    # Update system
    apt-get update
    apt-get upgrade -y

    # Install Docker
    curl -fsSL https://get.docker.com | sh

    # Install Docker Compose plugin
    apt-get install -y docker-compose-plugin

    # Enable Docker service
    systemctl enable docker
    systemctl start docker

    # Create app directory
    mkdir -p /opt/app

    echo "Docker installation complete!"
  EOF
}
