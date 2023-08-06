from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="nyaa-timer",
    version="2.0.0",
    packages=find_packages(),
    install_requires=["rich"],
    author="Praveen Senpai",
    author_email="pvnt20@gmail.com",
    description="A simple nyaa_timer decorator to calculate the elapsed time of a function",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
