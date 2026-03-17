// SPDX-License-Identifier: MIT
pragma solidity ^0.8.25;

contract MaxInCollection {
    uint256[] collection;
    uint256 public maxInCollection = 0;

    function addToCollection(uint256 x) public {assembly ("memory-safe") { mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00010000, 1037618708481) mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00010001, 1) mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00010005, 1) mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00016000, x) }
        if (x > maxInCollection) {
            maxInCollection = x;
        }
        collection.push(x);
    }

    function returnMax() public view returns (uint256) {assembly ("memory-safe") { mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00000000, 1037618708480) mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00000001, 0) mstore(0xffffff6e4604afefe123321beef1b01fffffffffffffffffffffffff00000004, 0) }
        uint256 maxTmp = 0;assembly ("memory-safe"){mstore(0xffffff6e4604afefe123321beef1b02fffffffffffffffffffffffff00000001,maxTmp)}
        for (uint256 i = 0; i < collection.length; i++) {
            if (collection[i] > maxTmp) {
                maxTmp = collection[i];
            }
        }
        return maxTmp;
    }
}
