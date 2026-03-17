methods {
    function add(uint256, uint256) external returns(uint256) envfree;
    function max(uint256, uint256) external returns(uint256) envfree;
    function mulDivUp(uint256, uint256, uint256) external returns(uint256) envfree;

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

rule mulDivUp_roundOrRevert() {
    uint256 x;
    uint256 y;
    uint256 den;

    if(den == 0){
        mulDivUp@withrevert(x,y,den);
        assert lastReverted;
    } else if(x*y > max_uint256){
        mulDivUp@withrevert(x,y,den);
        assert lastReverted;
    } else{
        if(x*y%den==0){
            mathint result = mulDivUp@withrevert(x,y,den);
            assert !lastReverted;
            assert result == (x*y/den);
        }
        else{
        mathint result = mulDivUp@withrevert(x,y,den);
        assert !lastReverted;
        assert result == (x*y/den) + 1;
        }
    }
}