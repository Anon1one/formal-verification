// SPDX-License-Identifier: MIT
pragma solidity ^0.8.25;

contract Math {
    uint256 internal constant MAX_UINT256 = 2 ** 256 - 1;

    function mod(uint256 x, uint256 y) external pure returns (uint256) {
        return x % y;
    }

    function max(uint256 x, uint256 y) external pure returns (uint256 z) {
        assembly {
            z := xor(x, mul(xor(x, y), gt(y, x)))
        }
    }

    function mulDivUp(uint256 x, uint256 y, uint256 denominator) external pure returns (uint256 z) {
        assembly {
            // Equivalent to require(denominator != 0 && (y == 0 || x <= type(uint256).max / y))
            if iszero(mul(denominator, iszero(mul(y, gt(x, div(MAX_UINT256, y)))))) {
                revert(0, 0)
            }

            // If x * y modulo the denominator is strictly greater than 0,
            // 1 is added to round up the division of x * y by the denominator.
            z := add(gt(mod(mul(x, y), denominator), 0), div(mul(x, y), denominator))
        }
    }
}
