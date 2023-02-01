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
}
