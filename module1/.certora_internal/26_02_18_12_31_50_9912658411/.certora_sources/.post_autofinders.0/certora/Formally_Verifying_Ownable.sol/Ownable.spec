methods {
    function restricted() external;
    function owner() external returns (address) envfree; 
}


definition nonpayable(env e) returns bool = e.msg.value == 0;

rule onlyOwnerModifierWorks(env e) {
    require nonpayable(e);
    address owner = owner();
    calldataarg args;
    restricted@withrevert(e,args);
    assert lastReverted <=> e.msg.sender != owner, "access control failed";
}