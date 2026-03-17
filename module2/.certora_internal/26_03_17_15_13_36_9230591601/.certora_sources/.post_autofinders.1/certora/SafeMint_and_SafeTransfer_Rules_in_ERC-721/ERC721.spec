methods {
    function balanceOf(address) external returns (uint256) envfree;
    function unsafeOwnerOf(uint256) external returns (address) envfree;
    function unsafeGetApproved(uint256) external returns (address) envfree;
    function isApprovedForAll(address,address) external returns (bool) envfree;
    function _.onERC721Received(address,address,uint256,bytes) external => DISPATCHER(true);
}

definition nonpayable(env e) returns bool = e.msg.value == 0;
definition authSanity(env e) returns bool = e.msg.sender != 0;
definition balanceLimited(address account) returns bool = balanceOf(account) < max_uint256;

function helperMintWithRevert(env e, method f, address to, uint256 tokenId) {
    if (f.selector == sig:safeMint(address, uint256).selector){
        safeMint(e,to, tokenId);
    } else if (f.selector == sig:safeMint(address, uint256, bytes).selector) {
        bytes params;
        require params.length < 0xffff;
        safeMint(e,to,tokenId,params);
    } else {
        require false;
    }
}

function helperTransferWithRevert(env e, method f, address from, address to, uint256 tokenId) {
    if (f.selector == sig:safeTransferFrom(address,address,uint256).selector) {
        safeTransferFrom(e, from, to, tokenId);
    } else if (f.selector == sig:safeTransferFrom(address,address,uint256,bytes).selector) {
        bytes params;
        require params.length < 0xffff; 
        safeTransferFrom(e, from, to, tokenId, params);
    } else {
        calldataarg args;
        f@withrevert(e, args);
    }
}

ghost mathint _supply {
    init_state axiom _supply == 0;
}

hook Sstore _balances[KEY address addr] uint256 newVal (uint256 oldVal) {
    _supply = _supply - oldVal + newVal;
}

ghost mapping(address => mathint) _balances {
    init_state axiom forall address a. _balances[a] == 0;
}

hook Sload uint256 value _balances[KEY address user] {
    require _balances[user] == to_mathint(value);
}

rule safeMint(env e, method f, address to, uint256 tokenId) filtered { f -> 
    f.selector == sig:safeMint(address, uint256).selector ||
    f.selector == sig:safeMint(address, uint256, bytes).selector
} {
    require nonpayable(e);

    uint256 otherTokenId;
    address otherAccount;

    require balanceLimited(to);

    mathint supplyBefore = _supply;
    uint256 balanceOfToBefore = balanceOf(to);
    uint256 balanceOfOtherBefore = balanceOf(otherAccount);
    address ownerBefore = unsafeOwnerOf(tokenId);
    address otherOwnerBefore = unsafeOwnerOf(otherTokenId);

    helperMintWithRevert@withrevert(e, f, to, tokenId);
    bool success = !lastReverted;

    assert success <=> (
        ownerBefore == 0 &&
        to != 0
    );

    assert success => (
        _supply == supplyBefore + 1 &&
        to_mathint(balanceOf(to)) == balanceOfToBefore + 1 &&
        unsafeOwnerOf(tokenId) == to
    );
    assert balanceOf(otherAccount) != balanceOfOtherBefore => otherAccount == to;
    assert unsafeOwnerOf(otherTokenId) != otherOwnerBefore => otherTokenId == tokenId;
}


rule safeTransferFrom(env e, method f, address from, address to, uint256 tokenId) filtered { f ->
    f.selector == sig:safeTransferFrom(address,address,uint256).selector ||
    f.selector == sig:safeTransferFrom(address,address,uint256,bytes).selector
} {
    require nonpayable(e);
    require authSanity(e);

    address operator = e.msg.sender;
    uint256 otherTokenId;
    address otherAccount;

    require balanceLimited(to);

    uint256 balanceOfFromBefore  = balanceOf(from);
    uint256 balanceOfToBefore    = balanceOf(to);
    uint256 balanceOfOtherBefore = balanceOf(otherAccount);
    address ownerBefore          = unsafeOwnerOf(tokenId);
    address otherOwnerBefore     = unsafeOwnerOf(otherTokenId);
    address approvalBefore       = unsafeGetApproved(tokenId);
    address otherApprovalBefore  = unsafeGetApproved(otherTokenId);

    helperTransferWithRevert@withrevert(e, f, from, to, tokenId);

    bool success = !lastReverted;

    assert success <=> (
        from == ownerBefore &&
        from != 0 &&
        to   != 0 &&
        (operator == from || operator == approvalBefore || isApprovedForAll(ownerBefore, operator))
    );

    assert success => (
        to_mathint(balanceOf(from)) == balanceOfFromBefore - assert_uint256(from != to ? 1: 0) &&
        to_mathint(balanceOf(to))   == balanceOfToBefore   + assert_uint256(from != to ? 1: 0) &&
        unsafeOwnerOf(tokenId)      == to &&
        unsafeGetApproved(tokenId)  == 0
    );

    assert balanceOf(otherAccount)         != balanceOfOtherBefore => (otherAccount == from || otherAccount == to);
    assert unsafeOwnerOf(otherTokenId)     != otherOwnerBefore     => otherTokenId == tokenId;
    assert unsafeGetApproved(otherTokenId) != otherApprovalBefore  => otherTokenId == tokenId;
}