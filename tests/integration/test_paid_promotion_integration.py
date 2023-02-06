import time
from web3 import Web3
from scripts.utils import get_account
from brownie import accounts, config, MockPaidPromotion, network, reverts, Contract


def test_paid_promotion_integration(skip_local_testing):
    # arrange
    account = get_account()
    second_account = accounts.add(config["wallets"]["from_key_2"])
    link = config["networks"][network.show_active()]["link_token"]
    link_contract = Contract.from_explorer(link)
    chainlink_oracle = config["networks"][network.show_active()]["chainlink_oracle"]
    job_id = config["networks"][network.show_active()]["job_id"]
    priority_fee = "10 gwei"
    promoter = account
    promoter_initial_balance = promoter.balance()
    client = second_account
    client_balance = Web3.toWei(1, "ether")
    video_id = "l4uCnAWj-6I"
    api_key = config["networks"][network.show_active()]["api_key"]
    api_url = f"https://youtube.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics&id={video_id}&key={api_key}"
    end_time_stamp = 2653911765
    amount = Web3.toWei(0.00001, "ether")

    # act
    paid_promotion = MockPaidPromotion.deploy(
        link, chainlink_oracle, job_id, {"from": account, "priority_fee": priority_fee}
    )

    start_collab_tx = paid_promotion.startACollab(
        promoter,
        client,
        api_url,
        end_time_stamp,
        amount,
        {"from": client, "priority_fee": priority_fee, "value": client_balance},
    )

    request_tx = link_contract.transferAndCall(
        paid_promotion,
        Web3.toWei(0.1, "ether"),
        paid_promotion.withdrawEther.encode_input(0),
        {"from": promoter, "priority_fee": priority_fee},
    )

    event_filter = paid_promotion.events.RequestViewsCount.createFilter(
        fromBlock="latest"
    )
    while True:
        events = event_filter.get_new_entries()
        if len(events) > 0:
            break

    # assert
    assert paid_promotion.id() == 1
    assert promoter.balance() > promoter_initial_balance

    assert paid_promotion.collabById(0)[5] == client_balance - (
        paid_promotion.collabById(0)[6] * amount
    )
