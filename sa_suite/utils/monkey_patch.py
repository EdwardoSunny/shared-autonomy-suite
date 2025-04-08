"""
Monkey patching module for RoboSuite integration.
This module patches the robosuite.make function to include custom environments.
"""
import robosuite
from sa_suite.utils.registry import CUSTOM_ENVIRONMENTS

def patch_robosuite():
    """
    Patch the robosuite.make function to support custom environments.
    This should be called once at the start of your program.
    """
    # Store the original make function
    original_make = robosuite.make
    
    # Define a wrapper function that intercepts the environment name
    def custom_make(env_name, *args, **kwargs):
        if env_name in CUSTOM_ENVIRONMENTS:
            # Create and return the custom environment
            env_class = CUSTOM_ENVIRONMENTS[env_name]
            return env_class(*args, **kwargs)
        else:
            # Call the original function for other environments
            return original_make(env_name, *args, **kwargs)
    
    # Replace the original function with our custom one
    robosuite.make = custom_make
    
    print("Successfully patched robosuite.make to support custom environments")
