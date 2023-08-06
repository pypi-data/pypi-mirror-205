import setuptools
from pathlib import Path

setuptools.setup(
    name='urgxy_env',
    author="GXY",
    version='0.0.4',
    description="An OpenAI Gym Env for Panda",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(include="urgxy_env*"),
    install_requires=['gym', 'pybullet', 'numpy'],  # And any other dependencies foo needs
    python_requires='>=3.6'
)