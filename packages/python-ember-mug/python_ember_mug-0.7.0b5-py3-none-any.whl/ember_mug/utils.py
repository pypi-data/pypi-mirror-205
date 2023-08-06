"""Helpful utils for processing mug data."""
from __future__ import annotations

import base64
import contextlib
import logging
import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bleak import BleakClient, BleakError

logger = logging.getLogger(__name__)


def decode_byte_string(data: bytes | bytearray) -> str:
    """Convert bytes to text as Ember expects."""
    if not data:
        return ''
    with contextlib.suppress(ValueError):
        b64_as_str = base64.encodebytes(data).decode("utf-8")
        return re.sub("[\r\n]", "", b64_as_str)
    logger.warning('Failed to decode bytes "%s". Forcing to string.', data)
    return str(data)


def encode_byte_string(data: str) -> bytes:
    """Encode string from Ember Mug."""
    return re.sub(b"[\r\n]", b"", base64.encodebytes(data.encode("utf8")))


def bytes_to_little_int(data: bytearray | bytes) -> int:
    """Convert bytes to little int."""
    return int.from_bytes(data, byteorder="little", signed=False)


def bytes_to_big_int(data: bytearray | bytes) -> int:
    """Convert bytes to big int."""
    return int.from_bytes(data, byteorder="big")


def temp_from_bytes(temp_bytes: bytearray, metric: bool = True) -> float:
    """Get temperature from bytearray and convert to Fahrenheit if needed."""
    temp = float(bytes_to_little_int(temp_bytes)) * 0.01
    if metric is False:
        # Convert to fahrenheit
        temp = (temp * 9 / 5) + 32
    return round(temp, 2)


async def log_services(client: BleakClient) -> None:
    """Log all services and all values for debugging/development."""
    logger.info("Logging all services that were discovered")
    for service in client.services:
        logger.info("[Service] %s: %s", service.uuid, service.description)
        for characteristic in service.characteristics:
            value: bytearray | BleakError | None = None
            if "read" in characteristic.properties:
                try:
                    value = await client.read_gatt_char(characteristic.uuid)
                except BleakError as e:
                    value = e
            logger.info(
                "\t[Characteristic] %s: %s | Name: %s | Value: '%s'",
                characteristic.uuid,
                ",".join(characteristic.properties),
                characteristic.description,
                value,
            )
            for descriptor in characteristic.descriptors:
                value = await client.read_gatt_descriptor(descriptor.handle)
                logger.info(
                    "\t\t[Descriptor] %s: Handle: %s | Value: '%s'",
                    descriptor.uuid,
                    descriptor.handle,
                    value,
                )
