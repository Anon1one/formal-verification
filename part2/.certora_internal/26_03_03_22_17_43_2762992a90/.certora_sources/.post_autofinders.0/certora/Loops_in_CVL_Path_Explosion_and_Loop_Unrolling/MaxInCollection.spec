/**
 * Path explotions problem:
 * the exponential increase of the execution paths for the prover to verify as the number of loop iterations or conditional branches increases.
 * The prover has a way to solve this issue: "bounded loop unrolling", the technique used by prover to limit the number of times a loop is symbolically explored
 * during verification, allowing prover to avaoid an otherwise infeasible search space caused by unknown and unbounded loop iterations.
*/

/**
 * Certora prover is a symbolic execution engine and it doesnt not test functions on one input at a time but it explores all the possible executions simultaneously.
 * The prover "symbolicaly" verifies the program over logical constraints instead of concrete values.
*/

/**
 * The certora prover performs two steps: 
 * 1. initial state check (Induction base) - he invariant holds immediately after the contract’s constructor finishes executing.
 * 2. induction step - this ensures the invariant must continue to hold after any state change
 * In Induction Step, prover follows three stages:
 * 
 * a. Before the Call Assumption: the asssumes a state S where the invariant already holds. This is called the inductive hypothesis, 
 * inductive hypothesis is a standard step in inductive reasoning.
 *
 * Here, prover does not know the contents of the collection array and that maxInCollection, it just simply assume the state S (as a part of proof method itself)
 * where that condition maxInCollection() == returnMax() is true
 * 
 * b. next, prover verify the function that could change the state, here it picks addToCollection. It does not chose a specific values like 100 or 1 as input to it,
 * instead it uses a symbolic variable, x, which represents any possible uint256

 * The prover now symbolically executes the function addToCollection, 
 * it has this if statement, prover not only verify the x > maxInCollection path but also x <= maxInCollection.
 * for x > maxInCollection, the state should be changed such that maxInCollection updated to x.
 * for x <= maxInCollection, the state should remain unchanged
 * 
 * c. After call verification: now prover must prove that invariant holds in the new state S'.
 * for this c step, prover will go for both the sides
 * LHS (maxInCollection) - simple, prover knows the new value of maxInCollection symbolically.
 * RHS (returnMax) - here prover symbolically execute returnMax function and this is interesting now becuase we have a for loop here.
 * In (simple) concrete execution, the loops runs a specific number of times,
 * but for prover, the array length is symbolic, so number of iterations is unknown.
 * And this is wild because prover need to consider all the possible array length at once, from empty array to max size, this is huge search space.
 * And this for loop iteself has another conditional (if) statement, and prover will explore both the cases (one if case condition holds, second reverse of that condition)
 * So every iteration doubles the number of symbolic paths the Prover must consider.
 *
 * If the array length is n, the prover faces roughly 2**n paths
 * example:
 * 2 elements => 4 paths (2²)
 * 3 elements => 8 paths (2³)
 * 10 elements => 1024 paths (2¹⁰)
 * For a symbolic (unbounded) length => effectively unmanageable
 *
 * This exponential growth makes it practically infeasible for the prover to explote all the paths within reasonable time and computation.
*/

/**
 * To solve this issue prover uses the technique called bounded loop unrolling.
 * The technique used by prover to limit the number of times a loop is symbolically explored during verification and default bound set to one iteration. 
 * Once this limit is reached, the prover stops exploring further because each additional iteration doubles the number of symbolic paths it must analyze.
 * As a result, the remaining paths are left unproven, if any path is left unchecked the inductive step of the proof becomes incomplete. and prover marks invariant as failed.
 * The same problem appears even in places where no explicit loop is visible. Hidden loops such as Solidity strings
*/

methods {
    function maxInCollection() external returns(uint256) envfree;
    function returnMax() external returns(uint256) envfree;
}
invariant maxEqReturnMax()
    maxInCollection() == returnMax();
