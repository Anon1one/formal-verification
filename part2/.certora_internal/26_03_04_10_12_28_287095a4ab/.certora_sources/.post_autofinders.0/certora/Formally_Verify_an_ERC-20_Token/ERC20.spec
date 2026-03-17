methods {
    function balanceOf(address) external returns uint256;
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

