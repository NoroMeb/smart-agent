from brownie import PaidPromotion, APIConsumer
from scripts.utils import get_account


account = get_account()


def main():
    # deploy()
    request()


def deploy():
    api_consumer = APIConsumer[-1]
    api_url = "https://youtube.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics&id=G7KNmW9a75Y&key=AIzaSyBJN4rbtGCZiMgSegJ2W8YnPC_gb0ynj3Q"
    paid_promotion = PaidPromotion.deploy(
        api_url, api_consumer, {"from": account, "priority_fee": "10 gwei"}
    )


def request():
    paid_promotion = PaidPromotion[-1]
    link = Contract.from_explorer("0x326C977E6efc84E512bB9C30f76E30c160eD06FB")
    api_url = "https://youtube.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics&id=G7KNmW9a75Y&key=AIzaSyBJN4rbtGCZiMgSegJ2W8YnPC_gb0ynj3Q"
    request_tx = link.transferAndCall(
        paid_promotion,
        Web3.toWei(0.1, "ether"),
        paid_promotion.requestViewsCountData.encode_input(api_url),
        {"from": account, "priority_fee": "10 gwei"},
    )
