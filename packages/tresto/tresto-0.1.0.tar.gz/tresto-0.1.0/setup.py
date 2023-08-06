from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="tresto",
    version="0.1.0",
    author="Arturo 'Buanzo' Busleiman",
    author_email="buanzo@buanzo.com.ar",
    description="Python unit testing integrated with Trello, providing visualization of project status, ideal for test-driven development",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/buanzo/tresto",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'py-trello>=1.10.0'
    ]
)
