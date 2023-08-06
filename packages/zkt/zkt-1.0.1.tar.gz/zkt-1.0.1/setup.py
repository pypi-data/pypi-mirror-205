from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="zkt",
    version="1.0.1",
    license="MIT",
    author="Noé Cruz",
    author_email="contactozurckz@gmail.com",
    description="Helper tool for api test automation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages("src"),
    package_dir={"": "src"},
    url="https://github.com/gmyrianthous/example-publish-pypi",
    keywords="zurckz test testing",
    install_requires=[
        "zpy-api-core",
    ],
    python_requires=">=3.6",
)
