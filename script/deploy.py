from moccasin.config import get_active_network 
from moccasin.boa_tools import VyperContract 
from src import coffee
from script.deploy_mocks import deploy_feed

def deploy_coffee(price_feed: str) -> VyperContract:
    coffee.deploy(price_feed) 

def moccasin_main():
    price_feed: VyperContract = deploy_feed()

    coffee = deploy_coffee(price_feed)
    # print("Coffee deployed at: ", coffee.address)


