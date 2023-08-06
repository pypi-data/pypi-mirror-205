from dataclasses import dataclass
import json
import random
import string
import threading

from typing import Callable, Optional, overload
from typeguard import typechecked
from paho.mqtt.client import Client
from iqrfpy.enums.message_types import MessageType
from iqrfpy.exceptions import TransportNotConnectedError, MessageNotReceivedError
from iqrfpy.confirmation import Confirmation
from iqrfpy.response_factory import ResponseFactory
from iqrfpy.transports.itransport import ITransport
from iqrfpy.messages import *

__all__ = [
    'MqttTransportParams',
    'MqttTransport',
]


@dataclass
@typechecked
class MqttTransportParams:
    host: str = 'localhost'
    port: int = 1883
    client_id: str = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(16))
    user: str = None
    password: str = None
    request_topic: str = None
    response_topic: str = None
    qos: int = 1
    keepalive: int = 60

    def __post_init__(self):
        if not (1024 <= self.port <= 65535):
            raise MqttParamsError('Port value should be between 1024 and 65535.')
        if (self.user is not None and self.password is None) or (self.user is None and self.password is not None):
            raise MqttParamsError('Both user and password parameters need to be specified, or neither of them.')
        if not (0 <= self.qos <= 2):
            raise MqttParamsError('QoS value should be between 0 and 2.')


class MqttTransport(ITransport):

    __slots__ = '_client', '_params', '_callback', '_timeout', '_cv'

    def __init__(self, params: MqttTransportParams, callback: Optional[Callable] = None,
                 auto_init: bool = False, timeout: Optional[int] = 5):
        self._client: Optional[Client] = None
        self._params: MqttTransportParams = params
        self._callback: Optional[Callable] = callback
        self._timeout: int = timeout
        self._msg_id: Optional[str] = None
        self._m_type: Optional[MessageType] = None
        self._cv: threading.Condition = threading.Condition()
        self._response: Optional[IResponse] = None
        if auto_init:
            self.initialize()

    def initialize(self) -> None:
        self._client = Client(self._params.client_id)
        self._client.on_connect = self._connect_callback
        self._client.on_message = self._message_callback
        if self._params.user is not None and self._params.password is not None:
            self._client.username_pw_set(self._params.user, self._params.password)
        self._client.connect(self._params.host, self._params.port)
        self._client.loop_start()

    def _connect_callback(self, client, userdata, flags, rc):
        # pylint: disable=W0613
        if rc == 0:
            self._client.subscribe(self._params.response_topic, self._params.qos)

    def _message_callback(self, client, userdata, message):
        # pylint: disable=W0613
        payload = json.loads(message.payload.decode('utf-8'))
        try:
            response = ResponseFactory.get_response_from_json(payload)
        except MessageNotReceivedError:
            with self._cv:
                self._cv.notify()
            return
        if self._callback is not None:
            self._callback(response)
        if response.get_msgid() == self._msg_id and response.get_mtype() == self._m_type:
            self._response = response
            with self._cv:
                self._cv.notify()

    def send(self, request: IRequest) -> None:
        self._response = None
        self._msg_id = None
        self._m_type = None
        if not self._client.is_connected():
            raise TransportNotConnectedError(f'MQTT client {self._params.client_id} not connected to broker.')
        self._client.publish(
            topic=self._params.request_topic,
            payload=json.dumps(request.to_json()),
            qos=self._params.qos
        )
        self._msg_id = request.get_msg_id()
        self._m_type = request.get_message_type()

    def receive(self, timeout: Optional[int] = None) -> IResponse:
        timeout_to_use = timeout if timeout is not None else self._timeout
        with self._cv:
            self._cv.wait(timeout=timeout_to_use)
        if self._response is None:
            raise MessageNotReceivedError(f'Response message to request with ID {self._msg_id} not received within the'
                                          f' specified time of {timeout_to_use} seconds.')
        return self._response

    def confirmation(self) -> Confirmation:
        raise NotImplementedError('Method not implemented.')

    def set_receive_callback(self, callback: Callable[[IResponse], None]) -> None:
        self._callback = callback

    @overload
    def send_and_receive(self, request: CoordinatorAddrInfoReq,
                         timeout: Optional[int] = None) -> CoordinatorAddrInfoRsp:
        ...

    @overload
    def send_and_receive(self, request: CoordinatorAuthorizeBondReq,
                         timeout: Optional[int] = None) -> CoordinatorAuthorizeBondRsp:
        ...

    @overload
    def send_and_receive(self, request: CoordinatorBackupReq,
                         timeout: Optional[int] = None) -> CoordinatorBackupRsp:
        ...

    @overload
    def send_and_receive(self, request: CoordinatorBondNodeReq,
                         timeout: Optional[int] = None) -> CoordinatorBondNodeRsp:
        ...

    @overload
    def send_and_receive(self, request: CoordinatorBondedDevicesReq,
                         timeout: Optional[int] = None) -> CoordinatorBondedDevicesRsp:
        ...

    @overload
    def send_and_receive(self, request: CoordinatorClearAllBondsReq,
                         timeout: Optional[int] = None) -> CoordinatorClearAllBondsRsp:
        ...

    @overload
    def send_and_receive(self, request: CoordinatorDiscoveredDevicesReq,
                         timeout: Optional[int] = None) -> CoordinatorDiscoveredDevicesRsp:
        ...

    @overload
    def send_and_receive(self, request: CoordinatorDiscoveryReq,
                         timeout: Optional[int] = None) -> CoordinatorDiscoveryRsp:
        ...

    @overload
    def send_and_receive(self, request: CoordinatorRemoveBondReq,
                         timeout: Optional[int] = None) -> CoordinatorRemoveBondRsp:
        ...

    @overload
    def send_and_receive(self, request: CoordinatorRestoreReq,
                         timeout: Optional[int] = None) -> CoordinatorRestoreRsp:
        ...

    @overload
    def send_and_receive(self, request: CoordinatorSetDpaParamsReq,
                         timeout: Optional[int] = None) -> CoordinatorSetDpaParamsRsp:
        ...

    @overload
    def send_and_receive(self, request: CoordinatorSetHopsReq,
                         timeout: Optional[int] = None) -> CoordinatorSetHopsRsp:
        ...

    @overload
    def send_and_receive(self, request: CoordinatorSetMidReq,
                         timeout: Optional[int] = None) -> CoordinatorSetMidRsp:
        ...

    @overload
    def send_and_receive(self, request: CoordinatorSmartConnectReq,
                         timeout: Optional[int] = None) -> CoordinatorSmartConnectRsp:
        ...

    @overload
    def send_and_receive(self, request: OsReadReq, timeout: Optional[int] = None) -> OsReadRsp:
        ...

    @overload
    def send_and_receive(self, request: EepromReadReq, timeout: Optional[int] = None) -> EepromReadRsp:
        ...

    @overload
    def send_and_receive(self, request: EepromWriteReq, timeout: Optional[int] = None) -> EepromWriteRsp:
        ...

    @overload
    def send_and_receive(self, request: LedgSetOnRsp, timeout: Optional[int] = None) -> LedgSetOnRsp:
        ...

    @overload
    def send_and_receive(self, request: LedgSetOffReq, timeout: Optional[int] = None) -> LedrSetOffRsp:
        ...

    @overload
    def send_and_receive(self, request: LedgPulseReq, timeout: Optional[int] = None) -> LedgPulseRsp:
        ...

    @overload
    def send_and_receive(self, request: LedgFlashingReq, timeout: Optional[int] = None) -> LedgFlashingRsp:
        ...

    @overload
    def send_and_receive(self, request: LedrSetOnReq, timeout: Optional[int] = None) -> LedrSetOnRsp:
        ...

    @overload
    def send_and_receive(self, request: LedrSetOffReq, timeout: Optional[int] = None) -> LedrSetOffRsp:
        ...

    @overload
    def send_and_receive(self, request: LedrPulseReq, timeout: Optional[int] = None) -> LedrPulseRsp:
        ...

    @overload
    def send_and_receive(self, request: LedrFlashingReq, timeout: Optional[int] = None) -> LedrFlashingRsp:
        ...

    def send_and_receive(self, request: IRequest, timeout: Optional[int] = None) -> IResponse:
        self.send(request)
        return self.receive(timeout)


class MqttParamsError(Exception):
    pass
