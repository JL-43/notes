---
tags:
  - Software Engineering
  - Informational
  - Web3
  - Blockchain
  - Protocols
---

# URIs VS Web3 Addresses

## Web3 Addresses as Raw Identifiers

A Web3 address like `0x1234567890abcdef1234567890abcdef12345678` is a raw identifier (typically a hexadecimal string) that represents an account, smart contract, or other blockchain entities. By itself, it does not conform to the structure of a URI, which follows a specific syntax (e.g., `scheme://host/path`). (see: [Scheme Vs. Protocol.md](./scheme_vs_protocol.md))

## Embedding Web3 Addresses in URIs

Web3 systems often embed addresses in URIs to define resources or interactions. For example:

- **Ethereum URI**: `ethereum:0x1234567890abcdef1234567890abcdef12345678`
  - This is a valid URI where `ethereum` is the scheme and the address is the path.
  - These URIs might include additional details for actions, like sending tokens or interacting with contracts: `ethereum:0x1234567890abcdef1234567890abcdef12345678?value=1000&gas=21000`
- **IPFS URI**: `ipfs://<CID>` (uses a unique content identifier rather than an address).
  - These follow the URI specification, making the address part of the URI.

## Why Web3 Addresses Aren’t URIs

According to the URI standard (RFC 3986), a URI must have:

- A scheme (e.g., http, ftp, ethereum, ipfs).
- Hierarchical components (authority, path, etc.).

A raw blockchain address lacks these structural elements—it is just an identifier, not a locator or resource descriptor.

## Web3 Addresses as Resource Identifiers

While a raw Web3 address (e.g., `0x1234567890abcdef1234567890abcdef12345678`) isn't a URI on its own, it becomes meaningful when it's integrated into protocols or systems that allow it to represent specific resources. Here are a few common examples:

### Navigating Smart Contracts and Accounts

- **Ethereum URIs**:
  - The Ethereum ecosystem uses a URI format to reference smart contracts, accounts, and transactions.
  - Example: `ethereum:0x1234567890abcdef1234567890abcdef12345678`
    - This URI identifies the account `0x1234567890abcdef1234567890abcdef12345678`.
  - URIs can include parameters for additional functionality, such as sending tokens or executing a transaction:
    - `ethereum:0x1234567890abcdef1234567890abcdef12345678?value=1000`

### Navigating Files via Decentralized Storage

- **IPFS (InterPlanetary File System)**:
    - Web3 addresses can indirectly refer to files stored on decentralized networks.
    - Example: `ipfs://<CID>` (Content Identifier)
        - While this is a URI with its own scheme (`ipfs`), the CID (content hash) acts similarly to a Web3 address in its uniqueness and immutability.
    - By embedding IPFS links, Web3 apps make resources accessible in a decentralized manner.
- **Arweave**:
    - Files on Arweave are referenced by transaction IDs, which function similarly to Web3 addresses.
        - Example: `arweave.net/<transaction_id>`

### On-Chain Domains and Websites

- **ENS (Ethereum Name Service)**:
    - ENS maps human-readable names (like `example.eth`) to Web3 addresses.
    - These can resolve to:
        - Wallet addresses
        - IPFS-hosted websites
        - Other on-chain resources
    - Example: `example.eth` could map to `ipfs://<CID>` or directly resolve to a Web3 address.
- **Decentralized Webpages**:
    - By combining ENS or other naming systems with protocols like IPFS, Web3 addresses can identify websites:
        - Example: `https://gateway.ipfs.io/ipfs/<CID>` or `https://example.eth`.

