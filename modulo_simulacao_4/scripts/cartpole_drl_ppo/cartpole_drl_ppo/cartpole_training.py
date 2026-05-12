from cartpole_drl_ppo.cartpole_env import CartPoleROS2Env
from stable_baselines3 import PPO
from ament_index_python.packages import get_package_share_directory

def main(args=None):
    
    package_name = 'cartpole_drl_ppo'
    model_pkg_path = get_package_share_directory(package_name) + "/" 

    env = CartPoleROS2Env()
    
    # 1. Adicionamos o device='cpu' para remover o aviso e melhorar a velocidade da MlpPolicy
    model = PPO('MlpPolicy', env, verbose=1, device='cpu')

    # 2. Aumentamos o total_timesteps para um valor real de treinamento (ex: 50000)
    # Se ficar apenas 1, o código fecha no mesmo segundo.
    #model.learn(total_timesteps=50000, progress_bar=True)
    model.learn(total_timesteps=500000, progress_bar=True)
    
    model.save(model_pkg_path + "ppo_cartpole_ros2")

    env.close()
   
if __name__ == '__main__':
    main()