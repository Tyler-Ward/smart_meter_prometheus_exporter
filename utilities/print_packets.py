def print_packets(file_name):
    with open(file_name, "r") as data_file:
        data_string = data_file.read()
        data_string = data_string.replace(",", " ")

        data = bytes.fromhex(data_string)

    marker = 0

    while marker < len(data):

        current_byte = data[marker]

        if current_byte == 0xF1:
            # This is a data block which continues to the next F2 command
            start = marker
            marker += 1
            while marker < len(data):
                if data[marker] == 0xF2:
                    break
                marker += 1
            marker += 1
            block = data[start:marker]
            print(block.hex(" "))
            continue

        # debug string ends with a LF 0x0A
        # Scan to the next data block
        start = marker
        marker += 1
        while marker < len(data):
            if data[marker] == 0x0A:
                marker += 1
                break
            if data[marker] == 0xF1:
                # report if a data block starts without a LF beforehand
                print("data block starts without LF at end of debug")
                break
            marker += 1
        block = data[start:marker]
        # print(block)
