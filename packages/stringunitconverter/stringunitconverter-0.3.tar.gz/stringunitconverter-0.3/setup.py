import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stringunitconverter",
    version="0.3",
    author="Arne Baeyens",
    author_email="mail@arnebaeyens.com",
    description="Unit converter: Returns multiplier for unit conversion, with units defined as strings.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/abaeyens/stringunitconverter",
    keywords='unit conversion, conversion',
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    package_data={'': ['*.json']},
    install_requires=['importlib_resources',
                      ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Intended Audience :: Manufacturing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
