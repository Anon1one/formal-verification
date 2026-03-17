methods {
    function balanceOf(address) external returns (uint256) envfree;
    function ownerOf(uint256) external returns (address) envfree;
    function isApprovedForAll(address,address) external returns (bool) envfree;
    function unsafeOwnerOf(uint256) external returns (address) envfree;
    function unsafeGetApproved(uint256) external returns (address) envfree;
    function _.onERC721Received(address,address,uint256,bytes) external => DISPATCHER(true);
}

definition balanceLimited(address account) returns bool = balanceOf(account) < max_uint256;
definition nonzerosender(env e) returns bool = e.msg.sender != 0;

function helperSoundFnCall(env e, method f) {
    if (f.selector == sig:mint(address,uint256).selector) {
        address to; uint256 tokenId;
        require balanceLimited(to);
        mint(e, to, tokenId);
    } else if (f.selector == sig:safeMint(address,uint256).selector) {
        address to; uint256 tokenId;
        require balanceLimited(to);
        safeMint(e, to, tokenId);
    } else if (f.selector == sig:safeMint(address,uint256,bytes).selector) {
        address to; uint256 tokenId; bytes data;
        require data.length < 0xffff;
        require balanceLimited(to);
        safeMint(e, to, tokenId, data);
    } else if (f.selector == sig:burn(uint256).selector) {
        uint256 tokenId;
        requireInvariant ownerHasBalance(tokenId);
        burn(e, tokenId);
    } else if (f.selector == sig:transferFrom(address,address,uint256).selector) {
        address from; address to; uint256 tokenId;
        require balanceLimited(to);
        requireInvariant ownerHasBalance(tokenId);
        //requireInvariant notMintedUnset(tokenId);
        transferFrom(e, from, to, tokenId);
    } else if (f.selector == sig:safeTransferFrom(address,address,uint256).selector) {
        address from; address to; uint256 tokenId;
        require balanceLimited(to);
        requireInvariant ownerHasBalance(tokenId);
        //requireInvariant notMintedUnset(tokenId);
        safeTransferFrom(e, from, to, tokenId);
    } else if (f.selector == sig:safeTransferFrom(address,address,uint256,bytes).selector) {
        address from; address to; uint256 tokenId; bytes data;
        require data.length < 0xffff;
        require balanceLimited(to);
        requireInvariant ownerHasBalance(tokenId);
        //requireInvariant notMintedUnset(tokenId);
        safeTransferFrom(e, from, to, tokenId, data);
    } else {
        calldataarg args;
        f(e, args);
    }
}

ghost mapping(address => mathint) _ownedByUser {
    init_state axiom forall address a. _ownedByUser[a] == 0;
}

hook Sstore _owners[KEY uint256 tokenId] address newOwner (address oldOwner) {
    _ownedByUser[newOwner] = _ownedByUser[newOwner] + to_mathint(newOwner != 0 ? 1 : 0);
    _ownedByUser[oldOwner] = _ownedByUser[oldOwner] - to_mathint(oldOwner != 0 ? 1 : 0);
}

ghost mathint _supply {
    init_state axiom _supply == 0;
}

ghost mapping(address => mathint) _balances {
    init_state axiom forall address a. _balances[a] == 0;
}

hook Sstore _balances[KEY address addr] uint256 newValue (uint256 oldValue) {
    _supply = _supply - oldValue + newValue;
}

hook Sload uint256 value _balances[KEY address user] {
    require _balances[user] == to_mathint(value);
}

invariant balanceOfConsistency(address user)
    to_mathint(balanceOf(user)) == _ownedByUser[user] &&
    to_mathint(balanceOf(user)) == _balances[user];

invariant ownerHasBalance(uint256 tokenId)
    unsafeOwnerOf(tokenId) != 0 => balanceOf(ownerOf(tokenId)) > 0 // fixed for Prover v8.3.1
    {
        preserved {
            requireInvariant balanceOfConsistency(ownerOf(tokenId));
        }
    }

invariant zeroAddressHasNoApprovedOperator(address a)
    !isApprovedForAll(0, a)
    {
        preserved with (env e) {
            require nonzerosender(e);
        }
    }

// invariant notMintedUnset(uint256 tokenId)
//     unsafeOwnerOf(tokenId) == 0 => unsafeGetApproved(tokenId) == 0;


rule supplyChange(env e) {
    require nonzerosender(e);
    requireInvariant zeroAddressHasNoApprovedOperator(e.msg.sender);

    mathint supplyBefore = _supply;
    method f; helperSoundFnCall(e, f);
    mathint supplyAfter = _supply;

    assert supplyAfter > supplyBefore => (
        supplyAfter == supplyBefore + 1 &&
        (
            f.selector == sig:mint(address,uint256).selector ||
            f.selector == sig:safeMint(address,uint256).selector ||
            f.selector == sig:safeMint(address,uint256,bytes).selector
        )
    );
    assert supplyAfter < supplyBefore => (
        supplyAfter == supplyBefore - 1 &&
        f.selector == sig:burn(uint256).selector
    );
}

rule balanceChange(env e, address account) {

    mathint balanceBefore = balanceOf(account);
    method f; helperSoundFnCall(e, f);
    mathint balanceAfter  = balanceOf(account);

    assert balanceBefore != balanceAfter => (
        balanceAfter == balanceBefore - 1 ||
        balanceAfter == balanceBefore + 1
    );

    assert balanceBefore != balanceAfter => (
        f.selector == sig:transferFrom(address,address,uint256).selector ||
        f.selector == sig:safeTransferFrom(address,address,uint256).selector ||
        f.selector == sig:safeTransferFrom(address,address,uint256,bytes).selector ||
        f.selector == sig:mint(address,uint256).selector ||
        f.selector == sig:safeMint(address,uint256).selector ||
        f.selector == sig:safeMint(address,uint256,bytes).selector ||
        f.selector == sig:burn(uint256).selector
    );
}

rule ownershipChange(env e, uint256 tokenId) {
    require nonzerosender(e);
    requireInvariant zeroAddressHasNoApprovedOperator(e.msg.sender);

    address ownerBefore = unsafeOwnerOf(tokenId);
    method f; helperSoundFnCall(e, f);
    address ownerAfter  = unsafeOwnerOf(tokenId);

    assert ownerBefore == 0 && ownerAfter != 0 => (
        f.selector == sig:mint(address,uint256).selector ||
        f.selector == sig:safeMint(address,uint256).selector ||
        f.selector == sig:safeMint(address,uint256,bytes).selector
    );

    assert ownerBefore != 0 && ownerAfter == 0 => (
        f.selector == sig:burn(uint256).selector
    );

    assert (ownerBefore != ownerAfter && ownerBefore != 0 && ownerAfter != 0) => (
        f.selector == sig:transferFrom(address,address,uint256).selector ||
        f.selector == sig:safeTransferFrom(address,address,uint256).selector ||
        f.selector == sig:safeTransferFrom(address,address,uint256,bytes).selector
    );
}

rule approvalChange(env e, uint256 tokenId) {
    address approvalBefore = unsafeGetApproved(tokenId);
    method f; helperSoundFnCall(e, f);
    address approvalAfter  = unsafeGetApproved(tokenId);

    assert approvalBefore != approvalAfter => (
        f.selector == sig:approve(address,uint256).selector ||
        (
            (
                f.selector == sig:transferFrom(address,address,uint256).selector ||
                f.selector == sig:safeTransferFrom(address,address,uint256).selector ||
                f.selector == sig:safeTransferFrom(address,address,uint256,bytes).selector ||
                f.selector == sig:burn(uint256).selector
            ) && approvalAfter == 0
        )
    );
}

rule approvedForAllChange(env e, address owner, address spender) {
    bool approvedForAllBefore = isApprovedForAll(owner, spender);
    method f; helperSoundFnCall(e, f);
    bool approvedForAllAfter  = isApprovedForAll(owner, spender);

    assert approvedForAllBefore != approvedForAllAfter => f.selector == sig:setApprovalForAll(address,bool).selector;
}
