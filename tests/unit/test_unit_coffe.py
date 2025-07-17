# --- Imports --- #

from eth_utils import to_wei
import boa
from tests.conftest import AMOUNT

# --- Tests --- #


def test_price_feed_is_correct(coffee, eth_usd):
    assert coffee.getPriceFeed() == eth_usd.address, "Price feed mismatch!!!"


def test_starting_value(coffee, owner_account):
    assert coffee.MINIMUM_USD() == to_wei(5, "ether"), "Minimum USD mismatch!!!"
    assert coffee.OWNER() == owner_account.address, "Msg.sender mismatch!!!"

def test_rate_is_accurate(coffee):
    eth_amount: int = to_wei(1, "ether")
    assert coffee.getRate(eth_amount) == 2500e18 

def test_can_buy_coffee(coffee_bought, alice):
    # Assert
    first_coffee_buyer = coffee_bought.buyers(0)
    assert boa.env.get_balance(coffee_bought.address) == (AMOUNT)
    assert coffee_bought.getTotalBuyers() == 1
    assert first_coffee_buyer == alice 


def test_many_can_buy_coffee(many_coffee_bought):
    # Assert
    assert boa.env.get_balance(many_coffee_bought.address) == (AMOUNT * 3)
    assert many_coffee_bought.getTotalBuyers() == 3


def test_can_withdraw_from_one_buyer(coffee_bought, owner_account):
    initial_pool: int = boa.env.get_balance(
        coffee_bought.address
    )  # 1_000_000_000_000_000_000.00
    assert initial_pool == (AMOUNT)

    initial_wallet: int = boa.env.get_balance(
        coffee_bought.OWNER()
    )  # 1000_000_000_000_000_000_000.00
    with boa.env.prank(owner_account.address):
        coffee_bought.withdraw()

    final_pool: int = boa.env.get_balance(coffee_bought.address)  # 0
    final_wallet: int = boa.env.get_balance(coffee_bought.OWNER())

    # @dev since default account in boa has initial balance, you need to check
    # if initial wallet plus initial pool equals final wallet
    assert final_pool == 0, "Pool did not empty after withdrawal!!!"
    assert final_wallet == initial_wallet + initial_pool, (
        "Wallet did not receive funds after withdrawal!!!"
    )


def test_can_withdraw_from_many_buyers(many_coffee_bought, owner_account):
    initial_pool: int = boa.env.get_balance(many_coffee_bought.address)
    assert initial_pool == (AMOUNT * 3)

    initial_wallet: int = boa.env.get_balance(many_coffee_bought.OWNER())
    with boa.env.prank(owner_account.address):
        many_coffee_bought.withdraw()

    final_pool: int = boa.env.get_balance(many_coffee_bought.address)
    final_wallet: int = boa.env.get_balance(many_coffee_bought.OWNER())

    assert final_pool == 0, "Pool did not empty after withdrawal!!!"
    assert final_wallet == initial_wallet + initial_pool, "Wallet did not receive funds after withdrawal!!!"


def test_fallback(coffee):
    dean = boa.env.generate_address("dean")
    boa.env.set_balance(dean, AMOUNT)
    initialDeanWallet: int = boa.env.get_balance(dean)

    initial_pool: int = boa.env.get_balance(coffee.address)

    with boa.env.prank(dean):
        coffee.__default__(value = AMOUNT)

    finalDeanWallet: int = boa.env.get_balance(dean)
    final_pool: int = boa.env.get_balance(coffee.address)

    assert finalDeanWallet == initialDeanWallet - AMOUNT, "Failed to buy coffee via fallback!!!"
    assert final_pool == initial_pool + AMOUNT, "Fallback failed!!!"


# --- Reverts --- #


def test_cannot_buy_coffee_without_enough_eth(coffee):
    with boa.reverts(coffee.ERROR_NOT_MINIMUM_USD()):
        coffee.buy_coffee()


def test_cannot_withdraw_if_not_owner(coffee_bought, alice):
    # Arrange
    boa.env.set_balance(alice, AMOUNT)

    # Act
    with boa.env.prank(alice):
        with boa.reverts(coffee_bought.ERROR_NOT_OWNER()):
            coffee_bought.withdraw()


