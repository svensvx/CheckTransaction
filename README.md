# CheckTransaction
This is a python tool for getting information about a transaction from your own full node. 

The advantage compared to other Blockexploerer tools is the ease of use. You don't have to install 
anything and don't have to change anything in the bitcoin.conf file to grant remote access (JSON-RPC). Because of this the functionality is heavily limited though.

## How to use
You input a Transaction-ID and the output displays:
- Transaction unconfirmed or confirmed (amount of confirmations)
- Input TxIDs and amounts
- Total fees and sats per vbyte
- Output addresses and amounts

This also works with addresses as input if they are still in the mempool. Otherwise the search space is to big.

## How it works

This tool mostly uses
```sh
bitcoin-cli getrawtransaction
```
and displays the important information easy to read.
 
This is really inefficient (especially when searching) but has the above mentioned advantage of no setup.
