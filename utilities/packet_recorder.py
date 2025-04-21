import serial
import recorder

# Record timestamped packets


def record_packets(port):

    recorder.setup_output()

    serialPort = serial.Serial(
        port=port, baudrate=115200
    )

    data_buffer = bytearray()
    reading_block = False

    while 1:
        data = serialPort.read()

        for byte in data:
            if (reading_block):
                data_buffer.append(byte)
                if byte == 0xF2:
                    recorder.save_data_block(data_buffer)
                    data_buffer.clear()
                    reading_block = False
            else:
                if byte == 0xF1:
                    data_buffer.append(byte)
                    reading_block = True
