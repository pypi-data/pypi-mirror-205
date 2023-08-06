import setuptools
from pathlib import Path

setuptools.setup(
    name='urgxy_env1',
    author="GXY",
    version='0.1.0',
    description="An OpenAI Gym Env for Panda",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(include="urgxy_env*"),
    install_requires=['gym', 'pybullet', 'numpy'],  # And any other dependencies foo needs
    python_requires='>=3.6'
)