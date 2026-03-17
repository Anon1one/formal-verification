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
    mathint ethDeposit = e.msg.value;
    require balanceOf(caller) + ethDeposit <= max_uint256;

    mathint totalSupplyBefore = totalSupply();
    mathint ethBalanceBefore = nativeBalances[caller];

    deposit@withrevert(e);

    assert lastReverted <=> (ethBalanceBefore < ethDeposit || totalSupplyBefore + ethDeposit > max_uint256);
}

rule withdraw_decreaseWethIncreaseEthBySameAmount(env e){
    uint256 amount;
    require e.msg.sender != currentContract;

    mathint ethBalanceBefore = nativeBalances[e.msg.sender];
    mathint wethBalanceBefore = balanceOf(e.msg.sender);

    withdraw(e,amount);

    mathint ethBalanceAfter = nativeBalances[e.msg.sender];
    mathint wethBalanceAfter = balanceOf(e.msg.sender);

    assert ethBalanceAfter == ethBalanceBefore + amount;
    assert wethBalanceAfter == wethBalanceBefore - amount;
}

rule withdraw_decreasesTotalSupply(env e) {
    uint256 amount;
    
	require balanceOf(e.msg.sender) <= totalSupply(); 
    mathint totalSupplyBefore = totalSupply();
    
    withdraw(e, amount);
    mathint totalSupplyAfter = totalSupply();

    assert totalSupplyAfter == totalSupplyBefore - amount;
}


persistent ghost bool g_lowLevelCallFail;

hook CALL(uint gas, address to, uint value, uint argsOffset, uint argsLength, uint retOffset, uint retLength) uint rc{
    if(rc == 0){
        g_lowLevelCallFail = true;
    }else{
        g_lowLevelCallFail = false;
    }
}

rule withdraw_revert(env e) {
    uint256 amount;
    address caller = e.msg.sender;

    mathint balanceOfCaller = balanceOf(caller);
    withdraw@withrevert(e,amount);

    assert lastReverted <=> (balanceOfCaller < amount || e.msg.value != 0 || g_lowLevelCallFail);
}

