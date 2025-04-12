import click
import utilities.data_dumper
import utilities.print_packets
import utilities.print_variables
import utilities.print_timings
import utilities.packet_recorder


@click.group()
def cli():
    pass


@cli.command()
@click.argument('port')
@click.argument('file_name')
def dump_data(port, file_name):
    """dumps a hex string of all bytes recieved on a serial port for later processing"""
    utilities.data_dumper.dump_data(port, file_name)


@cli.command()
@click.argument('file_name')
def print_packets(file_name):
    """prints packets from a previous serial dump"""
    utilities.print_packets.print_packets(file_name)


@cli.command()
@click.argument('file_name')
def print_variables(file_name):
    """prints variables from a previous serial dump"""
    utilities.print_variables.print_variables(file_name)


@cli.command()
@click.argument('port')
def record_packets(port):
    """save timestamped packets"""
    utilities.packet_recorder.record_packets(port)

@cli.command()
@click.argument('file_name')
def print_timings(file_name):
    """prints variables from a previous serial dump"""
    utilities.print_timings.print_timings(file_name)


if __name__ == "__main__":
    cli()

