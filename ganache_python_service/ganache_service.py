# -*- coding: utf-8 -*-
'''
@author: bortxomane
'''

import subprocess
import time
import json
import psutil
from .helpers import (is_port_closed, find_first_closed_port, clean_output, 
    extract, extract_and_convert_to_datetime, parse_section)
from .logger import Logger

class Ganache_Service():
    '''
    Initialize the Ganache service.
    
    :param ganache_path (str, default='ganache'): Path to initialize Ganache in case it's not in PATH.
    :param logs_path (str, default='./logs/ganache_service'): Path to store logs.
    :param ip (str, default='127.0.0.1'): IP address for Ganache to bind to.
    :param port (int, default=8545): Port number for Ganache.
    :param fork_url (str, optional): URL for the blockchain to fork from.
    :param fork_block (int, optional): Block number to fork from.
    :param block_time (int, 999999): Time (in seconds) between blocks.
    :param gas_price (int, optional): Gas price in Wei.
    :param gas_limit (int, default=6721975): Gas limit in wei.
    
    All parameters are passed as keyword arguments.
    '''
    def __init__(self, **kwargs) -> None:
        self.ganache_path = kwargs.get('ganache_path', 'ganache')
        self.ip = kwargs.get('ip', '127.0.0.1')
        self.port = kwargs.get('port', 8545)
               
        self.fork_url = kwargs.get('fork_url')
        self.fork_block = kwargs.get('fork_block')
        self.block_time = kwargs.get('block_time', 999999)
        self.gas_price = kwargs.get('gas_price')
        self.gas_limit = kwargs.get('gas_limit', 6721975)
        self.process = None

        self.logger = Logger.get_logger(kwargs.get('logs_path', './logs/ganache_service'))

    def start(self, mnemonic=None, accounts=None):
        '''Start ganache.'''
        if self.process:
            self.logger.warn('Already running an instance')
            return
        
        if not is_port_closed(self.ip, self.port):
            self.port = find_first_closed_port(self.ip)
            
        cmd = [self.ganache_path, '--host', self.ip, '-p', str(self.port)]
        if self.fork_url:
            if self.fork_block:
                cmd.extend(['--fork', f'{self.fork_url}@{self.fork_block}'])
            else:
                cmd.extend(['--fork', self.fork_url])

        if self.block_time:
            cmd.extend(['--blockTime', str(self.block_time)])

        if self.gas_price:
            cmd.extend(['--gasPrice', str(self.gas_price)])
            
        cmd.extend(['--gasLimit', str(self.gas_limit)])
        
        if mnemonic:
            cmd.extend(['-m', mnemonic])        
        if accounts:
            for acc in accounts:
                cmd.extend(['--account', acc])
        
        self.logger.info(' '.join(cmd))
        self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                                        encoding='utf-8', bufsize=1, universal_newlines=True)
        self._parse_output_onstart()
        if not self._wait_for_ganache_to_initialize():
            self.close()          

    def stop(self):
        '''Stopping ganache.'''
        if self.process:
            self._kill_process_tree(self.process.pid)
            self.process = None
            self.logger.info('Ganache node terminated')
        else:
            self.logger.warning('No running process found')

    def mine_block(self):
        '''Mine a block.'''
        self.send_rpc_request('evm_mine', [])

    def mine_blocks(self, n):
        '''Mine n blocks secuentially.'''
        for i in range(n):
            self.mine_block()

    def increase_time(self, seconds):
        '''Increase time in the Ganache environment.'''
        self.send_rpc_request('evm_increaseTime', [seconds])
        self.mine_block()
    
    def send_rpc_request(self, method, params):
        '''Send an RPC request to the Ganache CLI.'''
        payload = {
            'jsonrpc': '2.0',
            'id': 1,
            'method': method,
            'params': params
        }
        response = subprocess.check_output([
            'curl',
            '-X', 'POST',
            '-H', 'Content-Type: application/json',
            '--data', json.dumps(payload),
            f'http://{self.ip}:{self.port}'
        ])
        self.logger.debug(json.loads(response))
        return json.loads(response)       
            
    def _parse_output_onstart(self):
        '''Parse output, just for starting ganache.'''
        output_lines = []
        while True:
            line = self.process.stdout.readline()
            if not line and self.process.poll() is not None:
                break
            output_lines.append(line.strip())
            if 'RPC Listening on' in line:
                break
        self.output  = '\n'.join(output_lines)

        cleaned_output = clean_output(self.output)
        self.accounts = parse_section('Available Accounts', r'0x[a-fA-F0-9]{40}', cleaned_output)
        self.private_keys = parse_section('Private Keys', r'[a-fA-F0-9]{64}', cleaned_output)
        self.mnemonic = extract(r'Mnemonic:\s+(.*)', cleaned_output)
        self.base_hd_path = extract(r'Base HD Path:\s+(.*)', cleaned_output)
        self.gas_price = int(extract(r'Default Gas Price\s+=+\s+(\d+)', cleaned_output))
        self.gas_limit = int(extract(r'BlockGas Limit\s+=+\s+(\d+)', cleaned_output))
        self.call_gas_limit = int(extract(r'Call Gas Limit\s+=+\s+(\d+)', cleaned_output))
        self.chain_id = int(extract(r'Id:\s+(\d+)', cleaned_output))
        self.logger.info(self.output)
        if self.fork_url:
            self.network_id = int(extract(r'Network ID:\s+(\d+)', cleaned_output))
            self.time = extract_and_convert_to_datetime(r'Time:\s+(.+?)\sGMT', cleaned_output)
            self.hardfork = extract(r'Hardfork: (.*)', cleaned_output)
  
    def _wait_for_ganache_to_initialize(self, retries=10, delay=2):
        '''Wait for Ganache to initialize and be ready to accept connections.'''
        time.sleep(delay)
        attempts = 0
        for attempts in range(retries):
            time.sleep(delay)
            attempts += 1
            try:
                response = self.send_rpc_request('eth_blockNumber', [])
                if 'result' in response:
                    return True
            except Exception as e:
                self.logger.debug(f"Attempt {attempts} failed with error: {e}")

        self.logger.error('Failed to connect to Ganache after {retries} attempts.', stack_info=True)
        raise ConnectionError(f'Failed to connect to Ganache after {retries} attempts.')
        return False
                
    def _kill_process_tree(self,pid):
        '''Not the most suitable approach but sending Ctrl+C does not work.'''
        try:
            parent = psutil.Process(pid)
            for child in parent.children(recursive=True):
                child.kill()
            parent.kill()
        except psutil.NoSuchProcess:
            self.logger.warn(f'No process with PID {pid} found.')
            