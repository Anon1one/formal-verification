/**
 * following pattern of preconditions, pre-call and post-call states, and the method call then
 * Verification Model:
 * Liveness: When the function should succeed or revert.
 * Effect: What state changes must occur if it succeeds.
 * No side effects: Ensure unrelated storage is unchanged.
*/

methods {
    function balanceOf(address) external returns (uint256) envfree;
    function ownerOf(uint256) external returns (address) envfree;
    function unsafeOwnerOf(uint256) external returns (address) envfree;
    function unsafeGetApproved(uint256) external returns (address) envfree;
    function isApprovedForAll(address,address) external returns (bool)    envfree;

    function _.onERC721Received(address,address,uint256,bytes) external => DISPATCHER(true);
}

definition nonpayable(env e) returns bool = e.msg.value == 0;
definition balanceLimited(address account) returns bool = balanceOf(account) < max_uint256;
definition authSanity(env e) returns bool = e.msg.sender != 0;

ghost mapping(address => mathint) _ownedByUser {
    init_state axiom forall address a. _ownedByUser[a] == 0;
}

hook Sstore _owners[KEY uint256 tokenId] address newOwner (address oldOwner) {
    _ownedByUser[newOwner] = _ownedByUser[newOwner] + to_mathint(newOwner != 0 ? 1 : 0);
    _ownedByUser[oldOwner] = _ownedByUser[oldOwner] - to_mathint(oldOwner != 0 ? 1 : 0);
}

ghost mapping(address => mathint) _balances {
    init_state axiom forall address a. _balances[a] == 0;
}

hook Sload uint256 value _balances[KEY address user] {
    require _balances[user] == to_mathint(value);
}

invariant balanceOfConsistency(address user)
    to_mathint(balanceOf(user)) == _ownedByUser[user] &&
    to_mathint(balanceOf(user)) == _balances[user];

invariant ownerHasBalance(uint256 tokenId)
    unsafeOwnerOf(tokenId) != 0 => balanceOf(ownerOf(tokenId)) > 0 // fixed for Prover V8
    {
        preserved {
            requireInvariant balanceOfConsistency(ownerOf(tokenId));
        }
    }

rule transferFrom(env e, address from, address to, uint256 tokenId) {
    require nonpayable(e);
    require authSanity(e);

    address operator = e.msg.sender;
    uint256 otherTokenId;
    address otherAccount;

    requireInvariant ownerHasBalance(tokenId);
    require balanceLimited(to);

    uint256 balanceOfFromBefore  = balanceOf(from);
    uint256 balanceOfToBefore    = balanceOf(to);
    uint256 balanceOfOtherBefore = balanceOf(otherAccount);
    address ownerBefore          = unsafeOwnerOf(tokenId);
    address otherOwnerBefore     = unsafeOwnerOf(otherTokenId);
    address approvalBefore       = unsafeGetApproved(tokenId);
    address otherApprovalBefore  = unsafeGetApproved(otherTokenId);

    transferFrom@withrevert(e, from, to, tokenId);
    bool success = !lastReverted;

    // liveness
    assert success <=> (
        from == ownerBefore &&
        from != 0 &&
        to   != 0 &&
        (operator == from || operator == approvalBefore || isApprovedForAll(ownerBefore, operator))
    );

    // effect
    assert success => (
        to_mathint(balanceOf(from))            == balanceOfFromBefore - assert_uint256(from != to ? 1 : 0) &&
        to_mathint(balanceOf(to))              == balanceOfToBefore   + assert_uint256(from != to ? 1 : 0) &&
        unsafeOwnerOf(tokenId)                 == to &&
        unsafeGetApproved(tokenId)             == 0
    );

    // no side effect
    assert balanceOf(otherAccount)         != balanceOfOtherBefore => (otherAccount == from || otherAccount == to);
    assert unsafeOwnerOf(otherTokenId)     != otherOwnerBefore     => otherTokenId == tokenId;
    assert unsafeGetApproved(otherTokenId) != otherApprovalBefore  => otherTokenId == tokenId;
}

rule approve(env e, address spender, uint256 tokenId) {
    require nonpayable(e);
    require authSanity(e);

    address caller = e.msg.sender;
    address owner = unsafeOwnerOf(tokenId);
    uint256 otherTokenId;

    address otherApprovalBefore  = unsafeGetApproved(otherTokenId);

    approve@withrevert(e, spender, tokenId);
    bool success = !lastReverted;

    // liveness
    assert success => (
        owner != 0 &&
        (owner == caller || isApprovedForAll(owner, caller))
    );

    // effect
    assert success => unsafeGetApproved(tokenId) == spender;

    // no side effect
    assert unsafeGetApproved(otherTokenId) != otherApprovalBefore  => otherTokenId == tokenId;
}


rule setApprovalForAll(env e, address operator, bool approved) {
    require nonpayable(e);

    address owner = e.msg.sender;
    address otherOwner;
    address otherOperator;

    bool otherIsApprovedForAllBefore = isApprovedForAll(otherOwner, otherOperator);

    setApprovalForAll@withrevert(e, operator, approved);
    bool success = !lastReverted;

    assert success => operator != 0;
    assert success => isApprovedForAll(owner, operator) == approved;
    assert isApprovedForAll(otherOwner, otherOperator) != otherIsApprovedForAllBefore => (
        otherOwner == owner &&
        otherOperator == operator
    );
}

rule zeroAddressBalanceRevert() {
    balanceOf@withrevert(0);
    assert lastReverted;
}