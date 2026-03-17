/**
 * When using ghost variable we should remember that these varaibles get havoced by the prover if not constrained,
 * therefore we should make them contrained by using require statements in rules, as havoced ghost variables are no use for us
 * as they can produce false results

 * While these require statements works well for rule, this approach cannot be used for invariant verification
 * We cant use the require statement in invarant, because:
 * 1. An invariant must hold in every possible state of the contract, including the initial one, without relying on any precondition. 
 * In other words, invariants express unconditional truths about the system.
 * 2. Using a require statement inside an invariant doesn’t make sense, because require only limits paths during rule execution — it doesn’t define what is true before verification starts. 
 * What we need instead is a way to establish the initial state assumptions for the Prover.

 * To establish such initial truths — like setting a ghost variable’s starting value — we need a different construct: axioms.
 * Or in other words:
 * Since invariants cannot rely on preconditions, we need a way to define what the Prover should assume about the system before verification begins. This is where axioms come in.
 * axioms tell the prover to consider that fact must always accept as true

 * Simply put:
 * 1. A require statement limits what the Prover checks (it filters states).
 * 2. An axiom defines what the Prover believes (it establishes truths).
*/ 

/**
 * Two kinds of axioms: Initial State Axioms, Global Axioms
 *
 * An initial state axiom defines a property that the prover must assume to hold in the base step of invariant checking or right before the contract’s constructor executes.
 * it tells the Prover, “assume this condition is true when the contract is first deployed.”, which allows to control the initial value of ghosts
 * 
 * ghost type_of_ghost name_of_ghost {
    init_state axiom boolean_expression;
  }
 
 * While initial state axioms apply only to the contract’s first state, global axioms define properties that must hold in every state throughout verification.
 * global axiom is the way to tell prover the universal state(consistent condition for all possible contract execution) about ghosts
 * 
 * ghost type_of_ghost name_of_ghost {    
    axiom boolean_expression;
  }
*/

methods 
{
    function votesInFavor() external returns(uint256) envfree;
    function votesAgainst() external returns(uint256) envfree;
}

// this will not work, as prover will havoc the ghost
// the invariant alone gonna false results, as totalVotes will be havoced and will start at arbitrary value
// ghost mathint totalVotes;

// correct way:
ghost mathint totalVotes {    
  init_state axiom totalVotes == 0;
}

ghost mathint totalVotes {
    axiom totalVotes >= 0;
}

// This hook gets triggered every time a value in the hasVoted mapping is updated, which only happens when a user casts a vote. 
// In the hook, we increment totalVotes by 1—effectively counting every new voter regardless of whether they voted in favor or against.
hook Sstore hasVoted[KEY address voter] bool newStatus(bool oldStatus) {
    totalVotes = totalVotes + 1;
}

invariant totalVotesSum()
    totalVotes == votesInFavor() + votesAgainst();

invariant totalVotesShouldAlwaysGtInFavorVotes()
    totalVotes >= votesInFavor();
