from brownie import APIConsumer, Contract
from scripts.utils import get_account
from web3 import Web3

account = get_account()


def main():
    # deploy()
    # request_views_count()
    views_count()


def deploy():
    api_consumer = APIConsumer.deploy({"from": account, "priority_fee": "10 gwei"})
    link = Contract.from_explorer("0x326C977E6efc84E512bB9C30f76E30c160eD06FB")
    link.transfer(
        api_consumer,
        Web3.toWei(1, "ether"),
        {"from": account, "priority_fee": "10 gwei"},
    )


def request_views_count():
    api_consumer = APIConsumer[-1]
    tx = api_consumer.requestVolumeData({"from": account, "priority_fee": "10 gwei"})
    tx.wait(1)


def views_count():
    print("===")
    print(APIConsumer[-1].volume())
    print("===")
