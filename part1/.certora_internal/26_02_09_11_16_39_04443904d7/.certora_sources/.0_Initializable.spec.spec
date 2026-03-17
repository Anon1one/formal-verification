/**
 * 1. Once the initializer is called, it should never be callable again (all calls should revert).

 * 2. It should not be possible to call the initializer in the implementation contract. 
 * Only the initializer in the proxy should be callable, since all the state is kept in the proxy contract. 
 * This is why the logic contracts of proxy patterns call _disableInitializers() in the constructor.

 * 3. Once the initializer and reinitializer are disabled, they should stay disabled permanently.

 * 4. If we call the reinitializer function, we must increment the version from a previous one. 
 * The version is stored as a uint64 variable 
*/

methods{
    function initialize() external envfree;
    function reinitialize(uint64) external envfree;
    function disable() external envfree;
    function version() external returns uint64 envfree;

}

definition isInitialized()   returns bool = version() > 0;


rule cannotInitialiseTwice() {
    require isInitialized();

    initialize@withrevert();

    assert lastReverted;
}