from setuptools import setup, find_packages

setup(
    name='just-another-music-generator',
    version='0.0.2',
    packages=find_packages(
        include=[
            'just_another_music_generator',
            'just_another_music_generator.*'
        ]
    )
)
