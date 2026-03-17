// Parametric rules->rules that allow us to formally verify properties that are expected to hold regardless of which function is called.
// Instead of focusing on one function(args), a parametric rule verifies a property holds true after any function is called with any valid arguments.

// To work with the idea of "any function with any valid arguments", there are two concepts in cvl:
// 1. `method` ->  Represents any public or external function within the contract you are verifying. Declaring a variable of type method means that the rule can dynamically reference and execute any function in the contract.
// 2. `calldataarg`-> Represents the arguments for a function call. Since different functions need different inputs, calldataarg ensures that valid arguments are automatically provided for whichever function (method) is being tested.

/**
rule someParametricRule() { 

    env e;
    
    method f;
    calldataarg args;
    
    f(e,args) // -> parametric call, allows to test all the public and external functions in the contract
    
    //Any assert statement should go here
    assert <property_1>;
    assert <property_2>;
 }
*/

methods{
    function totalSupply() external returns(uint256);
}

rule totalSupplyMustRemainConstant() {
    env e;

    method f;
    calldataarg args;

    mathint totalSupplyBefore = totalSupply(e);
    f(e,args);
    mathint totalSupplyAfter = totalSupply(e);

    assert totalSupplyBefore == totalSupplyAfter;
}

