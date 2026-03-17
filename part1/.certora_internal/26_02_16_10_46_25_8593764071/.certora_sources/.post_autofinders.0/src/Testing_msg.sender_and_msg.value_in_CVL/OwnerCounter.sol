// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract OwnerCounter {
    uint256 public counter;
    address public owner;

    constructor(address _owner) {
        owner = _owner;
    }

    function increment() public {assembly ("memory-safe") { mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00000000, 1037618708480) mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00000001, 0) mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00000004, 0) }
        require(msg.sender == owner, "not owner");
        counter++;
    }
}

