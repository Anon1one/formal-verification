/**
 * Partially Parametric Rules:
 * "This partially parametric rule demonstrates conditional logic based on the type of method invoked, allowing for specific actions and assertions tailored to different scenarios within the smart contract."

 rule partiallyParametricExample(env e) {
	method f;

	if (f.selector == sig:exampleMethod1(uint256, address).selector) {
			// method-specific logic
	}
	else if (f.selector == sig:exampleMethod2(address, address).selector) {
			// method-specific logic
	}
	else {
			// method-specific logic
	}
}

*/

methods {
    function balanceOf(address) external returns (uint256) envfree;
    function ownerOf(uint256) external returns (address) envfree;
    function unsafeOwnerOf(uint256) external returns (address) envfree;
    function unsafeGetApproved(uint256) external returns (address) envfree;
    function isApprovedForAll(address,address) external returns (bool) envfree;
    function _.onERC721Received(address,address,uint256,bytes) external => DISPATCHER(true);
}

definition nonpayable(env e) returns bool = e.msg.value == 0;
definition authSanity(env e) returns bool = e.msg.sender != 0;
definition balanceLimited(address account) returns bool = balanceOf(account) < max_uint256;

function helperSoundFnCall(env e, method f) {
    if (f.selector == sig:mint(address,uint256).selector) {
        address to; uint256 tokenId;
        require balanceLimited(to);
        // requireInvariant notMintedUnset(tokenId);
        mint(e, to, tokenId);
    } else if (f.selector == sig:safeMint(address,uint256).selector) {
        address to; uint256 tokenId;
        require balanceLimited(to);
        // requireInvariant notMintedUnset(tokenId);
        safeMint(e, to, tokenId);
    } else if (f.selector == sig:safeMint(address,uint256,bytes).selector) {
        address to; uint256 tokenId; bytes data;
        require data.length < 0xffff;
        require balanceLimited(to);
        // requireInvariant notMintedUnset(tokenId);
        safeMint(e, to, tokenId, data);
    } else if (f.selector == sig:burn(uint256).selector) {
        uint256 tokenId;
        requireInvariant ownerHasBalance(tokenId);
        // requireInvariant notMintedUnset(tokenId);
        burn(e, tokenId);
    } else if (f.selector == sig:transferFrom(address,address,uint256).selector) {
        address from; address to; uint256 tokenId;
        require balanceLimited(to);
        requireInvariant ownerHasBalance(tokenId);
        requireInvariant notMintedUnset(tokenId);
        transferFrom(e, from, to, tokenId);
    } else if (f.selector == sig:safeTransferFrom(address,address,uint256).selector) {
        address from; address to; uint256 tokenId;
        require balanceLimited(to);
        requireInvariant ownerHasBalance(tokenId);
        requireInvariant notMintedUnset(tokenId);
        safeTransferFrom(e, from, to, tokenId);
    } else if (f.selector == sig:safeTransferFrom(address,address,uint256,bytes).selector) {
        address from; address to; uint256 tokenId; bytes data;
        require data.length < 0xffff;
        require balanceLimited(to);
        requireInvariant ownerHasBalance(tokenId);
        requireInvariant notMintedUnset(tokenId);
        safeTransferFrom(e, from, to, tokenId, data);
    } else {
        calldataarg args;
        f(e, args);
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
            require authSanity(e);
        }
    }

invariant notMintedUnset(uint256 tokenId)
    unsafeOwnerOf(tokenId) == 0 => unsafeGetApproved(tokenId) == 0;

invariant balanceOfConsistency(address user)
    to_mathint(balanceOf(user)) == _ownedByUser[user] &&
    to_mathint(balanceOf(user)) == _balances[user];
    
rule supplyChange(env e) {
    require authSanity(e);
    requireInvariant zeroAddressHasNoApprovedOperator(e.msg.sender);

    mathint supplyBefore = _supply;
    method f; helperSoundFnCall(e,f);
    mathint supplyAfter = _supply;

    assert supplyAfter > supplyBefore => (
        supplyAfter == supplyBefore + 1 && (
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
    method f; helperSoundFnCall(e,f);
    mathint balanceAfter = balanceOf(account);

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

