// SPDX-License-Identifier: MIT
pragma solidity ^0.8.25;

contract Counter {
    // State variables
    address private owner;
    uint256 private count;

    /// @notice Initializes the contract and sets the deployer as the owner
    constructor() {
        owner = msg.sender;
    }

    /// @notice Restricts function calls to the contract owner only
    modifier onlyOwner() {
        require(msg.sender == owner, "Counter: caller is not the owner");
        _;
    }

    // External functions

    /// @notice Increments the counter by 1
    /// @dev Only callable by the owner
    function increment() external onlyOwner {
        count++;
    }

    /// @notice Resets the counter to 0
    /// @dev Only callable by the owner
    function resetCounter() external onlyOwner {
        count = 0;
    }
}
