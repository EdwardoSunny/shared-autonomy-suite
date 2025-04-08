"""
Example script showing how to use the custom environments.
"""
import robosuite as suite

# Import sa_suite to register environments and patch robosuite
# This must be done before calling robosuite.make
import sa_suite
import numpy as np

def main():
    # List available custom environments
    print("Available custom environments:", sa_suite.list_registered_envs())
    
    # Create a custom environment using robosuite.make
    # This works because we've patched robosuite.make
    env = suite.make(
    env_name="PickPlaceSA", # try with other tasks like "Stack" and "Door"
    robots="Panda",  # try with other robots like "Sawyer" and "Jaco"
    has_renderer=True,
    has_offscreen_renderer=False,
    use_camera_obs=False,
    )

    # reset the environment
    env.reset()

    for i in range(1000):
        action = np.random.randn(*env.action_spec[0].shape) * 0.1
        obs, reward, done, info = env.step(action)  # take action in the environment
        env.render()  # render on display

if __name__ == "__main__":
    main()
