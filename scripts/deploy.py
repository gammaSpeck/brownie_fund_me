from brownie import FundMe, config, network
from scripts.utils import get_account, get_price_feed_address


def deploy_fund_me():
    account = get_account()

    price_feed_address = get_price_feed_address()
    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
