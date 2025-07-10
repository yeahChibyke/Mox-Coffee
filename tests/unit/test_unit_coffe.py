# --- Imports --- #

from eth_utils import to_wei
import boa

# --- Tests --- #

def test_price_feed_is_correct(coffee, eth_usd):
    assert coffee.PRICE_FEED() == eth_usd.address, "Price feed mismatch!!!"

def test_starting_value(coffee, owner_account):
    assert coffee.MINIMUM_USD() == to_wei(5, "ether"), "Minimum USD mismatch!!!"
    assert coffee.OWNER() == owner_account.address, "Msg.sender mismatch!!!"

# --- Reverts --- #

def test_cannot_buy_coffee_without_enough_eth(coffee):
    with boa.reverts("Minimum USD requirement not met!!!"):
        coffee.buy_coffee()



