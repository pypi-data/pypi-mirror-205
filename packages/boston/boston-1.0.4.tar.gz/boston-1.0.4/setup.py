import setuptools


setuptools.setup(
    name="boston", # Replace with your own username
    version="1.0.4",
    author="julmubm",
    author_email="dltpdn@gmail.com",
    description="loading boston housing price dataset like sklearn.datasets.load_boston() style.",
    long_description_content_type="text/markdown",
    url="https://github.com/dltpdn/boston",
    install_requires=['pandas'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)