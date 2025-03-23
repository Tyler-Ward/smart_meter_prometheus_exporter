import serial
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily, REGISTRY
from prometheus_client.registry import Collector
import prometheus_client.registry


smart_meter_electric_metering_instantaneous_demand_watts = None
smart_meter_electric_metering_current_summation_delivered_watthours = None


def decode_data_block(data: bytes) -> bytes:
    '''Removes control signals and substitutions from a recieved data block'''
    output_data = bytearray()
    marker = 0
    while marker < len(data):
        if data[marker] == 0xF0:
            print("seen F0 marker")
        if data[marker] == 0xF1:
            # trim start of message flag
            if marker != 0:
                print("Start marker not at beginning invalid packet")
            marker += 1
            continue
        if data[marker] == 0xF2:
            # trim end of message flag
            if marker != (len(data)-1):
                print("Start marker not at beginning invalid packet")
            marker += 1
            continue
        if data[marker] == 0xF3:
            # repalce substitution with correct value
            output_data.append(0xF0 + data[marker+1])
            marker += 2
            continue

        output_data.append(data[marker])
        marker += 1
    return bytes(output_data)


def process_data_block(data):
    global smart_meter_electric_metering_instantaneous_demand_watts
    global smart_meter_electric_metering_current_summation_delivered_watthours


    data = decode_data_block(data)

    if data[0:4] == b'\x00\x99\x57\x01':
        # elec meter
        if data[4:6] == b'\x02\x07':
            # metering
            if data[11:15] == b'\x00\x04\x00\x2a':
                # current power
                smart_meter_electric_metering_instantaneous_demand_watts = int.from_bytes(data[15:17], "little")
                print("current_usage = {} w".format(smart_meter_electric_metering_instantaneous_demand_watts))
            if data[6:10] == b'\x00\x00\x00\x25':
                # meter reading
                smart_meter_electric_metering_current_summation_delivered_watthours = int.from_bytes(data[10:16], "little")
                print("meter reading = {} kwh".format(smart_meter_electric_metering_current_summation_delivered_watthours/1000))



#prometheus_client.disable_created_metrics()


class MeterCollector(Collector):
    """
    Collects data from Netgear switches
    """

    def collect(self):
        print("collecting")
        if smart_meter_electric_metering_instantaneous_demand_watts is not None:
            yield GaugeMetricFamily(
                "smart_meter_electric_metering_instantaneous_demand_watts",
                "instentaneous power reported by the smart meter om watts",
                value = smart_meter_electric_metering_instantaneous_demand_watts )
        if smart_meter_electric_metering_current_summation_delivered_watthours is not None:
            yield CounterMetricFamily(
                "smart_meter_electric_metering_current_summation_delivered_watthours", 
                "current meter reading in watt hours",
                value = smart_meter_electric_metering_current_summation_delivered_watthours)




serialPort = serial.Serial(
    port="/dev/ttyUSB0", baudrate=115200
)

data_buffer = bytearray()

reading_block = False

REGISTRY.register(MeterCollector())
prometheus_client.start_http_server(8000)

while 1:
    # Read data out of the buffer until a carraige return / new line is found
    data = serialPort.read()

    for byte in data:
        if (reading_block):
            data_buffer.append(byte)
            if byte == 0xF2:
                #print(data_buffer.hex(" "))
                process_data_block(data_buffer)
                data_buffer.clear()
                reading_block = False
        else:
            if byte == 0xF1:
                data_buffer.append(byte)
                reading_block = True

