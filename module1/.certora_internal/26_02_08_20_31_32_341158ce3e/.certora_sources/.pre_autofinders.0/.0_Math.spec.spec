methods {
    function mod(uint256, uint256) external returns(uint256) envfree;
    function max(uint256, uint256) external returns(uint256) envfree;
    function mulDivUp(uint256, uint256, uint256) external returns (uint256) envfree;
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

    assert expected == x => x >= y;
}

// Vacuous Rules

// x<0 will never be reachable as x is uint256, therefore prover will pass
rule max_unreachableCondition_vacuouslyTrue() {
    uint256 x;
    uint256 y;

    mathint result = max(x, y);
    assert x < 0 => result == y;
}
// same goes here:
// doesnt matter what the RHS is, LHS is vacuous(unreachable) here, so prover will pass
rule max_unreachableCondition_vacuouslyTrueObvious() {
    uint256 x;
    uint256 y;

    mathint result = max(x, y);
    assert x < 0 => 1 == 2;
}

// Tautology

// regardless of LHS, the RHS is always true, therefore prover will pass
rule max_outcomeIsAlwaysTrue_tautology() {
    uint256 x;
    uint256 y;

    mathint result = max(x, y);
    assert x > y => result >= 0;
}

rule mulDivUp_roundUp() {
    uint256 x;
    uint256 y;
    uint256 den;

    require (den>0);
    assert ((x*y) % den > 0) => (mulDivUp(x,y,den) == (x*y/den + 1));
}

rule mulDivUp_noRoundUp() {
    uint256 x;
    uint256 y;
    uint256 den;

    require (den>0);

    assert ((x*y) % den == 0) => (mulDivUp(x,y,den) == (x*y/den));

}

rule mulDivUp_revertWhenDenominatorIsZero(){
    uint256 x;
    uint256 y;
    uint256 den;

    mulDivUp@withrevert(x,y,den);
    bool revertStatus = lastReverted;

    assert (den == 0) => revertStatus;
}

rule mulDivUp_revertWhenXTimesYIsGreaterThanMaxUint256(){
    uint256 x;
    uint256 y;
    uint256 den;

    mulDivUp@withrevert(x,y,den);
    bool revertStatus = lastReverted;

    assert (x*y>max_uint256) => revertStatus;
}

// It is important verify the reverse too
// Which means if we are checking P => Q, then we should also check Q => P

// Therefore:

rule mulDivUp_allRevertCases(){
    uint256 x;
    uint256 y;
    uint256 den;

    mulDivUp@withrevert(x,y,den);
    bool revertStatus = lastReverted;

    assert revertStatus => (x*y>max_uint256 || den == 0);
}

rule mulDivUp_noRevert() {
    uint256 x;
    uint256 y;
    uint256 den;

    mulDivUp@withrevert(x,y,den);
    bool revertStatus = lastReverted;

    assert (x*y<max_uint256 || den != 0) => revertStatus;
}