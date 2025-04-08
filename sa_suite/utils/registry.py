"""
Registry for custom environments in sa_suite.
This module stores and manages the registry of custom environments.
"""
import importlib
import inspect

# Dictionary to store custom environments
CUSTOM_ENVIRONMENTS = {}

def register_env_class(env_class):
    """
    Register a class as an available environment.
    
    Args:
        env_class: The environment class to register
    """
    class_name = env_class.__name__
    CUSTOM_ENVIRONMENTS[class_name] = env_class
    print(f"Registered custom environment: {class_name}")

def get_env_class(class_name):
    """
    Get an environment class by name.
    
    Args:
        class_name: Name of the environment class
        
    Returns:
        The environment class or None if not found
    """
    return CUSTOM_ENVIRONMENTS.get(class_name)

def list_registered_envs():
    """
    List all registered custom environments.
    
    Returns:
        List of registered environment names
    """
    return list(CUSTOM_ENVIRONMENTS.keys())
