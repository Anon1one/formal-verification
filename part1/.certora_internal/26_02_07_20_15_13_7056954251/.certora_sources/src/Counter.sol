// SPDX-License-Identifier: MIT
pragma solidity ^0.8.25;

contract Counter {

    function eqn(uint256 x, uint256 y) external pure returns (bool) {
        return (2 * x + 3 * y == 22) && (4 * x - y == 2);
    }
      function eqn2(uint256 x, uint256 y) external pure returns (bool) {
        return (2 * x + 3 * y == 22) && (4 * x + 6 * y == 50);
    }

}
