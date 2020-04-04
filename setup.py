import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="amazon_fresh_pkg", # Replace with your own username
    version="0.0.1",
    author="Obxino",
    author_email="zzhao212@gmail.com, qguo43@protonmail.com",
    description="Amazon fresh delivery time availability",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/guo43",
    packages=setuptools.find_packages(),
    entry_points={'console_scripts':['amazon_fresh=amazon_fresh.scan:main']}
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)