// SPDX-License-Identifier: MIT
pragma solidity ^0.8.25;

contract PointSystem {
    mapping (address => uint256) public pointsOf;
    uint256 public totalPoints;

    function addPoints(address _user, uint256 _amount) external {
        pointsOf[_user] += _amount;
        totalPoints += _amount;
    }
}
