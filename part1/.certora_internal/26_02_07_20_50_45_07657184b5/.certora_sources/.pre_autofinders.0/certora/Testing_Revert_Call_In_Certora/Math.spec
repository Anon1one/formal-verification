methods {
    function add(uint256, uint256) external returns (uint256) envfree;
}

/**
 * When you run this rule, this will pass
 * However, it should fail, as there is a case when this should revert 
 * i.e., when one of a and b is max uint256 and other non-zero, then solidity will revert and 
 * the assert statement should evaluate to false, and the rule should fail verification
 * However, this did not happen, and our rule was still verified by the Prover. 
 * This is because, by default, the Prover ignores revert cases during verification.
*/

rule checkAdd() {

    uint256 a;
    uint256 b;
    uint256 c = add(a,b);

    assert a + b == c;
}

// This raises an important question: Why does the Prover choose to ignore revert cases during verification?

/**
 * The reason is that reverts can be a normal part of operation—for example, if someone other than the contract owner tries to perform a privileged action. 
 * In such cases, a revert is not considered a failure; it is the expected behavior.
 * By ignoring revert paths, the Prover focuses on verifying successful execution scenarios where the function completes without errors. 
 * However, we can override this default behavior using the @withrevert method tag provided by CVL.
*/

/**
 * CVL Method Tags
 * "function_name@norevert();" and "function_name@withrevert();"
 * @norevert tag, tells prover to actively disregards any execution paths that result in a revert
 * @withrevert tag, tells prover to no longer ignores revert cases. It treats any scenario where a revert occurs as a violation.
 * by-default @norevert is the method tag, if no method tag is given
*/
rule checkAdd2() {

    uint256 a;
    uint256 b;
    
    uint256 c = add@withrevert(a,b);

    assert a + b == c;
}