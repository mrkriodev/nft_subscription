
import json
import random
import hashlib
import aiohttp
import asyncio
from pytoniq_core.boc import Slice
from tonsdk.utils import b64str_to_bytes
from tonsdk.boc import Cell as TonSdkCell
from tonsdk.provider import ToncenterClient
from tonsdk.utils import Address as TonSdkAddress
from tonsdk.contract.wallet import WalletVersionEnum, Wallets


# TESTNET
# from networks.testnet import *

# MAINNET
from networks.mainnet import *

def sha256_hash(text):
    sha256 = hashlib.sha256()
    sha256.update(text.encode('utf-8'))
    hex_digest = sha256.hexdigest()
    int_digest = int(hex_digest, 16)
    return int_digest

async def async_init():
    try:
        _, _, _, wallet = Wallets.from_mnemonics(WALLET_MNEMONIC, WalletVersionEnum.v4r2, 0)
        return wallet
    except Exception as error:
         print(error)

def get_wallet_addred(wallet):
    return wallet.address.to_string(True, True, True)

async def execute(to_run: dict, single_query=True):
    timeout = aiohttp.ClientTimeout(total=30)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        if single_query:
            to_run = [to_run]
        tasks = []
        for task in to_run:
            tasks.append(task["func"](session, *task["args"], **task["kwargs"]))

        return await asyncio.gather(*tasks, return_exceptions=True)

async def get_wallet_seqno(wallet, client):
    cur_adr_seq_no_task = client.raw_run_method(wallet.address.to_string(), 'seqno', [])
    cur_adr_seq_result = await execute(to_run=cur_adr_seq_no_task)
    cur_seq_no = int(cur_adr_seq_result[0].get('stack')[0][1], 16)
    return cur_seq_no

async def send_payload_to_adr(wallet, client, current_seqno: int, payload: TonSdkCell, address: str, forward_ton_amont: int = 0):
    transfer_query = wallet.create_transfer_message(
        to_addr=TonSdkAddress(address).to_string(),
        seqno=current_seqno,
        amount=(int(10**9) * forward_ton_amont),
        payload=payload
    )
    transfer_boc = transfer_query['message'].to_boc(False)
    transfer_task = client.raw_send_message(transfer_boc)
    transfer_result = await execute(to_run=transfer_task)

    print(f"[CURRENT SEQNO] --> {current_seqno}, [WAITING FOR {current_seqno + 1} SEQNO]")
    while await get_wallet_seqno(wallet=wallet, client=client) == current_seqno:
        await asyncio.sleep(1)

    print("[TRANSACTION CONFIRMED]")
    # print(f"[TRANSACTION CONFIRMED]\n[TRANSFER RESULT] --> {transfer_result}")

def store_snake_string(ton_sdk_cell: TonSdkCell, string: str, chunk_size: int = 127) -> TonSdkCell:
    max_size: int = chunk_size
    if (len(string) <= max_size):
        ton_sdk_cell.bits.write_bytes(bytes(string, encoding="utf-8"))
        return ton_sdk_cell
    
    total_length = len(string)
    current_index = 0
    current_cell: TonSdkCell = ton_sdk_cell
    while current_index < total_length:
        chunk = string[current_index:current_index + max_size]
        if current_index == 0:
            current_cell.bits.write_bytes(bytes(chunk, encoding="utf-8"))
        else:
            new_inner_cell: TonSdkCell = TonSdkCell()
            new_inner_cell.bits.write_bytes(bytes(chunk, encoding="utf-8"))
            current_cell.refs.append(new_inner_cell)
            current_cell = new_inner_cell
        current_index += max_size
    return ton_sdk_cell

def to_text_cell(string: str, chunk_size: int = 127) -> TonSdkCell:
    text_cell: TonSdkCell = TonSdkCell()
    text_cell.bits.write_uint(0, 8)
    text_cell = store_snake_string(text_cell, string, chunk_size=chunk_size)
    return text_cell


def serealize_change_attributes_mwssage(new_item_counter: int, tonsdk_change_attributes_cell: TonSdkCell, updated_attributes: str) -> TonSdkCell:
    tonsdk_change_attributes_cell.bits.write_uint(63355, 32) # Change Attributes operation code
    tonsdk_change_attributes_cell.bits.write_uint(random.randint(1, 10**9), 64)
    tonsdk_change_attributes_cell.bits.write_uint(new_item_counter, 16)
    tonsdk_change_attributes_cell.bits.write_uint(sha256_hash("attributes"), 256)
    tonsdk_change_attributes_cell.refs.append(to_text_cell(updated_attributes))
    inner_cell: TonSdkCell = TonSdkCell()
    inner_cell = store_snake_string(inner_cell, updated_attributes)
    tonsdk_change_attributes_cell.refs.append(inner_cell)
    return tonsdk_change_attributes_cell

async def chnage_single_item_attributes(client_tc: ToncenterClient, to_change_data: str, item_address: str):
    to_change_data = str(to_change_data).replace("\n", "").replace("'", '"')
    json_to_change_data = json.loads(to_change_data)

    default_content_data = client_tc.raw_run_method(address=item_address, method='get_default_attributes', stack_data=[])
    default_content_result = await execute(to_run=default_content_data)
    b64_bytes_str = default_content_result[0].get('stack')[0][1].get('bytes')
    default_attributes = Slice.one_from_boc(b64str_to_bytes(b64_bytes_str)).load_snake_string()

    json_default_attributes = json.loads(str(default_attributes).replace("\n", "").replace("'", '"'))
    
    for iter in range(0, len(json_to_change_data)):
        for jter in range(0, len(json_default_attributes)):
            if(json_default_attributes[jter]["trait_type"] == json_to_change_data[iter]["trait_type"]):
                json_default_attributes[jter]["value"] = json_to_change_data[iter]["value"]
    
    return {"address": item_address, "attributes": str(json_default_attributes)}