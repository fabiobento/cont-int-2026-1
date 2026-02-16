#!/usr/bin/env bash

# Para a execução se houver erro em qualquer comando
set -e

echo "######################################################################"
echo ">>> Iniciando Configuração do Ambiente Docker"
echo "######################################################################"

# Garante que lspci esteja disponível
sudo apt update
sudo apt install -y pciutils

# Função para verificar GPU NVIDIA
check_nvidia_driver() {
    echo ">>> Verificando GPU NVIDIA..."
    if lspci | grep -i nvidia > /dev/null; then
        if nvidia-smi > /dev/null 2>&1; then
            echo ">>> [OK] GPU NVIDIA detectada e driver funcionando."
            return 0
        else
            echo ">>> [AVISO] GPU NVIDIA encontrada, mas o driver não parece estar ativo."
            echo ">>> O NVIDIA Container Toolkit NÃO será instalado."
            return 1
        fi
    else
        echo ">>> Nenhuma GPU NVIDIA encontrada."
        return 1
    fi
}

# Função para instalar Docker
install_docker() {
    echo ">>> Instalando Docker..."
    
    # Dependências iniciais
    sudo apt install -y apt-transport-https ca-certificates curl software-properties-common gnupg

    # Prepara o diretório de chaves
    sudo install -m 0755 -d /etc/apt/keyrings
    
    # Baixa a chave oficial do Docker (se já existir, sobrescreve para atualizar)
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc

    # Adiciona o repositório
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
      $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
      sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
      
    sudo apt update
    
    # Instalação dos pacotes do Docker e ferramentas extras (git, ssh)
    sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin git openssh-server openssh-client
    
    # Configuração de usuário (Forma segura, sem chmod 666)
    if ! getent group docker > /dev/null; then
        sudo groupadd docker
    fi
    sudo usermod -aG docker ${USER}
    
    # Reinicia o serviço
    sudo systemctl restart docker
    
    echo ">>> Docker instalado com sucesso."
}

# Função para instalar NVIDIA Container Toolkit
install_nvidia_container_toolkit() {
    echo ">>> Configurando NVIDIA Container Toolkit..."
    
    # Configuração do repositório oficial (Production)
    curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor --yes -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
    && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

    sudo apt update
    sudo apt install -y nvidia-container-toolkit

    # Configura o runtime do Docker
    sudo nvidia-ctk runtime configure --runtime=docker
    sudo systemctl restart docker
    
    echo ">>> NVIDIA Container Toolkit configurado."
}

# Lógica principal
install_docker

if check_nvidia_driver; then
    install_nvidia_container_toolkit
fi

echo "######################################################################"
echo ">>> Instalação Concluída!"
echo ">>> IMPORTANTE: Para usar o docker sem 'sudo', você deve fazer LOGOUT e LOGIN novamente."
echo ">>> Ou digite 'newgrp docker' neste terminal agora."
echo "######################################################################"