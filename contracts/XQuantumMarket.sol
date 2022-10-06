// SPDX-License-Identifier: MIT

pragma solidity ^0.8.13;

contract XQuantumMarket {
    address [] public Buyer;
    address payable public Merchant;
    string [] Products;
    mapping ( string => bool ) ProductsBool;
    mapping ( address => string[] ) public BuyerToProduct;
    mapping ( string => uint256 ) public ProductToPrice;

    constructor () {
        Merchant = payable(msg.sender);
    }
    modifier isOwner() {
        require(msg.sender == Merchant, "Caller is not owner of smartContract.");
        _;
    }

    function getProducts() view public returns(string[] memory) {
        return Products;
    }
    function getBalance() external view returns (uint256) {
        return address(this).balance;
    }

    function setPrice(string memory product, uint256 newPrice) public isOwner {
        ProductToPrice[product] = newPrice;
    /* @dev::: if newProduct is an old existing product in the 
        ProductToPrice mapping then the price will get overwritten 
        which is actually desired. */
        if ( ProductsBool[product] == false ) {
            Products.push(product);
            ProductsBool[product] = true;
        }
    }
    function buyProduct(string memory product) payable public {
    /* @dev::: user puts value in Ether(unit) while products 
        value i.e. ProductToPrice[product] has been put in wei */
        require(msg.value >= (ProductToPrice[product] * 1/1000000000));
        BuyerToProduct[msg.sender].push(product);
        Buyer.push(msg.sender);
    }
    function withdraw() public isOwner {
        payable(msg.sender).transfer(address(this).balance);
    }
}