from setuptools import find_packages, setup


setup(
    name="securecrypto",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "argon2-cffi",
        "cryptography",
        "flask",
    ],
    entry_points={
        "console_scripts": [
            "securecrypto=securecrypto.cli:main",
        ],
    },
)
