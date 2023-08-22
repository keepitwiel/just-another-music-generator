from setuptools import setup

name = "just-another-music-generator"
package = "src"

setup(
    name=name,
    version="0.12.1",
    packages=[package],
    entry_points={"console_scripts": [f"{name}={package}.cli:cli"]},
)
