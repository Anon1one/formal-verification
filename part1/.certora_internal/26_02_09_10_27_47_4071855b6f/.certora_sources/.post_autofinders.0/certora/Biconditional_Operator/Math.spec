methods {
    function mod(uint256, uint256) external returns(uint256) envfree;
    function max(uint256, uint256) external returns(uint256) envfree;
    function min(uint256, uint256) external returns(uint256) envfree;
    function zeroFloorSub(uint256, uint256) external returns (uint256) envfree;
    function mulDivUp(uint256, uint256, uint256) external returns (uint256) envfree;
}

// Instead of Implication operator, we can use Biconditional operator
// when we want to verify P => Q and Q => P.
// instead of separately writing statements to test these implication separately
// we can simple do P <=> Q which is equivalent to asserting both P => Q and Q => P.

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


rule mulDivUp_allRevertCases_Biconditional(){
    uint256 x;
    uint256 y;
    uint256 den;

    mulDivUp@withrevert(x,y,den);
    bool revertStatus = lastReverted;

    assert revertStatus <=> (x*y>max_uint256 || den == 0);
}

rule mulDivUp_noRevert() {
    uint256 x;
    uint256 y;
    uint256 den;

    mulDivUp@withrevert(x,y,den);
    bool revertStatus = lastReverted;

    assert (x*y <= max_uint256 && den != 0) => !revertStatus;
}

/////////////////////////////////////////////////////////////////
/////////////////////////Exercises///////////////////////////////
/////////////////////////////////////////////////////////////////

rule min_alwaysRetursMin(){
    uint256 x;
    uint256 y;

    mathint res = min@withrevert(x,y);

    assert (x<y) => res == x;
}

rule min_alwaysRetursMin_reverse(){
    uint256 x;
    uint256 y;

    mathint res = min@withrevert(x,y);

    assert res == x => (x<=y);
}

rule zeroFloorSub_returnsXminusYIfXminusYIsGreaterThanZero() {
    uint256 x;
    uint256 y;

    mathint res = zeroFloorSub@withrevert(x,y);

    assert (x-y>0) => res == x - y; 
}

rule zeroFloorSub_returnsXminusYIfXminusYIsGreaterThanZero_reverse() {
    uint256 x;
    uint256 y;

    mathint res = zeroFloorSub@withrevert(x,y);

    assert res == x - y => (x-y>=0); 
}