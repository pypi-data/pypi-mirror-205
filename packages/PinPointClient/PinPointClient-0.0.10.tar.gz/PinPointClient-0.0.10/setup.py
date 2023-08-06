import setuptools

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name='PinPointClient',
    version="0.0.10",
    author="Yaşar Özyurt",
    author_email="blueromans@gmail.com",
    description='PinPoint Aws Pinpoint SMS/Mail Client Python package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/blueromans/PinPointClient.git',
    project_urls={
        "Bug Tracker": "https://github.com/blueromans/PinPointClient/issues",
    },
    install_requires=['boto3'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=['pinpoint'],
    python_requires=">=3.6",
)
