/**
 * "unwinding condition in a loop" for strings.
 * String in solidity is not single value but a dynamic array of bytes.
 * According to EVM's 256-bit word architecture, when you work with dynamic arrays, the compiler and EVM handle them by copying 32-byte chunks at a time
 *
 * In this spec, four hidden loops get trigerred during string handling here:
 * 1. when you call setTxt(_txt), the input arrives as calldata (read-only). And to process/use this string, its need to be copied to "memory"
 * so, its gonna copy 32-bytes at a time, until entire calldata is moved to memory
 * 2. the assignment txt = _txt, gonna moves this string same way from memory to storage, to save in contract state
 * 3. when you call the public getter in your rule, the data is gonna copied from storage to temporary memory again so it can be returned
 * so here another loops runs reading the string’s 32-byte words out of storage one by one.
 * 4. Next, in assertion, prover checks if two symbolic strings are equal, the only way to check equality for two dynamic arrays is to compare them word-by-word from beginning to end.
 * so this is final loop
*/

/**
 * For concrete execution, this hidden loop is simple, string length is known (a fixed number), loop runs definite number of times, things are predictable.
 * However, in formal verification things are symbolic, which represent all the possible sets of values or paths.
 * So, prover is forced to reason about an unbounded family of executions. This creates two huge problems:
 * 1. unknown loop size (unbounded search): as the string length is symbolic, the loop counter that controls the 32-byte copying is also symbolic.
 * the prover must therefore, check not just one execution path, but an entire family of paths. This issue is made exponentially worse by second problem: branching inside the loop.
 * 2. Exponential Branching (The Doubling Effect): The total number of paths explodes because the hidden loop frequently hits conditional checks (like comparing the current 32-byte word). 
 * to guarantee correctness, prover must explore both possibilities simultaneously. The exploration path is divided into two: true/false. 
 * this effectively doubles the the number of execution paths with every single iteration of the loop.
*/

/**
 * This combination of unbounded length and exponential branching is what creates the path explosion problem, quickly rendering the verification process computationally impossible.
 * The Prover gets overwhelmed by the enormous and rapidly growing number of possible execution paths and is forced to stop exploring the loop after a fixed number of iterations using bounded loop unrolling.
 * As prover cannot check all the possbile paths and paths remained unproven the proof is considered incomplete. Therefore, it cannot prove that the property holds for all possible strings, so rule fails to verify successfully
*/

/**
 * In this folder specs, the Prover failed to verify both rules: maxEqReturnMax() and storedStringShouldEqualToInput() becuase the prover cannot finish exploring all paths
 * The root cause is the same: the Prover cannot symbolically explore an unbounded number of loop iterations.
*/

/**
 * Solution:
 * use the flag: "--loop_iter" and "--optimistic_loop"
 * 
 * What happens her with "loop_iter":"<N>" option:
 * let N = 3
 * The Prover will now unroll up to 3 iterations of the hidden loop (the byte-copying loop inside txt = _txt).
 * Since each iteration copies one 32-byte word, this means the Prover can successfully verify the property for strings up to 96 bytes (3 × 32 = 96) in length.
 * However, for strings longer than 96 bytes, the Prover reaches its unrolling bound. At that point, those paths remain unproven.
 * As a result, the rule storedStringShouldEqualToInput() will still fail in the general case as the Prover cannot prove correctness for all string lengths.
 * The result will be the same no matter how much you raise the bound: any finite --loop_iter only proves the property for strings up to that number of 32-byte words. Larger strings remain unproven, 
 * and increasing the bound rapidly slows the Prover.
 * 
 * So now we can use optimistic_loop option here:
 * Instead of increasing the bound, the Prover can be told to assume everything beyond the bound works fine. That’s what --optimistic_loop does.
 * With --optimistic_loop, the Prover changes strategy:
 * 1. For iterations within the bound, it behaves normally and checks every case.
 * 2. For iterations beyond the bound, it assumes that the property will continue to hold without actually exploring those paths.


 While these flags are useful for debugging and managing verification, neither provides a complete, sound proof for an unknown and unbounded loops.

--loop_iter is incomplete.
--optimistic_loop is unsound (it makes assumptions).
*/


methods{
    function setTxt(string) external envfree;
    function txt() external returns(string) envfree;
}

rule storedStringShouldEqualToInput() {

    string _txt;

    //call
    setTxt(_txt);

    //assertions
    assert _txt == txt();

}
