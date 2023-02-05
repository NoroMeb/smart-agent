from web3 import Web3
from scripts.utils import get_account
from brownie import accounts, config, MockPaidPromotion, network


def test_paid_promotion_integration():
    # arrange
    account = get_account()
    second_account = accounts.add(config["wallets"]["from_key_2"])
    link = config["networks"][network.show_active()]["link_token"]
    chainlink_oracle = config["networks"][network.show_active()]["chainlink_oracle"]
    job_id = config["networks"][network.show_active()]["job_id"]
    priority_fee = "10 gwei"
    promoter = account
    client = second_account
    client_balance = Web3.toWei(2, "ether")
    video_id = "l4uCnAWj-6I"
    api_key = config["networks"][network.show_active()]["api_key"]
    api_url = f"https://youtube.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics&id={video_id}&key={api_key}"
    end_time_stamp = 2653911765
    amount = Web3.toWei(0.0001, "ether")

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
        {"from": account, "priority_fee": priority_fee, "value": client_balance},
    )

    request_tx = link.transferAndCall(
        paid_promotion,
        Web3.toWei(0.1, "ether"),
        paid_promotion.withdrawEther.encode_input(id),
        {"from": account, "priority_fee": priority_fee},
    )

    # assert
    assert paid_promotion.id() == 1
    assert paid_promotion.collabById(0) == (
        promoter,
        client,
        api_url,
        end_time_stamp,
        amount,
        client_balance,
    )
