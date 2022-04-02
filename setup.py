import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="roborecipe", # Replace with your own username
    version="0.0.1",
    install_requires=[
        "requests",
    ],
    entry_points={
        'console_scripts': [
            'roborecipe=roborecipe:main',
        ],
    },
    author="Erio.Akanuma",
    author_email="e.a@example.com",
    description="generate robot build instraction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)