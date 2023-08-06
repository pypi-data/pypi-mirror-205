# Azure Keyvault Stuff

A package that provides functionality for interacting with an Azure Keyvault

## Installation

Run the following to install the package:

``python -m pip install azure-keyring-stuff``

## Usage

```python
from azure_keyring_stuff import getClient, getSecret, setSecret, deleteSecret
from azure.identity import DefaultAzureCredential

client = getClient(vault_name="VAULT_NAME", credential=DefaultAzureCredential())

secret = getSecret(client=client, secret_name="SECRET_NAME")

new_secret = setSecret(client=client, secret_name="SECRET_NAME", secret_value="SECRET_VALUE")

deleted_secret = deleteSecret(client=client, secret_name="SECRET_NAME")

```