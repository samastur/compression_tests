from collections import namedtuple
import csv
import os
from os.path import join
import shutil
import time

import click
import pyimagediet.process as process

CONFIGURE_HELP = '''\
Inspect and print configuration customisation for your environment.'''

Stats = namedtuple('Stats', ['filename', 'orig_size', 'time', 'new_size',
                             'squeezed_by'])


'''
def get_configuration(ctx, param, value):
    if value:
        click.echo(get_config())
        ctx.exit()
'''


def get_files(dirname):
    for (root, dirs, files) in os.walk(dirname):
        for filename in files:
            yield join(root, filename)


def copy_dir(src, dest):
    dest_dir = os.path.join(dest, 'test_files')
    shutil.copytree(src, dest_dir)
    return dest_dir


def calc_effectiveness(orig_size, new_size):
    return round((1 - 1.0 * new_size/orig_size)*100, 2)


def test_compression(filename, config):
    st = None

    # Pre state
    statinfo = os.stat(filename)
    orig_size = statinfo.st_size
    start_time = time.time()

    # Compress
    changed = process.diet(filename, config)

    # Post state
    if changed:
        end_time = time.time()
        statinfo = os.stat(filename)
        new_size = statinfo.st_size

        st = Stats(
            filename,
            orig_size,
            round(end_time-start_time, 1),
            new_size,
            calc_effectiveness(orig_size, new_size)
        )

    return st


def clean_files(dirname):
    shutil.rmtree(dirname)


@click.command()
@click.option('--clean', is_flag=True, default=False,
              help='Remove test compressed files')
@click.option('--config', 'configuration', required=True, envvar='DIET_CONFIG',
              type=click.Path(exists=True))
@click.argument('test_dir', type=click.Path(exists=True))
@click.argument('output_dir', type=click.Path(exists=True))
def squeeze(test_dir, output_dir, configuration, clean):
    """Simple program that copies test_dir to output_dir, compresseses all
    images it finds in it and outputs efficiency stats."""
    total_time = total_size = total_reduced_size = no_files = 0

    raw_config = process.read_yaml_configuration(configuration)
    config = process.parse_configuration(raw_config)

    click.echo('Making a copy of test files...')
    files = copy_dir(test_dir, output_dir)

    click.echo('Testing...')
    stats_file = os.path.join(output_dir, 'stats.csv')
    with open(stats_file, 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|',
                               quoting=csv.QUOTE_MINIMAL)

        for filename in get_files(files):
            stats = test_compression(filename, config)
            if stats:  # Skip ignored files
                csvwriter.writerow(stats)

                no_files += 1
                total_time += stats.time
                total_size += stats.orig_size
                total_reduced_size += stats.new_size

    if clean:
        clean_files(files)

    summary = """\

Files: {}
Total size: {}
Reduced size: {}
Reduced by (%): {}
Time spent (seconds): {}
"""
    total_reduced_by = calc_effectiveness(total_size, total_reduced_size)
    click.echo(summary.format(no_files, total_size, total_reduced_size,
                              total_reduced_by, total_time))
