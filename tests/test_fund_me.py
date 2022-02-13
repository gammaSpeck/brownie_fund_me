from brownie import FundMe, accounts, network, exceptions
from scripts.deploy import deploy_fund_me
from scripts.utils import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
import pytest
import brownie


def test_can_fund_me():
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee() + 100
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for Local testing")

    fund_me = deploy_fund_me()
    bad_actor = accounts.add()
    with pytest.raises(AttributeError):
        fund_me.withdraw({"from": bad_actor})
