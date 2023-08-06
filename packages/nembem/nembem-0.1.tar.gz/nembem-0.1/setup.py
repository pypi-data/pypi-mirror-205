from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(name=
    'nembem',
    version='0.1',
    description='nembem_package',
    long_description =
    'spp package from final_project, first test',
    author=
    'Adam and Toke',
    packages=['nembem'],
    )