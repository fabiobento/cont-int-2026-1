import time
from stable_baselines3 import PPO
from cartpole_drl_ppo.cartpole_env import CartPoleROS2Env
from ament_index_python.packages import get_package_share_directory

def main(args=None):

    package_name = 'cartpole_drl_ppo'
    model_pkg_path = get_package_share_directory(package_name) + "/" 

    # 1. Adicionamos device='cpu' para carregar o modelo sem gerar gargalos ou avisos
    model = PPO.load(model_pkg_path + "ppo_cartpole_ros2.zip", device='cpu')
    env = CartPoleROS2Env()
    
    print("Iniciando a Inteligência Artificial! Pressione Ctrl+C para parar.")

    try:
        # 2. Laço infinito para o robô tentar de novo sempre que cair
        while True:
            obs, _ = env.reset()
            time.sleep(1) # Tempo para a física do Gazebo estabilizar após o reset

            done = False
            truncated = False
            
            # Executa as ações até o robô cair (done) ou o limite de tempo estourar (truncated)
            while not (done or truncated):        
                action, _ = model.predict(obs)
                obs, reward, done, truncated, info = env.step(action)
                time.sleep(0.01)
                
            print("O robô desequilibrou! Reiniciando o episódio...")
            
    except KeyboardInterrupt:
        print("Inferência encerrada pelo usuário.")
    finally:
        env.close()

if __name__ == '__main__':
    main()