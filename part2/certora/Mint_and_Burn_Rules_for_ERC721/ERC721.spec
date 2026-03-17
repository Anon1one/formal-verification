/**
 * Liveness — specifies the conditions under which the function does not revert.
 * Effect — specifies the state changes that occurred when the function did not revert.
 * No side-effect — specifies that no unintended state changes occur beyond those in the Effect assertion.
*/

methods {
    function balanceOf(address) external returns (uint256) envfree;
    function unsafeOwnerOf(uint256) external returns (address) envfree;
    function unsafeGetApproved(uint256) external returns (address) envfree;
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

    // liveness
    assert !lastreverted <=> ( to!= 0 && ownerBefore == 0);

    // effect
    assert !lastreverted => (
        totalSupplyAfter == totalSupplyBefore + 1 && 
        balanceOfAfter == balanceOfBefore + 1 && 
        unsafeOwnerOf(tokenId) == to
        );
    
    // no side effect
    assert balanceOf(otherAccount) != balanceOfOther => otherAccount == to;
    assert unsafeOwnerOf(otherTokenId) != OwnerOtherToken => otherTokenId == tokenId;
}

rule burn(env e, uint256 tokenId){

    require nonpayable(e);
    uint256 otherTokenId;
    address otherAccount;

    address owner = unsafeOwnerOf(tokenId);
    uint256 balanceOfOwnerBefore =  balanceOf(owner);
    uint256 balanceOfOtherBefore = balanceOf(otherAccount);
    mathint _supplyBefore = _supply;
    address otherOwnerBefore     = unsafeOwnerOf(otherTokenId);
    address otherApprovalBefore  = unsafeGetApproved(otherTokenId);

    burn@withrevert(e, tokenId);
    bool lastreverted = lastReverted;

    // liveness
    assert !lastreverted <=> (owner != 0);

    // effect
    assert !lastreverted => (
        unsafeOwnerOf(tokenId) !=0 =>(_supply == _supplyBefore - 1)  && 
        balanceOf(owner) == balanceOfOwnerBefore - 1 && 
        unsafeOwnerOf(tokenId) == 0 && unsafeGetApproved(tokenId) == 0
    );

    // no side effect
    assert balanceOf(otherAccount) == balanceOfOtherBefore => otherAccount != owner;
    assert unsafeOwnerOf(otherTokenId) != otherOwnerBefore => otherTokenId == tokenId;
    assert unsafeGetApproved(otherTokenId) != otherApprovalBefore => otherTokenId == tokenId;
}