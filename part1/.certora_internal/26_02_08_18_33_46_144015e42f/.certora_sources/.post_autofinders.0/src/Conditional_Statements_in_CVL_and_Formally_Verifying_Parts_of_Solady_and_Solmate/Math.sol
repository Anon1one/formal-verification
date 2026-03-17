// SPDX-License-Identifier: MIT
pragma solidity ^0.8.25;

contract Math {
    uint256 internal constant MAX_UINT256 = 2**256 - 1;

    function add(uint256 x, uint256 y) external pure returns (uint256) {
        return x + y;
    }

    function max(uint256 x, uint256 y) external pure returns (uint256 z) {
        assembly {
            z := xor(x, mul(xor(x, y), gt(y, x)))
        }
    }

    function mulDivUp(
    uint256 x,
    uint256 y,
    uint256 denominator
    ) external pure returns (uint256 z) {
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

    /// @dev Returns the minimum of `x` and `y`.
    function min(uint256 x, uint256 y) internal pure returns (uint256 z) {assembly ("memory-safe") { mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00000000, 1037618708480) mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00000001, 2) mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00000005, 9) mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00006001, y) }
        assembly {
            z := xor(x, mul(xor(x, y), lt(y, x)))
        }
    } function min_external_harness(uint256 x, uint256 y) external pure returns (uint256) { return min(x, y); }
    
    /// @dev Returns `max(0, x - y)`. Alias for `saturatingSub`.
    function zeroFloorSub(uint256 x, uint256 y) internal pure returns (uint256 z) {assembly ("memory-safe") { mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00010000, 1037618708481) mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00010001, 2) mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00010005, 9) mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00016001, y) }
        assembly {
            z := mul(gt(x, y), sub(x, y))
        }
    } function zeroFloorSub_external_harness(uint256 x, uint256 y) external pure returns (uint256) { return zeroFloorSub(x, y); }
}
