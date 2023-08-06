
from ..abi_contract_wrapper import ABIContractWrapper
from ..solidity_types import *
from ..credentials import Credentials

CONTRACT_ADDRESS =     {
    "cv": "0x77D991987ca85214f9686131C58c1ABE4C93E547",
    "sd": "0x0000000000000000000000000000000000000000"
}

ABI = """[
    {"name": "AuctionCancelled", "type": "event", "inputs": [{"name": "auctionId", "type": "uint256", "indexed": false, "internalType": "uint256"}, {"name": "tokenId", "type": "uint256", "indexed": true, "internalType": "uint256"}], "anonymous": false},
    {"name": "AuctionCreated", "type": "event", "inputs": [{"name": "auctionId", "type": "uint256", "indexed": false, "internalType": "uint256"}, {"name": "owner", "type": "address", "indexed": true, "internalType": "address"}, {"name": "tokenId", "type": "uint256", "indexed": true, "internalType": "uint256"}, {"name": "startingPrice", "type": "uint256", "indexed": false, "internalType": "uint256"}, {"name": "endingPrice", "type": "uint256", "indexed": false, "internalType": "uint256"}, {"name": "duration", "type": "uint256", "indexed": false, "internalType": "uint256"}, {"name": "winner", "type": "address", "indexed": false, "internalType": "address"}], "anonymous": false},
    {"name": "AuctionSuccessful", "type": "event", "inputs": [{"name": "auctionId", "type": "uint256", "indexed": false, "internalType": "uint256"}, {"name": "tokenId", "type": "uint256", "indexed": true, "internalType": "uint256"}, {"name": "totalPrice", "type": "uint256", "indexed": false, "internalType": "uint256"}, {"name": "winner", "type": "address", "indexed": false, "internalType": "address"}], "anonymous": false},
    {"name": "Initialized", "type": "event", "inputs": [{"name": "version", "type": "uint8", "indexed": false, "internalType": "uint8"}], "anonymous": false},
    {"name": "Paused", "type": "event", "inputs": [{"name": "account", "type": "address", "indexed": false, "internalType": "address"}], "anonymous": false},
    {"name": "Unpaused", "type": "event", "inputs": [{"name": "account", "type": "address", "indexed": false, "internalType": "address"}], "anonymous": false},
    {"name": "ERC721", "type": "function", "inputs": [], "outputs": [{"name": "", "type": "address", "internalType": "contract IERC721Upgradeable"}], "stateMutability": "view"},
    {"name": "auctionIdOffset", "type": "function", "inputs": [], "outputs": [{"name": "", "type": "uint256", "internalType": "uint256"}], "stateMutability": "view"},
    {"name": "auctions", "type": "function", "inputs": [{"name": "", "type": "uint256", "internalType": "uint256"}], "outputs": [{"name": "seller", "type": "address", "internalType": "address"}, {"name": "tokenId", "type": "uint256", "internalType": "uint256"}, {"name": "startingPrice", "type": "uint128", "internalType": "uint128"}, {"name": "endingPrice", "type": "uint128", "internalType": "uint128"}, {"name": "duration", "type": "uint64", "internalType": "uint64"}, {"name": "startedAt", "type": "uint64", "internalType": "uint64"}, {"name": "winner", "type": "address", "internalType": "address"}, {"name": "open", "type": "bool", "internalType": "bool"}], "stateMutability": "view"},
    {"name": "bid", "type": "function", "inputs": [{"name": "_tokenId", "type": "uint256", "internalType": "uint256"}, {"name": "_bidAmount", "type": "uint256", "internalType": "uint256"}], "outputs": [], "stateMutability": "nonpayable"},
    {"name": "bidFor", "type": "function", "inputs": [{"name": "_bidder", "type": "address", "internalType": "address"}, {"name": "_tokenId", "type": "uint256", "internalType": "uint256"}, {"name": "_bidAmount", "type": "uint256", "internalType": "uint256"}], "outputs": [], "stateMutability": "nonpayable"},
    {"name": "cancelAuction", "type": "function", "inputs": [{"name": "_tokenId", "type": "uint256", "internalType": "uint256"}], "outputs": [], "stateMutability": "nonpayable"},
    {"name": "cancelAuctionWhenPaused", "type": "function", "inputs": [{"name": "_tokenId", "type": "uint256", "internalType": "uint256"}], "outputs": [], "stateMutability": "nonpayable"},
    {"name": "createAuction", "type": "function", "inputs": [{"name": "_tokenId", "type": "uint256", "internalType": "uint256"}, {"name": "_startingPrice", "type": "uint128", "internalType": "uint128"}, {"name": "_endingPrice", "type": "uint128", "internalType": "uint128"}, {"name": "_duration", "type": "uint64", "internalType": "uint64"}, {"name": "_winner", "type": "address", "internalType": "address"}], "outputs": [], "stateMutability": "nonpayable"},
    {"name": "getAuction", "type": "function", "inputs": [{"name": "_tokenId", "type": "uint256", "internalType": "uint256"}], "outputs": [{"name": "", "type": "tuple", "components": [{"name": "seller", "type": "address", "internalType": "address"}, {"name": "tokenId", "type": "uint256", "internalType": "uint256"}, {"name": "startingPrice", "type": "uint128", "internalType": "uint128"}, {"name": "endingPrice", "type": "uint128", "internalType": "uint128"}, {"name": "duration", "type": "uint64", "internalType": "uint64"}, {"name": "startedAt", "type": "uint64", "internalType": "uint64"}, {"name": "winner", "type": "address", "internalType": "address"}, {"name": "open", "type": "bool", "internalType": "bool"}], "internalType": "struct ERC721AuctionBase.Auction"}], "stateMutability": "view"},
    {"name": "getAuctions", "type": "function", "inputs": [{"name": "_tokenIds", "type": "uint256[]", "internalType": "uint256[]"}], "outputs": [{"name": "", "type": "tuple[]", "components": [{"name": "seller", "type": "address", "internalType": "address"}, {"name": "tokenId", "type": "uint256", "internalType": "uint256"}, {"name": "startingPrice", "type": "uint128", "internalType": "uint128"}, {"name": "endingPrice", "type": "uint128", "internalType": "uint128"}, {"name": "duration", "type": "uint64", "internalType": "uint64"}, {"name": "startedAt", "type": "uint64", "internalType": "uint64"}, {"name": "winner", "type": "address", "internalType": "address"}, {"name": "open", "type": "bool", "internalType": "bool"}], "internalType": "struct ERC721AuctionBase.Auction[]"}], "stateMutability": "view"},
    {"name": "getCurrentPrice", "type": "function", "inputs": [{"name": "_tokenId", "type": "uint256", "internalType": "uint256"}], "outputs": [{"name": "", "type": "uint256", "internalType": "uint256"}], "stateMutability": "view"},
    {"name": "getUserAuctions", "type": "function", "inputs": [{"name": "_address", "type": "address", "internalType": "address"}], "outputs": [{"name": "", "type": "uint256[]", "internalType": "uint256[]"}], "stateMutability": "view"},
    {"name": "initialize", "type": "function", "inputs": [{"name": "_landCoreAddress", "type": "address", "internalType": "address"}, {"name": "_jewelTokenAddress", "type": "address", "internalType": "address"}, {"name": "_cut", "type": "uint256", "internalType": "uint256"}, {"name": "_auctionIdOffset", "type": "uint256", "internalType": "uint256"}], "outputs": [], "stateMutability": "nonpayable"},
    {"name": "isOnAuction", "type": "function", "inputs": [{"name": "_tokenId", "type": "uint256", "internalType": "uint256"}], "outputs": [{"name": "", "type": "bool", "internalType": "bool"}], "stateMutability": "view"},
    {"name": "jewelToken", "type": "function", "inputs": [], "outputs": [{"name": "", "type": "address", "internalType": "contract IJewelToken"}], "stateMutability": "view"},
    {"name": "maxPrice", "type": "function", "inputs": [], "outputs": [{"name": "", "type": "uint256", "internalType": "uint256"}], "stateMutability": "view"},
    {"name": "minPrice", "type": "function", "inputs": [], "outputs": [{"name": "", "type": "uint256", "internalType": "uint256"}], "stateMutability": "view"},
    {"name": "onERC721Received", "type": "function", "inputs": [{"name": "", "type": "address", "internalType": "address"}, {"name": "", "type": "address", "internalType": "address"}, {"name": "", "type": "uint256", "internalType": "uint256"}, {"name": "", "type": "bytes", "internalType": "bytes"}], "outputs": [{"name": "", "type": "bytes4", "internalType": "bytes4"}], "stateMutability": "pure"},
    {"name": "ownerCut", "type": "function", "inputs": [], "outputs": [{"name": "", "type": "uint256", "internalType": "uint256"}], "stateMutability": "view"},
    {"name": "pause", "type": "function", "inputs": [], "outputs": [], "stateMutability": "nonpayable"},
    {"name": "paused", "type": "function", "inputs": [], "outputs": [{"name": "", "type": "bool", "internalType": "bool"}], "stateMutability": "view"},
    {"name": "setFees", "type": "function", "inputs": [{"name": "_feeAddresses", "type": "address[]", "internalType": "address[]"}, {"name": "_feePercents", "type": "uint256[]", "internalType": "uint256[]"}], "outputs": [], "stateMutability": "nonpayable"},
    {"name": "setLimits", "type": "function", "inputs": [{"name": "_min", "type": "uint256", "internalType": "uint256"}, {"name": "_max", "type": "uint256", "internalType": "uint256"}], "outputs": [], "stateMutability": "nonpayable"},
    {"name": "totalAuctions", "type": "function", "inputs": [], "outputs": [{"name": "", "type": "uint256", "internalType": "uint256"}], "stateMutability": "view"},
    {"name": "unpause", "type": "function", "inputs": [], "outputs": [], "stateMutability": "nonpayable"},
    {"name": "userAuctions", "type": "function", "inputs": [{"name": "", "type": "address", "internalType": "address"}, {"name": "", "type": "uint256", "internalType": "uint256"}], "outputs": [{"name": "", "type": "uint256", "internalType": "uint256"}], "stateMutability": "view"}
]
"""     

class LandAuction(ABIContractWrapper):
    def __init__(self, chain_key:str, rpc:str):
        contract_address = CONTRACT_ADDRESS[chain_key]
        super().__init__(contract_address=contract_address, abi=ABI, rpc=rpc)

    def erc721(self, block_identifier:BlockIdentifier = 'latest') -> address:
        return self.contract.functions.ERC721().call(block_identifier=block_identifier)

    def auction_id_offset(self, block_identifier:BlockIdentifier = 'latest') -> uint256:
        return self.contract.functions.auctionIdOffset().call(block_identifier=block_identifier)

    def auctions(self, a:uint256, block_identifier:BlockIdentifier = 'latest') -> Tuple[address, uint256, uint128, uint128, uint64, uint64, address, bool]:
        return self.contract.functions.auctions(a).call(block_identifier=block_identifier)

    def bid(self, cred:Credentials, _token_id:uint256, _bid_amount:uint256) -> TxReceipt:
        tx = self.contract.functions.bid(_token_id, _bid_amount)
        return self.send_transaction(tx, cred)

    def bid_for(self, cred:Credentials, _bidder:address, _token_id:uint256, _bid_amount:uint256) -> TxReceipt:
        tx = self.contract.functions.bidFor(_bidder, _token_id, _bid_amount)
        return self.send_transaction(tx, cred)

    def cancel_auction(self, cred:Credentials, _token_id:uint256) -> TxReceipt:
        tx = self.contract.functions.cancelAuction(_token_id)
        return self.send_transaction(tx, cred)

    def cancel_auction_when_paused(self, cred:Credentials, _token_id:uint256) -> TxReceipt:
        tx = self.contract.functions.cancelAuctionWhenPaused(_token_id)
        return self.send_transaction(tx, cred)

    def create_auction(self, cred:Credentials, _token_id:uint256, _starting_price:uint128, _ending_price:uint128, _duration:uint64, _winner:address) -> TxReceipt:
        tx = self.contract.functions.createAuction(_token_id, _starting_price, _ending_price, _duration, _winner)
        return self.send_transaction(tx, cred)

    def get_auction(self, _token_id:uint256, block_identifier:BlockIdentifier = 'latest') -> tuple:
        return self.contract.functions.getAuction(_token_id).call(block_identifier=block_identifier)

    def get_auctions(self, _token_ids:Sequence[uint256], block_identifier:BlockIdentifier = 'latest') -> List[tuple]:
        return self.contract.functions.getAuctions(_token_ids).call(block_identifier=block_identifier)

    def get_current_price(self, _token_id:uint256, block_identifier:BlockIdentifier = 'latest') -> uint256:
        return self.contract.functions.getCurrentPrice(_token_id).call(block_identifier=block_identifier)

    def get_user_auctions(self, _address:address, block_identifier:BlockIdentifier = 'latest') -> List[uint256]:
        return self.contract.functions.getUserAuctions(_address).call(block_identifier=block_identifier)

    def initialize(self, cred:Credentials, _land_core_address:address, _jewel_token_address:address, _cut:uint256, _auction_id_offset:uint256) -> TxReceipt:
        tx = self.contract.functions.initialize(_land_core_address, _jewel_token_address, _cut, _auction_id_offset)
        return self.send_transaction(tx, cred)

    def is_on_auction(self, _token_id:uint256, block_identifier:BlockIdentifier = 'latest') -> bool:
        return self.contract.functions.isOnAuction(_token_id).call(block_identifier=block_identifier)

    def jewel_token(self, block_identifier:BlockIdentifier = 'latest') -> address:
        return self.contract.functions.jewelToken().call(block_identifier=block_identifier)

    def max_price(self, block_identifier:BlockIdentifier = 'latest') -> uint256:
        return self.contract.functions.maxPrice().call(block_identifier=block_identifier)

    def min_price(self, block_identifier:BlockIdentifier = 'latest') -> uint256:
        return self.contract.functions.minPrice().call(block_identifier=block_identifier)

    def on_erc721_received(self, a:address, b:address, c:uint256, d:bytes, block_identifier:BlockIdentifier = 'latest') -> bytes4:
        return self.contract.functions.onERC721Received(a, b, c, d).call(block_identifier=block_identifier)

    def owner_cut(self, block_identifier:BlockIdentifier = 'latest') -> uint256:
        return self.contract.functions.ownerCut().call(block_identifier=block_identifier)

    def pause(self, cred:Credentials) -> TxReceipt:
        tx = self.contract.functions.pause()
        return self.send_transaction(tx, cred)

    def paused(self, block_identifier:BlockIdentifier = 'latest') -> bool:
        return self.contract.functions.paused().call(block_identifier=block_identifier)

    def set_fees(self, cred:Credentials, _fee_addresses:Sequence[address], _fee_percents:Sequence[uint256]) -> TxReceipt:
        tx = self.contract.functions.setFees(_fee_addresses, _fee_percents)
        return self.send_transaction(tx, cred)

    def set_limits(self, cred:Credentials, _min:uint256, _max:uint256) -> TxReceipt:
        tx = self.contract.functions.setLimits(_min, _max)
        return self.send_transaction(tx, cred)

    def total_auctions(self, block_identifier:BlockIdentifier = 'latest') -> uint256:
        return self.contract.functions.totalAuctions().call(block_identifier=block_identifier)

    def unpause(self, cred:Credentials) -> TxReceipt:
        tx = self.contract.functions.unpause()
        return self.send_transaction(tx, cred)

    def user_auctions(self, a:address, b:uint256, block_identifier:BlockIdentifier = 'latest') -> uint256:
        return self.contract.functions.userAuctions(a, b).call(block_identifier=block_identifier)