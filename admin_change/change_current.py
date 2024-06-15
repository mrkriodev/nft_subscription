
import json
import aiofiles
from interface import *

async def update_attributes(nft_item_address: str, new_item_counter: int, client_tc: ToncenterClient):


    to_change_data: json = [{"trait_type": "AvailableTokenChecks", "value": f"{new_item_counter}"}]

    with open('./data/updated_items_attributes.json', mode='r+') as file: file.truncate(0)

    async with aiofiles.open('./data/updated_items_attributes.json', mode='a') as file:
        data = await chnage_single_item_attributes(client_tc=client_tc, to_change_data=to_change_data, item_address=nft_item_address)
        data_json = "[" + json.dumps(data) + "]"
        await file.write(data_json)
        

async def do(nft_item_address: str, new_item_counter: int):
    client_tc = ToncenterClient(base_url=BASE_URL, api_key=TON_CENTER_API_KEY)
    wallet_tc = await async_init()  

    wallet_address = get_wallet_addred(wallet=wallet_tc)

    await update_attributes(nft_item_address, new_item_counter, client_tc=client_tc)

    print("[WALLET ADDRESS] -->", wallet_address)
    
    tokens_json: str = ""
    with open('./data/updated_items_attributes.json', mode='r', encoding="utf-8") as file:
        tokens_json = json.loads(file.read())

    wallet_seqno = await get_wallet_seqno(wallet=wallet_tc, client=client_tc)

    tonsdk_change_attributes_cell: TonSdkCell = TonSdkCell()
    tonsdk_change_attributes_cell = serealize_change_attributes_mwssage(new_item_counter, tonsdk_change_attributes_cell, tokens_json[0]['attributes'])

    print("\n--------------NEW ITEM ATTRIBUTES----------------")
    print(tokens_json[0]['attributes'])
    print("--------------------------------------------\n")

    print("[TOKEN ADDRESS IN PROCCESS] -->", tokens_json[0]['address'])
    await send_payload_to_adr(wallet=wallet_tc, 
                            client=client_tc, 
                            current_seqno=wallet_seqno,
                            payload=tonsdk_change_attributes_cell, 
                            address=tokens_json[0]['address'], 
                            forward_ton_amont=0.01)
    
    print(f"item attributes have been successfully changed\n")