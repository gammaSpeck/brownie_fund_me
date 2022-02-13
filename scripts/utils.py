from brownie import accounts, network, config, MockV3Aggregator


DECIMALS = 8
STARTING_PRICE = 2000 * 10**8

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]


def get_account():
    active_network = network.show_active()
    if (
        active_network in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or active_network in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]

    return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    print("Deploying mocks")
    MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": get_account()})
    print("Mocks deployed!")


def get_price_feed_address():
    active_network = network.show_active()
    print(f"The active network is {active_network}")

    if active_network not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return config["networks"][active_network].get("eth_usd_price_feed")

    if len(MockV3Aggregator) <= 0:
        deploy_mocks()

    price_feed_address = MockV3Aggregator[-1].address
    return price_feed_address
