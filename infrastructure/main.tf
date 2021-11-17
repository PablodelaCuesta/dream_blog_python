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
variable "ssh_public_key" {}

resource "digitalocean_ssh_key" "ssh-key" {
  name       = "blog_webapp"
  public_key = var.ssh_public_key
}

resource "digitalocean_droplet" "web" {
  image = "ubuntu-20-04-x64"
  name = "web"
  region = "ams3"
  size = "s-1vcpu-2gb"
  ssh_keys = ["${digitalocean_ssh_key.ssh-key.fingerprint}"]



  provisioner "file" {
    source = "./scripts/docker.sh"
    destination = "/tmp/docker.sh"
  }

  provisioner "remote-exec" {
    inline = [
      "chmod +x /tmp/docker.sh",
      "sudo /tmp/docker.sh"
    ]
  }

  connection {
    host = self.ipv4_address
    type = "ssh"
    user = "root"
    private_key = "${file("~/.ssh/do/id_rsa_do")}"
  }

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