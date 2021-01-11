import tensorflow as tf
import os

import rlcard
from rlcard.agents.my_dqn_agent import MyDQNAgent
from rlcard.agents.dqn_agent import DQNAgent
from rlcard.agents import RandomAgent
from rlcard.utils import set_global_seed, tournament
from rlcard.utils import Logger
import datetime
import torch
import matplotlib.pyplot as plt
from rlcard.agents.my_dqn_agent import EstimatorNetwork as Model
# Make environment
env = rlcard.make('limit-holdem', config={'seed': 0})
eval_env = rlcard.make('limit-holdem', config={'seed': 0})

# Set the iterations numbers and how frequently we evaluate the performance
evaluate_every = 100
evaluate_num = 1000
episode_num = 2000

# The intial memory size
memory_init_size = 1000

# Train the agent every X steps
train_every = 1

# The paths for saving the logs and learning curves
log_dir = '.src/experiments/limit_holdem_dqn_result/' + datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + '/'

# The Array of loss
losses = []
# Set a global seed
set_global_seed(0)

# If True there is model in arg path
#Command line arg :TODO
path = './src/models/limit_holdem_dqn/' + '2021_01_11_15_03_53/model.pth'
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
agent_1 = MyDQNAgent(
    scope='dqn',
    action_num=env.action_num,
    replay_memory_init_size=memory_init_size,
    train_every=train_every,
    state_shape=[82],
    epsilon_decay_steps=episode_num,
    mlp_layers=[512,512]
)
agent_1.q_estimator.qnet.load_state_dict(torch.load(path, map_location=device))
random_agent = RandomAgent(action_num=eval_env.action_num)
env.set_agents([agent_1, random_agent])
eval_env.set_agents([agent_1, random_agent])

# Init a Logger to plot the learning curve
logger = Logger(log_dir)

for episode in range(episode_num):

    # Generate data from the environment
    trajectories, _ = env.run()

    # Feed transitions into agent memory, and train the agent
    # for ts in trajectories[0]:
    #     loss = agent.feed(ts)
    #     if loss:
    #         losses.append((env.timestep, loss))
    # Evaluate the performance. Play with random agents.
    if episode % evaluate_every == 0:
        logger.log_performance(env.timestep, tournament(eval_env, evaluate_num)[0])

# Close files in the logger
logger.close_files()
