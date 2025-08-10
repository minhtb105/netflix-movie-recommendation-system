import numpy as np
import pandas as pd
from recsim.environments import interest_evolution_environment
from recsim.simulator import runner_lib
from recsim.agents import random_agent


config = {
    'num_candidates': 1000,       
    'slate_size': 5,             
    'resample_documents': True,   
    'num_users': 100,            
}


env = interest_evolution_environment.create_environment(config)
agent = random_agent.RandomAgent(env.action_space)


num_episodes = 50         
max_episode_length = 30   

interaction_logs = []

def custom_logger(timestep):
    observation = timestep.observation
    reward = timestep.reward

    for i in range(config['slate_size']):
        interaction_logs.append({
            'user_id': observation['user'][0],        
            'session_step': timestep.step_type,        
            'doc_id': observation['doc']['doc_id'][i], 
            'click_prob': observation['response'][i], 
            'reward': reward,                         
        })


runner_lib.simulate(
    environment=env,
    agent=agent,
    num_episodes=num_episodes,
    max_episode_length=max_episode_length,
    callback_fn=custom_logger  
)

df = pd.DataFrame(interaction_logs)
df.to_csv('synthetic_interactions.csv', index=False)

print(df.head())
print(f'Synthetic data saved: {len(df)} interactions.')