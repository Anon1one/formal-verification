//SPDX-License-Identifier: MIT
pragma solidity ^0.8.25;

contract RareToken {
    uint256 public totalSupply;
    address public owner;
    
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);

    modifier onlyOwner() {
        require(msg.sender == owner, "Unauthorized");
        _;
    }

    constructor(uint256 _initialSupply) {
        owner = msg.sender;
        if (_initialSupply > 0) {
            _mint(msg.sender, _initialSupply);
        }
    }

    function transfer(address to, uint256 amount) public virtual returns (bool) {
        _transfer(msg.sender, to, amount);
        return true;
    }

    function approve(address spender, uint256 amount) public virtual returns (bool) {
        _approve(msg.sender, spender, amount);
        return true;
    }

    function transferFrom(address from, address to, uint256 amount) public virtual returns (bool) {
        address spender = msg.sender;
        uint256 currentAllowance = allowance[from][spender];
        require(currentAllowance >= amount, "Allowance exceeded");
        
        if (currentAllowance != type(uint256).max) {
            _approve(from, spender, currentAllowance - amount);
        }
        
        _transfer(from, to, amount);
        return true;
    }

    function mint(address account, uint256 amount) public onlyOwner {
        _mint(account, amount);
    }

    function burn(uint256 amount) public virtual {
        _burn(msg.sender, amount);
    }

    function _transfer(address from, address to, uint256 amount) internal virtual {
        require(from != address(0), "Invalid sender");
        require(to != address(0), "Invalid recipient");
        
        uint256 fromBalance = balanceOf[from];
        require(fromBalance >= amount, "Insufficient balance");
        
        balanceOf[from] = fromBalance - amount;
        balanceOf[to] += amount;
        emit Transfer(from, to, amount);
    }

    function _mint(address account, uint256 amount) internal virtual {
        require(account != address(0), "Invalid recipient");
        
        totalSupply += amount;
        balanceOf[account] += amount;
        emit Transfer(address(0), account, amount);
    }

    function _burn(address account, uint256 amount) internal virtual {
        require(account != address(0), "Invalid burner");
        
        uint256 accountBalance = balanceOf[account];
        require(accountBalance >= amount, "Burn exceeds balance");
        
        balanceOf[account] = accountBalance - amount;
        totalSupply -= amount;
        emit Transfer(account, address(0), amount);
    }

    function _approve(address ownerAccount, address spender, uint256 amount) internal virtual {
        require(ownerAccount != address(0), "Invalid owner");
        require(spender != address(0), "Invalid spender");
        
        allowance[ownerAccount][spender] = amount;
        emit Approval(ownerAccount, spender, amount);
    }
}
