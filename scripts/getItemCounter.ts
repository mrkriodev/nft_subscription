import { Address } from '@ton/core';
import { NetworkProvider } from '@ton/blueprint';
import { NftItem } from '../wrappers/NftItem';

export async function run(provider: NetworkProvider) {
    const nftItem = provider.open(NftItem.createFromAddress(Address.parse("EQCKIMho4jLDIcEEjtTc5WyBkl5pqh6UuqZuIchNGHzV3KaQ")));
    const result: number = await nftItem.getNftItemCounter();
    console.log("[ITEM COUNTER] -->", result);
}