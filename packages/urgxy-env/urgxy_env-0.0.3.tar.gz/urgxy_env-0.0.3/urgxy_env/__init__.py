from gym.envs.registration import register

register(
    id='urgxy_env-v3',
    entry_point='urgxy_env.envs:UrgxyEnv',
)