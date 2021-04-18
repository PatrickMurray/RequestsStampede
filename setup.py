"""
TODO
"""

import setuptools


VERSION = {
    "major": 0,
    "minor": 9,
    "patch": 1,
}


with open("README.md", "r") as handler:
    long_description = handler.read()


setuptools.setup(
    name="RequestsStampede",
    version="{}.{}.{}".format(
        VERSION.get("major"), VERSION.get("minor"), VERSION.get("patch")
    ),
    description="A wrapper around the Requests library that provides request retry logic and backoff delays.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/patrickmurray/RequestsStampede",
    author="Patrick Murray",
    author_email="patrick@murray.systems",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS",
    ],
    packages=setuptools.find_packages(),
    install_requires=["schema>=0.7.4", "pyyaml>=5.4.1", "requests>=2.25.1"],
    python_requires=">=3.7",
)
