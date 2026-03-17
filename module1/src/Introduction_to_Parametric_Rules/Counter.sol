// SPDX-License-Identifier: MIT
pragma solidity 0.8.25;

contract Counter {
    uint256 public count;
    address public owner;
    
    // Define custom errors
    error Unauthorized();
    error InvalidAddress();
    
    // Emit events for important state changes
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);
    event CountUpdated(uint256 newCount);

    constructor() {
        owner = msg.sender;
        emit OwnershipTransferred(address(0), msg.sender);
    }
    
  
  modifier onlyOwner() {

        if (msg.sender != owner) revert Unauthorized();
        _;
    }

    function increment() external {
        count += 1;
        emit CountUpdated(count);
    }

    function transferOwnership(address _newOwner) external onlyOwner {
        if (_newOwner == address(0)) revert InvalidAddress();
        emit OwnershipTransferred(owner, _newOwner);
        owner = _newOwner;
    }
}
