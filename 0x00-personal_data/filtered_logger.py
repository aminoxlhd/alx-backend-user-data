#!/usr/bin/env python3
"""Personal data"""

import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """filter_datum function"""
    for field in fields:
        regex = f"{field}=[^{separator}]*"
        message = re.sub(regex, f"{field}={redaction}", message)
    return message
