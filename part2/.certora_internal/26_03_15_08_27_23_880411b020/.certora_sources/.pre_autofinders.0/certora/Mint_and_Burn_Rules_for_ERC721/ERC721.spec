methods {
    function balanceOf(address) external returns (uint256) envfree;
    function unsafeOwnerOf(uint256) external returns (address) envfree;
}

definition nonpayable(env e) returns bool = e.msg.value == 0;
definition balanceLimited(address account) returns bool = balanceOf(account) < max_uint256;

ghost mathint _supply {
    init_state axiom _supply == 0;
}
hook Sstore _balances[KEY address addr] uint256 newVal (uint256 oldVal){
    _supply = _supply + newVal - oldVal;
}

rule mint(env e, address to, uint256 tokenId) {
    require nonpayable(e);

    uint256 otherTokenId;
    address otherAccount;

    require balanceLimited(to);

    address ownerBefore = unsafeOwnerOf(tokenId);
    mathint totalSupplyBefore = _supply;
    mathint balanceOfBefore = balanceOf(to);
    mathint balanceOfOther = balanceOf(otherAccount);
    address OwnerOtherToken = unsafeOwnerOf(otherTokenId);

    mint@withrevert(e, to, tokenId);

    bool lastreverted = lastReverted;
    mathint totalSupplyAfter = _supply;
    mathint balanceOfAfter = balanceOf(to);

    assert !lastreverted <=> ( to!= 0 && ownerBefore == 0);
    assert !lastreverted => (
        totalSupplyAfter == totalSupplyBefore + 1 && 
        balanceOfAfter == balanceOfBefore + 1 && 
        unsafeOwnerOf(tokenId) == to
        );
    
    assert balanceOf(otherAccount) != balanceOfOther => otherAccount == to;
    assert unsafeOwnerOf(otherTokenId) != OwnerOtherToken => otherTokenId == tokenId;
}