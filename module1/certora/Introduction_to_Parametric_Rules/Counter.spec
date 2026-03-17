/**
 * Does there exist any single function f in the contract such that, when executed once with some valid arguments args__, it transitions the state directly from count == 0 to count == 2?
 * But no function can increase the counter by 2 in a single execution, the Prover cannot find any function that satisfies the condition count(e) == 2, therefore this should fail

 * a parametric rule only analyzes the effect of one external function call in isolation. It does not examine sequences of calls or complex interactions within a single transaction. 
 * as rule to pass, increment needs to be called twice before satisfy statement, but prover wont do it for now

 * if we realax the satisfy to count(e) == 1, still rule will not pass
 * as The rule passes the verification if and only if every function instance satisfies all the conditions specified by the assert and satisfy statements. 
 * If even one function fails to meet the criteria, the entire rule fails.
 * `transferOwnership` -> will not pass, as it dont influence the count
 * we can also say this is not a valid parametric rule
*/
rule counterParametricCall() {
    env e;

    require count(e) == 0;

    method f;
    calldataarg args;

    f(e,args);

    satisfy count(e) == 2 ; // through satisfy, we are asking prover whether there is at least one possible way to reach a state where count is 2, starting from an initial state where count is 0.
}
