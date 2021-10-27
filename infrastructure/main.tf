terraform {
  required_providers {
    digitalocean = {
      source = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}

# Configure the DigitalOcean Provider
provider "digitalocean" {
  token = var.do_token
}

variable "do_token" {}
variable "private_key" {}
variable "public_key" {}

resource "digitalocean_ssh_key" "ssh-key" {
  name       = "ssh-key"
  public_key = var.public_key
}

resource "digitalocean_droplet" "web" {
  image = "ubuntu-20-04-x64"
  name = "web"
  region = "ams3"
  size = "s-1vcpu-1gb"
  ssh_keys = ["${digitalocean_ssh_key.ssh-key.fingerprint}"]

}

# Domain resource
resource "digitalocean_domain" "domain" {
  name ="pablodelacuesta.es"
  ip_address = digitalocean_droplet.web.ipv4_address
}

# Add a CNAME record that points www.pablodelacuesta.es -> pablodelacuesta.es
resource "digitalocean_record" "cname-ubuntu" {
  domain = digitalocean_domain.domain.name
  type = "CNAME"
  name = "www"
  value = "@"
}