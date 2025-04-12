import decoder
import datetime
import statistics
import pprint

all_data = dict()


def process_data_block(time, data):
    global all_data

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
            if attribute not in all_data[meter][cluster]:
                all_data[meter][cluster][attribute]={
                    "count": 0,
                    "timings": list(),
                }
            all_data[meter][cluster][attribute]["count"] += 1
            all_data[meter][cluster][attribute]["timings"].append(time)


def print_timings(file_name):
    with open(file_name, "r") as data_file:
        
        for line in data_file:
            time = datetime.datetime.fromisoformat(" ".join(line.split(" ")[0:2]))
            data = bytes.fromhex(" ".join(line.split(" ")[2:]))
            process_data_block(time, data)

    # print information on timings of packets
    for meter in all_data:

        print("meter: {}".format(meter))
        for cluster in dict(sorted(all_data[meter].items())):
            print("cluster {:04X} ({})".format(cluster, cluster))

            for attribute in dict(sorted(all_data[meter][cluster].items())):
                count = all_data[meter][cluster][attribute]["count"]

                if count==1:
                    rec_time = all_data[meter][cluster][attribute]["timings"][0]
                    print("   {:04X} ({}) - {} ({})".format(attribute, attribute, count, rec_time.isoformat()))
                else:
                    timediff=list()
                    for x in range(len(all_data[meter][cluster][attribute]["timings"])-1):
                        timediff.append(
                            (all_data[meter][cluster][attribute]["timings"][x+1] - 
                            all_data[meter][cluster][attribute]["timings"][x]).seconds
                        )
                    avg = statistics.mean(timediff)

                    print("   {:04X} ({}) - {} ({:.0f}s between measurements)".format(attribute, attribute, count, avg))

