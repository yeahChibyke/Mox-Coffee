from moccasin.config import get_active_network 
from moccasin.boa_tools import VyperContract 
from src import mox_coffee
from script.deploy_mocks import deploy_feed

def deploy_coffee(price_feed: VyperContract) -> VyperContract:
    coffee: VyperContract = mox_coffee.deploy(price_feed)
    print("Mox Coffee contract deployed at: ", coffee.address)
    usd_value: int = coffee.get_in_usd(1)
    print(usd_value)

    # active_network = get_active_network()
    # if active_network.has_explorer():
    #     result = active_network.moccasin_verify(coffee)
    #     result.wait_for_verification()

    # print(f"Mox Coffee verified at: {result}")
    return coffee

def moccasin_main() -> VyperContract:
    active_network = get_active_network()
    price_feed: VyperContract = active_network.manifest_named("price_feed")
    print(f"On {active_network.name} chain and using price feed at {price_feed.address}")
    return deploy_coffee(price_feed)

