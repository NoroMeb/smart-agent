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
    assert link is not None


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
    assert paid_promotion is not None


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
    skip_live_testing, start_collab, paid_promotion, second_account
):
    # arrange
    id = 0
    client = second_account

    # act
    paid_promotion.endCollab(id, {"from": client})

    # asset
    assert paid_promotion.balance() == 0


def test_end_collab_sets_client_balance_to_zero(
    skip_live_testing, start_collab, paid_promotion, second_account
):
    # arrange
    id = 0
    client = second_account

    # act
    paid_promotion.endCollab(id, {"from": client})

    # asset
    assert paid_promotion.collabById(0)[5] == 0


def test_end_collab_only_client(
    skip_live_testing, start_collab, paid_promotion, second_account
):
    # arrange
    id = 0
    random_account = get_account(index=4)

    # act / assert
    with reverts("Only client can call this function"):
        paid_promotion.endCollab(id, {"from": random_account})


def test_end_collab_before_end_timestamp(
    skip_live_testing, paid_promotion, second_account, api_url, account
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
    skip_live_testing, start_collab, link, paid_promotion, account
):
    # arrange
    id = 0

    # act
    tx = link.transferAndCall(
        paid_promotion,
        Web3.toWei(0.1, "ether"),
        paid_promotion.withdrawEther.encode_input(id),
        {"from": account},
    )

    assert paid_promotion.signatures.get("withdrawEther") in str(tx.subcalls)


def test_on_token_transfer_input_fee_less_than_fee(
    skip_live_testing, start_collab, link, paid_promotion, account
):
    # arrange
    id = 0
    fee = Web3.toWei(0.01, "ether")

    # act / assert
    with reverts("NOT ENOUGH FUNDS"):
        link.transferAndCall(
            paid_promotion,
            fee,
            paid_promotion.withdrawEther.encode_input(id),
            {"from": account},
        )


def test_on_token_transfer_non_promoter(
    skip_live_testing, start_collab, link, paid_promotion, account
):
    # arrange
    id = 0
    random_account = get_account(index=4)
    link.transfer(random_account, Web3.toWei(1, "ether") * 2, {"from": account})

    # act / assert
    with reverts("Only promoter can call this function"):
        tx = link.transferAndCall(
            paid_promotion,
            Web3.toWei(0.1, "ether"),
            paid_promotion.withdrawEther.encode_input(id),
            {"from": random_account},
        )
        tx.wait(1)


def test_withdraw_ether_makes_an_api_request(
    skip_live_testing, start_collab, paid_promotion, link, account
):
    # arrange
    link.transfer(paid_promotion.address, Web3.toWei(1, "ether") * 2, {"from": account})
    id = 0

    # act
    request_tx = paid_promotion.withdrawEther(0, {"from": account})
    request_tx.wait(1)

    # assert
    request_id = request_tx.events["ChainlinkRequested"]["id"]
    assert request_id is not None


def test_fulfill_update_last_views_count(
    skip_live_testing, paid_promotion, start_collab, mock_oracle, link, account
):
    # arrange
    link.transfer(paid_promotion.address, Web3.toWei(1, "ether") * 2, {"from": account})
    id = 0
    data = 100

    # act
    tx = paid_promotion.withdrawEther(id, {"from": account})
    request_id = tx.events["ChainlinkRequested"]["id"]
    mock_oracle.fulfillOracleRequest(request_id, data, {"from": account})

    # assert
    assert paid_promotion.collabById(0)[6] == data


def test_fulfill_transfer_promoter_owings(
    skip_live_testing, paid_promotion, start_collab, mock_oracle, link, account
):
    # arrange
    link.transfer(paid_promotion.address, Web3.toWei(1, "ether") * 2, {"from": account})
    id = 0
    data = 100
    promoter = account
    promoter_initial_balance = account.balance()
    amount = paid_promotion.collabById(0)[4]

    # act
    tx = paid_promotion.withdrawEther(id, {"from": account})
    request_id = tx.events["ChainlinkRequested"]["id"]
    mock_oracle.fulfillOracleRequest(request_id, data, {"from": account})

    # assert
    assert promoter.balance() == promoter_initial_balance + (data * amount)


def test_fulfill_decrease_client_balance(
    skip_live_testing,
    paid_promotion,
    start_collab,
    mock_oracle,
    link,
    account,
    second_account,
):
    # arrange
    link.transfer(paid_promotion.address, Web3.toWei(1, "ether") * 2, {"from": account})
    id = 0
    data = 100
    client = second_account
    initial_client_balance = paid_promotion.collabById(0)[5]
    amount = paid_promotion.collabById(0)[4]

    # act
    tx = paid_promotion.withdrawEther(id, {"from": account})
    request_id = tx.events["ChainlinkRequested"]["id"]
    mock_oracle.fulfillOracleRequest(request_id, data, {"from": account})

    # assert
    assert paid_promotion.collabById(0)[5] == initial_client_balance - (data * amount)


def test_fulfill_promoter_owings_greater_client_balance(
    skip_live_testing,
    paid_promotion,
    mock_oracle,
    link,
    account,
    second_account,
    api_url,
):
    # arrange
    promoter = account
    client = second_account
    end_timestamp = 1675433147
    amount = Web3.toWei(0.01, "ether")
    client_balance = Web3.toWei(0.1, "ether")
    paid_promotion.startACollab(
        promoter,
        client,
        api_url,
        end_timestamp,
        amount,
        {"from": account, "value": client_balance},
    )
    link.transfer(paid_promotion.address, Web3.toWei(1, "ether") * 2, {"from": account})
    id = 0
    data = 100

    print(f"client balance : {Web3.fromWei(paid_promotion.collabById(0)[5], 'ether')}")
    print(f"promoter owings : {data * amount}")

    # act
    tx = paid_promotion.withdrawEther(id, {"from": account})
    request_id = tx.events["ChainlinkRequested"]["id"]
    fulfill = mock_oracle.fulfillOracleRequest(request_id, data, {"from": account})

    assert fulfill.subcalls[0].get("revert_msg") == "Not enough funds"
