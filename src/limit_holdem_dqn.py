''' An example of learning a Deep-Q Agent on Texas Limit Holdem
'''

import tensorflow as tf
import os

import rlcard
from rlcard.agents.my_dqn_agent import MyDQNAgent
from rlcard.agents.dqn_agent import DQNAgent
from rlcard.agents import RandomAgent
from rlcard.utils import set_global_seed, tournament
from rlcard.utils import Logger
import datetime

import matplotlib.pyplot as plt
import torch

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
log_dir = './src/experiments/limit_holdem_dqn_result/' + datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + '/'

# The Array of loss
losses = []
# Set a global seed
set_global_seed(0)

with tf.Session() as sess:

    # Initialize a global step
    global_step = tf.Variable(0, name='global_step', trainable=False)

    # Set up the agents
    agent = MyDQNAgent(
                     scope='dqn',
                     action_num=env.action_num,
                     replay_memory_init_size=memory_init_size,
                     train_every=train_every,
                     state_shape=[82],
                     epsilon_decay_steps=episode_num,
                     mlp_layers=[512,512])
    # ここで自分のもう一つのエージェントを追加しよう。
    random_agent = RandomAgent(action_num=eval_env.action_num)
    env.set_agents([agent, random_agent])
    eval_env.set_agents([agent, random_agent])

    # Initialize global variables
    sess.run(tf.global_variables_initializer())

    # Init a Logger to plot the learning curve
    logger = Logger(log_dir)

    for episode in range(episode_num):

        # Generate data from the environment
        trajectories, _ = env.run(is_training=True)

        # Feed transitions into agent memory, and train the agent
        for ts in trajectories[0]:
            loss = agent.feed(ts)
            if loss:
                losses.append((env.timestep, loss))
        # Evaluate the performance. Play with random agents.
        if episode % evaluate_every == 0:
            logger.log_performance(env.timestep, tournament(eval_env, evaluate_num)[0])

    # Close files in the logger
    logger.close_files()

    # Plot the learning curve
    logger.plot('DQN')
    
    # Save model
    save_dir = './src/models/limit_holdem_dqn/'
    dt = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    save_dir += dt + '/'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    torch.save(agent.q_estimator.qnet.state_dict(), save_dir + 'model.pth')
    
    # plot loss
    
    xs = []
    ys = []
    print(losses)
    for (x, y) in losses:
        xs.append(int(x))
        ys.append(float(y))
    fig, ax = plt.subplots()
    ax.plot(xs, ys, label="DQN")
    ax.set(xlabel='timestep', ylabel='loss')
    ax.legend()
    ax.grid()
    save_path = log_dir + 'loss_log.png'
    save_dir = os.path.dirname(save_path)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    fig.savefig(save_path)