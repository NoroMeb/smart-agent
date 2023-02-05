from scripts.utils import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
import pytest
from brownie import MockPaidPromotion, network, MockLinkToken, MockOracle, config
from web3 import Web3


@pytest.fixture()
def skip_live_testing():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing !")


@pytest.fixture()
def skip_local_testing():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for live testing !")


@pytest.fixture()
def account():
    account = get_account(index=0)

    return account


@pytest.fixture()
def second_account():
    return get_account(index=1)


@pytest.fixture()
def link(account):
    amount = 10000
    link = MockLinkToken.deploy(amount, {"from": account})
    return link


@pytest.fixture()
def mock_oracle(link, account):
    return MockOracle.deploy(link, {"from": account})


@pytest.fixture()
def api_url():
    api_key = config["networks"][network.show_active()]["api_key"]
    video_id = "bY2yvESoWAs"
    return f"https://youtube.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics&id={video_id}&key={api_key}"


@pytest.fixture()
def paid_promotion(link, mock_oracle, account):
    job_id = "1"
    return MockPaidPromotion.deploy(link, mock_oracle, job_id, {"from": account})


@pytest.fixture()
def start_collab(account, second_account, api_url, paid_promotion):
    promoter = account
    client = second_account
    end_timestamp = 1675433147
    amount = Web3.toWei(0.01, "ether")
    client_balance = Web3.toWei(1, "ether")
    paid_promotion.startACollab(
        promoter,
        client,
        api_url,
        end_timestamp,
        amount,
        {"from": account, "value": client_balance},
    )
