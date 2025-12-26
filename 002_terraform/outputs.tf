output "server_ip" {
  value       = hcloud_server.web.ipv4_address
  description = "Public IPv4 address of the server"
}
