from src.mocks import mock_v3_aggregator 

from moccasin.boa_tools import VyperContract 

STARTING_DECIMALS = 8
STARTING_PRICE = int(2500e8)

def deploy_feed() -> VyperContract:
    return mock_v3_aggregator.deploy(STARTING_DECIMALS, STARTING_PRICE) 

deploy_feed()