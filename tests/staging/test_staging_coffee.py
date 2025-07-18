# --- Imports --- #

import pytest
from moccasin.config import get_active_network 
from script.deploy import deploy_coffee
from tests.conftest import AMOUNT
import boa 


@pytest.mark.staging
@pytest.mark.local
@pytest.mark.ignore_isolation
def test_can_buy_coffee_and_withdraw_live():
    active_network = get_active_network()
    price_feed = active_network.manifest_named("price_feed")
    coffee = deploy_coffee(price_feed)
    coffee.buy_coffee(value = AMOUNT)
    amount_bought = boa.env.get_balance(coffee.address)
    assert amount_bought == AMOUNT
    coffee.withdraw()
    assert boa.env.get_balance(coffee.address) == 0
