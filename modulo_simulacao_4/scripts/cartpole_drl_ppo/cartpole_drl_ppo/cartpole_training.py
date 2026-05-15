"""
Script de Treinamento do Agente de DRL (Deep Reinforcement Learning).

Este script inicializa o ambiente customizado CartPoleROS2Env e utiliza 
o algoritmo PPO (Proximal Policy Optimization) da biblioteca Stable Baselines3 
para treinar uma rede neural (MlpPolicy) a equilibrar o pêndulo.
Após o treinamento, o modelo resultante é salvo no diretório de instalação do pacote.
"""

from cartpole_drl_ppo.cartpole_env import CartPoleROS2Env
from stable_baselines3 import PPO
from ament_index_python.packages import get_package_share_directory

def main(args=None):
    """
    Função principal que orquestra a criação do ambiente, configuração e 
    execução do treinamento do modelo PPO.
    """
    package_name = 'cartpole_drl_ppo'
    # Obtém o caminho de instalação do pacote (onde o modelo será salvo)
    model_pkg_path = get_package_share_directory(package_name) + "/" 

    # Instancia o ambiente customizado do CartPole integrado com ROS 2
    env = CartPoleROS2Env()
    
    # Inicializa o modelo PPO utilizando uma política Multi-Layer Perceptron (MlpPolicy).
    # O device='cpu' é utilizado para remover o aviso do PyTorch e frequentemente melhora a 
    # velocidade para redes pequenas em comparação à transferência de dados para a GPU.
    model = PPO('MlpPolicy', env, verbose=1, device='auto')

    # Inicia o processo de aprendizado (treinamento) do agente interagindo com o ambiente.
    # O total_timesteps define quantos passos (interações) o agente fará no total.
    # Exemplo: 500.000 passos garantem um bom tempo de exploração e consolidação da política.
    # A barra de progresso (progress_bar=True) facilita o acompanhamento no terminal.
    model.learn(total_timesteps=500000, progress_bar=True)
    
    # Salva os pesos e configurações da rede neural treinada no caminho do pacote
    model.save(model_pkg_path + "ppo_cartpole_ros2")

    # Encerra o ambiente corretamente após a conclusão do treinamento
    env.close()
   
if __name__ == '__main__':
    main()