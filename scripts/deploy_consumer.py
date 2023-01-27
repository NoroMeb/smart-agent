from brownie import APIConsumer, Contract, config, network
from scripts.utils import get_account
from web3 import Web3

account = get_account()


def main():
    # deploy()
    # request_views_count()
    # views_count()
    withdraw_link()


def deploy():
    link_token = config["networks"][network.show_active()]["link_token"]
    chainlink_oracle = config["networks"][network.show_active()]["chainlink_oracle"]
    job_id = config["networks"][network.show_active()]["job_id"]
    api_consumer = APIConsumer.deploy(
        link_token,
        chainlink_oracle,
        job_id,
        {"from": account, "priority_fee": "10 gwei"},
    )
    link = Contract.from_explorer("0x326C977E6efc84E512bB9C30f76E30c160eD06FB")
    link.transfer(
        api_consumer,
        Web3.toWei(0.5, "ether"),
        {"from": account, "priority_fee": "10 gwei"},
    )


def request_views_count():
    api_consumer = APIConsumer[-1]
    api_url = "https://youtube.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics&id=G7KNmW9a75Y&key=AIzaSyBJN4rbtGCZiMgSegJ2W8YnPC_gb0ynj3Q"
    tx = api_consumer.requestViewsCountData(
        api_url, {"from": account, "priority_fee": "10 gwei"}
    )
    tx.wait(1)


def views_count():
    print("===")
    print(APIConsumer[-1].viewsCount())
    print("===")


def withdraw_link():
    consumer = APIConsumer[-1]
    withdraw_tx = consumer.withdrawLink({"from": account, "priority_fee": "10 gwei"})
