
import asyncio
import change_current
import get_counter_value

new_item_counter: int = 10
nft_item_address: str = "EQAiNrvSfgRQ3NbhSFocTvLC4qedPAu5fCQygTfxcV76uhu4"

if __name__ == "__main__":
    asyncio.run(change_current.do(nft_item_address, new_item_counter))
    # asyncio.run(get_counter_value.do(nft_item_address))

