from brownie import PaidPromotion, Contract, config, network
from scripts.utils import get_account
from web3 import Web3


account = get_account()
api_key = config["networks"][network.show_active()]["api_key"]


def main():
    # deploy()
    # start_a_collab("bY2yvESoWAs")
    # start_a_collab("9kP12wIp3wA")
    # request_views_count(1)
    view()


def deploy():
    link_token = config["networks"][network.show_active()]["link_token"]
    chainlink_oracle = config["networks"][network.show_active()]["chainlink_oracle"]
    job_id = config["networks"][network.show_active()]["job_id"]

    paid_promotion = PaidPromotion.deploy(
        link_token,
        chainlink_oracle,
        job_id,
        {"from": account, "priority_fee": "10 gwei"},
    )


def start_a_collab(video_id):
    paid_promotion = PaidPromotion[-1]
    promoter = "0x108A176896bAD4E05b5C4BE738839fDC4238c526"
    client = "0x8FB5F1947F1325072307c87e987162f4Cdf823aC"
    api_url = f"https://youtube.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics&id={video_id}&key={api_key}"
    end_time_stamp = 1680348420
    level = 10000
    amount = Web3.toWei(0.8, "ether")

    start_collab_tx = paid_promotion.startACollab(
        promoter,
        client,
        api_url,
        end_time_stamp,
        level,
        amount,
        {"from": account, "priority_fee": "10 gwei"},
    )


def request_views_count(id):
    paid_promotion = PaidPromotion[-1]
    link = Contract.from_explorer("0x326C977E6efc84E512bB9C30f76E30c160eD06FB")
    request_tx = link.transferAndCall(
        paid_promotion,
        Web3.toWei(0.1, "ether"),
        paid_promotion.requestViewsCountData.encode_input(id),
        {"from": account, "priority_fee": "10 gwei"},
    )


def view():
    paid_promotion = PaidPromotion[-1]
    print("========================")
    print(paid_promotion.collabById(0))
    print("========================")
