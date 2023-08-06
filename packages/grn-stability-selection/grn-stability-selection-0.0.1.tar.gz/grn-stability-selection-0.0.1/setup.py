from pathlib import Path

from setuptools import find_packages, setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="grn-stability-selection",
    packages=find_packages(exclude=[]),
    version="0.0.1",
    license="MIT",
    description="Stability selection for sparse gene regulatory networks",
    long_description="GRN - Stability Selection",
    author="Soel Micheletti",
    author_email="msoel@ethz.ch",
    url="https://github.com/soelmicheletti/grn-stability-selection",
    keywords=[
        "gene regulatory networks",
        "statistical inference",
    ],
    install_requires=["mixem>=0.1.4", 
                      "scikit-learn",
                      "pandas",
                      "numpy"
                     ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
)
