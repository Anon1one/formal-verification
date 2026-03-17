methods {
    function add(uint256, uint256) external returns(uint256) envfree;
    function max(uint256, uint256) external returns(uint256) envfree;

}

rule add_sumWithOverflowRevert{
    uint256 x;
    uint256 y;

    mathint _sum = x+y;

    if(_sum<=max_uint256){
        mathint result = add@withrevert(x,y);
        assert !lastReverted;
        assert _sum == result;
    }
    else{
        add@withrevert(x,y);
        assert lastReverted;
    }
}

rule max_returnsMax{
    uint256 x;
    uint256 y;

    mathint expectedMax;

    if(x>=y){
        expectedMax = x;
    }
    else{
        expectedMax = y;
    }
    mathint z = max@withrevert(x,y);
    assert !lastReverted;
    assert expectedMax == z;
}