from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import sys


class PostInstallCommand(install):
    def run(self):
        install.run(self)
        self.spawn([sys.executable, "post_install.py"])


setup(
    name="api_hunter_cli",
    version="0.1.3",
    description="CLI tool for finding hidden apis in a certain url.",
    author="Charly Molero",
    author_email="perez.moleroc@gmail.com",
    url="https://github.com/engcarlosperezmolero/",
    packages=find_packages(),
    install_requires=[
        "playwright",
        "typer[all]",
        "yaspin",
        "inquirer",
    ],
    entry_points={
        "console_scripts": [
            "apihunter=apihunter.__main__:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    package_data={
            "api_hunter_cli": ["post_install.py"],
        },
    cmdclass={"post_install": PostInstallCommand},
)
