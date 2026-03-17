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

/**
 * This prevents the Prover from initializing a state where a single account’s balance exceeds the total sum which can leads to false positives.
 * (this sload is may be neccessary here as, we have unchecked block in contract, the prover will try to make it overflow here, 
 * but this was not the case when unchecked is not used)
 *
 * The local hook variable points captures the value read from the storage mapping with the key user.
 * In a contract operation, storage reads occur before the variable is updated or processed. For example, 
 * in this Solidity line pointsOf[_user] += _amount, pointsOf[_user] must read its current value before adding _amount.
 * 
 * This implementation constrains the Prover to explore only states where g_sumOfUserPoints is greater than or equal to points.
 * Alternatively, we could have also used require statment i.e., pointsOf[address] (points for any particular user) to always be less than or equal to g_sumOfUserPoints
*/
hook Sload uint256 points pointsOf[KEY address account] {
	require g_sumOfUserPoints >= points;
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

rule sumOfAllIndividualPointsEqualsTotalPoints_betterRule(env e, method f, calldataarg args){
    require totalPoints() == 0 && ghost_IndividualPointsSum == 0;
    // Or require totalPoints() == ghost_IndividualPointsSum;
    f(e,args);
    assert ghost_IndividualPointsSum == totalPoints();
}

// turn it into invarinat: (add that init_state axiom)
invariant sumOfAllIndividualPointsEqualsTotalPoints_invariant()
    totalPoints() == ghost_IndividualPointsSum;
