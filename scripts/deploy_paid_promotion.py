from brownie import PaidPromotion, APIConsumer, Contract, config, network
from scripts.utils import get_account
from web3 import Web3


account = get_account()


def main():
    # deploy()
    # request()
    view()


def deploy():
    link_token = config["networks"][network.show_active()]["link_token"]
    chainlink_oracle = config["networks"][network.show_active()]["chainlink_oracle"]
    api_url = "https://youtube.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics&id=G7KNmW9a75Y&key=AIzaSyBJN4rbtGCZiMgSegJ2W8YnPC_gb0ynj3Q"
    job_id = config["networks"][network.show_active()]["job_id"]

    paid_promotion = PaidPromotion.deploy(
        api_url,
        link_token,
        chainlink_oracle,
        job_id,
        {"from": account, "priority_fee": "10 gwei"},
    )


def request_views_count():
    paid_promotion = PaidPromotion[-1]
    link = Contract.from_explorer("0x326C977E6efc84E512bB9C30f76E30c160eD06FB")
    api_url = "https://youtube.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics&id=G7KNmW9a75Y&key=AIzaSyBJN4rbtGCZiMgSegJ2W8YnPC_gb0ynj3Q"
    request_tx = link.transferAndCall(
        paid_promotion,
        Web3.toWei(0.1, "ether"),
        paid_promotion.requestViewsCountData.encode_input(api_url),
        {"from": account, "priority_fee": "10 gwei"},
    )


def view():
    paid_promotion = PaidPromotion[-1]
    print("========================")
    print(paid_promotion.viewsCount())
    print("========================")
