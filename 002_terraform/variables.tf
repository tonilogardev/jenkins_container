variable "hcloud_token" {
  description = "Hetzner Cloud API Token"
  type        = string
  sensitive   = true
}

variable "domain_name" {
  description = "Domain name for the server"
  type        = string
}

variable "location" {
  description = "Hetzner location (e.g., nbg1)"
  type        = string
  default     = "nbg1"
}

variable "server_type" {
  description = "Hetzner server type (e.g., cax11)"
  type        = string
  default     = "cax11"
}

variable "ssh_public_key" {
  description = "SSH Public Key content"
  type        = string
}
