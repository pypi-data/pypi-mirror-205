from __future__ import annotations
from typeguard import typechecked
from uuid import uuid4
from typing import List, Union
from iqrfpy.enums.commands import EEPROMRequestCommands
from iqrfpy.enums.message_types import EEPROMMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.utils.common import Common
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.irequest import IRequest

__all__ = ['WriteRequest']


@typechecked
class WriteRequest(IRequest):
    __slots__ = '_address', '_data'

    def __init__(self, nadr: int, address: int, data: List[int], hwpid: int = dpa_constants.HWPID_MAX,
                 msgid: str = str(uuid4())):
        self._validate(address, data)
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.EEPROM,
            pcmd=EEPROMRequestCommands.WRITE,
            m_type=EEPROMMessages.WRITE,
            hwpid=hwpid,
            msgid=msgid
        )
        self._address = address
        self._data = data

    @staticmethod
    def _validate_address(address: int):
        if not (dpa_constants.BYTE_MIN <= address <= dpa_constants.BYTE_MAX):
            raise RequestParameterInvalidValueError('Address should be between 0 and 255.')

    @staticmethod
    def _validate_data(data: List[int]):
        if len(data) > dpa_constants.REQUEST_PDATA_MAX_LEN:
            raise RequestParameterInvalidValueError('Data should be at most 58 bytes long.')
        if not Common.values_in_byte_range(data):
            raise RequestParameterInvalidValueError('Data values should be between 0 and 255.')

    def _validate(self, address: int, data: List[int]) -> None:
        self._validate_address(address)
        self._validate_data(data)

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        self._pdata = [self._address, self._length]
        return super().to_dpa(mutable=mutable)

    def to_json(self) -> dict:
        self._params = {'address': self._address, 'length': self._length}
        return super().to_json()
