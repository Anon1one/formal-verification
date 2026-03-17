// storage hook
/**
 * we need this hook because lets say 'owner' variable is private and there is no getter for it
 * Standard CVL rules are limited to interacting with the contract through its public interface, so they cannot capture these internal changes.
 * therefore cvl cannot access this variable directly, hence we need hooks
*/

/**
 * Limitations with hooks:
 * CVL variables defined inside hooks are scoped locally to the hook, meaning they cannot be accessed directly for rules.
 * and the solution -> ghost variables -> persistent, specification-level storage that mirrors or extends the contract’s actual state
 * Ghost variables are special variables that allow to communicate information between hooks and rules
*/

/**
 * when declaring ghost variables it is important to prefix them with 'ghost' or 'ghost_'
 * Certora Prover treats ghost variables much like regular storage:
 * 1. Any update to a ghost is reverted automatically if the transaction in progress later reverts, just like storage.
 * 2. At the start of a verification run, ghosts (as with other CVL variables) represent arbitrary (havoced) values 
 * unless they are explicitly set in the specification, reflecting the Prover’s symbolic view of storage.
*/

methods{
    function increment() external;
}

ghost address ghost_Owner;
ghost uint256 ghost_preCount;
ghost uint256 ghost_postCount;

hook Sstore count uint256 postCount (uint256 preCount){
    ghost_preCount = preCount;
    ghost_postCount = postCount;
}

// whenever there is read operation (sload) on variable 'owner' storage slot, this hook will be trigerred and store it in contractOwner
hook Sload address contractOwner owner { 
    ghost_Owner = contractOwner;
}

// suppose we want to verify that the owner must never change once set in contructor
rule checkOwnerConsistency(env e) {

    resetCounter(e);

    address prevOwner = ghost_Owner;
    method f;
    calldataarg args;
    f(e, args);

    address currentOwner = ghost_Owner;
    assert prevOwner == currentOwner;
}

rule checkOnOneCallIncrementShouldOnlyIncreaseCountByOne (){
    env e;
    increment(e);
    assert ghost_postCount == ghost_preCount + 1;
}