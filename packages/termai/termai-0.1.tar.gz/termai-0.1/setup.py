from setuptools import setup

setup(
    name='termai',
    version='0.1',
    author='Brad Ganley',
    author_email='bradganley@pm.me',
    description='Command-line tools for generating text and images using OpenAI',
    url='https://git.toad.city/brad/termai',
    packages=['termai'],
    install_requires=[
        'click==8.0.1',
        'openai==0.10.5',
        'requests==2.26.0',
        'Pillow==8.3.2',
    ],
    entry_points={
        'console_scripts': [
            'termpics=termai.termpics:main',
            'termchat=termai.termchat:main',
        ],
    },
)
