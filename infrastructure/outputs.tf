output "droplet_ip_address" {
    value = digitalocean_droplet.web.ipv4_address
}