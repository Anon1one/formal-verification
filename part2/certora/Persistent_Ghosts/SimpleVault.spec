/**
 * Ghost varaibles can be havoc'ed:
 * - When the Prover encounters an unresolved external call, or
 * - rolled back to their previous state (reset) when the call reverts.

 * To tell prover to not not to havoc them when it encounters unresolved external call
 * we can use `persistent` ghost, which are not havoced when encounter such issue
 * rest of the time Persistent ghosts are like any other ghost varaibles, they aslo can be havoc'ed in pre-state call
 * but unlike simple ghosts, they will not be havoced when encounters an unresolved external call or reverts
 * therefore they must still be properly constrained as a precondition (via require statements) in rules and initialized using the init_state axiom for invariants’ base cases.
 * and also as you know ghost variables mimics the storage, so they get rolled back when reverts, but
 * presistent ghosts will not revert, they maintains its value (does not havoc) across both unresolved external calls and reverts.

syntax:

persistent ghost bool g_flag;
persistent ghost uint256 g_count;

Or

persistent ghost bool g_flag {
    init_state axiom g_flag == false;
}

persistent ghost uint256 g_count {
    init_state axiom g_count == 0;
}

*/

methods {
    function balanceOf(address) external returns uint256 envfree;
}

/**
 * If you have not used persistent ghost, there could be the case that initially that ghost may be set true (due to havocing, pre-state) and low level call reverts,
 * the ghost varaible should be set to false now, but as the call reverted, the ghost variable will be rolled back to previous state i.e true, which is not correct, 
 * therefore we need to use persistent ghost here
*/

persistent ghost bool g_lowLevelCallSuccess;

hook CALL(uint gas, address to, uint value, uint argsOffset, uint argsLength, uint retOffset, uint retLength) uint returnCode {
    if (returnCode == 0) {
        g_lowLevelCallSuccess = false;
    } else {
        g_lowLevelCallSuccess = true;
    }
}

rule withdraw_revert(env e) {
    uint256 amount;
    require g_lowLevelCallSuccess;

    mathint balanceBefore = balanceOf(e.msg.sender);

    withdraw@withrevert(e, amount);
    bool isLastReverted = lastReverted;

    assert isLastReverted <=> (
        amount > balanceBefore ||   // insufficient balance: withdrawal amount exceeds user balance
        e.msg.value != 0 ||         // non-payable: ETH was sent to this non-payable function
        !g_lowLevelCallSuccess      // transfer failure: low-level call ETH transfer failed
    );
}

/**
 * Persistent ghost should be used carefully
 * One should not add `persistent` keyword as a quick fix to pass failing rules, 
 * this creates a false sense of verification success by ignoring the effects of unknown contract implementations or unresolved calls.
*/