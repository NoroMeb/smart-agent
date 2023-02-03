// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

abstract contract IERC677Receiver {
    function onTokenTransfer(
        address sender,
        uint256 value,
        bytes memory data
    ) external virtual;
}

abstract contract ERC677 is ERC20 {
    event Transfer(
        address indexed from,
        address indexed to,
        uint256 value,
        bytes data
    );

    /**
     * @dev transfer token to a contract address with additional data if the recipient is a contact.
     * @param to The address to transfer to.
     * @param value The amount to be transferred.
     * @param data The extra data to be passed to the receiving contract.
     */
    function transferAndCall(
        address to,
        uint256 value,
        bytes memory data
    ) public virtual returns (bool success) {
        super.transfer(to, value);
        emit Transfer(msg.sender, to, value, data);
        if (isContract(to)) {
            contractFallback(to, value, data);
        }
        return true;
    }

    function contractFallback(
        address to,
        uint256 value,
        bytes memory data
    ) private {
        IERC677Receiver receiver = IERC677Receiver(to);
        receiver.onTokenTransfer(msg.sender, value, data);
    }

    function isContract(address addr) private view returns (bool hasCode) {
        uint256 length;
        assembly {
            length := extcodesize(addr)
        }
        return length > 0;
    }
}
