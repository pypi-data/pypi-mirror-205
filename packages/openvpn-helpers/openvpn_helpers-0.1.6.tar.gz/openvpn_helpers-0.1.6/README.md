# OpenVPN Helpers

## Installation

```
pip install openvpn-helpers
```

## OpenVPN Inliner

Embeds CA Certificate, Client Key & Certificate and TLS Auth Key into the OpenVPN config file.

### Usage

```
openvpn-inliner source.conf dest.conf --ca ca.crt --ta ta.key --cert client.crt --key client.key 
```