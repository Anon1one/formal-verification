/**
 * The dispatch line: function _.onERC721Received(address,address,uint256,bytes) external => DISPATCHER(true) instructs the Prover to route onERC721Received() 
 calls to all contracts in the verification scene (_ is a wildcard) that implement onERC721Received() and test its implementation against the balanceOfConsistency invariant. 
 Since we only have one contract that implements onERC721Received, which is the mock receiver, then that is the only contract that the Prover will test.

 * With DISPATCHER(true), only the contracts in the scene are selected for dispatch, and the Prover tries each matching implementation to determine if any can cause a violation.
*/
methods {
    function ownerOf(uint256) external returns (address) envfree;
    function balanceOf(address) external returns (uint256) envfree;
    function unsafeOwnerOf(uint256) external returns (address) envfree;
    function _.onERC721Received(address,address,uint256,bytes) external => DISPATCHER(true);
}

ghost mapping(address => mathint) _balances {
    init_state axiom forall address a. _balances[a] == 0;
}

hook Sload uint256 val _balances[KEY address addr] {
    require _balances[user] == to_mathint(val);
}

ghost mapping(address => mathint) _ownedByUser {
    init_state axiom forall address a. _ownedByUser[a] == 0;
}

hook Sstore _owners[KEY address addr] address newOwner (address oldOwner){
    _ownedByUser[newOwner] = _ownedByUser[newOwner] + to_mathint(newOwner != 0 ? 1:0);
    _ownedByUser[oldOwner] = _ownedByUser[oldOwner] - to_mathint(oldOwner != 0 ? 1:0);
}

invariant balanceOfConsistency(address user)
    to_mathint(balanceOf(user)) == _ownedByUser[user] &&
    to_mathint(balanceOf(user)) == _balances[user];

invariant ownerHasBalance(uint256 tokenId)
    unsafeOwnerOf(tokenId) != 0 => balanceOf(ownerOf(tokenId)) > 0
    {
        preserved {
            requireInvariant balanceOfConsistency(ownerOf(tokenId));
        }
    }