#!/usr/bin/env python3
"""Personal data"""

import re


def filter_datum(fields, redaction, message, separator):
    """filter_datum function"""
    pattern = r"(?:" + separator.join(fields) + r")=([^;]+);"
    return re.sub(pattern, r"\1=" + redaction + ";", message)
