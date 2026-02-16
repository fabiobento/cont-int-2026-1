```shell
#!/bin/bash -eu

# Licença BSD
# Copyright (c) 2024 RUNTIME Robotics
# Copyright (c) 2014 OROCA and ROS Korea Users Group

#set -x

name_ros_distro=jazzy 
user_name=$(whoami)
echo "#######################################################################################################################"
echo ""
echo ">>> {Iniciando a Instalação do ROS 2 Jazzy}"
echo ""
echo ">>> {Verificando a versão do seu Ubuntu} "
echo ""

# Obtendo a versão e o número de lançamento do Ubuntu
version=`lsb_release -sc`
relesenum=`grep DISTRIB_DESCRIPTION /etc/*-release | awk -F 'Ubuntu ' '{print $2}' | awk -F ' LTS' '{print $1}'`
echo ">>> {Sua versão do Ubuntu é: [Ubuntu $version $relesenum]}"

# Verificando se a versão é a Noble (24.04), caso contrário, encerra o script
case $version in
  "noble" )
  ;;
  *)
    echo ">>> {ERRO: Este script só funciona no Ubuntu Noble (24.04).}"
    exit 0
esac

echo ""
echo ">>> {O ROS 2 Jazzy é totalmente compatível com o Ubuntu Noble 24.04}"
echo ""
echo "#######################################################################################################################"
echo ">>> {Passo 1: Configurar os repositórios do Ubuntu}"
echo ""

# Verifica o locale para UTF-8
locale

sudo apt update 
sudo apt install -y locales

# --- CONFIGURAÇÃO DE LOCALE (Preservando PT-BR) ---
# Garante que o pt_BR.UTF-8 exista.
sudo locale-gen pt_BR pt_BR.UTF-8
# --------------------------------------------------

# Verifica as configurações de locale após a geração
locale


##############################################################


sudo apt install -y software-properties-common
sudo add-apt-repository universe

echo ""
echo ">>> {Concluído: Repositórios do Ubuntu adicionados}"
echo ""
echo "#######################################################################################################################"
echo ">>> {Passo 2: Configurar chaves e fontes}"
echo ""
echo ">>> {Instalando curl para adicionar as chaves}"

echo ">>> {Verificando e removendo chaves existentes, se houver}"

if [ -f "/etc/apt/sources.list.d/ros2.list" ]; then
    sudo rm /etc/apt/sources.list.d/ros2.list
fi

if [ -f "/usr/share/keyrings/ros-archive-keyring.gpg" ]; then
    sudo rm /usr/share/keyrings/ros-archive-keyring.gpg
fi

echo ">>> {Instalando o pacote de fonte APT do ROS 2}"


sudo apt update 
sudo apt install -y curl openssl 

# Obtém a versão mais recente do instalador de fontes APT do ROS via GitHub
export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F\" '{print $4}')
curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo $VERSION_CODENAME)_all.deb" 
sudo apt install /tmp/ros2-apt-source.deb


echo ">>> {Concluído: Chaves adicionadas}"
echo ""
echo "#######################################################################################################################"
echo ">>> {Passo 4: Atualizando o índice de pacotes do Ubuntu}"
echo ""
sudo apt update
sudo apt -y upgrade 

echo ""
echo "#######################################################################################################################"
echo ">>> {Passo 5: Instalar ROS e Ferramentas de Compilação C++}"
echo ""

# Define o valor padrão como 1: Instalação Desktop Completa
echo "Escolha o tipo de instalação:"
echo "1) Desktop Full (Recomendado)"
echo "2) ROS-Base (Mínimo)"
read -p "Digite sua opção (Padrão é 1): " answer 

case "$answer" in
  1)
    package_type="desktop-full"
    ;;
  2)
    package_type="ros-base"
    ;;    
  * )
    package_type="desktop-full"
    ;;
esac

echo "#######################################################################################################################"
echo ""
echo ">>>  {Iniciando a instalação do ROS...}"
echo ""
sudo apt install -y ros-${name_ros_distro}-${package_type} 
# Instala ferramentas essenciais para compilação C++ (g++, make, etc) e ferramentas do ROS
sudo apt install -y ros-dev-tools build-essential cmake

echo ""
echo ""
echo "#######################################################################################################################"
echo ">>> {Passo 6: Configurando o Ambiente ROS}" 
echo ""

# Adiciona o comando de inicialização do ROS ao .bashrc do usuário
echo "source /opt/ros/${name_ros_distro}/setup.bash" >> /home/$user_name/.bashrc

# --- CONFIGURAÇÃO PYTHON PARA PT-BR ---
# Força o Python a usar UTF-8 para evitar problemas com caracteres especiais em scripts
echo "export PYTHONUTF8=1" >> /home/$user_name/.bashrc
echo "export PYTHONIOENCODING=utf-8" >> /home/$user_name/.bashrc
# --------------------------------------

# Carrega as novas configurações no terminal atual
source /home/$user_name/.bashrc

echo ""
echo "#######################################################################################################################"
echo ">>> {Passo 7: Testando a Instalação (ROS, Python & C++)}"
echo ""
echo ">>> 1. Versão do ROS distribuída:"
printenv ROS_DISTRO

echo ""
echo ">>> 2. Teste de Codificação Python:"
python3 -c "import sys; print(f'   [OK] Python Encoding: {sys.stdout.encoding}. Caracteres: Acentuação e Cedilha (ã, ê, ç).')"

echo ""
echo ">>> 3. Teste de Compilador C++ e Codificação:"
# Cria um arquivo C++ temporário para teste de sanidade
cat <<EOF > /tmp/test_cpp_ros.cpp
#include <iostream>
int main() {
    std::cout << "   [OK] C++ configurado. Compilador g++ funcionando com acentos (á, é, í, ó, ú)." << std::endl;
    return 0;
}
EOF

# Tenta compilar e executar o teste
if g++ /tmp/test_cpp_ros.cpp -o /tmp/test_cpp_ros; then
    /tmp/test_cpp_ros
    rm /tmp/test_cpp_ros.cpp /tmp/test_cpp_ros
else
    echo "   [ERRO] Falha ao compilar teste C++."
fi

echo "#######################################################################################################################"
```