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

    assert success <=> (e.msg.sender == ownerBefore && newOwner!=0), "caller is not the current owner";
    assert success => newOwner == owner(), "Owner was not changed after Ownership transfer";
}

rule ownershipCanOnlyBeChangesThroughtransferOwnershipOrrenounceOwnership(env e){
    require nonpayable(e);

    address ownerBefore = owner();
    method f; calldataarg args;
    f(e,args);
    address ownerAfter = owner();

    assert ownerBefore != ownerAfter => (
        (e.msg.sender==ownerBefore && ownerAfter!=0 && f.selector == sig:transferOwnership(address).selector) ||
        (e.msg.sender==ownerBefore && ownerAfter==0 && f.selector == sig:renounceOwnership().selector)
    );
}