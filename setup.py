import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Facebooker",
    version="0.0.2",
    author="gpwork4u",
    author_email="gpwork4u@gmail.com",
    description="An un official facebook api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gpwork4u/Facebooker",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'beautifulsoup4',
        'requests'
    ],
    python_requires='>=3.6',
)
