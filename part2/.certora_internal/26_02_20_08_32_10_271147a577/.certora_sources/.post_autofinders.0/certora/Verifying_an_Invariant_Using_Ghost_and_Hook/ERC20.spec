methods{
    function totalSupply() external envfree;
    function balanceOf(address) external returns(uint256) envfree;
}

ghost mathint  g_sumOfBalances{
    init_state axiom g_sumOfBalances == 0;
}

hook Sstore balanceOf[KEY address user] uint256 newVal (uint256 oldVal){
    g_sumOfBalances = g_sumOfBalances + newVal - oldVal;
}

invariant sumOfAllBalancesShouldBeEqualToTotalSupply()
    totalSupply() == g_sumOfBalances;
