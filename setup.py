import os

from setuptools import find_packages, setup


# Read requirements from requirements.txt
def read_requirements(filename="requirements.txt"):
    with open(filename) as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


# Read long description from README
def read_long_description(filename="README.md"):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


setup(
    name="ai-exam-paper-generator",
    version="0.1.0",
    description="LLM-based exam paper answer generator",
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    author="Vaibhav Waykole",
    author_email="vaibhavwaykole@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=read_requirements(),
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "exam-generator=src.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
