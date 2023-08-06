import ipaddress
import struct
from dataclasses import astuple
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from adc_socketx import commands, config, data_models


INFO = 'ADC socket data eXchange script. GTLAB Diagnostic LLC, 2023'

console = Console()

app = typer.Typer(
    add_completion=False,
    help=INFO,
)


def parse_ipv4_and_connect(ip: str) -> None:
    try:
        ipaddress.IPv4Address(ip)
    except ValueError as e:
        msg = f'err: {e}. Please check.'
        typer.secho(msg, fg=typer.colors.BRIGHT_RED)
        raise typer.Exit()

    commands.sock.host = ip
    commands.sock.connect()


@app.command()
def get_info(
    ip: str = typer.Option(config.SOCKET_HOST, help='IPv4 connection address')
) -> None:
    """Get the ADC information (s/n, frequency, channels, calibration)."""
    parse_ipv4_and_connect(ip)
    data = commands.adc_get_info()
    table = Table(show_header=False)

    for table_row in zip(config.COMMAND_GET_INFO['table_info_columns'], data):
        table.add_row(table_row[0], str(table_row[1]), style='green')

    console.print(table)
    commands.sock.disconnect()


@app.command()
def get_lan(
    ip: str = typer.Option(config.SOCKET_HOST, help='IPv4 connection address')
) -> None:
    """Get lan configuration (port, ip, netmask, gateway, MAC)."""
    parse_ipv4_and_connect(ip)
    data = commands.adc_get_lan()
    table = Table(show_header=False)
    col = config.COMMAND_GET_LAN['table_info_columns']
    table.add_row(col[0], str(data[0]))
    for index, value in enumerate(range(1, 13, 4)):
        table.add_row(
            col[index + 1],
            '.'.join(str(___) for ___ in data[value:value + 4]),
        )
    table.add_row(col[4], data[13].hex().upper())

    console.print(table)
    commands.sock.disconnect()


@app.command()
def set_lan(
    ipv4: str = typer.Argument(
        ..., help='New IPv4 address/netmask. Example: 192.168.0.50/24'
    ),
    gateway: str = typer.Argument(
        config.SOCKET_GATEWAY, help='New IPv4 Gateway'
    ),
    ip: str = typer.Option(
        config.SOCKET_HOST, help='IPv4 connection address'
    )
) -> None:
    """Set lan (ipv4) settings (ip/netmask, gateway)."""
    try:
        new_ip = ipaddress.IPv4Interface(ipv4)
        new_gateway = ipaddress.IPv4Address(gateway)
    except ValueError as e:
        msg = f'err: {e}. Please check.'
        typer.secho(msg, fg=typer.colors.BRIGHT_RED)
        raise typer.Exit()

    if not (new_ip.is_private and new_gateway.is_private):
        typer.secho(
            'err: Only private IP addresses is supported',
            fg=typer.colors.BRIGHT_RED
        )
        raise typer.Exit()

    confirm_string = (
        f'Change the ip-address to: {new_ip}\n'
    )

    if new_gateway:
        confirm_string += (
            f'Change gateway to: {new_gateway}\n'
            f'Are you sure?'
        )

    typer.confirm(
        confirm_string,
        abort=True
    )

    parse_ipv4_and_connect(ip)

    data = commands.adc_get_lan()
    lan_config = data_models.LanConfig(*data)

    l_new_ip, l_new_netmask, l_new_gateway = (
        str(new_ip.ip).split('.'),
        str(new_ip.netmask).split('.'),
        str(new_gateway).split('.'),
    )

    for i in range(4):
        setattr(lan_config, f'ip_{i + 1}', int(l_new_ip[i]))
        setattr(lan_config, f'mask_{i + 1}', int(l_new_netmask[i]))
        setattr(lan_config, f'gateway_{i + 1}', int(l_new_gateway[i]))

    lan_command = struct.pack(
        config.COMMAND_SET_LAN['struct_pack_str'], *astuple(lan_config)
    )

    if commands.adc_set_lan(lan_command):
        console.print(
            f'The new ip address is set to {new_ip}. '
            f'Don\'t forget to update your settings!',
            style='green'
        )
    else:
        console.print('err: Failed to update ip settings!', style='red')

    commands.sock.disconnect()


@app.command()
def get_wav(
    seconds: int = typer.Argument(..., min=1, max=600),
    ch: int = typer.Option(
        config.NUM_OF_CHANNELS_DEFAULT,
        min=1, max=2,
        help='Set the number of channels to record'
    ),
    iepe: bool = True,
    ip: str = typer.Option(
        config.SOCKET_HOST,
        help='IPv4 connection address'
    ),
    out: Path = typer.Option(
        None,
        help='Path and name (only .wav extension!) of the file to be written',
        file_okay=True,
        dir_okay=False
    )
) -> None:
    """Record a signal from the ADC to a .wav file."""

    if out and out.suffix != '.wav':
        typer.secho(
            'err: Please add the .wav extension to the file',
            fg=typer.colors.BRIGHT_RED
        )
        raise typer.Exit()

    parse_ipv4_and_connect(ip)
    if ch == 1:
        num_of_frames = round(config.FRAMES_1CH_PER_SECOND * seconds)
        commands.adc_set_mode(False, iepe, iepe)
    else:
        num_of_frames = round(config.FRAMES_2CH_PER_SECOND * seconds)
        commands.adc_set_mode(True, iepe, iepe)

    if not commands.record_to_wav(num_of_frames, ch, out):
        console.print('Something went wrong, check the settings', style='red')

    commands.sock.disconnect()


@app.command()
def reboot(
    ip: str = typer.Option(config.SOCKET_HOST, help='IPv4 connection address')
) -> None:
    """Reboot the ADC."""
    parse_ipv4_and_connect(ip)
    if commands.adc_reboot():
        console.print('ADC rebooted!', style='green')
    commands.sock.disconnect()


if __name__ == '__main__':
    app()
