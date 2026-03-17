methods{
    function totalSupply() external returns(uint256) envfree;
    function balanceOf(address) external returns(uint256) envfree;
}

ghost mathint g_sumOfBalances{
    init_state axiom g_sumOfBalances == 0;
}

// the store hook only says: “If you ever touch this slot by writing to it, then the previous value must be reasonable.” 
// It does not say: “All balances are always reasonable whenever you look at them.”
// so the havoced values may still persist if Sstore is not triggered
// therefore that alternative method is more reliable

hook Sstore balanceOf[KEY address user] uint256 newVal (uint256 oldVal){
    require oldVal <= g_sumOfBalances; 
    g_sumOfBalances = g_sumOfBalances + newVal - oldVal;
}

invariant sumOfAllBalancesShouldBeEqualToTotalSupply()
    totalSupply() == g_sumOfBalances;

/**
 * In this alternative method (more reliable method), we are using sload,
 * every time the Prover reads a balance from balanceOf, 
 * we are telling the Prover: “Whenever you read a balance, that balance must be less than or equal to sumOfBalances”
 * This applies even if the slot was never written to. 
 * The Prover might havoc balanceOf[addr] to some arbitrary value at the start, but the moment it reads that value, the load hook checks it. 
 * If the value is impossible, that whole path is thrown away.
*/

/**Alternatively:

methods{
    function totalSupply() external returns(uint256) envfree;
    function balanceOf(address) external returns(uint256) envfree;
}

ghost mathint g_sumOfBalances{
    init_state axiom g_sumOfBalances == 0;
}

hook Sload uint256 val balanceOf[KEY address user] {
    require val <= g_sumOfBalances;
}
hook Sstore balanceOf[KEY address user] uint256 newVal (uint256 oldVal){
    g_sumOfBalances = g_sumOfBalances + newVal - oldVal;
}

invariant sumOfAllBalancesShouldBeEqualToTotalSupply()
    (totalSupply()) == g_sumOfBalances;
*/
