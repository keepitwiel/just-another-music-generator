from setuptools import setup

name = "just-another-music-generator"
package = "just_another_music_generator"

setup(
    name=name,
    version="0.12.0",
    packages=[package],
    entry_points={"console_scripts": [f"{name}={package}.cli:cli"]},
)
