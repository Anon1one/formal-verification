/**
 * write rules for functions that expect a non-zero payment (i.e., functions marked as payable)
 * how to make assertions about account balances
 * how to get the balance of the current contract, akin to address(this).balance in Solidity
*/

// methods {
//     function isWhitelisted(address) external returns(bool);
// }

definition fee() returns uint256 = 50000000000000000;

rule particularFeeShouldBePayedToRegister() {
    env e;

    require !isWhitelisted(e.msg.sender);

    require(e.msg.value >= fee());

    register@withrevert(e);
    assert !lastReverted;
}