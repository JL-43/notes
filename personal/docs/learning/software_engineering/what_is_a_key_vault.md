---
tags:
  - Software Engineering
  - Informational
  - Security
---

# What is a Key Vault?

## Introduction to Key Vaults

Key Vaults are a way to manage "secrets", "keys", and "certificates".

  - Key Vaults operate on the Zero Trust security strategy.
    - 3 Principles:
        - "Verify Explicitly"
        - Use Least Privilege Access
        - Assume Breach

We "centralize" application secrets, which allows us distribution control.

  - In azure, we have the capability to monitor the access and usage of the keys

The keyvault also allows the user to not have to store any application secrets within the application itself.

Applications will, instead, access the secret using URIs (See: [what is a URI?](https://blog.hubspot.com/website/uri-vs-url)) in order to retrieve specific versions of a secret. This removes the need to write custom code to protect the information.

## How to create a Key Vault (Azure Specific):

1. Navigate to "Key Vault" in Azure Portal (Assuming logged in)
2. In the sidebar:
   1. `Objects` > `Secrets` > `Generate/Import`
3. Create a secret, with the following values:
   1. `Upload options`: Manual
   2. `Name`: Type a name. Must be unique within the key vault. See: [Key Vault objects, identifiers, and versioning](https://learn.microsoft.com/en-us/azure/key-vault/general/about-keys-secrets-certificates#objects-identifiers-and-versioning)
   3. `Value`: Type the secret value. Key Vault API returns and accepts values as `strings`
   4. Leave others at default
   5. `Create`

From here, take note of two properties:
1. Vault Name
2. Vault URI

By default, only the creating user has access to perform operations on the key vault.

