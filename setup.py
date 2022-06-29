from setuptools import setup

setup(
    name="geocluster",
    version="0.1",
    description="",
    author="Bellingcat",
    packages=["geocluster"],
    entry_points={"console_scripts": ["geocluster = geocluster.cli:main"]},
    install_requires=[
        "click",
        "geojson",
        "keplergl",
        "numpy",
        "pandas",
        "scikit-learn",
    ],
    extras_require={"dev": ["black", "wheel"]},
    include_package_data=True,
    zip_safe=False,
)
