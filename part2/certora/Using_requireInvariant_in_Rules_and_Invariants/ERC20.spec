/**
 * Sometimes you need other invaraint to be true first, before proceeding with new rule/invaraint
 * you can use `requireInvariant` in order to tell prover that that invariant is req first to prove this one 
*/

methods {
    function totalSupply() external returns(uint256) envfree;
    function balanceOf(address) external returns(uint256) envfree; // Add this
}

ghost mathint g_sumOfBalances{
    init_state axiom g_sumOfBalances == 0;
}

hook Sstore balanceOf[KEY address user] uint256 newVal (uint256 oldVal){
    require oldVal <= g_sumOfBalances; 
    g_sumOfBalances = g_sumOfBalances + newVal - oldVal;
}

invariant sumOfAllBalancesShouldBeEqualToTotalSupply()
    totalSupply() == g_sumOfBalances;

// `requireInvariant` in "rule"

// If we run this rule without requireInvariant, this would fail, as the prover will havoc, such that 
// initial individual balances will not be equal to totalSupply, so we need that invariant first to be considered by the prover
rule checkTransferSuccess(env e){

    requireInvariant sumOfAllBalancesShouldBeEqualToTotalSupply();

    address to;
    uint256 amount;

    require e.msg.sender != currentContract;
    require e.msg.sender != to;

    mathint precallSenderBalance   = balanceOf(e.msg.sender);
    mathint precallReceiverBalance = balanceOf(to);
    mathint precallTotalSupply = totalSupply();

    transfer(e, to, amount);

    mathint postcallSenderBalance   = balanceOf(e.msg.sender);
    mathint postcallReceiverBalance = balanceOf(to);
    mathint postcallTotalSupply = totalSupply();
    
    assert postcallSenderBalance == precallSenderBalance - amount;
    assert postcallReceiverBalance == precallReceiverBalance + amount;
    assert precallTotalSupply == postcallTotalSupply;
}

// `requireInvariant` in "invariant"

invariant indBalanceCap(address a)
    to_mathint(balanceOf(a)) <= to_mathint(totalSupply())
{
    preserved with (env e) {
        requireInvariant sumOfAllBalancesShouldBeEqualToTotalSupply();
    }
}

// we could have also use simple `require` instead of `requireInvariant`, but they differ in reliability
// requireInvariant enforces a condition already proven to be universally true.
// while `require`, enfore the condition defines by us, which may be incomplete/wrong/too much constraining etc
// There it is better to use `requireInvariant` when you can use it
