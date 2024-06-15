import { Address } from '@ton/core';
import { NetworkProvider } from '@ton/blueprint';
import { NftItem } from '../wrappers/NftItem';

export async function run(provider: NetworkProvider) {
    const nftItem = provider.open(NftItem.createFromAddress(Address.parse("EQB8u2kaKlGCVY9Y0_lbxIYC0TT-a0l6cT_mEmyDMlLEl9Pq")));
    const result: Address = await nftItem.getAdminAddress();
    console.log("[ADMIN ADRESS] -->", result);
}