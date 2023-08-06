from setuptools import setup

VERSION = '0.0.1'
DESCRIPTION = 'Azure Key Vault Helper Package'
LONG_DESCRIPTION = 'A package that provides helper functions for interacting with Azure Key Vault.'

with open("README.md", "r") as fh:
    long_description = fh.read()

# Setting up
setup(
    name="azure-keyvault-stuff",
    url="https://github.com/george-oconnor/azure-keyvault-stuff",
    version=VERSION,
    author="george.oconnor (George O' Connor)",
    author_email="<george@georgestools.com>",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=["azure_keyvault_stuff"],
    package_dir={'': 'src'},
    install_requires=[],
    keywords=['python', 'azure', 'keyvault', 'helper', 'secret', 'secrets', 'client', 'get', 'set', 'delete', 'vault', 'value', 'values', 'credential', 'credentials', 'azure.identity.DefaultAzureCredential()'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ]
)