methods {
    function balanceOf(address) external returns uint256 envfree;
    function totalSupply() external returns uint256 envfree;
}

rule deposit_amountOfEthDepositedShouldBeEqualToWethRecieved(env e){
    require e.msg.sender != currentContract;
    require balanceOf(e.msg.sender) + e.msg.value <= max_uint256;
    mathint ethBalanceBefore = nativeBalances[e.msg.sender];
    mathint wethBalancesBefore = balanceOf(e.msg.sender);

    deposit(e);

    mathint ethBalanceAfter = nativeBalances[e.msg.sender];
    mathint wethBalanceAfter = balanceOf(e.msg.sender);

    assert ethBalanceAfter == ethBalanceBefore - e.msg.value;
    assert wethBalanceAfter == wethBalanceBefore + e.msg.value;
}
