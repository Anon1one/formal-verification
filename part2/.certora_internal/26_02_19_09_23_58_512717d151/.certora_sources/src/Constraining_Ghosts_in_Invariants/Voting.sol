// SPDX-License-Identifier: MIT
pragma solidity ^0.8.25;

/// @title A simple voting contract
contract Voting {

    // `hasVoted[user]` is true if the user voted.
    mapping(address => bool) public hasVoted;

    // keep the count of votes in favor
    uint256 public votesInFavor;

    // keep the count of votes against
    uint256 public votesAgainst; 


    // @notice Allows a user to vote in favor of the proposal.
    function inFavor() external {
        // Ensure the user has not already voted
        require(!hasVoted[msg.sender], "You have already voted.");
        hasVoted[msg.sender] = true;

        votesInFavor += 1;
    }

    /// @notice Allows a user to vote against the proposal.
    function against() external {
        // Ensure the user has not already voted
        require(!hasVoted[msg.sender], "You have already voted.");
        hasVoted[msg.sender] = true;

        votesAgainst += 1;
  }
}
