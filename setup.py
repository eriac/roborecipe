import setuptools
import roborecipe

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="roborecipe",
    version=roborecipe.__version__,
    install_requires=[
        "PyOpenGL",
        "jinja2",
        "pillow",
        "networkx",
        "panda3d-viewer",
    ],
    entry_points={
        'console_scripts': [
            'roborecipe=roborecipe.roborecipe_main:main',
        ],
    },
    author="Erio.Akanuma",
    author_email="e.a@example.com",
    description="generate robot build instruction from scripts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eriac/roborecipe",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)