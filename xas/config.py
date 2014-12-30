# -*- coding: utf-8 -*-

# Copyright (C) 2014 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from __future__ import print_function

import argparse

from xivo.config_helper import parse_config_file
from xivo.xivo_logging import get_log_level_by_name


def load(argv):
    default_config = {
        'debug': False,
        'foreground': False,
        'user': 'root',
        'log_level': 'info',
        'config_file': '/etc/xas/config.yml',
        'log_filename': '/var/log/xas.log',
        'pid_filename': '/var/run/xas/xas.pid',
        'rest_api': {
            'listen': '',
            'port': 8888,
        },
    }
    config = dict(default_config)

    config.update(_parse_cli_args(argv, default_config))
    config.update(parse_config_file(config['config_file']))
    _interpret_raw_values(config)

    return config


def _parse_cli_args(argv, default_config):
    parser = argparse.ArgumentParser()
    parser.add_argument('-c',
                        '--config-file',
                        action='store',
                        default=default_config['config_file'],
                        help="The path where is the config file. Default: %(default)s")
    parser.add_argument('-d',
                        '--debug',
                        action='store_true',
                        default=default_config['debug'],
                        help="Log debug messages. Overrides log_level. Default: %(default)s")
    parser.add_argument('-f',
                        '--foreground',
                        action='store_true',
                        default=default_config['foreground'],
                        help="Foreground, don't daemonize. Default: %(default)s")
    parser.add_argument('-l',
                        '--log-level',
                        action='store',
                        default='INFO',
                        help="Logs messages with LOG_LEVEL details. Must be one of:\n"
                             "critical, error, warning, info, debug. Default: %(default)s")
    parser.add_argument('-u',
                        '--user',
                        action='store',
                        default=default_config['user'],
                        help="The owner of the process.")
    parsed_args = parser.parse_args(argv)
    return vars(parsed_args)


def _interpret_raw_values(config):
    config['log_level'] = get_log_level_by_name(config['log_level'])
