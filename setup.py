"""
Industrial Plant Simulation Software
Setup configuration
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="plant-simulation-software",
    version="0.1.0-dev",
    author="Your Name",
    author_email="your.email@example.com",
    description="Educational chemical process simulation software",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/plant-simulation-software",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Chemistry",
    ],
    python_requires=">=3.10",
    install_requires=[
        "numpy>=1.24.0",
        "scipy>=1.10.0",
        "pandas>=2.0.0",
    ],
)