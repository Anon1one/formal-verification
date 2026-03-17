methods {
    function add(uint256, uint256) external returns (uint256) envfree;
}

rule checkAdd() {

    uint256 a;
    uint256 b;
    uint256 c = add(a,b);

    assert a + b == c;
}
