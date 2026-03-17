// SPDX-License-Identifier: MIT
pragma solidity ^0.8.25;

contract Math {
    function add(uint256 x, uint256 y) external pure returns (uint256) {
        return x + y;
    }

    function max(uint256 x, uint256 y) external pure returns (uint256 z) {
        assembly {
            z := xor(x, mul(xor(x, y), gt(y, x)))
        }
    }
}
