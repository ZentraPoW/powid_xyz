
let CHAIN_ID;
let CHAIN_NAME;
let PURCHASE_CONTRACT;
let POWID_CONTRACT;
let USDT_CONTRACT;
let RPC_URL;
let INDEXER_HOST;

if(window.location.hostname == 'test.powid.xyz'){
  CHAIN_ID = '0xa';
  CHAIN_NAME = 'OP';
  PURCHASE_CONTRACT = '0x7CdFB1fbf7d4E314E6c54577781DC7A7B00f2C9d'; // USDT Purchase
  // PURCHASE_CONTRACT = '0xaEa9a28e079CcFD6Be1AB999395265d42cdE315F'; // old PoWIDPurchase
  POWID_CONTRACT = '0xa8691bEaEE825Ace9F620Bed657Fa742Db134892';
  USDT_CONTRACT = '0x94b008aA00579c1307B0EF2c499aD98a8ce58e58'; // USDT on OP
  RPC_URL = 'https://mainnet.optimism.io';
  INDEXER_HOST = 'https://testindexer.zentra.dev';
}else{
  CHAIN_ID = '0x7a69';
  CHAIN_NAME = 'Hardhat';
  PURCHASE_CONTRACT = '0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0'; // Mock Purchase on harthat 
  USDT_CONTRACT = '0x5FbDB2315678afecb367f032d93F642f64180aa3'; // Mock USDT on harthat
  RPC_URL = 'http://127.0.0.1:8545';
  INDEXER_HOST = 'http://127.0.0.1:8090';
}


const HANDLE_LETTERS = 'abcdefghijklmnopqrstuvwxyz0123456789_';

const PURCHASE_ABI = [
  "function purchase(bytes memory _handle) public",
  "function available(bytes memory _handle) public view returns (uint256)"
];

const USDT_ABI = [
  "function allowance(address owner, address spender) external view returns (uint256)",
  "function approve(address spender, uint256 value) external returns (bool)",
  "function transferFrom(address from, address to, uint256 value) external returns (bool)",
  "function decimals() view returns (string)",
  "function symbol() view returns (string)",
  "function balanceOf(address addr) view returns (uint)"
];

export {
  CHAIN_ID,
  CHAIN_NAME,
  PURCHASE_CONTRACT,
  POWID_CONTRACT,
  USDT_CONTRACT,
  RPC_URL,
  INDEXER_HOST,
  HANDLE_LETTERS,
  PURCHASE_ABI,
  USDT_ABI,
}