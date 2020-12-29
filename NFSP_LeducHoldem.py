### Settings for Evaluation ###
# Set the iterations numbers and how frequently we evaluate/save plot
from rlcard.agents.nfsp_agent import NFSPAgent
import tensorflow as tf
from rlcard.utils.logger import Logger
from rlcard.utils.utils import set_global_seed
from rlcard.agents.random_agent import RandomAgent
import rlcard
evaluate_every = 100
save_plot_every = 1000
evaluate_num = 10000

# The paths for saving the logs and learning curves
root_path = './experiments/leduc_holdem_nfsp_result/'
log_path = root_path + 'log.txt'
csv_path = root_path + 'performance.csv'
figure_path = root_path + 'figures/'
### Settings for Evaluation ###

### Step 1: Make the Environment. ###
# Make environment
env = rlcard.make('leduc-holdem')
eval_env = rlcard.make('leduc-holdem')
# Set a global seed
set_global_seed(0)

### Step 2: Initialize the NFSP agents. ###
with tf.Session() as sess:
    # Set agents
    global_step = tf.Variable(0, name='global_step', trainable=False)
    agents = []
    for i in range(env.player_num):
        agent = NFSPAgent(sess,
                          scope='nfsp' + str(i),
                          action_num=env.action_num,
                          state_shape=env.state_shape,
                          hidden_layers_sizes=[128, 128],
                          min_buffer_size_to_learn=1000,
                          q_replay_memory_init_size=1000,
                          # q_norm_step=100,
                          q_mlp_layers=[128, 128])
        agents.append(agent)

    # Initialize the parameters of policy networks
    sess.run(tf.global_variables_initializer())
    env.set_agents(agents)  # Setup all nfsp agents into training environments

    # Setup random agent for evaluation
    random_agent = RandomAgent(action_num=eval_env.action_num)
    eval_env.set_agents([agents[0], random_agent])

    ### Step 3: Generate game data and train the agents. ###
    episode_num = 10000000  # set the episode number
    # Count the number of steps
    step_counters = [0 for _ in range(env.player_num)]

    # Init a Logger to plot the learning curve
    logger = Logger(xlabel='timestep', ylabel='reward',
                    legend='NFSP on Leduc Holdem', log_path=log_path, csv_path=csv_path)

    for episode in range(episode_num):

        # First sample a policy for the episode
        for agent in agents:
            agent.sample_episode_policy()

        # Generate data from the environment
        trajectories, _ = env.run(is_training=True)

        # Feed transitions into agent memory, and train the agent
        for i in range(env.player_num):
            for ts in trajectories[i]:
                agents[i].feed(ts)
                step_counters[i] += 1

                # Train the agent
                train_count = step_counters[i] - (memory_init_size + norm_step)
                if train_count > 0 and train_count % 64 == 0:
                    rl_loss = agents[i].train_rl()
                    sl_loss = agents[i].train_sl()
                    print('\rINFO - Agent {}, step {}, rl-loss: {}, sl-loss: {}'.format(i,
                                                                                        step_counters[i], rl_loss, sl_loss), end='')

        ### Evaluation Step: Evaluate the agent every 100 steps and generate the plot for analysis. ###
        # Evaluate the performance. Play with random agents.
        if episode % evaluate_every == 0:
            reward = 0
            for eval_episode in range(evaluate_num):
                _, payoffs = eval_env.run(is_training=False)
                reward += payoffs[0]

            logger.log('\n########## Evaluation ##########')
            logger.log('Timestep: {} Average reward is {}'.format(
                env.timestep, float(reward)/evaluate_num))

            # Add point to logger
            logger.add_point(x=env.timestep, y=float(reward)/evaluate_num)

        # Make plot
        if episode % save_plot_every == 0 and episode > 0:
            logger.make_plot(save_path=figure_path+str(episode)+'.png')

    # Make the final plot
    logger.make_plot(save_path=figure_path+'final_'+str(episode)+'.png')
