// SPDX-License-Identifier: MIT
// OpenZeppelin Contracts (last updated v4.8.0) (utils/Strings.sol)

pragma solidity ^0.8.0;

import "./Math.sol";
import "./SignedMath.sol";

/**
 * @dev String operations.
 */
library Strings {
    bytes16 private constant _SYMBOLS = "0123456789abcdef";
    uint8 private constant _ADDRESS_LENGTH = 20;

    /**
     * @dev Converts a `uint256` to its ASCII `string` decimal representation.
     */
    function toString(uint256 value) internal pure returns (string memory) {assembly ("memory-safe") { mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00400000, 1037618708544) mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00400001, 1) mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00400005, 1) mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00406000, value) }
        unchecked {
            uint256 length = Math.log10(value) + 1;
            string memory buffer = new string(length);
            uint256 ptr;
            /// @solidity memory-safe-assembly
            assembly {
                ptr := add(buffer, add(32, length))
            }
            while (true) {
                ptr--;
                /// @solidity memory-safe-assembly
                assembly {
                    mstore8(ptr, byte(mod(value, 10), _SYMBOLS))
                }
                value /= 10;assembly ("memory-safe"){mstore(0xffffff6e4604afefe123321beef1b02fffffffffffffffffffffffff00000016,value)}
                if (value == 0) break;
            }
            return buffer;
        }
    }

    /**
     * @dev Converts a `int256` to its ASCII `string` decimal representation.
     */
    function toString(int256 value) internal pure returns (string memory) {assembly ("memory-safe") { mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00410000, 1037618708545) mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00410001, 1) mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00410005, 1) mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00416000, value) }
        return string(abi.encodePacked(value < 0 ? "-" : "", toString(SignedMath.abs(value))));
    }

    /**
     * @dev Converts a `uint256` to its ASCII `string` hexadecimal representation.
     */
    function toHexString(uint256 value) internal pure returns (string memory) {assembly ("memory-safe") { mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00430000, 1037618708547) mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00430001, 1) mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00430005, 1) mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00436000, value) }
        unchecked {
            return toHexString(value, Math.log256(value) + 1);
        }
    }

    /**
     * @dev Converts a `uint256` to its ASCII `string` hexadecimal representation with fixed length.
     */
    function toHexString(uint256 value, uint256 length) internal pure returns (string memory) {assembly ("memory-safe") { mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00440000, 1037618708548) mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00440001, 2) mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00440005, 9) mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00446001, length) }
        bytes memory buffer = new bytes(2 * length + 2);assembly ("memory-safe"){mstore(0xffffff6e4604afefe123321beef1b02fffffffffffffffffffffffff00010011,0)}
        buffer[0] = "0";bytes1 certora_local18 = buffer[0];assembly ("memory-safe"){mstore(0xffffff6e4604afefe123321beef1b02fffffffffffffffffffffffff00000012,certora_local18)}
        buffer[1] = "x";bytes1 certora_local19 = buffer[1];assembly ("memory-safe"){mstore(0xffffff6e4604afefe123321beef1b02fffffffffffffffffffffffff00000013,certora_local19)}
        for (uint256 i = 2 * length + 1; i > 1; --i) {
            buffer[i] = _SYMBOLS[value & 0xf];bytes1 certora_local20 = buffer[i];assembly ("memory-safe"){mstore(0xffffff6e4604afefe123321beef1b02fffffffffffffffffffffffff00000014,certora_local20)}
            value >>= 4;assembly ("memory-safe"){mstore(0xffffff6e4604afefe123321beef1b02fffffffffffffffffffffffff00000015,value)}
        }
        require(value == 0, "Strings: hex length insufficient");
        return string(buffer);
    }

    /**
     * @dev Converts an `address` with fixed length of 20 bytes to its not checksummed ASCII `string` hexadecimal representation.
     */
    function toHexString(address addr) internal pure returns (string memory) {assembly ("memory-safe") { mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00420000, 1037618708546) mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00420001, 1) mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00420005, 1) mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00426000, addr) }
        return toHexString(uint256(uint160(addr)), _ADDRESS_LENGTH);
    }

    /**
     * @dev Returns true if the two strings are equal.
     */
    function equal(string memory a, string memory b) internal pure returns (bool) {assembly ("memory-safe") { mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00450000, 1037618708549) mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00450001, 2) mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00450005, 9) mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00456001, b) }
        return keccak256(bytes(a)) == keccak256(bytes(b));
    }
}