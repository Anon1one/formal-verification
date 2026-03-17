/**
 * write rules for functions that expect a non-zero payment (i.e., functions marked as payable)
 * how to make assertions about account balances
 * how to get the balance of the current contract, akin to address(this).balance in Solidity
*/

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