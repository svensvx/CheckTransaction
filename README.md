# CheckTransaction
This is a python tool for getting information about a transaction from your own full node. 

The advantage compared to other Blockexplorer tools is the ease of use. There is no setup process.

## How to use
Navigate into the folde and run
```sh
python3 checktransaction.py
```
You input a Transaction-ID and the output displays:
- Transaction unconfirmed or confirmed (amount of confirmations)
- Input TxIDs and amounts
- Total fees and sats per vbyte
- Output addresses and amounts

This also works with addresses as input if the transaction is still in the mempool. Otherwise the search space is to big.

## How it works

This tool mostly uses
```sh
bitcoin-cli getrawtransaction
```
 
This is really inefficient (especially when searching for addresses), but has the above mentioned advantage of no setup.
