// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "./data/APIConsumer.sol";
import "@chainlink/contracts/src/v0.8/interfaces/LinkTokenInterface.sol";

contract PaidPromotion is APIConsumer {
    constructor(
        string memory _apiUrl,
        address _chainlinkToken,
        address _chainlinkOracle,
        bytes memory _jobId
    ) APIConsumer(_chainlinkToken, _chainlinkOracle, _jobId, _apiUrl) {}
}
