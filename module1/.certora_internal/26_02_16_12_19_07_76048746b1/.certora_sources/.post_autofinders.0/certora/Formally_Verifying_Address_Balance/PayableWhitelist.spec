/**
 * write rules for functions that expect a non-zero payment (i.e., functions marked as payable)
 * how to make assertions about account balances
 * how to get the balance of the current contract, akin to address(this).balance in Solidity
*/

// "nativeBalances[address]", this is a built-in cvl function, that retrieves the current ETH balance of a given address. 
// "currentContract"  is a built-in variable that refers to the contract being verified.

methods {
    function isWhitelisted(address) external returns(bool) envfree;
}

definition fee() returns uint256 = 50000000000000000;

rule particularFeeShouldBePayedToRegister() {
    env e;

    require !isWhitelisted(e.msg.sender);

    // through this require we want the ether balance of the msg.sender should be greater than the msg.value
    // so that prover wont revert because of balance issue
    require nativeBalances[e.msg.sender] >= e.msg.value; // "nativeBalances[address]", this is a built-in cvl function, that retrieves the current ETH balance of a given address. 

    register@withrevert(e);
    assert lastReverted <=> e.msg.value < 5*10^16;
}

rule particularFeeShouldBePayedToRegister_modified() {
    env e;

    require !isWhitelisted(e.msg.sender);
    require nativeBalances[e.msg.sender] >= e.msg.value; 

    register@withrevert(e);
    assert lastReverted <=> e.msg.value < 5*10^16 && !isWhitelisted(e.msg.sender);
}

rule particularFeeShouldBePayedToRegister_implication(){
    env e;
    register@withrevert(e);
    assert e.msg.value < fee() => lastReverted;
}

// after register is called the contract balance should increase by msg.value
rule checkBalances() {
    env e;
    // passing "currentContract" to "nativeBalances" will give the current eth balance of the contract that is being verified
    mathint balanceBefore = nativeBalances[currentContract]; // "currentContract"  is a built-in variable that refers to the contract being verified.
    require e.msg.sender != currentContract; // if msg.sender==currentContract, then the balance will not increase, as contract itself has called register
    require e.msg.value >= fee();
    require nativeBalances[e.msg.sender] >= e.msg.value; 

    register@withrevert(e);
    mathint balanceAfter = nativeBalances[currentContract];

    assert balanceAfter == balanceBefore + e.msg.value;
}