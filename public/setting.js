
let CHAIN_ID;
let CHAIN_NAME;
let PURCHASE_CONTRACT;
let PURCHASE_REFERRAL_CONTRACT;
let POWID_CONTRACT;
let USDT_CONTRACT;
let RPC_URL;
let INDEXER_HOST;
let SUBMIT_HOST;
let REFERRAL_PREFIX;

if(window.location.hostname == 'test.powid.xyz'){
  CHAIN_ID = '0xa';
  CHAIN_NAME = 'OP';
  PURCHASE_CONTRACT = '0xf3277Ecd65450BeFe656961B9Bfa25c3f1933EDB'; // USDT Purchase
  // PURCHASE_CONTRACT = '0x7CdFB1fbf7d4E314E6c54577781DC7A7B00f2C9d'; // test USDT Purchase
  // PURCHASE_CONTRACT = '0xaEa9a28e079CcFD6Be1AB999395265d42cdE315F'; // old PoWIDPurchase
  PURCHASE_REFERRAL_CONTRACT = '0x3F0f5bcC6a001C004A1C6AE2dd4151De0f513294';
  // PURCHASE_REFERRAL_CONTRACT = '0xB28F5E2725D92bc74C3fdBbf3657450c808fca06';
  POWID_CONTRACT = '0x4695880aE1cE27A11E239eaEeeC5AF5217B25453';
  // POWID_CONTRACT = '0xa8691bEaEE825Ace9F620Bed657Fa742Db134892';
  USDT_CONTRACT = '0x94b008aA00579c1307B0EF2c499aD98a8ce58e58'; // USDT on OP
  RPC_URL = 'https://mainnet.optimism.io';
  INDEXER_HOST = 'https://testindexer.zentra.dev';
  SUBMIT_HOST = 'https://submit.powid.xyz';
  REFERRAL_PREFIX = 'https://test.powid.xyz/referral.html?';
}else{
  CHAIN_ID = '0x7a69';
  CHAIN_NAME = 'Hardhat';
  PURCHASE_CONTRACT = '0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0'; // Mock Purchase on harthat
  PURCHASE_REFERRAL_CONTRACT = '0xCf7Ed3AccA5a467e9e704C703E8D87F634fB0Fc9'; // Mock PurchaseReferral on harthat 
  USDT_CONTRACT = '0x5FbDB2315678afecb367f032d93F642f64180aa3'; // Mock USDT on harthat
  RPC_URL = 'http://127.0.0.1:8545';
  INDEXER_HOST = 'http://127.0.0.1:8090';
  SUBMIT_HOST = 'https://submit.powid.xyz';
  REFERRAL_PREFIX = 'http://127.0.0.1:8070/referral?';
}


const HANDLE_LETTERS = 'abcdefghijklmnopqrstuvwxyz0123456789_';

const PURCHASE_ABI = [
  "function purchase(bytes memory _handle) public",
  "function available(bytes memory _handle) public view returns (uint256)",
];

const PURCHASE_REFERRAL_ABI = [
  "function whitelist_used(address _addr) public view returns (bool)",
  "function available(bytes memory _handle) public view returns (bool)",
  "function bonusOf(bytes memory _handle) public view returns (uint256)",
  "function purchase_with_bonus(bytes memory _handle, bytes memory _referral) public",
  "function purchase_by_referral(bytes memory _handle, bytes memory _referral) public",
  "function withdraw() public",
  "function change_owner(address _owner) public",
  "function set_live(bool _live) public",
  "function set_price_and_bonus(uint256 _price_discount, uint256 _bonus_referral) public",
  "function reg_with_whitelist(bytes memory _handle, bytes32[] memory proofs) public",
  "function set_whitelist_root(bytes32 _root) public",
];

const USDT_ABI = [
  "function allowance(address owner, address spender) external view returns (uint256)",
  "function approve(address spender, uint256 value) external returns (bool)",
  "function transferFrom(address from, address to, uint256 value) external returns (bool)",
  "function decimals() view returns (string)",
  "function symbol() view returns (string)",
  "function balanceOf(address addr) view returns (uint)",
];

export {
  CHAIN_ID,
  CHAIN_NAME,
  PURCHASE_CONTRACT,
  PURCHASE_REFERRAL_CONTRACT,
  POWID_CONTRACT,
  USDT_CONTRACT,
  RPC_URL,
  INDEXER_HOST,
  REFERRAL_PREFIX,
  HANDLE_LETTERS,
  PURCHASE_ABI,
  PURCHASE_REFERRAL_ABI,
  USDT_ABI,
}
