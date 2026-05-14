"""
Script de Inferência/Predição do Agente de DRL.

Este script carrega o modelo PPO previamente treinado e o utiliza para 
controlar o ambiente CartPoleROS2Env em tempo real. O robô tenta 
equilibrar o pêndulo infinitamente, reiniciando o episódio de forma 
automática sempre que o pêndulo cair ou o carrinho sair dos limites.
"""

import time
from stable_baselines3 import PPO
from cartpole_drl_ppo.cartpole_env import CartPoleROS2Env
from ament_index_python.packages import get_package_share_directory

def main(args=None):
    """
    Função principal que carrega o modelo treinado, inicializa o ambiente
    e executa o laço de controle (inferência) de forma contínua.
    """
    package_name = 'cartpole_drl_ppo'
    # Obtém o diretório de instalação do pacote onde o modelo foi salvo
    model_pkg_path = get_package_share_directory(package_name) + "/" 

    # Carrega a rede neural pré-treinada a partir do arquivo .zip.
    # Utilizamos device='cpu' para carregar o modelo sem gerar gargalos ou avisos
    # caso estejamos em uma máquina sem GPU ou com configurações PyTorch simples.
    model = PPO.load(model_pkg_path + "ppo_cartpole_ros2.zip", device='cpu')
    
    # Instancia o ambiente customizado integrado com ROS 2
    env = CartPoleROS2Env()
    
    print("Iniciando a Inteligência Artificial! Pressione Ctrl+C para parar.")

    try:
        # Laço infinito para o robô continuar tentando indefinidamente
        while True:
            # Reseta o ambiente para a posição inicial e obtém a primeira observação
            obs, _ = env.reset()
            # Tempo de espera para a física do simulador Gazebo estabilizar após o reset
            time.sleep(1) 

            done = False
            truncated = False
            
            # Laço do episódio atual: executa ações continuamente enquanto a simulação for válida
            # O laço para se o robô cair/sair da pista (done) ou o limite de tempo estourar (truncated)
            while not (done or truncated):        
                # A rede neural prevê a melhor ação a tomar com base na observação atual (obs)
                action, _ = model.predict(obs)
                
                # O ambiente aplica a ação e devolve o novo estado, a recompensa e os status
                obs, reward, done, truncated, info = env.step(action)
                
                # Pequena pausa para sincronizar os cálculos com o tempo de simulação
                time.sleep(0.01)
                
            # Mensagem exibida no terminal quando a condição "done" ou "truncated" for atingida
            print("O robô desequilibrou ou falhou! Reiniciando o episódio...")
            
    except KeyboardInterrupt:
        # Tratamento seguro caso o usuário decida parar a execução usando Ctrl+C no terminal
        print("Inferência encerrada pelo usuário (Ctrl+C).")
    finally:
        # Garante que as conexões do ROS 2 e threads sejam limpas antes de fechar o script
        env.close()

if __name__ == '__main__':
    main()