// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "@chainlink/contracts/src/v0.8/ChainlinkClient.sol";
import "@chainlink/contracts/src/v0.8/ConfirmedOwner.sol";

contract MockPaidPromotion is ChainlinkClient, ConfirmedOwner {
    using Chainlink for Chainlink.Request;

    bytes public jobId;
    uint256 public fee;

    event RequestViewsCount(bytes32 indexed requestId, uint256 viewsCount);

    struct Collab {
        address promoter;
        address client;
        string apiUrl;
        uint256 endTimestamp;
        uint256 amount;
        uint256 clientBalance;
        uint256 lastViewsCount;
    }

    mapping(uint256 => Collab) public collabById;
    uint256 public id;

    constructor(
        address _chainlinkToken,
        address _chainlinkOracle,
        string memory _jobId
    ) ConfirmedOwner(msg.sender) {
        setChainlinkToken(_chainlinkToken);
        setChainlinkOracle(_chainlinkOracle);
        jobId = bytes(_jobId);
        fee = (1 * LINK_DIVISIBILITY) / 10; // 0,1 * 10**18 (Varies by network and job) .
        id = 0;
    }

    // modifier onlyPromoter() {
    //     require(msg.sender == promoter, "Only promoter can call this function");
    //     _;
    // }

    modifier onlyClient(uint256 _id) {
        address client = collabById[_id].client;
        require(msg.sender == client, "Only client can call this function");
        _;
    }

    function startACollab(
        address _promoter,
        address _client,
        string memory _apiUrl,
        uint256 _endTimestamp,
        uint256 _amount
    ) external payable {
        Collab memory collab = Collab(
            _promoter,
            _client,
            _apiUrl,
            _endTimestamp,
            _amount,
            msg.value,
            0
        );
        collabById[id] = collab;
        id = id + 1;
    }

    function withdrawEther(uint256 _id) public returns (bytes32 requestId) {
        string memory apiUrl = collabById[_id].apiUrl;

        Chainlink.Request memory req = buildChainlinkRequest(
            bytes32(jobId),
            address(this),
            this.fulfill.selector
        );

        id = _id;

        // Set the URL to perform the GET request on
        req.add("get", apiUrl);

        req.add("path", "items,0,statistics,viewCount");

        req.addInt("times", 1);

        // Sends the request
        return sendChainlinkRequest(req, fee);
    }

    function TestwithdrawEther(uint256 _id) public returns (uint256) {
        return 4;
    }

    function fulfill(bytes32 _requestId, uint256 _viewsCount)
        public
        recordChainlinkFulfillment(_requestId)
    {
        emit RequestViewsCount(_requestId, _viewsCount);

        Collab memory collab = collabById[id];
        uint256 promoterOwings = (_viewsCount - collab.lastViewsCount) *
            100000000000000;
        collab.lastViewsCount = _viewsCount;
        require(promoterOwings >= collab.clientBalance, "Not enough funds");
        payable(collab.promoter).transfer(promoterOwings);
        collab.clientBalance = collab.clientBalance - promoterOwings;
    }

    function onTokenTransfer(
        address _sender,
        uint256 _fee,
        bytes calldata _data
    ) public {
        require(_fee >= fee, "NOT ENOUGH FUNDS");
        bytes memory data = _data[4:];
        uint256 _id = abi.decode(data, (uint256));
        Collab memory collab = collabById[_id];
        require(
            _sender == collab.promoter,
            "Only promoter can call this function"
        );
        TestwithdrawEther(_id);
    }

    function endCollab(uint256 _id) external onlyClient(_id) {
        Collab memory collab = collabById[_id];
        require(block.timestamp >= collab.endTimestamp, "ITS NOT THE TIME YET");
        payable(msg.sender).transfer(collab.clientBalance);
        collab.clientBalance = 0;
        collabById[_id] = collab;
    }
}
