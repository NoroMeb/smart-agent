from brownie import Contract, MockLinkToken, PaidPromotion
from web3 import Web3


def test_deploy_link(skip_live_testing, account):
    # arrange
    amount = 10000

    # act
    link = MockLinkToken.deploy(amount, {"from": account})

    # assert
    assert link.balanceOf(account) == Web3.toWei(amount, "ether")


def test_constructor(skip_live_testing):
    # arrange

    # act
    link = MockLinkToken.deploy(amount, {"from": account})

    # assert
    assert link.balanceOf(account) == Web3.toWei(amount, "ether")
