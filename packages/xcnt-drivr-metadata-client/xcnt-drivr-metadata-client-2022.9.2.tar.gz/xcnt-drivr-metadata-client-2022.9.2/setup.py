import os
import sys
from typing import Dict, List

from setuptools import find_namespace_packages, setup

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 8)
EGG_NAME = "xcnt-drivr-metadata-client"


def list_packages(source_directory: str = "src") -> List[str]:
    packages = list(find_namespace_packages(source_directory, exclude="venv"))
    return packages


def list_namespace_packages(source_directory: str = "src") -> List[str]:
    if len(list_packages(source_directory=source_directory)) > 0:
        return ["xcnt", "xcnt.drivr"]
    else:
        return []


def get_package_dir() -> Dict[str, str]:
    if not os.path.isdir("src"):
        return {}
    return {"": "src"}


requirements = [
    "inflection>=0.5.1",
    "marshmallow>=3,<4",
    "sqlalchemy>=1.3,<2",
    "webargs>=7.0.0b1,<9",
    "xcnt-cqrs>=2022.2.1",
    "xcnt-cqrs-sqlalchemy>=2022.1.1",
]

minimum_sqlalchemy_search_version = "2022.2.2"
kafka_http_client_requirements = ["xcnt-cqrs-kafka-http-client>=2022.2.0"]
sqlalchemy_search_requirements = [f"xcnt-sqlalchemy-search>={minimum_sqlalchemy_search_version}"]
sqlalchemy_search_apispec_requirements = [
    f"xcnt-sqlalchemy-search[apispec]>={minimum_sqlalchemy_search_version}",
    "apispec>=4.3.0",
]
test_requirements = (
    [
        "black>=19.10b0",
        "coverage>=7,<8",
        "factory_boy>=2.12.0",
        "flake8>=6,<7",
        "mypy>=0.812",
        "mypy-extensions>=0.4.3",
        "pre-commit>=3.0.4,<4",
        "psycopg2>=2.8.5,<3",
        "sqlalchemy-cockroachdb>=1.3.1",
        "pytest-cases>=1.13.1,<4",
        "pytest>=5.4.1,<8.0.0",
        "pytest-html",
        "pytest-mock>=3.3.0,<4",
        "python-dotenv>=0.13.0,<1",
        "twine>=3.1.1,<5",
        "xcnt-cqrs-mypy-plugin>=2022.0.0",
        "python-semantic-release>=7.19.2,<8",
        "types-setuptools",
    ]
    + kafka_http_client_requirements  # noqa: W503
    + sqlalchemy_search_requirements  # noqa: W503
    + sqlalchemy_search_apispec_requirements  # noqa: W503
)


__version__ = "2022.9.2"
setup(
    name=EGG_NAME,
    version=__version__,
    python_requires=">={}.{}".format(*REQUIRED_PYTHON),
    url="https://github.com/xcnt/cqrs-metadata-client",
    author="XCNT Dev Team",
    author_email="dev-infra@xcnt.io",
    description="",
    long_description="",
    license="Internal",
    packages=list_packages(),
    package_dir=get_package_dir(),
    entry_points={
        "xcnt.sqlalchemy.search.field.parser": [
            "metadata = xcnt.drivr.metadata_client.search.parser:MetadataFieldParser",
            "metadata_item = xcnt.drivr.metadata_client.search.parser:MetadataItemParser",
            "metadata_key_value_store_field = xcnt.drivr.metadata_client.search.parser:MetadataKeyValueStoreFieldParser",  # noqa: E501
            "metadata_type_key = xcnt.drivr.metadata_client.search.parser:MetadataTypeKeyParser",
        ],
        "xcnt.sqlalchemy.search.field.apispec": [
            "metadata = xcnt.drivr.metadata_client.search.apispec:MetadataFieldOpenAPIConverterPlugin",
            "metadata_key_value_field = xcnt.drivr.metadata_client.search.apispec:MetadataKeyValueStoreFieldOpenAPIConverterPlugin",  # noqa: E501
        ],
        "xcnt.sqlalchemy.search.field.apigatewaycrd": [
            "metadata = xcnt.drivr.metadata_client.search.api_gateway_crd:MetadataFieldAPIGatewayCRDConverterPlugin",
            "metadata_key_value_field = xcnt.drivr.metadata_client.search.api_gateway_crd:MetadataKeyValueStoreFieldAPIGatewayCRDConverterPlugin",  # noqa: E501
        ],
    },
    include_package_data=True,
    install_requires=requirements,
    extras_require={
        "test": test_requirements,
        "search": sqlalchemy_search_requirements,
        "apispec": sqlalchemy_search_apispec_requirements,
        "kafka-http-client": kafka_http_client_requirements,
    },
    zip_safe=False,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    project_urls={"GitHub": "https://github.com/xcnt/drivr-metadata-client"},
    namespace_packages=list_namespace_packages(),
)
