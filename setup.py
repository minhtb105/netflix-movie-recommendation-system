from setuptools import setup, find_packages

setup(
    name="netflix_recommender",
    version="0.1.0",
    packages=find_packages(where="."), 
    include_package_data=True,
    install_requires=[
        "python-dotenv==1.1.1",
        "requests==2.32.4",
        "pandas==2.3.1",
        "numpy==2.3.2",
        "pyyaml==6.0.2",
        "feast==0.51.0",
        "sentence_transformers==5.0.0",
        "redis==6.2.0"
    ],
)
