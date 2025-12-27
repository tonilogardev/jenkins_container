output "server_ip" {
  value       = hcloud_server.web.ipv4_address
  description = "Public IPv4 address of the server"
}

output "server_ipv6" {
  value       = hcloud_server.web.ipv6_address
  description = "Public IPv6 address of the server"
}

output "dns_zone_id" {
  value       = hcloud_zone.main.id
  description = "ID of the DNS zone"
}
