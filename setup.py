from setuptools import setup, find_packages

setup(
    name="business-feedback-analyzer",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "nltk",
        "spacy",
        "scikit-learn",
        "matplotlib",
        "ollama-client"
    ],
    entry_points={
        "console_scripts": [
            "business-feedback-analyzer=src.app:main",
        ],
    },
)