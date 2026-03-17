// see the blog

// methods {
//     function increment() external envfree;
//     function count() external returns (uint) envfree;
// }

// // Ghost variable to track how many times the `count` variable is updated
// ghost mathint countIncrementCall;

// // Hook triggered before `count` is updated via SSTORE
// hook Sstore count uint256 updatedValue (uint256 prevValue) {
//     // Increment the ghost each time `count` is about to be modified
//     countIncrementCall = countIncrementCall + 1; 
// }


// // Rule to verify that `increment()` increases `count` by exactly the number of times it's called
// rule checkCounterIncrements() {

//     //Add the require statement to constrain the ghost
//     require countIncrementCall == 0;

//     // Capture the value of `count` before any updates
//     mathint precallCountValue = count();

//     // Perform three increment operations
//     increment();
//     increment();
//     increment();

//     // Capture the value of `count` after updates
//     mathint postCallCountValue = count();

//     // Assert that `count` increased by the same amount as tracked by the ghost
//     assert postCallCountValue == precallCountValue + countIncrementCall;
// }
