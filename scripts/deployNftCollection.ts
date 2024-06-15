import { Address, toNano } from '@ton/core';
import { NftCollection } from '../wrappers/NftCollection';
import { compile, NetworkProvider } from '@ton/blueprint';
import { buildCollectionContentCell } from './nftContent/onChain';

const collection_name = "tс_shard_ai";
const collection_description = "tс_shard_ai";
const collection_image_uri = "https://raw.githubusercontent.com/mrkriodev/tc_hackaton/main/image.png";

export async function run(provider: NetworkProvider) {
    
    const nftCollection = provider.open(NftCollection.createFromConfig({
        ownerAddress: provider.sender().address as Address, 
        nextItemIndex: 0,
        collectionContent: buildCollectionContentCell({
            name: collection_name,
            description: collection_description,
            image: collection_image_uri,
        }),
        nftItemCode: await compile("NftItem"),
        royaltyParams: {
            royaltyFactor: 20, 
            royaltyBase: 100,
            royaltyAddress: provider.sender().address as Address
        }
    }, await compile('NftCollection')));
    console.log(provider.sender().address as Address)
    await nftCollection.sendDeploy(provider.sender(), toNano('0.05'));
    console.log()
    await provider.waitForDeploy(nftCollection.address);

    console.log(`NFT Collection deployed at <https://testnet.tonviewer.com/${nftCollection.address}>`);
}