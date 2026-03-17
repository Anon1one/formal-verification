// SPDX-License-Identifier: MIT
pragma solidity ^0.8.25;

contract PayableWhitelist {
    mapping(address => bool) public whitelisted;

    function register() external payable {
        require(msg.value >= 0.05 ether, "whitelist fee is 0.05 eth");
        require(!whitelisted[msg.sender], "already whitelisted");

        whitelisted[msg.sender] = true;
    }

    function isWhitelisted(address _account) external view returns (bool) {
        return whitelisted[_account];
    }
}
