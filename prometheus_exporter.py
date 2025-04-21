import serial
from prometheus_client.core import REGISTRY
from prometheus_client.registry import Collector
import prometheus_client.registry
import decoder
import time
import recorder
import os
from prometheus_metrics import output_fields

all_data = dict()


def get_attribute(meter, cluster, attribute):
    '''Gets a value from the data structure'''
    if meter in all_data:
        if cluster in all_data[meter]:
            if attribute in all_data[meter][cluster]:
                return all_data[meter][cluster][attribute]
    return None


def process_data_block(data):
    data = decoder.decode_data_block(data)

    if data[0] == 0x00:
        decoded = decoder.value_decoder(data)

        if decoded["meter"] not in all_data:
            all_data[decoded["meter"]] = dict()
        if decoded["cluster"] not in all_data[decoded["meter"]]:
            all_data[decoded["meter"]][decoded["cluster"]] = dict()

        for attribute in decoded["parameters"]:
            all_data[decoded["meter"]][decoded["cluster"]][attribute] = decoded["parameters"][attribute]
            all_data[decoded["meter"]][decoded["cluster"]][attribute]["updated"] = time.time()


class MeterCollector(Collector):
    """
    Collects data from Netgear switches
    """

    def collect(self):
        print("collecting")
        for item in output_fields:
            attribute = get_attribute(item["meter"], item["cluster"], item["attribute"])
            if attribute is not None:
                value = attribute["value"]
                if "attribute_modifier" in item:
                    value = item["attribute_modifier"](item, all_data, value)

                yield item["metric_type"](
                        item["metric_name"],
                        item["metric_description"],
                        value=value
                        )


serialPort = serial.Serial(
    port="/dev/ttyUSB0", baudrate=115200
)

data_buffer = bytearray()

reading_block = False

REGISTRY.register(MeterCollector())
prometheus_client.start_http_server(8000)

record_data = os.getenv("RECORD_DATA", 'False').lower() in ('true', '1', 't')

if record_data:
    recorder.setup_output("/packet_logs")

while 1:
    # Read data out of the buffer until a carraige return / new line is found
    data = serialPort.read()

    for byte in data:
        if (reading_block):
            data_buffer.append(byte)
            if byte == 0xF2:
                if record_data:
                    recorder.save_data_block(data_buffer)
                process_data_block(data_buffer)
                data_buffer.clear()
                reading_block = False
        else:
            if byte == 0xF1:
                data_buffer.append(byte)
                reading_block = True
