from datetime import datetime
import time

from iqrfpy.peripherals.ledr.requests.pulse import PulseRequest
from iqrfpy.iresponse import IResponse
from iqrfpy.transports.mqtt_transport import MqttTransportParams, MqttTransport


def handler(response: IResponse) -> None:
    print(f'received response at {datetime.now()}')
    print(response.get_mtype())
    print(response.get_msgid())


params = MqttTransportParams(
        host='localhost',
        port=1883,
        client_id='python-lib-test',
        request_topic='Iqrf/DpaRequest',
        response_topic='Iqrf/DpaResponse',
        qos=1,
        keepalive=25
    )
transport = MqttTransport(params=params, callback=handler, auto_init=True)

while True:
    time.sleep(5)
    print(f'sending request at {datetime.now()}')
    transport.send(PulseRequest(nadr=0))
