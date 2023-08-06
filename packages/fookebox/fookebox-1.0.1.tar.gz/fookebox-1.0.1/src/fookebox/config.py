# fookebox, https://code.ott.net/fookebox/
# Copyright (c) 2007-2023 Stefan Ott. all rights reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
This module deals with the fookebox config file
"""
from configparser import ConfigParser, SectionProxy


def _parser() -> ConfigParser:
    config = ConfigParser()
    config['DEFAULT'] = {
        'mpd_host': 'localhost',
        'mpd_port': '6600',
        'max_queue_length': '5',
        'enable_controls': 'true',
        'listen_port': '8888',
        'auto_queue': 'true',
        'auto_queue_time_left': '3',
        'show_search': 'true',
        'site_name': 'fookebox',
        'enable_song_removal': 'true',
        'enable_queue_album': 'true',
    }
    return config


def default_config() -> SectionProxy:
    """
    Get default configuration values.

    Returns
    -------
    A SectionProxy object representing the default fookebox configuration.
    """
    config = _parser()
    return config['DEFAULT']


def load_config(filename: str) -> SectionProxy:
    """
    Load a configuration file.

    Parameters
    ----------
    filename : str
        absolute file system path of the config file to load

    Returns
    -------
    A SectionProxy object representing the loaded fookebox configuration.
    """
    config = _parser()
    config.read(filename)

    if config.has_section('fookebox'):
        return config['fookebox']

    return config['DEFAULT']
