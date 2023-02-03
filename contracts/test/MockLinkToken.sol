// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "./ERC677.sol";

contract MockLinkToken is ERC677 {
    constructor(uint256 _amount) ERC20("Mock LINK", "LINK") {
        _mint(msg.sender, _amount * 10**18);
    }
}
