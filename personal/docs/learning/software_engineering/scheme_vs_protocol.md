---
tags:
  - Software Engineering
  - Informational
  - Protocols
---

# Understanding the Difference Between Scheme and Protocol

## Overview

The terms `scheme`, in relation to URIs, (See: [what is a URI?](https://blog.hubspot.com/website/uri-vs-url)) and `protocol` are often used interchangeably, but they serve distinct purposes in the context of networking and resource identification. This document explores the differences, their relationship, and why they often appear closely tied.

---

## 1. **What is a Scheme?**
A `scheme` is a formal identifier that specifies the type of resource being accessed and the mechanism for locating it. It is part of the structure of a URI (Uniform Resource Identifier), as defined in [RFC 3986](https://www.rfc-editor.org/rfc/rfc3986).

- **Purpose**: Indicates how to interpret the rest of the URI.
- **Examples**:
  - `http` (Hypertext Transfer Protocol)
  - `https` (Secure Hypertext Transfer Protocol)
  - `ftp` (File Transfer Protocol)
  - `mailto` (Email addresses)
  - `ethereum` (Web3 Ethereum address)
- **Key Characteristics**:
  - Schemes do **not enforce implementation details**—they only indicate what to do or expect.
  - Syntax: A scheme is followed by a colon (`:`) and, optionally, additional components (`//host/path`).
    - Example: In `http://example.com`, the scheme is `http`.

---

## 2. **What is a Protocol?**
A `protocol` is the set of rules and standards used to enable communication between systems. Protocols define how data is exchanged over a network.

- **Purpose**: Dictates the "how" of communication—rules, handshakes, formats, and behaviors.
- **Examples**:
  - `HTTP` (Hypertext Transfer Protocol)
  - `FTP` (File Transfer Protocol)
  - `SMTP` (Simple Mail Transfer Protocol)
  - `Ethereum JSON-RPC` (Blockchain communication)
- **Key Characteristics**:
  - Protocols specify technical implementation details for data transfer, formatting, and responses.
  - They operate at the network, transport, or application layers.

---

## 3. **Why Are They Closely Tied?**
`Schemes` and `protocols` are closely tied because schemes often map directly to protocols in practice. This alignment creates the impression that they are the same thing.

| **Scheme**     | **Protocol**                            | **Relationship**                                                   |
|-----------------|----------------------------------------|---------------------------------------------------------------------|
| `http`         | Hypertext Transfer Protocol (HTTP)     | The `http` scheme indicates that the resource is accessed via HTTP. |
| `ftp`          | File Transfer Protocol (FTP)           | The `ftp` scheme implies the use of the FTP protocol.               |
| `mailto`       | SMTP (email sending protocol)          | The `mailto` scheme maps to email-related protocols like SMTP.      |
| `ethereum`     | Ethereum JSON-RPC, WalletConnect       | The `ethereum` scheme often involves blockchain-related protocols.  |

---

## 4. **Key Differences**
Here’s a table summarizing the differences between schemes and protocols:

| **Aspect**         | **Scheme**                                | **Protocol**                          |
|---------------------|-------------------------------------------|----------------------------------------|
| **Definition**      | URI component identifying the type of resource | Set of rules for communication         |
| **Scope**           | Descriptive (what to expect)              | Prescriptive (how to operate)          |
| **Examples**        | `http`, `mailto`, `ethereum`              | HTTP, SMTP, Ethereum JSON-RPC          |
| **Implementation**  | Does not define behavior                  | Defines communication rules explicitly |

---

## 5. **Why Does It Feel Like Schemes = Protocols?**
This confusion arises because:

1. **Historical Design**: Early internet services like HTTP and FTP were tightly coupled with their schemes.
   
2. **Common Usage**: When developers say "use the `http` scheme," they’re implicitly referring to the HTTP protocol.

However, schemes are more **abstract** than protocols:
- The `mailto` scheme doesn’t enforce a specific protocol—it could involve SMTP, IMAP, or POP3, depending on the system.
- The `ethereum` scheme doesn’t prescribe the specific blockchain interaction protocol—it could be JSON-RPC, WebSocket, or others.

---

## 6. **Conclusion**
While schemes and protocols are closely tied, they serve different purposes:
- A **scheme** identifies the type of resource and hints at how to interact with it.
- A **protocol** implements the actual rules for that interaction.

Think of schemes as **"labels that point to a communication mechanism"** and protocols as **"the actual communication rules."**
