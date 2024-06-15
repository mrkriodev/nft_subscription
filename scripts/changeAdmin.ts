import { Address, toNano } from '@ton/core';
import { NetworkProvider } from '@ton/blueprint';
import { NftItem } from '../wrappers/NftItem';

export async function run(provider: NetworkProvider) {
    const nftItem = provider.open(NftItem.createFromAddress(Address.parse("")));
    await nftItem.sendChangeAdmin(provider.sender(), {
        value: toNano("0.05"),
        queryId: Math.floor(Date.now() / 1000),
        newAdminAddress: Address.parse("")
    });
}