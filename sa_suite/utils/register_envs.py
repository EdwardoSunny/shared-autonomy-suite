"""
Register all custom environments in the sa_suite package.
This module imports and registers all custom environments with the registry.
"""
from sa_suite.utils.registry import register_env_class

# Import all your custom environment classes
from sa_suite.environments.pick_place_sa import PickPlaceSA
# Add more imports as needed
# from sa_suite.environments.other_env import OtherEnv

def register_all_envs():
    """
    Register all custom environments in the sa_suite package.
    """
    # Register individual environments
    register_env_class(PickPlaceSA)
    # Add more environments as you create them
    # register_env_class(OtherEnv)
    
    print("All custom environments registered successfully")
