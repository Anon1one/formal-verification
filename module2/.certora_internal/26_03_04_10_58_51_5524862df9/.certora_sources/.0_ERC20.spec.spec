methods {
    function balanceOf(address) external returns uint256 envfree;
    function allowance(address, address) external returns (uint256) envfree;
    function totalSupply() external returns uint256 envfree;
    function mint(address,uint256) external envfree; 
}
rule transferBalance(env e) {
    address receiver;
    uint256 amount;

    require (balanceOf(e.msg.sender) + balanceOf(receiver) <= max_uint256);

    mathint initialReceiverBalance = balanceOf(receiver);
    mathint initialSenderBalance = balanceOf(e.msg.sender);

    transfer(e,receiver,amount);

    mathint AfterTransferReceiverBalance = balanceOf(receiver);
    mathint AfterTransferSenderBalance = balanceOf(e.msg.sender);

    if(receiver!=e.msg.sender){
        assert AfterTransferReceiverBalance == initialReceiverBalance + amount;
        assert AfterTransferSenderBalance == initialSenderBalance - amount;
    }
    else{
        assert initialSenderBalance == AfterTransferSenderBalance;
        assert initialReceiverBalance == AfterTransferReceiverBalance;
    }
}

rule transfer_reverts(env e){
    address receiver;
    uint256 amount;

    mathint senderBalance = balanceOf(e.msg.sender);

    transfer@withrevert(e,receiver,amount);
    bool NoSuccess = lastReverted;

    assert NoSuccess <=> (senderBalance<amount || e.msg.value != 0);
}

rule transferFrom_Balance(env e) {
    address receiver;
    address sender;
    uint256 amount;

    require (balanceOf(sender) + balanceOf(receiver) <= max_uint256);

    mathint initialReceiverBalance = balanceOf(receiver);
    mathint initialSenderBalance = balanceOf(sender);

    transferFrom(e,sender,receiver,amount);

    mathint AfterTransferReceiverBalance = balanceOf(receiver);
    mathint AfterTransferSenderBalance = balanceOf(sender);

    if(receiver!=sender){
        assert AfterTransferReceiverBalance == initialReceiverBalance + amount;
        assert AfterTransferSenderBalance == initialSenderBalance - amount;
    }
    else{
        assert initialSenderBalance == AfterTransferSenderBalance;
        assert initialReceiverBalance == AfterTransferReceiverBalance;
    }
}

rule transferFrom_reverts(env e){
    address receiver;
    address sender;
    uint256 amount;

    mathint senderBalance = balanceOf(sender);
    mathint spenderAllowance = allowance(sender,e.msg.sender);

    transferFrom@withrevert(e,sender,receiver,amount);
    bool NoSuccess = lastReverted;

    assert NoSuccess <=> (senderBalance<amount || e.msg.value != 0 || spenderAllowance < amount);
}

rule transferFrom_ChangesAllowance(env e){
    address receiver;
    address sender;
    uint256 amount;

    mathint spenderAllowanceBefore = allowance(sender,e.msg.sender);
    transferFrom(e,sender,receiver,amount);
    mathint spenderAllowanceAfter = allowance(sender,e.msg.sender);

    if(spenderAllowanceBefore != max_uint256){
        assert spenderAllowanceAfter == spenderAllowanceBefore - amount;
    }else{
        assert spenderAllowanceAfter == spenderAllowanceBefore;
    }
}

rule approve(env e) {
    address spender;
    uint256 amount;

    approve@withrevert(e,spender,amount);
    bool reverted = lastReverted;

    mathint spenderAllowanceAfter = allowance(e.msg.sender,spender);

    assert !reverted => spenderAllowanceAfter == amount;
    assert reverted <=> e.msg.value != 0;
}

rule transfer_transferFrom_approve_returns_true_on_success(env e){
    address receiver;
    address sender;
    uint256 amount;
    address spender;

    bool firstReturnValue = transferFrom@withrevert(e,sender,receiver,amount);
    bool firstRevert = lastReverted;
    bool SecondReturnValue = approve@withrevert(e,spender,amount);
    bool SecondRevert = lastReverted;
    bool ThirdReturnValue = transfer@withrevert(e,receiver,amount);
    bool ThirdRevert = lastReverted;

    assert !firstRevert => (firstReturnValue == true);
    assert !SecondRevert => (SecondReturnValue == true);
    assert !ThirdRevert => (ThirdReturnValue == true);

}

rule mint_changes_totalSupply_and_balanceOf_receiver(){
    address receiver;
    uint256 amount;

    require(totalSupply()>=balanceOf(receiver));

    mathint totalSupplyBefore = totalSupply();
    mathint balanceOfReceiverBefore = balanceOf(receiver);
    mint(receiver,amount);
    mathint totalSupplyAfter = totalSupply();
    mathint balanceOfReceiverAfter = balanceOf(receiver);

    assert totalSupplyAfter == totalSupplyBefore + amount;
    assert balanceOfReceiverAfter == balanceOfReceiverBefore + amount;
}

rule mint_reverts(){
    address receiver;
    uint256 amount;

    mathint totalSupply = totalSupply();
    mint@withrevert(receiver,amount);
    bool reverted = lastReverted;

    assert reverted <=> (totalSupply+amount>max_uint256);
}

rule burn_changes_totalSupply_and_balanceOf_receiver(){
    address holder;
    uint256 amount;

    require(totalSupply()>=balanceOf(holder));

    mathint totalSupplyBefore = totalSupply();
    mathint balanceOfReceiverBefore = balanceOf(holder);
    burn(holder,amount);
    mathint totalSupplyAfter = totalSupply();
    mathint balanceOfReceiverAfter = balanceOf(holder);

    assert totalSupplyAfter == totalSupplyBefore - amount;
    assert balanceOfReceiverAfter == balanceOfReceiverBefore - amount;
}

rule burn_reverts(){
    address holder;
    uint256 amount;

    mathint holderBalance = balanceOf(holder);
    burn@withrevert(holder,amount);
    bool reverted = lastReverted;

    assert reverted <=> (holderBalance<amount);
}