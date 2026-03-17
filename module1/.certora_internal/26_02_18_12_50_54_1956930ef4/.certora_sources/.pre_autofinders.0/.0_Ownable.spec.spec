methods {
    function owner() external returns (address) envfree; 
}

definition nonpayable(env e) returns bool = e.msg.value == 0;

rule onlyOwnerModifierWorks(env e) {
    require nonpayable(e);
    address owner = owner();
    restricted@withrevert(e);
    assert lastReverted <=> e.msg.sender != owner, "access control failed";
}

rule renounceOwnership(env e) {
    require nonpayable(e);
    address ownerBefore = owner();

    renounceOwnership@withrevert(e);

    address ownerAfter = owner();

    assert lastReverted <=> e.msg.sender != ownerBefore;
    assert !lastReverted => ownerAfter == address(0);
}