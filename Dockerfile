FROM jenkins/jenkins:lts

# Disable the setup wizard
ENV JAVA_OPTS -Djenkins.install.runSetupWizard=false

# Install plugins
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN jenkins-plugin-cli -f /usr/share/jenkins/ref/plugins.txt

# Install Docker CLI and Compose
USER root
RUN apt-get update && apt-get install -y lsb-release \
    && curl -fsSLo /usr/share/keyrings/docker-archive-keyring.asc https://download.docker.com/linux/debian/gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.asc] https://download.docker.com/linux/debian $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list \
    && apt-get update && apt-get install -y docker-ce-cli docker-compose-plugin \
    && apt-get install -y wget unzip \
    && wget https://releases.hashicorp.com/terraform/1.9.0/terraform_1.9.0_linux_amd64.zip \
    && unzip terraform_1.9.0_linux_amd64.zip \
    && mv terraform /usr/local/bin/ \
    && rm terraform_1.9.0_linux_amd64.zip
