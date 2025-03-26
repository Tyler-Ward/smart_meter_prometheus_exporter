import serial
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily, REGISTRY
from prometheus_client.registry import Collector
import prometheus_client.registry
import decoder


smart_meter_electric_metering_instantaneous_demand_watts = None
smart_meter_electric_metering_current_summation_delivered_watthours = None
smart_meter_gas_metering_current_summation_delivered_m3 = None


def process_data_block(data):
    global smart_meter_electric_metering_instantaneous_demand_watts
    global smart_meter_electric_metering_current_summation_delivered_watthours
    global smart_meter_gas_metering_current_summation_delivered_m3

    data = decoder.decode_data_block(data)

    if data[0] == 0x00:
        decoded = decoder.value_decoder(data)

        if decoded["meter"] == b'\x00\x99\x57\x01':
            # elec meter
            if decoded["cluster"] == decoder.Cluster.metering.value:
                # metering
                if decoder.MeteringParmeter.instantaneous_demand.value in decoded["parameters"]:
                    # current power
                    smart_meter_electric_metering_instantaneous_demand_watts = decoded["parameters"][decoder.MeteringParmeter.instantaneous_demand.value]["value"]
                    print("current_usage = {} w".format(smart_meter_electric_metering_instantaneous_demand_watts))
                if decoder.MeteringParmeter.current_summation_delivered.value in decoded["parameters"]:
                    # meter reading
                    smart_meter_electric_metering_current_summation_delivered_watthours = decoded["parameters"][decoder.MeteringParmeter.current_summation_delivered.value]["value"]
                    print("meter reading = {} kwh".format(smart_meter_electric_metering_current_summation_delivered_watthours/1000))

        if decoded["meter"] == b'\x00\x00\x00\x02':
            # gas meter
            if decoded["cluster"] == decoder.Cluster.metering.value:
                # metering
                if decoder.MeteringParmeter.current_summation_delivered.value in decoded["parameters"]:
                    # meter reading
                    smart_meter_gas_metering_current_summation_delivered_m3 = decoded["parameters"][decoder.MeteringParmeter.current_summation_delivered.value]["value"]/1000
                    print("gas meter reading = {} m3".format(smart_meter_gas_metering_current_summation_delivered_m3))




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
        if smart_meter_gas_metering_current_summation_delivered_m3 is not None:
            yield CounterMetricFamily(
                "smart_meter_gas_metering_current_summation_delivered_m3",
                "current meter reading in cubic meters",
                value = smart_meter_gas_metering_current_summation_delivered_m3)



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

