// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract OwnerCounter {
    uint256 public counter;
    address public owner;

    constructor(address _owner) {
        owner = _owner;
    }

    function increment() public {
        require(msg.sender == owner, "not owner");
        counter++;
    }
}

