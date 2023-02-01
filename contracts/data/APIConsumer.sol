// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "@chainlink/contracts/src/v0.8/ChainlinkClient.sol";
import "@chainlink/contracts/src/v0.8/ConfirmedOwner.sol";

contract APIConsumer is ChainlinkClient, ConfirmedOwner {
    using Chainlink for Chainlink.Request;

    uint256 public viewsCount;
    bytes private jobId;
    uint256 internal fee;

    event RequestViewsCount(bytes32 indexed requestId, uint256 viewsCount);

    constructor() ConfirmedOwner(msg.sender) {
        setChainlinkToken(0x326C977E6efc84E512bB9C30f76E30c160eD06FB);
        setChainlinkOracle(0x99c3F6340B42B3E378f6f899ACD4f764c0cb54CC);
        jobId = "ec013753fda740f8bc74a966daea0723";
        fee = (1 * LINK_DIVISIBILITY) / 10; // 0,1 * 10**18 (Varies by network and job) .
    }

    function requestViewsCountData(string memory _apiUrl)
        public
        returns (bytes32 requestId)
    {
        Chainlink.Request memory req = buildChainlinkRequest(
            bytes32(jobId),
            address(this),
            this.fulfill.selector
        );

        // Set the URL to perform the GET request on
        req.add("get", _apiUrl);

        req.add("path", "items,0,statistics,viewCount");

        // Sends the request
        return sendChainlinkRequest(req, fee);
    }

    /**
     * Receive the response in the form of uint256
     */
    function fulfill(bytes32 _requestId, uint256 _viewsCount)
        public
        recordChainlinkFulfillment(_requestId)
    {
        emit RequestViewsCount(_requestId, _viewsCount);
        viewsCount = _viewsCount;
    }
}
