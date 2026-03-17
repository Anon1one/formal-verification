/**
 * Sometimes while writing "invariants", you need to have certain assumption, that can restrict prover
 * to not to explore impractical execution paths, that paths that are not valid to occur in blockchain
 * for example: the prover will also try to explore the path where the contract (lets say ERC20) can call its own functions 
 * and especially talking about tranfer/transferfrom, but these function should only be called by EOA/Other contract,
 * hence it is a impractical state
 *
 * To resolve such issues, we need to put assumptions in the invaraints and that can be done by "preserved" blocks

 * Syntax:

// Generic preserved block

 invariant invariant_name()
    invariant_expression
{
    preserved {
        // assumptions about the invariant
    }

    // Or
    preserved with (env e) { ... }

}

Sometimes, we want the preserved block to be applied to only to a particular function, or only with certain environmental
details (like msg.sender or msg.value), in that case we can use "with" clause:

// function-specific preserved blocks

invariant invariant_name(param_1, param_2,...)
    invariant_expression;
{
    preserved functionName(type arg, ...) with (env e) {
        // additional assumptions applicable only for this particular function
    }

}

 * Preserved blocks are applied during induction step of invariant checking
 * They are executed after the invariant is assumed to hold in the pre-state but before the corresponding method is symbolically 
 * executed, ensuring that the Prover starts each induction step from a state that is both mathematically valid and contextually realistic.

 * We may also restrict which functions the invariant is checked against using "filtered { ... }" block
 * A function-specific preserved block (preserved functionName(…) with (env e) { ... }) applies only when the Prover is checking that named function. 
 * If the named function is not included by the filter, that preserved block has no effect.

invariant invariant_name()
    invariant_expression;
    filtered {
        // restrict which functions are checked
    }
{
    preserved functionName(type arg, ...) with (env e) {
        // assumptions or requireInvariant statements
    }

    // Or (considering all functions in that filtered set)
    preserved with (env e) { ... }

}

* filter blocks narrow down where an invariant is applied, and preserved block  describe what must still hold when those functions are executed.
* only using preserved blocks are generally preferred over filter blocks, filters are riskier because they remove entire functions from invariant checking.
* Preserved blocks are usually safer because they constrain assumptions about the state or execution environment rather than excluding behavior altogether.
*/

methods {
    function totalSupply() external returns(uint256) envfree;
    function balanceOf(address) external returns (uint256) envfree;
}

invariant tokenIntegrity()
    nativeBalances[currentContract] >= totalSupply()
{
    // these preserved blocks are necessary to  eliminate every unrealistic execution path, that reported false violation
    preserved with(env e) {
        require e.msg.sender != currentContract;
    }

    preserved withdraw(uint256 amount) with (env e) {
        require balanceOf(e.msg.sender) <= totalSupply();
    }
}