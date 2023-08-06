# Copyright Formic Technologies 2023
import uuid
import logging
import hashlib
from datetime import datetime

logger = logging.getLogger(__name__)

from asyncua.ua.uatypes import VariantType

def positive_sha256_hash(obj):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(str(obj).encode('utf-8'))
    return int(sha256_hash.hexdigest()[:8], 16)  # Make sure there are not too many bytes for UInt32

type_map = {
    VariantType.SByte: int,
    VariantType.Byte: int,
    VariantType.ByteString: bytes,
    VariantType.Int32: int,
    VariantType.Int64: int,
    VariantType.UInt16: int,
    VariantType.UInt32: int,
    VariantType.UInt64: int,
    VariantType.Boolean: bool,
    VariantType.Double: float,
    VariantType.Float: float,
    VariantType.String: str,
    VariantType.DateTime: datetime,
    VariantType.Guid: uuid.UUID,
}


def convert_type(value, var_type):
    if (type_map[var_type] == int or type_map[var_type] == float) and isinstance(value, str):
        value = positive_sha256_hash(value)

    return type_map[var_type](value)

