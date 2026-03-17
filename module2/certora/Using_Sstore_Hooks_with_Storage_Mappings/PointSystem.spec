// examples to understand syntax:

/** Example 1:

/// syntax:

hook Sstore balances[KEY address user] uint256 newVal (uint256 oldVal) {
    // Implement hook logic for the balances mapping where:
		// - KEY is `user`
		// - old (previous) value is `oldVal`
		// - new (current) value is `newVal`
}

/// implementing:

ghost mathint g_balanceDelta;

hook Sstore balances[KEY address user] uint256 newVal (uint256 oldVal) {
    g_balanceDelta = newVal - oldVal;
}

rule deltaNotMoreThan10() {
    ...
    assert g_balanceDelta <= 10;
}
*/

/** Example 2:

/// syntax:

hook Sstore balances[KEY address user] uint256 newVal {
	// implement hook logic
}

/// implementing:

ghost mathint g_balance;

hook Sstore balances[KEY address user] uint256 newVal {
	g_balance = newVal;
}

rule balanceDoesNotExceed2000() {
	...
	assert g_balance <= 2000;
}
*/

methods {
    function totalPoints() external returns(uint256) envfree;
    function addPoints(address,uint256) external envfree;
    function pointsOf(address) external returns uint256 envfree;
}

ghost mathint ghost_IndividualPointsSum{
    init_state axiom ghost_IndividualPointsSum == 0;
}

hook Sstore pointsOf[KEY address user] uint256 newVal (uint256 oldVal){
    ghost_IndividualPointsSum = ghost_IndividualPointsSum + newVal - oldVal;
}

rule sumOfAllIndividualPointsEqualsTotalPoints(){
    address account1;address account2;
    uint256 amount1;uint256 amount2;

    require account1 != account2;

    mathint totalPointsBefore = totalPoints();
    mathint pointsOfAccount1Before = pointsOf(account1);
    mathint pointsOfAccount2Before = pointsOf(account2);

    addPoints(account1,amount1);
    addPoints(account2,amount2);

    mathint totalPointsAfter = totalPoints();
    mathint pointsOfAccount1After = pointsOf(account1);
    mathint pointsOfAccount2After = pointsOf(account2);

    mathint totalPointsDelta = totalPointsAfter - totalPointsBefore;
    mathint pointsOfAccount1Delta = pointsOfAccount1After - pointsOfAccount1Before;
    mathint pointsOfAccount2Delta = pointsOfAccount2After - pointsOfAccount2Before;

    assert totalPointsDelta == pointsOfAccount1Delta + pointsOfAccount2Delta;
}
// the above rule only check for two accounts which is the subset of all account
// but we want to verify generally for all accounts (not subset but for full set)

// better rule:
rule sumOfAllIndividualPointsEqualsTotalPoints_betterRule(env e, method f, calldataarg args){
    require totalPoints() == 0 && ghost_IndividualPointsSum == 0;
    // Or require totalPoints() == ghost_IndividualPointsSum;
    f(e,args);
    assert ghost_IndividualPointsSum == totalPoints();
}

// turn it into invarinat: (add that init_state axiom)
invariant sumOfAllIndividualPointsEqualsTotalPoints_invariant()
    totalPoints() == ghost_IndividualPointsSum;
