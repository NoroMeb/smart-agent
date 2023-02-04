from brownie import Contract, MockLinkToken, MockPaidPromotion, reverts
from web3 import Web3
from scripts.utils import get_account
import pprint


def test_deploy_link(skip_live_testing, account):
    # arrange
    amount = 10000

    # act
    link = MockLinkToken.deploy(amount, {"from": account})

    # assert
    assert link.balanceOf(account) == Web3.toWei(amount, "ether")


def test_constructor(skip_live_testing, link, mock_oracle, account):
    # arrange
    job_id = "1"
    excepted_id = 0
    excepted_fee = Web3.toWei(0.1, "ether")

    # act
    paid_promotion = MockPaidPromotion.deploy(
        link, mock_oracle, job_id, {"from": account}
    )

    # assert
    assert paid_promotion.jobId().decode("utf-8") == job_id
    assert paid_promotion.id() == excepted_id
    assert paid_promotion.fee() == excepted_fee


def test_start_collab_map_id_to_collab(
    skip_live_testing, paid_promotion, account, second_account, api_url
):
    # arrange
    promoter = get_account(index=0)
    client = get_account(index=1)
    end_timestamp = 1675433147
    amount = Web3.toWei(0.001, "ether")
    client_balance = Web3.toWei(1, "ether")
    # act
    paid_promotion.startACollab(
        promoter,
        client,
        api_url,
        end_timestamp,
        amount,
        {"from": account, "value": client_balance},
    )

    # assert
    assert paid_promotion.collabById(0) == (
        promoter,
        client,
        api_url,
        end_timestamp,
        amount,
        client_balance,
        0,
    )


def test_start_collab_increment_id(
    skip_live_testing, paid_promotion, account, second_account, api_url
):
    # arrange
    promoter = get_account(index=0)
    client = get_account(index=1)
    end_timestamp = 1675433147
    amount = Web3.toWei(0.001, "ether")
    client_balance = Web3.toWei(1, "ether")
    # act
    paid_promotion.startACollab(
        promoter,
        client,
        api_url,
        end_timestamp,
        amount,
        {"from": account, "value": client_balance},
    )

    # assert
    assert paid_promotion.id() == 1


def test_start_collab_send_funds_to_contract(
    skip_live_testing, paid_promotion, account, second_account, api_url
):
    # arrange
    promoter = get_account(index=0)
    client = get_account(index=1)
    end_timestamp = 1675433147
    amount = Web3.toWei(0.001, "ether")
    client_balance = Web3.toWei(1, "ether")
    # act
    paid_promotion.startACollab(
        promoter,
        client,
        api_url,
        end_timestamp,
        amount,
        {"from": account, "value": client_balance},
    )

    # assert
    assert paid_promotion.balance() == client_balance


def test_end_collab_transfer_funds_to_client(
    start_collab, paid_promotion, second_account
):
    # arrange
    id = 0
    client = second_account

    # act
    paid_promotion.endCollab(id, {"from": client})

    # asset
    assert paid_promotion.balance() == 0


def test_end_collab_sets_client_balance_to_zero(
    start_collab, paid_promotion, second_account
):
    # arrange
    id = 0
    client = second_account

    # act
    paid_promotion.endCollab(id, {"from": client})

    # asset
    assert paid_promotion.collabById(0)[5] == 0


def test_end_collab_only_client(start_collab, paid_promotion, second_account):
    # arrange
    id = 0
    random_account = get_account(index=4)

    # act / assert
    with reverts("Only client can call this function"):
        paid_promotion.endCollab(id, {"from": random_account})


def test_end_collab_before_end_timestamp(
    paid_promotion, second_account, api_url, account
):
    # arrange
    promoter = get_account(index=0)
    client = get_account(index=1)
    end_timestamp = 2653812532
    amount = Web3.toWei(0.001, "ether")
    client_balance = Web3.toWei(1, "ether")
    paid_promotion.startACollab(
        promoter,
        client,
        api_url,
        end_timestamp,
        amount,
        {"from": account, "value": client_balance},
    )
    id = 0

    # act / assert
    with reverts("ITS NOT THE TIME YET"):
        paid_promotion.endCollab(id, {"from": client})


def test_on_token_transfer_calls_withdraw_ether(
    start_collab, link, paid_promotion, account
):
    # arrange
    id = 0

    # act
    tx = link.transferAndCall(
        paid_promotion,
        Web3.toWei(0.1, "ether"),
        paid_promotion.TestwithdrawEther.encode_input(id),
        {"from": account},
    )

    # assert
    assert False
