"""
Shared Autonomy Suite (sa_suite) package.
This package extends RoboSuite with custom environments for shared autonomy.
"""
# Version information
__version__ = "0.1.0"

# Import core functionality
from sa_suite.utils.registry import list_registered_envs, get_env_class
from sa_suite.utils.monkey_patch import patch_robosuite

# Automatically register all environments and patch robosuite when imported
from sa_suite.utils.register_envs import register_all_envs

# Register all environments
register_all_envs()

# Monkey patch robosuite
patch_robosuite()
