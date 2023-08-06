from typing import List
from pathlib import Path
import setuptools

description = "A collection of Expectations to validate for degradation, bias, and related Ethical Data concerns with Great Expectations."

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


def get_requirements() -> List[str]:
    with open("/Users/austin/great_expectations/great_expectations/contrib/great_expectations_ethical_ai_expectations/requirements.txt") as f:
        requirements = f.read().splitlines()
    return requirements


setuptools.setup(
    name="great_expectations_ethical_ai_expectations",
    author_email="austin@greatexpectations.io",
    author="Great Expectations",
    version="0.1.0",
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=get_requirements(),
)
