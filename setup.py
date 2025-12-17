from setuptools import setup, find_packages

setup(
    name="stock-analytics",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "yfinance",
        "pandas",
        "flask",
        "plotly",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="Stock market analytics with star schema data warehouse",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/stock-analytics",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
