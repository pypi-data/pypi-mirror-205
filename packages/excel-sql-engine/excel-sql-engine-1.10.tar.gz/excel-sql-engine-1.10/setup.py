import setuptools
from PyxlSql.pyxlVersion import PyxlVersion

# CAVEAT : This file is edited by tests/patch_files.py to set up the version name from the latest tag
with open("README.md", "r") as fh:
    long_description = fh.read()

# see https://setuptools.pypa.io/en/latest/references/keywords.html
setuptools.setup(
    name="excel-sql-engine",
    version=PyxlVersion.spec,
    author="Fabien BATTINI",                    # noqa
    author_email="fabien.battini@gmail.com",
    description="A tiny SQL engine for Excel files, based on Openpyxl",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/fabien.battini/pyxlsql",
    license_files=["LICENCE"],
    keywords='excel sql',
    packages=setuptools.find_packages(),
    classifiers=[
        # see https://pypi.org/classifiers/
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",  # noqa
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business :: Office Suites",
    ],
    entry_points={
        'console_scripts': [
            'pyxl_sql = PyxlSql.pyxlSql:run_pyxl_sql', # noqa
        ]
    },
    python_requires='>=3.6',
)