from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
import time
import math
from web3.exceptions import TransactionNotFound
# Replace with your Infura project ID and private key
private_key = ""

# Replace with your account address
account_address = "0xb16b77C16773DEF8fA279A1228Eba9308eCD7841"

# Connect to Infura
w3 = Web3(Web3.HTTPProvider("https://babel-api.testnet.iotex.io"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
# Uniswap Router ABI and contract address
pancakeswap_router_abi = '''[
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "_factory",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "_weth",
          "type": "address"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "constructor"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "internalType": "address",
          "name": "sender",
          "type": "address"
        },
        {
          "indexed": false,
          "internalType": "uint256",
          "name": "amount0In",
          "type": "uint256"
        },
        {
          "indexed": false,
          "internalType": "address",
          "name": "_tokenIn",
          "type": "address"
        },
        {
          "indexed": true,
          "internalType": "address",
          "name": "to",
          "type": "address"
        }
      ],
      "name": "Swap",
      "type": "event"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "tokenA",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "tokenB",
          "type": "address"
        },
        {
          "internalType": "bool",
          "name": "stable",
          "type": "bool"
        },
        {
          "internalType": "uint256",
          "name": "amountADesired",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "amountBDesired",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "amountAMin",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "amountBMin",
          "type": "uint256"
        },
        {
          "internalType": "address",
          "name": "to",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "deadline",
          "type": "uint256"
        }
      ],
      "name": "addLiquidity",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "amountA",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "amountB",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "liquidity",
          "type": "uint256"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "token",
          "type": "address"
        },
        {
          "internalType": "bool",
          "name": "stable",
          "type": "bool"
        },
        {
          "internalType": "uint256",
          "name": "amountTokenDesired",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "amountTokenMin",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "amountETHMin",
          "type": "uint256"
        },
        {
          "internalType": "address",
          "name": "to",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "deadline",
          "type": "uint256"
        }
      ],
      "name": "addLiquidityETH",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "amountToken",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "amountETH",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "liquidity",
          "type": "uint256"
        }
      ],
      "stateMutability": "payable",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "factory",
      "outputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "amountIn",
          "type": "uint256"
        },
        {
          "internalType": "address",
          "name": "tokenIn",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "tokenOut",
          "type": "address"
        }
      ],
      "name": "getAmountOut",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "amount",
          "type": "uint256"
        },
        {
          "internalType": "bool",
          "name": "stable",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "amountIn",
          "type": "uint256"
        },
        {
          "components": [
            {
              "internalType": "address",
              "name": "from",
              "type": "address"
            },
            {
              "internalType": "address",
              "name": "to",
              "type": "address"
            },
            {
              "internalType": "bool",
              "name": "stable",
              "type": "bool"
            }
          ],
          "internalType": "struct Router.route[]",
          "name": "routes",
          "type": "tuple[]"
        }
      ],
      "name": "getAmountsOut",
      "outputs": [
        {
          "internalType": "uint256[]",
          "name": "amounts",
          "type": "uint256[]"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "tokenA",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "tokenB",
          "type": "address"
        },
        {
          "internalType": "bool",
          "name": "stable",
          "type": "bool"
        }
      ],
      "name": "getReserves",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "reserveA",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "reserveB",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "pair",
          "type": "address"
        }
      ],
      "name": "isPair",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "tokenA",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "tokenB",
          "type": "address"
        },
        {
          "internalType": "bool",
          "name": "stable",
          "type": "bool"
        }
      ],
      "name": "pairFor",
      "outputs": [
        {
          "internalType": "address",
          "name": "pair",
          "type": "address"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "tokenA",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "tokenB",
          "type": "address"
        },
        {
          "internalType": "bool",
          "name": "stable",
          "type": "bool"
        },
        {
          "internalType": "uint256",
          "name": "amountADesired",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "amountBDesired",
          "type": "uint256"
        }
      ],
      "name": "quoteAddLiquidity",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "amountA",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "amountB",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "liquidity",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "tokenA",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "tokenB",
          "type": "address"
        },
        {
          "internalType": "bool",
          "name": "stable",
          "type": "bool"
        },
        {
          "internalType": "uint256",
          "name": "liquidity",
          "type": "uint256"
        }
      ],
      "name": "quoteRemoveLiquidity",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "amountA",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "amountB",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "tokenA",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "tokenB",
          "type": "address"
        },
        {
          "internalType": "bool",
          "name": "stable",
          "type": "bool"
        },
        {
          "internalType": "uint256",
          "name": "liquidity",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "amountAMin",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "amountBMin",
          "type": "uint256"
        },
        {
          "internalType": "address",
          "name": "to",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "deadline",
          "type": "uint256"
        }
      ],
      "name": "removeLiquidity",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "amountA",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "amountB",
          "type": "uint256"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "token",
          "type": "address"
        },
        {
          "internalType": "bool",
          "name": "stable",
          "type": "bool"
        },
        {
          "internalType": "uint256",
          "name": "liquidity",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "amountTokenMin",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "amountETHMin",
          "type": "uint256"
        },
        {
          "internalType": "address",
          "name": "to",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "deadline",
          "type": "uint256"
        }
      ],
      "name": "removeLiquidityETH",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "amountToken",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "amountETH",
          "type": "uint256"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "token",
          "type": "address"
        },
        {
          "internalType": "bool",
          "name": "stable",
          "type": "bool"
        },
        {
          "internalType": "uint256",
          "name": "liquidity",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "amountTokenMin",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "amountETHMin",
          "type": "uint256"
        },
        {
          "internalType": "address",
          "name": "to",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "deadline",
          "type": "uint256"
        },
        {
          "internalType": "bool",
          "name": "approveMax",
          "type": "bool"
        },
        {
          "internalType": "uint8",
          "name": "v",
          "type": "uint8"
        },
        {
          "internalType": "bytes32",
          "name": "r",
          "type": "bytes32"
        },
        {
          "internalType": "bytes32",
          "name": "s",
          "type": "bytes32"
        }
      ],
      "name": "removeLiquidityETHWithPermit",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "amountToken",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "amountETH",
          "type": "uint256"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "tokenA",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "tokenB",
          "type": "address"
        },
        {
          "internalType": "bool",
          "name": "stable",
          "type": "bool"
        },
        {
          "internalType": "uint256",
          "name": "liquidity",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "amountAMin",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "amountBMin",
          "type": "uint256"
        },
        {
          "internalType": "address",
          "name": "to",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "deadline",
          "type": "uint256"
        },
        {
          "internalType": "bool",
          "name": "approveMax",
          "type": "bool"
        },
        {
          "internalType": "uint8",
          "name": "v",
          "type": "uint8"
        },
        {
          "internalType": "bytes32",
          "name": "r",
          "type": "bytes32"
        },
        {
          "internalType": "bytes32",
          "name": "s",
          "type": "bytes32"
        }
      ],
      "name": "removeLiquidityWithPermit",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "amountA",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "amountB",
          "type": "uint256"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "tokenA",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "tokenB",
          "type": "address"
        }
      ],
      "name": "sortTokens",
      "outputs": [
        {
          "internalType": "address",
          "name": "token0",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "token1",
          "type": "address"
        }
      ],
      "stateMutability": "pure",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "amountOutMin",
          "type": "uint256"
        },
        {
          "components": [
            {
              "internalType": "address",
              "name": "from",
              "type": "address"
            },
            {
              "internalType": "address",
              "name": "to",
              "type": "address"
            },
            {
              "internalType": "bool",
              "name": "stable",
              "type": "bool"
            }
          ],
          "internalType": "struct Router.route[]",
          "name": "routes",
          "type": "tuple[]"
        },
        {
          "internalType": "address",
          "name": "to",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "deadline",
          "type": "uint256"
        }
      ],
      "name": "swapExactETHForTokens",
      "outputs": [
        {
          "internalType": "uint256[]",
          "name": "amounts",
          "type": "uint256[]"
        }
      ],
      "stateMutability": "payable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "amountIn",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "amountOutMin",
          "type": "uint256"
        },
        {
          "components": [
            {
              "internalType": "address",
              "name": "from",
              "type": "address"
            },
            {
              "internalType": "address",
              "name": "to",
              "type": "address"
            },
            {
              "internalType": "bool",
              "name": "stable",
              "type": "bool"
            }
          ],
          "internalType": "struct Router.route[]",
          "name": "routes",
          "type": "tuple[]"
        },
        {
          "internalType": "address",
          "name": "to",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "deadline",
          "type": "uint256"
        }
      ],
      "name": "swapExactTokensForETH",
      "outputs": [
        {
          "internalType": "uint256[]",
          "name": "amounts",
          "type": "uint256[]"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "amountIn",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "amountOutMin",
          "type": "uint256"
        },
        {
          "components": [
            {
              "internalType": "address",
              "name": "from",
              "type": "address"
            },
            {
              "internalType": "address",
              "name": "to",
              "type": "address"
            },
            {
              "internalType": "bool",
              "name": "stable",
              "type": "bool"
            }
          ],
          "internalType": "struct Router.route[]",
          "name": "routes",
          "type": "tuple[]"
        },
        {
          "internalType": "address",
          "name": "to",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "deadline",
          "type": "uint256"
        }
      ],
      "name": "swapExactTokensForTokens",
      "outputs": [
        {
          "internalType": "uint256[]",
          "name": "amounts",
          "type": "uint256[]"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "amountIn",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "amountOutMin",
          "type": "uint256"
        },
        {
          "internalType": "address",
          "name": "tokenFrom",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "tokenTo",
          "type": "address"
        },
        {
          "internalType": "bool",
          "name": "stable",
          "type": "bool"
        },
        {
          "internalType": "address",
          "name": "to",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "deadline",
          "type": "uint256"
        }
      ],
      "name": "swapExactTokensForTokensSimple",
      "outputs": [
        {
          "internalType": "uint256[]",
          "name": "amounts",
          "type": "uint256[]"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "weth",
      "outputs": [
        {
          "internalType": "contract IWETH",
          "name": "",
          "type": "address"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "stateMutability": "payable",
      "type": "receive"
    }
  ]'''
pancakeswap_router_address = "0xa7e7678dFF355d3f9C409b3e998A1FDB2467410F"
router_contract = w3.eth.contract(address=Web3.to_checksum_address(pancakeswap_router_address), abi=pancakeswap_router_abi)
pancakeswap_pair_abi = '''[
    {
      "inputs": [],
      "stateMutability": "nonpayable",
      "type": "constructor"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "internalType": "address",
          "name": "owner",
          "type": "address"
        },
        {
          "indexed": true,
          "internalType": "address",
          "name": "spender",
          "type": "address"
        },
        {
          "indexed": false,
          "internalType": "uint256",
          "name": "amount",
          "type": "uint256"
        }
      ],
      "name": "Approval",
      "type": "event"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "internalType": "address",
          "name": "sender",
          "type": "address"
        },
        {
          "indexed": false,
          "internalType": "uint256",
          "name": "amount0",
          "type": "uint256"
        },
        {
          "indexed": false,
          "internalType": "uint256",
          "name": "amount1",
          "type": "uint256"
        },
        {
          "indexed": true,
          "internalType": "address",
          "name": "to",
          "type": "address"
        }
      ],
      "name": "Burn",
      "type": "event"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "internalType": "address",
          "name": "sender",
          "type": "address"
        },
        {
          "indexed": true,
          "internalType": "address",
          "name": "recipient",
          "type": "address"
        },
        {
          "indexed": false,
          "internalType": "uint256",
          "name": "amount0",
          "type": "uint256"
        },
        {
          "indexed": false,
          "internalType": "uint256",
          "name": "amount1",
          "type": "uint256"
        }
      ],
      "name": "Claim",
      "type": "event"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "internalType": "address",
          "name": "sender",
          "type": "address"
        },
        {
          "indexed": false,
          "internalType": "uint256",
          "name": "amount0",
          "type": "uint256"
        },
        {
          "indexed": false,
          "internalType": "uint256",
          "name": "amount1",
          "type": "uint256"
        }
      ],
      "name": "Fees",
      "type": "event"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "internalType": "address",
          "name": "sender",
          "type": "address"
        },
        {
          "indexed": false,
          "internalType": "uint256",
          "name": "amount0",
          "type": "uint256"
        },
        {
          "indexed": false,
          "internalType": "uint256",
          "name": "amount1",
          "type": "uint256"
        }
      ],
      "name": "Mint",
      "type": "event"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "internalType": "address",
          "name": "sender",
          "type": "address"
        },
        {
          "indexed": false,
          "internalType": "uint256",
          "name": "amount0In",
          "type": "uint256"
        },
        {
          "indexed": false,
          "internalType": "uint256",
          "name": "amount1In",
          "type": "uint256"
        },
        {
          "indexed": false,
          "internalType": "uint256",
          "name": "amount0Out",
          "type": "uint256"
        },
        {
          "indexed": false,
          "internalType": "uint256",
          "name": "amount1Out",
          "type": "uint256"
        },
        {
          "indexed": true,
          "internalType": "address",
          "name": "to",
          "type": "address"
        }
      ],
      "name": "Swap",
      "type": "event"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": false,
          "internalType": "uint256",
          "name": "reserve0",
          "type": "uint256"
        },
        {
          "indexed": false,
          "internalType": "uint256",
          "name": "reserve1",
          "type": "uint256"
        }
      ],
      "name": "Sync",
      "type": "event"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "internalType": "address",
          "name": "from",
          "type": "address"
        },
        {
          "indexed": true,
          "internalType": "address",
          "name": "to",
          "type": "address"
        },
        {
          "indexed": false,
          "internalType": "uint256",
          "name": "amount",
          "type": "uint256"
        }
      ],
      "name": "Transfer",
      "type": "event"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "name": "allowance",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "spender",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "amount",
          "type": "uint256"
        }
      ],
      "name": "approve",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "name": "balanceOf",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "blockTimestampLast",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "to",
          "type": "address"
        }
      ],
      "name": "burn",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "amount0",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "amount1",
          "type": "uint256"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "claimFees",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "claimed0",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "claimed1",
          "type": "uint256"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "claimStakingFees",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "name": "claimable0",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "name": "claimable1",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "tokenIn",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "amountIn",
          "type": "uint256"
        }
      ],
      "name": "current",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "amountOut",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "currentCumulativePrices",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "reserve0Cumulative",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "reserve1Cumulative",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "blockTimestamp",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "decimals",
      "outputs": [
        {
          "internalType": "uint8",
          "name": "",
          "type": "uint8"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "fees",
      "outputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "amountIn",
          "type": "uint256"
        },
        {
          "internalType": "address",
          "name": "tokenIn",
          "type": "address"
        }
      ],
      "name": "getAmountOut",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "getReserves",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "_reserve0",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "_reserve1",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "_blockTimestampLast",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "index0",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "index1",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "isStable",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "lastObservation",
      "outputs": [
        {
          "components": [
            {
              "internalType": "uint256",
              "name": "timestamp",
              "type": "uint256"
            },
            {
              "internalType": "uint256",
              "name": "reserve0Cumulative",
              "type": "uint256"
            },
            {
              "internalType": "uint256",
              "name": "reserve1Cumulative",
              "type": "uint256"
            }
          ],
          "internalType": "struct Pair.Observation",
          "name": "",
          "type": "tuple"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "metadata",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "dec0",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "dec1",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "r0",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "r1",
          "type": "uint256"
        },
        {
          "internalType": "bool",
          "name": "st",
          "type": "bool"
        },
        {
          "internalType": "address",
          "name": "t0",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "t1",
          "type": "address"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "to",
          "type": "address"
        }
      ],
      "name": "mint",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "liquidity",
          "type": "uint256"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "name",
      "outputs": [
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "name": "nonces",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "observationLength",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "name": "observations",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "timestamp",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "reserve0Cumulative",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "reserve1Cumulative",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "owner",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "spender",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "value",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "deadline",
          "type": "uint256"
        },
        {
          "internalType": "uint8",
          "name": "v",
          "type": "uint8"
        },
        {
          "internalType": "bytes32",
          "name": "r",
          "type": "bytes32"
        },
        {
          "internalType": "bytes32",
          "name": "s",
          "type": "bytes32"
        }
      ],
      "name": "permit",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "tokenIn",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "amountIn",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "points",
          "type": "uint256"
        }
      ],
      "name": "prices",
      "outputs": [
        {
          "internalType": "uint256[]",
          "name": "",
          "type": "uint256[]"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "tokenIn",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "amountIn",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "granularity",
          "type": "uint256"
        }
      ],
      "name": "quote",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "amountOut",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "reserve0",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "reserve0CumulativeLast",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "reserve1",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "reserve1CumulativeLast",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "tokenIn",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "amountIn",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "points",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "window",
          "type": "uint256"
        }
      ],
      "name": "sample",
      "outputs": [
        {
          "internalType": "uint256[]",
          "name": "",
          "type": "uint256[]"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "to",
          "type": "address"
        }
      ],
      "name": "skim",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "stable",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "name": "supplyIndex0",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "name": "supplyIndex1",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "amount0Out",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "amount1Out",
          "type": "uint256"
        },
        {
          "internalType": "address",
          "name": "to",
          "type": "address"
        },
        {
          "internalType": "bytes",
          "name": "data",
          "type": "bytes"
        }
      ],
      "name": "swap",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "symbol",
      "outputs": [
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "sync",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "token0",
      "outputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "token1",
      "outputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "tokens",
      "outputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "totalSupply",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "dst",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "amount",
          "type": "uint256"
        }
      ],
      "name": "transfer",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "src",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "dst",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "amount",
          "type": "uint256"
        }
      ],
      "name": "transferFrom",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "function"
    }
  ]
'''
token_abi = '''
[
    {
        "constant": true,
        "inputs": [],
        "name": "name",
        "outputs": [
            {
                "name": "",
                "type": "string"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [
            {
                "name": "_spender",
                "type": "address"
            },
            {
                "name": "_value",
                "type": "uint256"
            }
        ],
        "name": "approve",
        "outputs": [
            {
                "name": "",
                "type": "bool"
            }
        ],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "totalSupply",
        "outputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [
            {
                "name": "_from",
                "type": "address"
            },
            {
                "name": "_to",
                "type": "address"
            },
            {
                "name": "_value",
                "type": "uint256"
            }
        ],
        "name": "transferFrom",
        "outputs": [
            {
                "name": "",
                "type": "bool"
            }
        ],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "decimals",
        "outputs": [
            {
                "name": "",
                "type": "uint8"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [
            {
                "name": "_owner",
                "type": "address"
            }
        ],
        "name": "balanceOf",
        "outputs": [
            {
                "name": "balance",
                "type": "uint256"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [],
        "name": "symbol",
        "outputs": [
            {
                "name": "",
                "type": "string"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [
            {
                "name": "_to",
                "type": "address"
            },
            {
                "name": "_value",
                "type": "uint256"
            }
        ],
        "name": "transfer",
        "outputs": [
            {
                "name": "",
                "type": "bool"
            }
        ],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [
            {
                "name": "_owner",
                "type": "address"
            },
            {
                "name": "_spender",
                "type": "address"
            }
        ],
        "name": "allowance",
        "outputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "payable": true,
        "stateMutability": "payable",
        "type": "fallback"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": true,
                "name": "owner",
                "type": "address"
            },
            {
                "indexed": true,
                "name": "spender",
                "type": "address"
            },
            {
                "indexed": false,
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "Approval",
        "type": "event"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": true,
                "name": "from",
                "type": "address"
            },
            {
                "indexed": true,
                "name": "to",
                "type": "address"
            },
            {
                "indexed": false,
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "Transfer",
        "type": "event"
    }
]
'''
filtered_pairs = [[
        "0x87B873224EaD2a8cbBB7CfB39b18a795e7DA8CC7",
        "0x89c3A24FF5cE28385e7a09646A105E8fc3E66CBd",
        "false",
        "0x46483b20Bf3B62c575750FA1Ca3DCc494cbE52a6"
    ],
    [
        "0x791674ddb34e873603544511C130f012c49fd104",
        "0x87B873224EaD2a8cbBB7CfB39b18a795e7DA8CC7",
        "false",
        "0x404BD919BA0b7E0E5d0c1f6edfb9742cE212453C"
    ],
    [
        "0x791674ddb34e873603544511C130f012c49fd104",
        "0xD5526a2BcEEBb0771ea33A79068feB35d4337e82",
        "true",
        "0x1EE6D34c98e1c23287E299A6c9FA0d2D7FD34402"
    ],
    [
        "0x791674ddb34e873603544511C130f012c49fd104",
        "0xc6179D5941d056F221116Ef26404723e3a4271A1",
        "true",
        "0x6798ACeEf8389f9f8Edc5fEDD4A8b6a386e9A798"
    ],
    [
        "0x87B873224EaD2a8cbBB7CfB39b18a795e7DA8CC7",
        "0xD5526a2BcEEBb0771ea33A79068feB35d4337e82",
        "false",
        "0x71d978B81A6c3Be84D7cA0cF336B62fcee39A579"
    ],
    [
        "0x791674ddb34e873603544511C130f012c49fd104",
        "0x89c3A24FF5cE28385e7a09646A105E8fc3E66CBd",
        "false",
        "0xc023868D02593171E5f09D83eF6B8303C399f3f7"
    ],
    [
        "0x89c3A24FF5cE28385e7a09646A105E8fc3E66CBd",
        "0xD5526a2BcEEBb0771ea33A79068feB35d4337e82",
        "op",
        "0xd8c52dA8eEb9c28FCB27B3C68997Ca4947e8DE90"
    ],
    [
        "0x87B873224EaD2a8cbBB7CfB39b18a795e7DA8CC7",
        "0xc6179D5941d056F221116Ef26404723e3a4271A1",
        "op",
        "0x3b4c44EeA567Cb2D8F3Aa9fBee96629387e8F049"
    ],
    [
        "0x87B873224EaD2a8cbBB7CfB39b18a795e7DA8CC7",
        "0x89c3A24FF5cE28385e7a09646A105E8fc3E66CBd",
        "op",
        "0x815a3F855De0A47423E0Ffeed350cf8C97150426"
    ]]
def get_pair_address(tokenA, tokenB, pairs_list):
    for pair in pairs_list:
        if (pair[0] == tokenA and pair[1] == tokenB) or (pair[1] == tokenA and pair[0] == tokenB):
            return pair[3]  # Return the pair address
    return None  # Return None if no pair is found
def get_reserves(pair_address, token_in_address, token_out_address):
    # Establish contract for pair
    pair_contract = w3.eth.contract(address=pair_address, abi=pancakeswap_pair_abi)

    # Establish contracts for tokens
    token_in_contract = w3.eth.contract(address=token_in_address, abi=token_abi)
    token_out_contract = w3.eth.contract(address=token_out_address, abi=token_abi)

    try:
        token_in_balance = token_in_contract.functions.balanceOf(pair_address).call()

        token_in_decimals = token_in_contract.functions.decimals().call()
        token_in_reserve = token_in_balance / (10 ** token_in_decimals)

        token_out_balance = token_out_contract.functions.balanceOf(pair_address).call()

        token_out_decimals = token_out_contract.functions.decimals().call()
        token_out_reserve = token_out_balance / (10 ** token_out_decimals)

        return token_in_reserve, token_out_reserve

    except Exception as e:
        print(f"Error encountered while fetching reserves: {str(e)}")
        return 0, 0  # Return default values in case of an error
def check_if_pair_is_stable(pair_address):
    # Establish contract for pair
    pair_contract = w3.eth.contract(address=pair_address, abi=pancakeswap_pair_abi)
    return pair_contract.functions.isStable().call()


#approved_tokens = {"0xc2741FB2B16DC6B0690DB833B984d20d7e56119a"}  # BNB address
BNB_ADDRESS= '0x87B873224EaD2a8cbBB7CfB39b18a795e7DA8CC7' # wIOTX as address
MAX_UINT256 = 2**255 - 1

def is_token_approved(token_address, spender_address, owner_address):
    token_contract = w3.eth.contract(address=token_address, abi=token_abi)
    allowance = token_contract.functions.allowance(owner_address, spender_address).call()
    print(f"Allowance for token {token_address}: {allowance}")  # Debug print
    return allowance > 0

def approve_max_token(owner_address, token_address, spender_address, nonce):
    token_contract = w3.eth.contract(address=token_address, abi=token_abi)

    allowance = token_contract.functions.allowance(owner_address, spender_address).call()
    if allowance < MAX_UINT256:
        txn = token_contract.functions.approve(spender_address, MAX_UINT256).build_transaction({
            'chainId': 4690,
            'gas': 50000,  # Adjust if needed
            'gasPrice': w3.eth.gas_price,
            'nonce': nonce,
        })

        signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
        txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
        if receipt.status == 1:
            print(f"Approval for token {token_address} successful.")
        else:
            print("Token approval failed.")
        nonce += 1

    return nonce

def execute_single_swap(token_in, token_out, amount_in, nonce, route):
    router_contract = w3.eth.contract(address=pancakeswap_router_address, abi=pancakeswap_router_abi)

    if token_in == BNB_ADDRESS or token_out == BNB_ADDRESS:
        if not is_token_approved(token_in, pancakeswap_router_address, account_address):
            print("Token not yet approved, approving now...")
            nonce = approve_max_token(account_address, token_in, pancakeswap_router_address, nonce)

    deadline = int(time.time()) + 300  # current time + 5 minutes

    # Transform the route to the required format
    transformed_route = []
    for i in range(len(route) - 1):
        pair_address = get_pair_address(route[i], route[i+1], filtered_pairs)
        is_stable = check_if_pair_is_stable(pair_address)
        transformed_route.append((route[i], route[i+1], is_stable))

    # Calculate an estimated amount_out_minimum, allowing for a 3% transfer fee
    amount_out_minimum = 0

    estimated_gas = router_contract.functions.swapExactTokensForTokens(
        amount_in,
        amount_out_minimum,
        transformed_route,  # Use the transformed route here
        account_address,
        deadline
    ).estimate_gas({
        'from': account_address,
        'value': 0,
        'gasPrice': w3.eth.gas_price,
    })

    txn = router_contract.functions.swapExactTokensForTokens(
        amount_in,
        amount_out_minimum,
        transformed_route,  # Use the transformed route here
        account_address,
        deadline
    ).build_transaction({
        'chainId': 4690,
        'gas': estimated_gas,
        'gasPrice': w3.eth.gas_price,
        'nonce': nonce,
    })

    # Sign and send the transaction
    signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
    txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print(f"Swap initiated with transaction hash: {txn_hash.hex()}")  # Debug print

    return txn_hash, nonce + 1


def execute_arb_trade(route):
    # Ensure the route is circular by adding the starting token to the end

    initial_amount = 0.5  # Example starting amount

    final_amount = circular_swap(route, initial_amount)

    if final_amount > initial_amount:
        profit = final_amount - initial_amount
        print(f"Arbitrage successful! Profit: {profit} ETH")
    else:
        print("Arbitrage trade was not profitable.")


def circular_swap(route, amount_in, start_nonce=None):
    if start_nonce is None:
        start_nonce = w3.eth.get_transaction_count(account_address, 'pending')

    current_token = route[0]
    nonce = start_nonce

    # Convert amount_in to integer (wei)
    amount_in_wei = int(amount_in * 1e18)

    # Only need to swap once since the entire route is swapped in a single transaction
    token_in = route[0]
    token_out = route[-1]

    print(f"---- Swap Step 1 ----")
    print(f"Expected Token IN: {token_in}")
    print(f"Expected Token OUT: {token_out}")
    print(f"Current Amount IN: {amount_in_wei}")

    print(f"Swapping {token_in} to {token_out}...")
    txn_hash, nonce = execute_single_swap(token_in, token_out, amount_in_wei, nonce, route)

    # For now, just return the initial amount_in as the final amount.
    # You will need to replace this with a more accurate estimate of the amount received.
    final_amount = amount_in

    print(f"Amount after swap: {final_amount}")

    return final_amount



def get_slippage(amount_to_buy, reserve_in, reserve_out):
    # Perfect Exchange (PE): This would be the amount of tokens we expect to receive if there was no slippage.
    # For a Uniswap pool, this is simply the ratio of the reserves.
    perfect_exchange = reserve_out / reserve_in * amount_to_buy
    # Actual Exchange (AE): This is the amount of tokens we will actually receive.
    # This is calculated using the Uniswap formula.
    r = 0.997  # fee factor
    actual_exchange = r * amount_to_buy * reserve_out / (reserve_in + r * amount_to_buy)
    # Slippage = (PE - AE) / PE
    slippage = (perfect_exchange - actual_exchange) / perfect_exchange
    return slippage

def find_arb(pairs, token_in, token_out, max_hops, current_pairs, path, best_trades, count=5, max_slippage=0.01, visited_tokens=set()):
    for pair in pairs:
        newPath = path.copy()

        if token_in not in pair:
            continue

        if len(newPath) == 2 and token_in == newPath[0]:
            continue

        reserve_A, reserve_B = get_reserves(pair[3], pair[0], pair[1])

        if reserve_A < 0 or reserve_B < 0:
            continue

        next_tokens = [pair[1] if token_in != pair[1] else pair[0]]

        for temp_out in next_tokens:
            if temp_out in visited_tokens:
                continue

            newPath.append(temp_out)

            if len(newPath) == 3 and newPath[0] == newPath[2]:
                continue

            if token_in == pair[0]:
                reserve_in = reserve_A
                reserve_out = reserve_B
            else:
                reserve_in = reserve_B
                reserve_out = reserve_A

            if temp_out == token_out and len(newPath) > 2:
                current_pairs += [(pair[0], pair[1], pair[3], reserve_in, reserve_out)]
                starting_amount = 10
                amount_in = starting_amount
                print(f"Starting amount for path {newPath}: {starting_amount} ETH")

                for j in range(len(newPath) - 1):
                    token_A = newPath[j]
                    token_B = newPath[j+1]

                    for p in current_pairs:
                        if (p[0] == token_A and p[1] == token_B) or (p[1] == token_A and p[0] == token_B):
                            reserve_A, reserve_B = p[3], p[4]
                            pair_address = p[2]
                            break

                    amount_out = get_amount_out(pair_address, token_A, token_B, amount_in)
                    print(f"Swap from {token_A} to {token_B}: Starting with {amount_in}, after swap got {amount_out}")
                    amount_in = amount_out

                print(f"Ending amount for path {newPath}: {amount_in} ETH")

                while amount_in > starting_amount:
                    profit = amount_in - starting_amount
                    new_trade = {
                        'profit': profit,
                        'route': newPath
                    }
                    best_trades.append(new_trade)
                    print(f"Profitable trade found: {new_trade}")
                    execute_arb_trade(newPath)

                    # Re-calculate the amount out for the same path
                    amount_in = starting_amount
                    for j in range(len(newPath) - 1):
                        token_A = newPath[j]
                        token_B = newPath[j+1]

                        for p in current_pairs:
                            if (p[0] == token_A and p[1] == token_B) or (p[1] == token_A and p[0] == token_B):
                                reserve_A, reserve_B = p[3], p[4]
                                pair_address = p[2]
                                break

                        amount_out = get_amount_out(pair_address, token_A, token_B, amount_in)
                        amount_in = amount_out

                    print(f"Rechecking amount for path {newPath}: {amount_in} ETH")

                print(f"Trade no longer profitable on path {newPath}")
                continue
            elif max_hops > 1:
                visited_tokens.add(temp_out)
                best_trades = find_arb(pairs, temp_out, token_out, max_hops - 1, current_pairs + [(pair[0], pair[1], pair[3], reserve_in, reserve_out)], newPath.copy(), best_trades, count, max_slippage, visited_tokens)
                visited_tokens.remove(temp_out)

    return best_trades



def get_token_order(tokenA_address, tokenB_address):
    if tokenA_address < tokenB_address:
        return "tokenA", "tokenB"  # tokenA is Token 0 and tokenB is Token 1
    else:
        return "tokenB", "tokenA"  # tokenB is Token 0 and tokenA is Token 1


def get_sqrt_price(pair_address, tokenA_address=None, tokenB_address=None):
    slot0_abi = [{
        "constant": True,
        "inputs": [],
        "name": "slot0",
        "outputs": [
            {"name": "sqrtPriceX96", "type": "uint160"},
            # ... (other outputs if any)
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    }]

    pair_contract = w3.eth.contract(address=pair_address, abi=slot0_abi)

    # Fetch the sqrtPriceX96
    print(f"Fetching sqrtPriceX96 from pair: {pair_address}")
    result = pair_contract.functions.slot0().call()
    print(f"Result from slot0: {result}")

    # Check if result is a tuple or list and extract sqrtPriceX96
    if isinstance(result, (list, tuple)) and len(result) > 0:
        sqrt_price = result[0]
    elif isinstance(result, int):
        sqrt_price = result
    else:
        print(f"Unexpected result format from slot0: {result}")
        return None

    return sqrt_price


def get_uniswap_version(pair_address, tokenA_address=None, tokenB_address=None):
    slot0_abi = [{
        "constant": True,
        "inputs": [],
        "name": "slot0",
        "outputs": [
            {"name": "sqrtPriceX96", "type": "uint160"},
            # ... other outputs
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    }]

    print(f"Using pair_address: {pair_address}")
    pair_contract = w3.eth.contract(address=pair_address, abi=slot0_abi)  # Using slot0 ABI
    try:
        pair_contract.functions.slot0().call()
        return "V3"
    except Exception as e:
        print(f"Error when calling slot0 on {pair_address}: {e}")
        return "V2"

def get_current_price(pair_address, tokenA_address, tokenB_address):
    version = get_uniswap_version(pair_address)

    if version == "V3":
        sqrt_price_x96 = get_sqrt_price(pair_address)
        price = (sqrt_price_x96 ** 2) / (2 ** 192)
        return price
    else:
        # For V2, calculate price from reserves
        reserveA, reserveB = get_reserves(pair_address, tokenA_address, tokenB_address)

        # Depending on the order of tokens in the pair, adjust the price calculation
        token_order_A, token_order_B = get_token_order(tokenA_address, tokenB_address)

        if token_order_A == "tokenA":
            price = reserveB / reserveA
        else:
            price = reserveA / reserveB

        return price

def adjust_precision(value, decimals):
    return int(value * (10 ** (18 - decimals)))

def get_token_decimals(token_address):
    # Fetching token decimals from the token's contract
    token_contract = w3.eth.contract(address=token_address, abi=token_abi)
    return token_contract.functions.decimals().call()

q96 = 2**96
eth = 10**18

def price_to_tick(p):
    tick = math.floor(math.log(p, 1.0001))
    print(f"price_to_tick: p={p}, tick={tick}")
    return tick

def price_to_sqrtp(p):
    sqrtp = int(math.sqrt(p) * q96)
    print(f"price_to_sqrtp: p={p}, sqrtp={sqrtp}")
    return sqrtp

def sqrtp_to_price(sqrtp):
    price = (sqrtp / q96) ** 2
    print(f"sqrtp_to_price: sqrtp={sqrtp}, price={price}")
    return price

def calc_amount0(liq, pa, pb):
    if pa > pb:
        pa, pb = pb, pa
    amount = int(liq * q96 * (pb - pa) / pb / pa)
    print(f"calc_amount0: liq={liq}, pa={pa}, pb={pb}, amount={amount}")
    return amount

def calc_amount1(liq, pa, pb):
    if pa > pb:
        pa, pb = pb, pa
    amount = int(liq * (pb - pa) / q96)
    print(f"calc_amount1: liq={liq}, pa={pa}, pb={pb}, amount={amount}")
    return amount

def liquidity(pair_address):
    liquidity_abi = [
      {
          "constant": True,
          "inputs": [],
          "name": "liquidity",
          "outputs": [{"name": "", "type": "uint128"}],
          "payable": False,
          "stateMutability": "view",
          "type": "function",
      }
  ]
    pair_contract = w3.eth.contract(address=pair_address, abi=liquidity_abi)
    return pair_contract.functions.liquidity().call()

def get_amount_out(pair_address, token_in_address, token_out_address, amount_in):
    version = get_uniswap_version(pair_address)
    token_in_reserve, token_out_reserve = get_reserves(pair_address, token_in_address, token_out_address)
    r = 0.997
    # Adjusting precision
    token_in_decimals = get_token_decimals(token_in_address)
    token_out_decimals = get_token_decimals(token_out_address)
#    token_in_reserve = adjust_precision(token_in_reserve, token_in_decimals)
#    token_out_reserve = adjust_precision(token_out_reserve, token_out_decimals)

    if version == "V3":
        sqrtp_cur = get_sqrt_price(pair_address, token_in_address, token_out_address)

        # Determine which token is token0 and which is token1 for internal V3 calculations
        is_token_in_token0 = token_in_address < token_out_address

        # Multiplying amount_in by token's decimals
        amount_in = amount_in * (10 ** token_in_decimals)

        # Fetch liquidity directly from the pair
        liq = liquidity(pair_address)

        # Step 1: Calculate sqrtP_target
        if is_token_in_token0:
            price_next = int((liq * q96 * sqrtp_cur) // (liq * q96 + r*amount_in * sqrtp_cur))
        else:
            price_next = int(sqrtp_cur + (r*amount_in * q96) // liq)
        # Step 2: Determine the new price
        new_price = (price_next / q96) ** 2

        # Step 3: Compute the token amounts for the swap
        if is_token_in_token0:
            amount_out = calc_amount1(liq, price_next, sqrtp_cur)
        else:
            amount_out = calc_amount0(liq, price_next, sqrtp_cur)


        return amount_out / eth
    else:
        reserve_in = token_in_reserve
        reserve_out = token_out_reserve
        K = reserve_in * reserve_out
        amount_out_v2 = reserve_out - (K / (reserve_in + r * amount_in))
        return amount_out_v2

def main():
    while True:
        # Run the function / LOXO : 0x89c3A24FF5cE28385e7a09646A105E8fc3E66CBd
        token_in = '0x87B873224EaD2a8cbBB7CfB39b18a795e7DA8CC7'
        token_out = '0x87B873224EaD2a8cbBB7CfB39b18a795e7DA8CC7'
        max_hops = 4
        current_pairs = []
        path = [token_in]
        best_trades = []

        best_trades = find_arb(filtered_pairs, token_in, token_out, max_hops, current_pairs, path, best_trades)
        print(best_trades)

        # If there are arbitrage opportunities, execute the best one
        if best_trades:
            # Extract the best arbitrage opportunity
            best_arb_opportunity = max(best_trades, key=lambda x: x['profit'])

            # Check if the route starts with the defined token_in
            if best_arb_opportunity['route'][0][0] == token_in:
                circular_swap(best_arb_opportunity, nonce)
            else:
                print("The best arbitrage opportunity does not start with the defined token_in.")

        # Sleep for a set amount of time before running again
        time.sleep(6)  # Sleep for 10 minutes. You can adjust this interval as needed.

if __name__ == "__main__":
    main()