from setuptools import setup

setup(
    name="hcli",
    version="1.0.16",
    packages=["hcli", "hcli.commands", "hcli.api", "hcli.utils", "hcli.utils.terminal"],
    url="https://github.com/hudduapp/cli",
    install_requires=["typer", "rich", "huddu", "inquirer", "pyyaml"],
    license="MIT",
    author="Joshua3212",
    author_email="hello@huddu.io",
    description="Official CLI for huddu.io",
    entry_points={"console_scripts": ["hcli=hcli.main:app"]},
)
