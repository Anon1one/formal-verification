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
definition isDisabled()      returns bool = version() == max_uint64;

invariant notInitializing()
    !initializing()
    filtered { f ->
        f.selector != sig:nested_init_init().selector &&
        f.selector != sig:nested_init_reinit(uint64).selector &&
        f.selector != sig:nested_reinit_init(uint64).selector &&
        f.selector != sig:nested_reinit_reinit(uint64,uint64).selector
}

rule cannotInitialiseTwice() {
    require isInitialized();

    initialize@withrevert();

    assert lastReverted, "can only initialise once";
}

rule initializeEffects() {
    requireInvariant notInitializing(); // this is making sure, we start when contract is uninitialised

    bool isUninitializedBefore = isUninitialized(); // should be True

    initialize@withrevert();
    bool success = !lastReverted; // success = true

    // this assert is saying, 
    assert success <=> isUninitializedBefore, "can only initialise a uninitialised contract";
    assert success => version() == 1, "initialse must set the version to 1";         
    
}

rule cannotReinitializeOnceDisabled() {
    require isDisabled();

    uint64 n;
    initialise@withrevert(n);

    assert lastReverted, "contract is disabled";
}

rule reinitializeShouldMakeTheNewVersionBigger() {
    requireInvariant notInitializing();

    uint64 preVersion  = version();

    uint64 n;
    reinitialize@withrevert(n);
    bool success = !lastReverted;

    assert success <=> versionBefore < n;
    assert success => version() == n;

}

rule disableEffect() {
    requireInvariant notInitializing();

    disable@withrevert();
    bool success = !lastReverted;

    assert success,      "call to _disableInitializers failed";
    assert isDisabled(), "disable state not set";
}
