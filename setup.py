from setuptools import setup

# version.py defines the VERSION and VERSION_SHORT variables.
# We use exec here so we don't import cached_path whilst setting up.
VERSION = {}  # type: ignore
with open("geoclustering/version.py", "r") as version_file:
    exec(version_file.read(), VERSION)

setup(
    name="geoclustering",
    version=VERSION["VERSION"],
    description="📍 command-line tool for clustering geolocations.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    author="Bellingcat",
    author_email="tech@bellingcat.com",
    license="MIT",
    packages=["geoclustering"],
    package_data={"geoclustering": ["kepler_config.json"]},
    keywords=["cluster", "gis", "pattern-analysis"],
    entry_points={"console_scripts": ["geoclustering = geoclustering.__main__:main"]},
    install_requires=[
        "click",
        "geojson",
        "numpy",
        "pandas",
        "scikit-learn",
    ],
    extras_require={
        "dev": ["black", "wheel", "pre-commit", "pytest"],
        "full": ["keplergl"],
    },
    include_package_data=True,
    zip_safe=False,
)
