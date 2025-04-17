from setuptools import setup, find_packages

# Read requirements from requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

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
