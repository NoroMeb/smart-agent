// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "./data/APIConsumer.sol";
import "@chainlink/contracts/src/v0.8/interfaces/LinkTokenInterface.sol";

contract PaidPromotion is APIConsumer {
    address payable public promoter;
    address public client;
    mapping(uint256 => uint256) levelToAmount;
    uint256 public promoterOwing;
    uint256 public endTimestamp;

    constructor(
        string memory _apiUrl,
        address payable _promoter,
        address _client,
        uint256 _endTimestamp,
        uint256 _level,
        uint256 _amount
    ) payable APIConsumer() {
        promoter = _promoter;
        client = _client;
        endTimestamp = _endTimestamp;
    }

    modifier onlyPromoter() {
        require(msg.sender == promoter, "Only promoter can call this function");
        _;
    }

    modifier onlyClient() {
        require(msg.sender == client, "Only client can call this function");
        _;
    }

    function onTokenTransfer(
        address _sender,
        uint256 _fee,
        bytes calldata _data
    ) public {
        require(_fee >= fee, "NOT ENOUGH FUNDS");

        bytes memory data = _data[4:];

        string memory apiUrl = abi.decode(data, (string));

        requestViewsCountData(apiUrl);
        // (bool success, ) = address(this).call(_data);
        // require(success, "NOT SUCCESS");
    }
}
