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

/**
 * CVL Special Variable: `lastReverted`
 * this is a special boolean Variable, which is updated after each method call—including those made without @withrevert
 * lastReverted=true -> most recent contract function reverted --
 * lastReverted=false -> -- or executed successfully
 * By default lastReverted remains false, (funtion is without @withrevert or with @norevert ) because 
 * prover do not explore revert scenarios until or unless told
*/

/**
 * When a function is called with @withrevert, the Prover no longer ignores revert scenarios, and if a revert occurs, lastReverted is updated to true.
*/

rule addShouldRevert() {

    uint256 a;
    uint256 b;

    require(a + b > max_uint256);

    add@withrevert(a,b);

    assert lastReverted; 
}

rule addShouldNotRevert2() {

    uint256 a;
    uint256 b;

    require(a + b <= max_uint256);

    add@withrevert(a,b);

    assert !lastReverted;
}

/**
 * we should always store the value of lastReverted immediately after relevant function call
 * as it can happen that lastReverted can get overwritten by some other function
 * It means that if a function reverts but another function executes immediately afterward, the original revert status is lost.
*/

rule checkMath() {

    uint256 a;
    
    divide@withrevert(a,0);
    bool divideCallStatus = lastReverted;

    add@withrevert(a,0);
    bool addCallStatus = lastReverted;

    assert divideCallStatus == true;
    assert addCallStatus == false;
}

// If we don’t store `lastReverted` immediately after calling `divide(a, 0)`, the next function call (`add(a, 0)`) will update it again, 
// completely erasing the information about the division operation failing.