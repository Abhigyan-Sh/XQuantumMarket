> ## About Project

working in Brownie Ethereum development environment to deploy and interact with Smart Contract..

Smart Contract address
----

[0x3f7dDA2f7019D8Bddb8b2475bBB703a7E6Ce6EDb](https://goerli.etherscan.io/address/0x3f7dda2f7019d8bddb8b2475bbb703a7e6ce6edb#readContract)  click me to interact on Block Explorer.

---

> # Testing

Here I have built two test levels [unit tests](https://github.com/Abhigyan-Sh/XQuantumMarket/blob/main/tests/test_unit.py), [integration tests](https://github.com/Abhigyan-Sh/XQuantumMarket/blob/main/tests/test_integration.py) to test the smartContract on **local development network** as well as **on out chain**.

### What all needs to be tested:

- only the owner of smartContract should be able to set the price also track the products array and productToPrice mapping updations.

- can only buy if the payed price is not lesser than the price of the product, also ensure 
buyer and buyerToProduct gets updated.

- only the owner of the smartContract can withdraw funds and that owner do actually gets payed back.

- for a pre-existing product the price should get overwritten alongwith it product should 
not get pushed into the array again.

- we do have a history of purchase from buyers addresses and that we can access 
that history and it doesn't gets overwritten with addition of new products anywhere
in outer or inner array.
____

># Ending Readme..

> Thanks for letting me to work on this challenge. Hope you liked it !

Looking forward to hear on further steps !
------