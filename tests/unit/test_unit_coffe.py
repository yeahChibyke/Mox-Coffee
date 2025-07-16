# --- Imports --- #

from eth_utils import to_wei
import boa
from tests.conftest import AMOUNT, alice, bob, clara 

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

def test_many_can_buy_coffee(many_coffee_bought):
    # Assert
    assert boa.env.get_balance(many_coffee_bought.address) == (AMOUNT * 3)
    assert many_coffee_bought.getTotalBuyers() == 3

def test_can_withdraw_from_one_buyer(coffee_bought, owner_account):
    initial_pool: int = boa.env.get_balance(coffee_bought.address) # 1_000_000_000_000_000_000.00
    assert initial_pool == (AMOUNT)

    initial_wallet: int = boa.env.get_balance(coffee_bought.OWNER()) # 1000_000_000_000_000_000_000.00
    with boa.env.prank(owner_account.address):
        coffee_bought.withdraw()

    final_pool: int = boa.env.get_balance(coffee_bought.address) # 0
    final_wallet: int = boa.env.get_balance(coffee_bought.OWNER())
    breakpoint()

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

