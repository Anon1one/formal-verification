rule totalSupplyBehaviourCheckAccordingToTheFunction(){
    env e;

    mathint totalSupplyBefore = totalSupply(e);

    method f;
    calldataarg args;
    f(e,args);

    mathint totalSupplyAfter = totalSupply(e);

    if(f.selector == sig:mint(address,uint256).selector){
        assert totalSupplyAfter >= totalSupplyBefore,"Total Supply must not decrease on mint";
    }
    else if(f.selector == sig:burn(uint256).selector){
        assert totalSupplyAfter <= totalSupplyBefore,"Total Supply must not increase on burn";
    }else{
        assert totalSupplyAfter == totalSupplyBefore, "Total Supply must not change";
    }
}