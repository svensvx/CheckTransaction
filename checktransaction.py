import subprocess
import ast
from decimal import *


def txallinfo(txids):
    # Variables
    outputs_value = []
    sumoutputs = 0
    input_txids = []
    input_vouts = []
    input_value = []
    outputadresses = []
    suminput = 0
    getcontext().prec = 7

    txinfo = subprocess.getoutput("bitcoin-cli getrawtransaction " + txids + " 1")
    txinfo_d = ast.literal_eval(txinfo)
    vsize = txinfo_d["vsize"]

    # Printing TX information
    print("Transaction ID: ", txinfo_d["txid"])
    if "confirmations" in txinfo_d:
        print("Included in Block: ", txinfo_d["blockhash"])
        print("Number of confirmations: ", txinfo_d["confirmations"])
    else:
        print("Transaction is unconfirmed")

    # Getting outputTX addresses and values
    print("")
    output_vouts = (txinfo_d["vout"])
    for outputs in range(len(output_vouts)):
        specific_output = (output_vouts[outputs])
        scriptpubkey_info = specific_output["scriptPubKey"]
        if "addresses" in scriptpubkey_info:
            outputadresses.append(scriptpubkey_info["addresses"])
            outputs_value.append((specific_output["value"]))
            sumoutputs = sumoutputs + float((specific_output["value"]))
        else:
            outputadresses.append("OP_RETURN")
            outputs_value.append(int(0))
    # Lists with input txids and vouts
    input_info = (txinfo_d["vin"])
    for inputs in range(len(input_info)):
        specific_input = input_info[inputs]
        input_txids.append(specific_input["txid"])
        input_vouts.append(specific_input["vout"])
    # Value of input tx
    for l in range(len(input_txids)):
        input_id = input_txids[l]
        inputinfo = subprocess.getoutput("bitcoin-cli getrawtransaction " + input_id + " 1")
        inputinfo_d = ast.literal_eval(inputinfo)
        input_value.append(inputinfo_d["vout"][input_vouts[l]]["value"])

    # Printing inputTX Values
    print("Input:")
    for transactionnumber in range(len(input_txids)):
        print(transactionnumber, "TxID: ", input_txids[transactionnumber], ": ", round((input_value[transactionnumber]), 8), " BTC")
        suminput = suminput + input_value[transactionnumber]

    # Calculating and printing fees
    fees = round(Decimal(suminput) - Decimal(sumoutputs), 8)
    feessats = fees * 100000000
    feesperbyte = round((feessats / vsize), 1)
    print("")
    print("Fees: ", fees, "BTC / ", feesperbyte, "sats/vbyte")
    print("")

    # Printing output information
    print("Output: ")
    for numberofoutputs in range(len(outputs_value)):
        outputadresses2 = str(outputadresses[numberofoutputs]).replace("['", "")
        outputadresses3 = outputadresses2.replace("']", "")
        if outputs_value[numberofoutputs] == 0:
            print(numberofoutputs, "Address: ", outputadresses3, ": ", "0 BTC")
        else:
            print(numberofoutputs, "Address: ", outputadresses3, ": ", round((outputs_value[numberofoutputs]), 8), " BTC")
    print("")


def gettxfromaddress(address):
    tx_for_address = []
    address_input = str("[\'") + address + str("\']")
    rawmempool = (subprocess.getoutput("bitcoin-cli getrawmempool"))
    rawmempool_d = rawmempool.replace('"', '')
    rawmempool_d2 = rawmempool_d.replace(',', '')
    rawmempool_d3 = rawmempool_d2.replace(']', '')
    rawmempool_d4 = rawmempool_d3.replace('[', '')
    rawmempool_l = rawmempool_d4.split()
    print("Searching in mempool...")
    for txnumber in range(len(rawmempool_l)):
        txid = rawmempool_l[txnumber]
        txinfo = subprocess.getoutput("bitcoin-cli getrawtransaction " + txid + " 1")
        txinfo_dict = ast.literal_eval(txinfo)
        output_vouts = (txinfo_dict["vout"])
        for outputs in range(len(output_vouts)):
            scriptpubkey_info = output_vouts[outputs]["scriptPubKey"]
            if "addresses" in scriptpubkey_info:
                if str(scriptpubkey_info["addresses"]) == address_input:
                    tx_for_address.append(txid)
                    print("Found a transaction")
    return tx_for_address


txoraddress = input("Enter Transaction ID (or Address if in Mempool): ")
if len(txoraddress) > 50:
    txallinfo(txoraddress)
else:
    tx_for_address2 = gettxfromaddress(txoraddress)
    for txidnum in range(len(tx_for_address2)):
        newtx = tx_for_address2[txidnum]
        print("")
        print("Transaction Nr.", txidnum+1)
        print("___________________")
        print("")
        txallinfo(newtx)
        print("######################################################################################")
