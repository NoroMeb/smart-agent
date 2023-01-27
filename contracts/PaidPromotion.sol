// SPDX-License-Identifier: MIT
pragma solidity 0.8.7;

import "./data/APIConsumer.sol";
import "@chainlink/contracts/src/v0.8/interfaces/LinkTokenInterface.sol";

contract PaidPromotion {
    APIConsumer public apiConsumer;
    string public apiUrl;
    LinkTokenInterface public linkToken;

    constructor(
        string memory _apiUrl,
        address _apiConsumerAddress,
        address _linkToken
    ) {
        apiConsumer = APIConsumer(_apiConsumerAddress);
        apiUrl = _apiUrl;
        linkToken = LinkTokenInterface(_linkToken);
    }

    function getViwesCount() external {
        apiConsumer.requestViewsCountData(apiUrl);
    }
}
