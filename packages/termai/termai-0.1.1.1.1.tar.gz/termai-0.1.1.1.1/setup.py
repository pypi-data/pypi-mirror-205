from setuptools import setup, find_packages

setup(
    name='termai',
    version='0.1.1.1.1',
    author='Brad Ganley',
    author_email='bradganley@pm.me',
    description='A package for generating and manipulating text and images using OpenAI.',
    packages=find_packages(),
    install_requires=[
        'click==8.0.1',
        'openai==0.10.5',
        'requests==2.26.0',
        'Pillow==8.3.2'
    ],
    entry_points={"console_scripts": ["termchat = termai.cli:cli"]}
    )
