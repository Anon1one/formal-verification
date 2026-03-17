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

    assert lastReverted <=> e.msg.sender != ownerBefore, "caller should be owner";
    assert !lastReverted => owner() == 0, "Owner is not set to 0";
}

rule transferOwnership(env e){
    require nonpayable(e);

    address newOwner;

    address ownerBefore = owner();
    transferOwnership@withrevert(e, newOwner);
    bool success = !lastReverted;

    assert success <=> (e.msg.sender == ownerBefore && newOwner!=0), "caller is not the owner";
    assert success => newOwner == owner(), "Owner is not changed";
}