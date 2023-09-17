# Ganache Service Library

Easily manage and interact with Ganache from your Python applications using the `Ganache_Service` class.

## Table of Contents

- [Installation](#installation)
- [Features](#features)
- [Usage](#usage)
  - [Initialization](#initialization)
  - [Methods](#methods)
  - [Attributes](#attributes)
- [Contributing](#contributing)
- [License](#license)

## Installation
```python
pip install ganache_python_serv
```
You will need to have ganache installed globaly in node.js.
## Features

- Initialize Ganache with custom configurations.
- Start and stop Ganache programmatically.
- Interact with the Ganache environment, including mining blocks and adjusting time.
- Monitor Ganache's output and extract key details.

## Usage

### Initialization

Initialize the `Ganache_Service` with custom configurations:
```python
from ganache_service import Ganache_Service

service = Ganache_Service(**kwargs)
```
See Attributes for the initilization optional values.

### Methods

- `start(mnemonic=None, accounts=None)`: Start Ganache with optional mnemonic and accounts.
- `stop()`: Stop the running Ganache instance.
- `mine_block()`: Mine a single block.
- `mine_blocks(n)`: Mine `n` blocks sequentially.
- `increase_time(seconds)`: Increase time in the Ganache environment by a specified number of seconds.

### Attributes

#### Initialization Attributes

These attributes can be set during the initialization of the `Ganache_Service` class:

- `ganache_path`: Path to the Ganache executable. Default: `'ganache'`
- `ip_address`: IP address for Ganache to bind to. Default: `'127.0.0.1'`
- `port`: Port number for Ganache. Default: `8545`
- `fork_url`: URL for the blockchain to fork from. No default value. 
- `fork_block`: Block number to fork from. No default value. 
- `block_time`: Time (in seconds) between blocks. Default: `999999`
- `gas_price`: Gas price in Wei. Default: `20000000000`
- `gas_limit`: Gas limit in Wei. Default: `6721975`

All initialization attributes have to be specified as keyword arguments. If fork parameters aren't specified ganache will start with a clean state.

#### Ganache Output Attributes

These attributes capture the output and details of the running Ganache instance:

- `process`: The subprocess instance representing the running Ganache process.
- `accounts`: List of available accounts.
- `private_keys`: Corresponding private keys for the accounts.
- `mnemonic`: Mnemonic phrase.
- `base_hd_path`: Base HD path.
- `default_gas_price`: Default gas price.
- `block_gas_limit`: Block gas limit.
- `call_gas_limit`: Call gas limit.
- `network_id`: Network ID.
- `time`: Time of initialization.
- `hardfork`: Current hardfork.
- `chain_id`: Chain ID.

## Contributing

This library is in its early stages and has ample room for enhancement and optimization. We recognize the potential for significant improvements and warmly welcome contributions from the community. If you have ideas, suggestions, or improvements, please feel free to submit a pull request or open an issue on our [GitHub repository](https://github.com/Bortxop/ganache-python-service). Your involvement is invaluable to the growth and success of this project.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


