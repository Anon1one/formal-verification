// SPDX-License-Identifier: MIT
pragma solidity ^0.8.25;

contract MaxInCollection {
    uint256[] collection;
    uint256 public maxInCollection = 0;

    function addToCollection(uint256 x) public {
        if (x > maxInCollection) {
            maxInCollection = x;
        }
        collection.push(x);
    }

    function returnMax() public view returns (uint256) {
        uint256 maxTmp = 0;
        for (uint256 i = 0; i < collection.length; i++) {
            if (collection[i] > maxTmp) {
                maxTmp = collection[i];
            }
        }
        return maxTmp;
    }
}
