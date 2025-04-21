from enum import Enum


class Cluster(Enum):
    time = 0x000A
    metering = 0x0702
    prepayment = 0x0705


class TimeParameter(Enum):
    time = 0x0000


class MeteringParmeter(Enum):
    current_summation_delivered = 0x0000
    current_summation_received = 0x0001
    supply_status = 0x0014
    status = 0x0200
    ambient_consumption_indicator = 0x0207
    site_id = 0x0307
    customer_id_number = 0x0311
    instantaneous_demand = 0x0400
    current_day_consumption_delivered = 0x0401
    previous_day_consumption_delivered = 0x0403
    current_week_consumption_delivered = 0x0430
    previous_week_consumption_delivered = 0x0432
    current_month_consumption_delivered = 0x0440
    previous_month_consumption_delivered = 0x0442
    bill_to_date_delivered = 0x0A00
    bill_delivered_trailing_digit = 0x0A04
    current_day_alternative_consumption_delivered = 0x0C01
    previous_day_alternative_consumption_delivered = 0x0C03
    current_week_alternative_consumption_delivered = 0x0C30
    previous_week_alternative_consumption_delivered = 0x0C32
    current_month_alternative_consumption_delivered = 0x0C40
    previous_month_alternative_consumption_delivered = 0x0C42


class PrepaymentParameter(Enum):
    payment_control_configuration = 0x0000
    current_day_cost_consumption_delivered = 0x051C
    previous_day_cost_consumption_delivered = 0x051E
    current_week_cost_consumption_delivered = 0x0530
    previous_week_cost_consumption_delivered = 0x0532
    current_month_cost_consumption_delivered = 0x0540
    previous_month_cost_consumption_delivered = 0x0542


class Encodings(Enum):
    bitmap_8 = 0x18
    bitmap_16 = 0x19
    bitmap_32 = 0x1b
    int_24 = 0x2A
    uint_8 = 0x20
    uint_24 = 0x22
    uint_32 = 0x23
    uint_48 = 0x25
    enum_8 = 0x30
    string = 0x41
    utc = 0xE2


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


def value_decoder(data: bytes):

    meter_id = data[1:3]
    cluster = int.from_bytes(data[4:6], "little")
    parameters = dict()

    marker = 6
    while marker < len(data):
        attribute = int.from_bytes(data[marker:marker+2], "little")
        status = data[marker+2]
        if status != 0x00:
            # skip all data after any non ok status responeses (only seen in time outputs)
            break
        encoding = data[marker+3]

        marker += 4
        if encoding == Encodings.bitmap_8.value:
            value = data[marker]
            marker += 1
        elif encoding == Encodings.bitmap_16.value:
            value = data[marker:marker+2]
            marker += 2
        elif encoding == Encodings.bitmap_32.value:
            value = data[marker:marker+4]
            marker += 4
        elif encoding == Encodings.int_24.value:
            value = int.from_bytes(data[marker:marker+3], "little", signed=True)
            marker += 3
        elif encoding == Encodings.uint_8.value:
            value = int.from_bytes(data[marker:marker+1], "little", signed=False)
            marker += 1
        elif encoding == Encodings.uint_24.value:
            value = int.from_bytes(data[marker:marker+3], "little", signed=False)
            marker += 3
        elif encoding == Encodings.uint_32.value:
            value = int.from_bytes(data[marker:marker+4], "little", signed=False)
            marker += 4
        elif encoding == Encodings.uint_48.value:
            value = int.from_bytes(data[marker:marker+6], "little", signed=False)
            marker += 6
        elif encoding == Encodings.enum_8.value:
            value = data[marker]
            marker += 1
        elif encoding == Encodings.string.value:
            length = data[marker]
            value = data[marker+1:marker+1+length].decode('ascii')
            marker += 1+length
        elif encoding == Encodings.utc.value:
            value = int.from_bytes(data[marker:marker+4], "little", signed=False)
            marker += 4
        else:
            print(
                "unrecognised data encoding {:04X} in atibute {:04X} and cluster {:04X}"
                .format(encoding, attribute, cluster))
            print(data.hex(" "))
            return None

        parameters[attribute] = {"type": encoding, "value": value}

    return {
        "meter": meter_id,
        "cluster": cluster,
        "parameters": parameters
    }
