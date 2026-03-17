### Overflow and Mathint

* `mathint` is an unbounded type in CVL that models arithmetic without overflow or underflow.
* Arithmetic in CVL defaults to `mathint`, making specifications safer by avoiding accidental casting to bounded types.
* `require_uint256` restricts a `mathint` type to the `uint256` range, hence ignoring values beyond `max_uint256`. Thus, it can hide overflows.
* Use `mathint` whenever possible, and use `uint` or `int` for contract function arguments.

