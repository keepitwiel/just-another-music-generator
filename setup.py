from setuptools import setup

setup(
    name='just-another-music-generator',
    version='0.2.1',
    packages=[
        'just_another_music_generator',
    ],
    entry_points={
        'console_scripts': [
            'just-another-music-generator=just_another_music_generator.cli:cli',
        ]
    }
)
