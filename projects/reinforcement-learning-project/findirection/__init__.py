from gym.envs.registration import register

register(
    id = 'FindDirEnv-v0',
    entry_point = 'findirection.envs:FindDirection_v0',
)

register(
    id = 'FindDirEnv-v1',
    entry_point = 'findirection.envs:FindDirection_v1',
)