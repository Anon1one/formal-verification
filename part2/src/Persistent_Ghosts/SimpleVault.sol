// SPDX-License-Identifier: MIT
pragma solidity ^0.8.25;

contract SimpleVault {
    mapping(address => uint256) public balanceOf;

    /// deposit ETH into the vault
    function deposit() external payable {
        balanceOf[msg.sender] += msg.value;
    }

    /// withdraw ETH from the vault
    function withdraw(uint256 amount) external {
        require(balanceOf[msg.sender] >= amount, "Insufficient balance");
        balanceOf[msg.sender] -= amount;

        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "ETH transfer failed");
    }
}
