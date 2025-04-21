import decoder
import pprint

all_data = dict()


def process_data_block(data):

    data = decoder.decode_data_block(data)

    if data[0] == 0x00:
        decoded = decoder.value_decoder(data)

        meter = decoded["meter"]
        cluster = decoded["cluster"]

        if meter not in all_data:
            all_data[meter] = dict()
        if cluster not in all_data[meter]:
            all_data[meter][cluster] = dict()

        for attribute in decoded["parameters"]:
            recieved_count = 0
            if attribute in all_data[meter][cluster]:
                recieved_count = all_data[meter][cluster][attribute]["count"]
            all_data[meter][cluster][attribute] = decoded["parameters"][attribute]
            all_data[meter][cluster][attribute]["count"] = recieved_count + 1


def print_variables(file_name):
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
            process_data_block(block)
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

    pprint.pprint(all_data)

    # merge all meters into one to print list of seen variables

    combined_data = dict()

    for meter in all_data:

        print("meter: {}".format(meter))
        for cluster in dict(sorted(all_data[meter].items())):
            print("cluster {:04X} ({})".format(cluster, cluster))

            for attribute in dict(sorted(all_data[meter][cluster].items())):
                type_name = decoder.Encodings(all_data[meter][cluster][attribute]["type"]).name
                print("   {:04X} ({}) - {}".format(attribute, attribute, type_name))

        for cluster in all_data[meter]:
            if cluster in combined_data:
                for attribute in all_data[meter][cluster]:
                    combined_data[cluster][attribute] = all_data[meter][cluster][attribute]
            else:
                combined_data[cluster] = all_data[meter][cluster]

    # print a formatted list of all variables seen

    for cluster in dict(sorted(combined_data.items())):
        print("cluster {:04X} ({})".format(cluster, cluster))

        for attribute in dict(sorted(combined_data[cluster].items())):
            type_name = decoder.Encodings(combined_data[cluster][attribute]["type"]).name
            print("   {:04X} ({}) - {}".format(attribute, attribute, type_name))
