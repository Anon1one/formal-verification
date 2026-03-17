methods {
    function balanceOf(address) external returns uint256 envfree;
    function totalSupply() external returns uint256 envfree;
}

rule deposit_amountOfEthDepositedShouldBeEqualToWethRecieved(env e){
    require e.msg.sender != currentContract;
    require balanceOf(e.msg.sender) + e.msg.value <= max_uint256;
    mathint ethBalanceBefore = nativeBalances[e.msg.sender];
    mathint wethBalanceBefore = balanceOf(e.msg.sender);

    deposit(e);

    mathint ethBalanceAfter = nativeBalances[e.msg.sender];
    mathint wethBalanceAfter = balanceOf(e.msg.sender);

    assert ethBalanceAfter == ethBalanceBefore - e.msg.value;
    assert wethBalanceAfter == wethBalanceBefore + e.msg.value;
}

rule deposit_increasesTotalSupply(env e) {
    mathint totalSupplyBefore = totalSupply();

    deposit(e);
    mathint totalSupplyAfter = totalSupply();

    assert totalSupplyAfter == totalSupplyBefore + e.msg.value;
}

rule deposit_revert(env e) {
    address caller = e.msg.sender;
    address ethDeposit = e.msg.value;
    require balanceOf(caller) + ethDeposit <= max_uint256;

    mathint totalSupplyBefore = totalSupply();
    mathint ethBalanceBefore = nativeBalances[caller];

    deposit@withrevert(e);

    assert lastReverted <=> (ethBalanceBefore <= ethDeposit || totalSupplyBefore + ethDeposit > max_uint256);
}