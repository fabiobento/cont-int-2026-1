"""
Arquivo de configuração de instalação do pacote ROS 2 (Python).
Define as dependências, pontos de entrada (executáveis) e metadados do pacote.
"""
from setuptools import find_packages, setup

package_name = 'turtle_controller'

setup(
    name=package_name,
    version='0.0.0',
    # Busca automaticamente os pacotes e submódulos, excluindo pastas de testes
    packages=find_packages(exclude=['test']),
    data_files=[
        # Registra o pacote no índice de recursos do ament para ser localizado pelo ROS 2
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        # Instala o manifesto (package.xml) no diretório 'share' do pacote
        ('share/' + package_name, ['package.xml']),
    ],
    # Define os pacotes Python necessários para a instalação
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ed',
    maintainer_email='todo.todo@todo.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    # Define as dependências necessárias para rodar os testes
    tests_require=['pytest'],
    # Configuração dos executáveis do pacote (pontos de entrada)
    entry_points={
        'console_scripts': [
            # Cria o comando 'turtle_controller' apontando para a função 'main' do nó criado
            "turtle_controller = turtle_controller.turtle_controller:main"
        ],
    },
)
