methods{
    function nonces(address) external returns(uint256) envfree;
    function useNonce(address account) external returns (uint256) envfree;
    function useCheckedNonce(address, uint256) external envfree;
}

// Helper function
function nonceSanity(address account) returns bool {
    return nonces(account) < max_uint256;
}

rule nonceOnlyIncrements(env e, method f, calldataarg args, address account) {
    require nonceSanity(account);
    mathint nonceBefore = useNonce(account);
    f(e, args);
    mathint nonceAfter = useNonce(account);

    assert nonceBefore == nonceAfter || nonceAfter == nonceBefore + 1, "nonce cant decrease";
}