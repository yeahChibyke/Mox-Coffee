# --- Imports --- #

import pytest 
from moccasin.config import get_active_network 
from script.deploy import deploy_coffee
from script.deploy_mocks import deploy_feed
from eth_utils import to_wei
import boa 

# -- Variables -- #

AMOUNT = to_wei(1, "ether")
alice = boa.env.generate_address("first_buyer")
bob = boa.env.generate_address("second_buyer")
clara = boa.env.generate_address("third_buyer")

# --- Session Fixtures --- #

@pytest.fixture(scope = "session")
def owner_account():
    return get_active_network().get_default_account()

@pytest.fixture(scope = "session")
def eth_usd():
    return deploy_feed() 

# --- Function Fixtures --- #

@pytest.fixture(scope = "function")
def coffee(eth_usd):
    return deploy_coffee(eth_usd) 

@pytest.fixture(scope = "function")
def coffee_bought(coffee):
    boa.env.set_balance(alice, AMOUNT)
    with boa.env.prank(alice):
        coffee.buy_coffee(value = AMOUNT)
    return coffee

@pytest.fixture(scope = "function")
def many_coffee_bought(coffee):
    boa.env.set_balance(alice, AMOUNT)
    boa.env.set_balance(bob, AMOUNT)
    boa.env.set_balance(clara, AMOUNT)

    with boa.env.prank(alice):
        coffee.buy_coffee(value = AMOUNT)
    with boa.env.prank(bob):
        coffee.buy_coffee(value = AMOUNT)
    with boa.env.prank(clara):
        coffee.buy_coffee(value = AMOUNT)
    return coffee

