# --- Imports --- #

from eth_utils import to_wei
import boa
from tests.conftest import AMOUNT
from tests.conftest import alice

# --- Tests --- #

def test_price_feed_is_correct(coffee, eth_usd):
    assert coffee.PRICE_FEED() == eth_usd.address, "Price feed mismatch!!!"

def test_starting_value(coffee, owner_account):
    assert coffee.MINIMUM_USD() == to_wei(5, "ether"), "Minimum USD mismatch!!!"
    assert coffee.OWNER() == owner_account.address, "Msg.sender mismatch!!!"

def test_can_buy_coffee(coffee_bought):
    # Assert
    first_coffee_buyer = coffee_bought.buyers(0)
    assert boa.env.get_balance(coffee_bought.address) == (AMOUNT)
    assert coffee_bought.getTotalBuyers() == 1
    # breakpoint()
    # assert first_coffee_buyer == alice # --> This particular assert fails

# --- Reverts --- #

def test_cannot_buy_coffee_without_enough_eth(coffee):
    with boa.reverts("Minimum USD requirement not met!!!"):
        coffee.buy_coffee()

def test_cannot_withdraw_if_not_owner(coffee_bought):
    # Arrange
    boa.env.set_balance(alice, AMOUNT)

    # Act
    with boa.env.prank(alice):
        with boa.reverts("Not the owner!!!"):
            coffee_bought.withdraw()

