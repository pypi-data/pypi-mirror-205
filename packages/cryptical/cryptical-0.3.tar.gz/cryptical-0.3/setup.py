from setuptools import setup

setup(
    name="cryptical",
    version="0.3",
    author="Harshit Tyagi",
    author_email="damnitharshit@gmail.com",
    description="A simple GUI password manager",
    packages=["cryptical"],
    install_requires=[
        "cryptography>=40.0.1",
        "customtkinter>=5.1.2",
        "Pillow>=9.5.0",
        "setuptools>=67.6.1",
    ],
    entry_points={
        "console_scripts": [
            "cryptical = cryptical.cryptical:main",
        ],
    },
)
