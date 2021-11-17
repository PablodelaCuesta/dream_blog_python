# Remove olders versions of Docker
apt-get remove docker docker-engine docker.io containerd runc

# Tools
apt-get update

apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Docker official GPG key
 curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Install docker engine
apt-get install docker-ce docker-ce-cli containerd.io -y

# Install docker-compose
apt-get install docker-compose -y

echo 'Docker installed!'