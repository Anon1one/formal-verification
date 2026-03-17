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

// ghost mathint ghost_IndividualPointsSum;

// hook Sstore pointsOf[KEY address user] uint256 val{
//     ghost_IndividualPointsSum = ghost_IndividualPointsSum + val;
// }

rule sumOfAllIndividualPointsEqualsTotalPoints(){
    address account1;address account2;
    uint256 amount1;uint256 amount2;

    require account1 != account2;
    require pointsOf(account1) == 0 && pointsOf(account2) == 0;
    require totalPoints() ==  0;

    addPoints(account1,amount1);
    addPoints(account2,amount2);

    assert to_mathint(totalPoints()) == pointsOf(account1) + pointsOf(account2);
}

