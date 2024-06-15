
import { Address, beginCell, toNano } from '@ton/core';
import { NftCollection } from '../wrappers/NftCollection';
import { NetworkProvider } from '@ton/blueprint';
import { setItemContentCell, setItemDefaultContentCell } from './nftContent/onChain';
import { CollectionMint } from '../wrappers/helpers/CollectionHelpers';

const item_description = `tс_shard_ai`;
const item_image_uri = "https://raw.githubusercontent.com/mrkriodev/tc_hackaton/main/image.png";
const item_counter = 10;

const item_attributes = 
`
[
    {
        "trait_type": "AvailableTokenChecks",
        "value": "${item_counter}"
    }
]
`;


function construct_item(provider: NetworkProvider, item_index: number, item_name: string) {

    let item: CollectionMint = {
        amount: toNano("0.01"),
        index: item_index,
        ownerAddress: provider.sender().address as Address,

        defaultContent: setItemDefaultContentCell( {
            name: item_name,
            description: item_description, 
            image: item_image_uri,
        }),

        content: setItemContentCell({
            name: item_name,
            description: item_description, 
            image: item_image_uri,
            attributes: item_attributes
        }),

        defaultAttributes: beginCell().storeStringTail(item_attributes).endCell(),
        adminAddress: provider.sender().address as Address,
        itemCounter: 10
    }

    return item;
}

export async function run(provider: NetworkProvider) {

    const address = Address.parse("EQDnFZrOgD8YigoupcM2SAjd_0e97kFmrrN-E-PYYJjdnkkJ"); // Collection address here
    const nftCollection = provider.open(NftCollection.createFromAddress(address));


    let items_array: CollectionMint[] = [];


    for (let iter: number = 0; iter < 10; iter++) {
        let current_item = construct_item(provider, iter, `tс_shard_ai #${iter + 1}`)
        items_array.push(current_item);
    }
    
    await nftCollection.sendBatchMint(provider.sender(), {
        value: toNano('0.8'),
        queryId: Date.now(),
        nfts: items_array
    });
}