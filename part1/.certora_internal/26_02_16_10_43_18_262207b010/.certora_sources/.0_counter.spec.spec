// function that are non-envfreee are need not to be necessarily included in methods block
// so we can exclude increment function from methods block

methods {
    function owner() external returns(address) envfree;
    function counter() external returns (uint256) envfree;

    // function increment() external;
}

rule OnlyOwnerCanCallIncrement() {
    env e;

    require(e.msg.value == 0);

    address owner = owner();

    increment@withrevert(e);

    assert !lastReverted <=> e.msg.sender == owner; // if increment does not revert, then msg.sender is the owner
}