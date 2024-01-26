#!/usr/local/bin/python3
# requires a text file containing the following:
# lines starting with '#' are comments and ignored
# lines starting with '/' are directories and are created
# lines starting with '!' are files to be copied and renamed,
#   two fields are required, separated by a ',', localname, piconame
# 1 line starting with '+' will be copied to main.py
# directory lines must appear prior to the files in the directories
# all other lines are considered valid files in the current directory
# -p port required to set to board serial port


import click
import re
from CoolTerm.pyboard import Pyboard
import sys
from CoolTerm.CT_connect import conn
from CoolTerm.CT_disconnect import disc


def show_progress_bar(size, total_size, op="copying"):
    if not sys.stdout.isatty():
        return
    verbose_size = 2048
    bar_length = 20
    if total_size < verbose_size:
        return
    elif size >= total_size:
        # Clear progress bar when copy completes
        click.echo("\r" + " " * (13 + len(op) + bar_length) + "\r", end="")
    else:
        bar = size * bar_length // total_size
        progress = size * 100 // total_size
        click.echo(
            "\r ... {} {:3d}% [{}{}]".format
            (op, progress, "#" * bar, "-" * (bar_length - bar)),
            end="",
        )


folder = re.compile(r'^/')
comment = re.compile(r'^#')
main_prog = re.compile(r'^\+')
change = re.compile(r'^!')


@click.command('build')
@click.version_option("1.1.3", prog_name="mpbuild")
@click.option('-p', '--port', required=True, type=str,
              help='Port address (e.g., /dev/cu.usbmodem3101, COM3).')
@click.argument('build',
                type=click.Path(exists=True, readable=True),
                required=True)
@click.option('-n', '--dry-run', 'dryrun', is_flag=True, default=False,
              help='Show commands w/o execution & print file format.')
@click.option('-v', '--verbose', is_flag=True, default=False,
              help='Print lines in build file prior to execution.')
def build(port, build, dryrun, verbose):
    """
    Builds an MicroPython application on a board.
    Uses a text file containing names of folders and files to copy files
    and create folders, approriately to a board running MicroPython.
    Requires -p port for serial port: as in -p /dev/cu.usb... or -p COM3
    Board storage must be empty or program exits.

    \b
    * Requires a text file containing the following:
    * Filenames can NOT have blanks in their names.
    * lines starting with '\\n *' are comments and ignored
    * lines starting with '/' are directories and are created
    * lines starting with '!' are files to be copied and renamed,
    + 2 fields are required, separated by a ', ', localname, piconame
    * 1 line starting with '+' will be copied to main.py
    * directory lines must be prior to the files in the directories
    * all other lines are valid files in the current directory
    * -p port required to set to board serial port
    """

    click.echo(f"Building uP application using {build} file on {port} port")
    disc()

    pyb = Pyboard(port, 115200)
    pyb.enter_raw_repl()
    with open(build, 'r') as files:
        file_list = files.readlines()

    dirs = []
    local_files = pyb.fs_listdir("/")
    if len(local_files) != 0:
        click.echo(f"Flash memory not empty, delete files and try again.")
        click.echo(f"Files on board are the following: ")
        for file in local_files:
            if file[3] == 0:
                # directory, don't print size
                click.echo(f"{file[0]}/")
            else:
                # file, print both name and size
                click.echo(f"{file[0]:>20}\t{file[3]}")
        sys.exit()

    for file in file_list:
        if verbose:
            click.echo(f"{file.strip()}")
        # line begins with a slash, create a dir using the following text
        if folder.match(file):
            d = file.strip()
            dirs.append(d)
            if dryrun:
                click.echo(f"pyb.fs_mkdir({d})")
            else:
                pyb.fs_mkdir(d)

        # line begins with a #, ignore the line its a comment
        elif comment.match(file):
            continue

        # line begins with a +, copy it to main.py
        elif main_prog.match(file):
            s = file[1:].strip()
            if dryrun:
                click.echo(f"pyb.fs_put({s}, main.py)")
            else:
                pyb.fs_put(
                    s, 'main.py', progress_callback=show_progress_bar)

        # line begins with a +, copy it to main.py
        elif change.match(file):
            s, d = file[1:].split(',')
            if dryrun:
                click.echo(f"pyb.fs_put({s}, {d.strip()})")
            else:
                pyb.fs_put(
                    s, d.strip(), progress_callback=show_progress_bar)

        # all other lines are assumed to be valid files to copy to board
        else:
            s = file.strip()
            if dryrun:
                click.echo(f"pyb.fs_put({s}, {s})")
            else:
                pyb.fs_put(s, s, progress_callback=show_progress_bar)

    click.echo(f"/")
    pyb.fs_ls('/')
    for d in dirs:
        click.echo(f"{d}/")
        pyb.fs_ls(d)
    pyb.exit_raw_repl()
    pyb.close()

    conn()


if __name__ == '__main__':
    build()
