methods {
    function add(uint256, uint256) external returns(uint256) envfree;
    function max(uint256, uint256) external returns(uint256) envfree;
    function min(uint256, uint256) external returns(uint256) envfree;
    function zeroFloorSub(uint256, uint256) external returns(uint256) envfree;
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

// rule add_sumWithOverflowRevert_ternary() {
//     uint256 x;
//     uint256 y;

//     mathint _sum = x + y;
//     mathint result = add@withrevert(x, y);

//     assert _sum <= max_uint256 ? !lastReverted : lastReverted; 
// }

rule max_returnsMax{
    uint256 x;
    uint256 y;

    mathint expectedMax;

    // instead of if/else we can also use ternary operator:
    // remove if/else and add, mathint expectedMax = x>=y ? x : y;

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

    mathint result = mulDivUp@withrevert(x,y,den);
    if(den == 0 || x*y > max_uint256){
        assert lastReverted;
    } else{
        if(x*y%den==0){
            assert !lastReverted;
            assert result == (x*y/den);
        }
        else{
        assert !lastReverted;
        assert result == (x*y/den) + 1;
        }
    }
}

rule min_returnsMin{
    uint256 x;
    uint256 y;

    mathint expected = x>=y ? y : x;

    mathint z = min@withrevert(x,y);

    assert !lastReverted;
    assert expected == z;
}

rule zeroFloorSub_returnsMaxOf0andXSubtractY{
    uint256 x;
    uint256 y;

    mathint expected = x-y > 0 ? x-y : 0;

    mathint result = zeroFloorSub@withrevert(x,y);

    assert !lastReverted;
    assert expected == result;
}