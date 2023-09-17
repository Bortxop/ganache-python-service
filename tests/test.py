# -*- coding: utf-8 -*-
"""
Created on Sun Sep  3 03:36:56 2023

@author: bortxomane
"""
import unittest
import sys

path_to_library = r'../ganache_python_service/'
if path_to_library not in sys.path:
    sys.path.insert(0, path_to_library)

from ganache_python_service.ganache_service import Ganache_Service

"""Normally this is the path to ganache"""
youruser="bor-t"
ganache_path = rf'C:/Users/{youruser}/AppData/Roaming/npm/ganache.cmd'
if ganache_path not in sys.path:
    sys.path.insert(0, ganache_path)

class TestGanacheService(unittest.TestCase):

    def setUp(self):
        self.default_service = Ganache_Service(ganache_path = ganache_path)
    def tearDown(self):
        if self.default_service.process:
            self.default_service.stop()

    def test_default_initialization(self):       
        self.assertEqual(self.default_service.ganache_path, ganache_path)
        self.assertEqual(self.default_service.ip, '127.0.0.1')
        self.assertEqual(self.default_service.port, 8545)
        self.assertIsNone(self.default_service.fork_url)
        self.assertIsNone(self.default_service.fork_block)
        self.assertEqual(self.default_service.block_time, 999999)
        self.assertIsNone(self.default_service.gas_price)
        self.assertEqual(self.default_service.gas_limit, 6721975)

    def test_start_stop(self):
        self.default_service.start()
        self.assertIsNotNone(self.default_service.process)
        self.default_service.stop()
        self.assertIsNone(self.default_service.process)

    def test_mine_block(self):
        self.default_service.start()
        initial_block = self.default_service.send_rpc_request('eth_blockNumber', [])
        self.default_service.mine_block()
        new_block = self.default_service.send_rpc_request('eth_blockNumber', [])
        self.assertNotEqual(initial_block, new_block)
        self.default_service.stop()

if __name__ == '__main__':
    unittest.main()
