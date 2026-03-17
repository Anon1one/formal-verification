// SPDX-License-Identifier: MIT
pragma solidity ^0.8.25;

contract Math {

    function add(uint256 x, uint256 y) public pure returns (uint256) {
        return x + y;
    }
    function divide(uint256 x, uint256 y) public pure returns (uint256) {
        return x / y;
    }
}
