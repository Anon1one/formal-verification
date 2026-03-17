methods {
    function mod(uint256, uint256) external returns(uint256) envfree;
    function max(uint256, uint256) external returns(uint256) envfree;
}

// suppose we want to only check one case of a function
// using if/else is not feasible as cvl will through error
// something like " last statement of the rule mod_ifXLessThanY_resultIsX_usingIf is not an assert or satisfy command (but must be)"
// for this we can use implication operator

rule mod_ifXLessThanY_resultIsX_usingIf(){
    uint256 x;
    uint256 y;

    mathint expected = mod(x,y);

    assert x<y => expected == x;
}

rule max_ifXGreaterThanY_resultX(){
    uint256 x;
    uint256 y;

    mathint expected = max(x,y);

    assert x > y => expected == x;
}

// we can also use it other way around

rule max_resultX_ifXGreaterThanYEqualY(){
    uint256 x;
    uint256 y;

    mathint expected = max(x,y);

    assert expected == x => x >= y ;
}