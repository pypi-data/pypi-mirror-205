#!/usr/bin/env python
""" Inline helper for OpenVPN """
import re
import argparse


def load_file(filename):
    " Load the file "
    with open(filename, encoding='utf-8') as file_to_open:
        content = file_to_open.read()
    return content


def write_file(filename, content):
    " Write the file "
    with open(filename, 'w', encoding='utf-8') as file_to_write:
        file_to_write.write(content)


def _check_presence(tag, content):
    " Check if the tag does exist "
    raw_string = _get_match_raw(tag)
    pattern = re.compile(raw_string, re.MULTILINE + re.DOTALL)
    return pattern.fullmatch(content)


def _get_match_raw(tag):
    " Create raw string for the tag "
    raw_string = rf".+?<{tag}>(.+?)</{tag}>.+?"
    return raw_string


def is_ca(content):
    " Predicate for the CA Certificate "
    return _check_presence("ca", content)


def is_cert(content):
    " Predicate for the Client Certificate "
    return _check_presence("cert", content)


def is_key(content):
    " Predicate for the Client Key "
    return _check_presence("key", content)


def is_ta(content):
    " Predicate for the TLS Auth "
    return _check_presence("tls-auth", content)


def _add_tag(tag, value, content):
    " Add the tag to the config "
    to_add = f"<{tag}>\n{value}</{tag}>\n"
    return content+to_add


def add_ca(value, content):
    " Wrapper to add the CA Certificate "
    return _add_tag("ca", value, content)


def add_cert(value, content):
    " Wrapper to add the Client Certificate "
    return _add_tag("cert", value, content)


def add_key(value, content):
    " Wrapper to add the Client Key "
    return _add_tag("key", value, content)


def add_ta(value, content):
    " Wrapper to add the TLS Auth key "
    return _add_tag("tls-auth", value, content)


def main():
    " Main function "
    parser = argparse.ArgumentParser(
            description='OpenVPN inline config helper')
    parser.add_argument('source', help='Source OpenVPN config file')
    parser.add_argument('destination', help='Destination OpenVPN config file')
    parser.add_argument('--ca', help='CA certificate path')
    parser.add_argument('--cert', help='Client certificate path')
    parser.add_argument('--key', help='Client key path')
    parser.add_argument('--ta', help='TLS auth key path')
    args = parser.parse_args()
    content = load_file(args.source)

    if args.ca:
        if not is_ca(content):
            print("adding ca")
            ca_content = load_file(args.ca)
            content = add_ca(ca_content, content)
    if args.cert:
        if not is_cert(content):
            print("adding cert")
            cert_content = load_file(args.cert)
            content = add_cert(cert_content, content)
    if args.key:
        if not is_key(content):
            print("adding key")
            key_content = load_file(args.key)
            content = add_key(key_content, content)
    if args.ta:
        if not is_ta(content):
            print("adding ta")
            ta_content = load_file(args.ta)
            content = add_ta(ta_content, content)
    write_file(args.destination, content)


if __name__ == "__main__":
    main()
