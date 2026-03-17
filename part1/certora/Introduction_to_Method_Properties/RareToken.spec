/**
 * Parametric rules are used to verify the universal rules, but what if the invariant is not universal
 * but depend on some functions, then we can use method properties, to dictate the behaviour of certora
 * treating parametric rules, we can put cases in parametric rule to dictate what should be asserted acc to the function
*/

/**
 * Method Properties
 * available method properties include: 
 * "f.selector", "f.isPure", "f.isView", "f.isFallback","f.numberOfArguments","f.contract"
 * most commonly used: "f.selector", "f.isPure", "f.isView"
*/

/**
 * It is also important to exclude/include the functions that important/not important for our rule
 *
 * Here, view/pure functions are not important, because they wont write to the state of the contract
 * as including them will slow down the verification process, so it is better to exclude them
 * for this we can use `filtered` Blocks
 *
 * filter block reduces computational overhead, making the process desirably optimised
*/
rule totalSupplyBehaviourCheckAccordingToTheFunction(method f, calldataarg args,env e) filtered{
    f -> !f.isView  // this line is saying to prover, to exclude all the view functions from verification
}{
    // initial state
    mathint totalSupplyBefore = totalSupply(e);

    // call any function
    f(e,args);

    // same state after calling that f
    mathint totalSupplyAfter = totalSupply(e);

    // function sepecific assertions
    if(f.selector == sig:mint(address,uint256).selector){
        assert totalSupplyAfter >= totalSupplyBefore, "Total Supply must not decrease on mint";
    }
    else if(f.selector == sig:burn(uint256).selector){
        assert totalSupplyAfter <= totalSupplyBefore, "Total Supply must not increase on burn";
    }else{
        assert totalSupplyAfter == totalSupplyBefore, "Total Supply must not change";
    }
}