// SPDX-License-Identifier: MIT
pragma solidity ^0.8.25; 

import "./ERC20.sol";

contract ERC20Harness is ERC20 {    
    constructor (
        string memory _name, 
        string memory _symbol, 
        uint8 _decimals
    ) ERC20(_name, _symbol, _decimals) {}
    
    /// Left without access controls; integrators are expected to implement their own.
    function mint(address _to, uint256 _amount) external {
        _mint(_to, _amount);
    }
	
    /// Left without access controls; integrators are expected to implement their own.
    function burn(address _from, uint256 _amount) external {
        _burn(_from, _amount);
    }
}
