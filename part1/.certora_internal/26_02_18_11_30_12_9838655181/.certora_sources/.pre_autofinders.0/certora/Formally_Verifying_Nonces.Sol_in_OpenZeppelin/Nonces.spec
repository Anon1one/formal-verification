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
    mathint nonceBefore = nonces(account);
    f(e, args);
    mathint nonceAfter = nonces(account);

    assert nonceBefore == nonceAfter || nonceAfter == nonceBefore + 1, "nonce cant decrease";
}

rule useNonceCheck(address account){
    require nonceSanity(account);

    address other;

    mathint nonceBeforeOther = nonces(other);
    mathint nonceBefore = nonces(account);


    mathint nonceUsed = useNonce@withrevert(account);
    bool success = !lastReverted;

    mathint nonceAfterOther = nonces(other);
    mathint nonceAfter = nonces(account);

    assert success;

    assert nonceAfter == nonceBefore + 1 && nonceBefore == nonceUsed;

    assert nonceAfterOther != nonceBeforeOther => other == account, "Other account nonce should not increase";
}