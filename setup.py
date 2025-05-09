from setuptools import setup, find_packages

setup(
    name="skillmortex",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[r.strip() for r in open("requirements.txt").readlines()],
    include_package_data=True,
    package_data={"skillmortex": ["data/*.csv", "figures/*.png"]},
    author="Dimitrios Christos Kavargyris",
    author_email="dkavargy@csd.auth.gr",
    description="A framework for modeling digital skill decay, survival, and obsolescence using epidemiological and statistical methods",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/skillmortex",  # replace with actual URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.7",
)
