# -*- coding: utf-8 -*-
'''
@author: bortxomane
'''

import socket
from datetime import datetime
import re

def is_port_closed(ip, port):
    '''Return True if the port is closed, False otherwise.'''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        result = s.connect_ex((ip, port))
        return result != 0

def find_first_closed_port(ip, port_start = 1024, port_end = 65534):
    '''Return a first port that is available.'''
    for port in range(port_start, port_end + 1):
        if is_port_closed(ip, port):
            return port
    return None

def extract_and_convert_to_datetime(pattern, output):
    '''Extract a date-time pattern from the output and convert it to a datetime object.'''
    time_str = extract(pattern, output)
    if time_str:
        return datetime.strptime(time_str, '%a %b %d %Y %H:%M:%S')
    return None

def clean_output(output):
    '''Remove ANSI escape sequences from the output.'''
    return re.sub(r'\x1b\[.*?m', '', output)

def parse_section(section_name, pattern,output):
    '''Extract a section from the output using a specific regex pattern.'''
    section_pattern = r'{}.*?=\n(.*?)\n\n'.format(section_name)
    section_match = re.search(section_pattern, output, re.DOTALL)
    if section_match:
        return re.findall(pattern, section_match.group(1))
    return []

def extract(pattern,output):
    ''''Extract a pattern from the output.'''
    match = re.search(pattern, output)
    if match:
        return match.group(1)
    return None