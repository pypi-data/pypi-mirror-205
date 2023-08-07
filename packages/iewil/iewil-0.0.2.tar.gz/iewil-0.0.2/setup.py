from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'Streaming video data via networks'

# Setting up
setup(
    name="iewil",
    version=VERSION,
    author="iewilmaestro",
    author_email="<purna.iera@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['iewil'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)