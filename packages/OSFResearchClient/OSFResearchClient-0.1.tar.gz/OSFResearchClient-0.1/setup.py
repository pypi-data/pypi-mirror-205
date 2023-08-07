from setuptools import setup

setup(
    name="OSFResearchClient",
    version="0.1",
    description="Client Wrapper class for OSF API calls",
    packages=["client"],
    author="DisruptionLab",
    install_requires=["requests"]
)