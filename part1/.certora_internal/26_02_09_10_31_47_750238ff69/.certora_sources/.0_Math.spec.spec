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

rule mulDivUp_roundUp_Biconditional() {
    uint256 x;
    uint256 y;
    uint256 den;

    require (den>0);
    assert ((x*y) % den > 0) <=> (mulDivUp(x,y,den) == (x*y/den + 1));
}

rule mulDivUp_noRoundUp_Biconditional() {
    uint256 x;
    uint256 y;
    uint256 den;

    require (den>0);

    assert ((x*y) % den == 0) <=> (mulDivUp(x,y,den) == (x*y/den));

}

rule mulDivUp_allRevertCases_Biconditional(){
    uint256 x;
    uint256 y;
    uint256 den;

    mulDivUp@withrevert(x,y,den);
    bool revertStatus = lastReverted;

    assert revertStatus <=> (x*y>max_uint256 || den == 0);
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