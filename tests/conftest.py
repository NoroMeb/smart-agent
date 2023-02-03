from scripts.utils import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
import pytest
from brownie import PaidPromotion, network, MockLinkToken
from web3 import Web3


@pytest.fixture()
def skip_live_testing():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing !")


@pytest.fixture()
def account():
    account = get_account()

    return account


@pytest.fixture()
def paid_promotion():
    return PaidPromotion.deploy()


@pytest.fixture()
def link():
    account = get_account()
    amount = 10000
    link = MockLinkToken.deploy(amount, {"from": account})
    return link
