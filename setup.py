from setuptools import setup, find_packages
import re

# Read requirements from requirements.txt
with open('requirements.txt') as f:
    requirements_text = f.read()

# Parse regular dependencies (excluding editable ones)
requirements = []
for line in requirements_text.splitlines():
    line = line.strip()
    # Skip empty lines and comments
    if not line or line.startswith('#'):
        continue
    # Skip editable installs (starting with -e)
    if line.startswith('-e'):
        continue
    requirements.append(line)

setup(
    name="sa_suite",
    version="0.1.0",
    description="Shared autonomy tasks for robosuitek",
    author="Edward Sun",
    author_email="edward.sun2015@gmail.com",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [],
    },
)
