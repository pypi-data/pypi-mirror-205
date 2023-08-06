import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tonconsole",
    version="0.0.21",
    author="nessshon",
    description="Connecting businesses to the TON ecosystem.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nessshon/tonconsole/",
    packages=setuptools.find_packages(exclude="tonconsole"),
    python_requires='>=3.10',
    install_requires=[
        "aiohttp>=3.8.3",
        "libscrc>=1.8.1",
        "pydantic>=1.10.4",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
