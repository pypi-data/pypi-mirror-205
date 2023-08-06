import setuptools
from pathlib import Path


setuptools.setup(
    name="gdev-powertools",  # ? nombre del paquete en pypi
    version="0.0.1",
    author_email="dolgasan@gmail.com",
    description="GDEV Powertools",
    long_description=Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url="https://github.com/XXXXXXXXXXX/gdev-aws-powertools",
    packages=setuptools.find_packages(  # ? le indicamos cuales son los directorios que vamos a incluir o ignorar
        exclude=["tests", "mocks"],
    ),
    install_requires=[
        "boto3",
        "requests",
    ],
    keywords=["aws", "lambda"],
)
