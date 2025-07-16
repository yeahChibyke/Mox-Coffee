# pragma version ^0.4.0
# @license MIT

from interfaces import AggregatorV3Interface  

import get_price_helper

# Errors
ERROR_NOT_OWNER: public(constant(String[25])) = "Not the contract owner!!!"
ERROR_NOT_MINIMUM_USD: public(constant(String[34])) = "Minimum USD requirement not met!!!"

# Constants & Immutables
MINIMUM_USD: public(constant(uint256)) = as_wei_value(5, "ether")
OWNER: public(immutable(address))
PRICE_FEED: public(immutable(AggregatorV3Interface))

buyers: public(DynArray[address, 100]) #limited to 100 buyers
totalBuyers: uint256

# --|| Init Def ||-- #

@deploy
def __init__(address_to_use: address):
    OWNER = msg.sender
    PRICE_FEED = AggregatorV3Interface(address_to_use)

# -------------------------------------- #

# -- || Modifiers || -- #

@internal 
def _only_owner():
    assert msg.sender == OWNER, ERROR_NOT_OWNER

# --|| External Defs ||-- #

@external 
@payable
def buy_coffee():
    self._buy_coffee()

@external 
def withdraw():
    self._only_owner()
    self.buyers = [] # reset buyers array after every withdrawal
    self.totalBuyers = 0
    raw_call(OWNER, b"", value = self.balance)

@external 
def get_in_usd(eth_amount: uint256) -> uint256:
    return get_price_helper._get_eth_to_usd_rate(PRICE_FEED, eth_amount)

# -------------------------------------- #

# --|| Internal Defs ||-- #

@internal 
@payable
def _buy_coffee():
    usd_value_of_eth: uint256 = get_price_helper._get_eth_to_usd_rate(PRICE_FEED, msg.value)
    assert usd_value_of_eth >= MINIMUM_USD, ERROR_NOT_MINIMUM_USD
    self.buyers.append(msg.sender)
    self.totalBuyers = self.totalBuyers + 1

# -------------------------------------- #

# --|| Getter Defs ||-- #

@external 
@view 
def getTotalBuyers() -> uint256: 
    return self.totalBuyers

@external 
def getRate(amount: uint256) -> uint256:
    return get_price_helper._get_eth_to_usd_rate(PRICE_FEED, amount)

@external
@view 
def getPriceFeed() -> AggregatorV3Interface:
    return PRICE_FEED
    
# -------------------------------------- #

# --|| Fallback ||-- #

@external 
@payable 
def __default__():
    self._buy_coffee()
