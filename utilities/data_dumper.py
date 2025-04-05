import serial

# Simple script to dump serial data from the display to a file as a formatted hex string


def dump_data(port, file_name):

    serialPort = serial.Serial(
        port=port, baudrate=115200
    )

    with open(file_name, "a") as file:

        while 1:
            # Read data out of the buffer until a carraige return / new line is found
            data = serialPort.read()

            file.write(data.hex(","))
            file.write(",")

