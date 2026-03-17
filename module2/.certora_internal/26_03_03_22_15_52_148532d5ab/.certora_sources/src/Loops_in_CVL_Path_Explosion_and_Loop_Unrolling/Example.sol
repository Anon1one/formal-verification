// SPDX-License-Identifier: MIT
pragma solidity ^0.8.25;

contract Example {
    string public txt;

    function setTxt(string memory _txt) external {
        txt = _txt;
    }
}
