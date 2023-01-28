// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "@chainlink/contracts/src/v0.8/ChainlinkClient.sol";
import "@chainlink/contracts/src/v0.8/ConfirmedOwner.sol";

contract APIConsumer is ChainlinkClient, ConfirmedOwner {
    using Chainlink for Chainlink.Request;

    uint256 public viewsCount;
    bytes private jobId;
    uint256 private fee;
    string apiUrl;

    event RequestViewsCount(bytes32 indexed requestId, uint256 viewsCount);

    constructor(
        address _chainlinkToken,
        address _chainlinkOracle,
        bytes memory _jobId,
        string memory _apiUrl
    ) ConfirmedOwner(msg.sender) {
        setChainlinkToken(_chainlinkToken);
        setChainlinkOracle(_chainlinkOracle);
        jobId = _jobId;
        fee = (1 * LINK_DIVISIBILITY) / 10; // 0,1 * 10**18 (Varies by network and job) .
        apiUrl = _apiUrl;
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

    function onTokenTransfer(
        address sender,
        uint256 fee,
        bytes memory data
    ) public {
        (bool success, ) = address(this).call(data);
        require(success, "NOT SUCCESS");
    }
}
