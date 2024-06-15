
from interface import *


async def do(nft_item_address: str):
    client_tc = ToncenterClient(base_url=BASE_URL, api_key=TON_CENTER_API_KEY)
    wallet_tc = await async_init()  
    wallet_address = get_wallet_addred(wallet=wallet_tc)

    jetton_minter_data = client_tc.raw_run_method(address=nft_item_address, method='get_counter', stack_data=[])
    jetton_minter_data_result = await execute(to_run=jetton_minter_data)
    b64_bytes_str_content = jetton_minter_data_result[0].get('stack')[0][1]

    counter: int = int(b64_bytes_str_content, 16)
    print("[COUNTER] -->", counter)