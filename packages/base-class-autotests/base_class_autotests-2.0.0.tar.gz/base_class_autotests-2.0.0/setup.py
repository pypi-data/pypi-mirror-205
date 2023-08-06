from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = [
    "selenium==4.9.0",
    "allure-pytest==2.13.1"
]

setup(
    name="base_class_autotests",
    version="2.0.0",
    author="Kostuchenko_VA, Mishin_VA",
    author_email="kostuchenko_va@magnit.ru, mishin_va@magnit.ru",
    description="Base class with basic checks of the elements",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://coderepo.corp.tander.ru/mishin_va/basic_checks",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
