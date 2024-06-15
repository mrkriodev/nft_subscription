import { Address, Cell, DictionaryValue, beginCell } from "@ton/core";

export type CollectionMint = {
    amount: bigint;
    index: number;
    ownerAddress: Address;
    content: Cell;
    defaultContent: Cell;
    defaultAttributes: Cell;
    adminAddress: Address;
    itemCounter: number

}

export const MintValue: DictionaryValue<CollectionMint> = {
    serialize(src, builder) {
        const nftMessage = beginCell();
        nftMessage.storeAddress(src.ownerAddress)
        nftMessage.storeRef(src.content)
        nftMessage.storeRef(src.defaultContent)
        nftMessage.storeRef(src.defaultAttributes)
        nftMessage.storeAddress(src.adminAddress)
        nftMessage.storeUint(src.itemCounter, 16)


        builder.storeCoins(src.amount);
        builder.storeRef(nftMessage);
    },

    parse(src) {
        return {
            amount: src.loadCoins(),
            index: src.loadUint(64),
            ownerAddress: src.loadAddress(),
            content: src.loadRef(),
            defaultContent: src.loadRef(),
            defaultAttributes: src.loadRef(),
            adminAddress: src.loadAddress(),
            itemCounter: src.loadUint(8)
        }
    }
};