// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "./data/APIConsumer.sol";
import "@chainlink/contracts/src/v0.8/interfaces/LinkTokenInterface.sol";

contract PaidPromotion is APIConsumer {
    constructor(
        address _chainlinkToken,
        address _chainlinkOracle,
        bytes memory _jobId,
        string memory _apiUrl
    ) APIConsumer(_chainlinkToken, _chainlinkOracle, _jobId, _apiUrl) {}
}
