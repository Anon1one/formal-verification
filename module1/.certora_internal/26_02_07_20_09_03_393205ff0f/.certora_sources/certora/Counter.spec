methods {
    function count() external returns(uint256) envfree;
    function increment() external envfree;
    function decrement() external envfree;
}


rule checkIncrement() {
    uint256 precallCount = count();

    increment();

    uint256 postcallCount = count();

    assert postcallCount == precallCount + 1;

}

rule checkCounter(){
    uint256 precallCount = count();

    increment();
    decrement();

    uint256 postcallCount = count();

    assert postcallCount == precallCount;
}
rule searchValidExecution {

    increment();
    increment();
    increment();

    satisfy count() == 8;
}