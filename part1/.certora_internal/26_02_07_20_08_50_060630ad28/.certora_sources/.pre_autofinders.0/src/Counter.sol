// SPDX-License-Identifier: MIT  
pragma solidity ^0.8.25;  

contract Counter {  
    uint256 public count;  

    // Increment the count  
    function increment() public {  
        count += 1;  
    }  

    // Decrement the count  
    function decrement() public {    
        count -= 1;  
    }  

}
