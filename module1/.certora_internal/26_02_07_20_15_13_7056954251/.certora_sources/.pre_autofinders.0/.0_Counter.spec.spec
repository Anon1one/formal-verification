methods {

    function eqn(uint256, uint256) external returns (bool) envfree;
    function eqn2(uint256, uint256) external returns (bool) envfree;

}

rule checkEqn() {

    uint256 x; 
    uint256 y;

    satisfy eqn(x, y) == true;
}

rule checkEqn2() {

    uint256 x; 
    uint256 y;

    satisfy eqn2(x, y) == true;
}
