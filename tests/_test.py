from brownie import network, accounts, exceptions
import pytest
from scripts.helpful_scripts import (
    get_account, 
    LOCAL_ETHEREUM_DEVELOPMENT)
from scripts.deploy import deployer

""" 
What all needs to be tested here, 
- only the owner can set the price also check the 
products array and prductToPrice mapping.
- can only buy if the payed price is not lesser than the price of the product, also check 
buyer and buyerToProduct gets updated.
- for a pre-existing product the price should get overwritten and that it product should 
not get pushed into the array again.
- only the owner of the smart contract can withdraw funds.
and that owner do actually gets payed back.
- we do have a history of purchase from buyers addresses and that we can access 
that history and it doesn't gets overwritten with addition of new products anywhere
in outer or inner array.
"""
def test_can_fund_and_withdraw():
    account= get_account()
    fund_me= deploy_fund_me()
    entrance_fee= fund_me.getEntranceFee() + 100        # just in case you need some extra 
    tx= fund_me.fund({"from":account,"value":entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    tx2= fund_me.withdraw({"from":account})
    tx2.wait(1)
# 
# now on command- 'brownie test' - our only test runs successfully

# (some extra bit: commanding 'brownie run script/deploy.py' is same as 'brownie run scripts/deploy.py --network development)

# we always want that if we are deploying through testnet then process is already slow so only the test we want to run should run and others should be skipped 
# we can use pytest skip functionality to do that and for this we install it through command- 'pip install pytest'
# so what we do now is that if we are working with testnet then the following test should be skipped while others will run but if in case i work with local blockchain then following function should also run alongwith other functions

def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENT:
        pytest.skip("Only for local testing.")
    account= accounts.add()
    fund_me= deploy_fund_me()
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from":account})

# PYTEST.SKIP >> now we know that this function above has been skipped when we use command- 'brownie run scripts/test_fund_me.py --network rinkeby but with command- 'brownie run scripts/test_fund_me.py' the function gets executed 
# when this function is skipped it says 1 deselected and a letter 's' will be seen written there which is a acronym here for word 'skipped'

# EXCEPTIONS >> when we deployed this on our local blockchain then we expect the function to run but later an error(showing VirtualMachineError) to flash because withdraw function is an onlyOwner function so not just any account will be able to run the withdraw function
# so we need to tell our brownie that the failure of withdraw function is fine (i mean it should happen but the code shouldn't stop right there) and should continue further and for this i write pytest mantr before or to say i envelope calling of withdraw function in pytest mantr

# now we see no 'revert' is written in red and exception thrown in terminal at us but
# what we see now is function ran successfully and all green but yes that withdraw has been reverted without being told

# -------------------MAINNET FORK
# now the last version of testing we are going to go through is mainnet-fork
# so now comes the mainnet itself
# 'mainnet fork' is a built-in part of brownie and pulls from infura, and we can interact with them the same way as we have done till now

# MADE CHANGE1:
# IN brownie-config.yaml added a new network 
    # mainnet-fork:
    # eth_usd_price_feed: docs.chain.link/USING PRICE FEEDS(heading)/Ethereum Price feeds/ ETH/USD copy the address
    # verify: False
# now if we run this using command- 'brownie run scripts/test_fund_me.py' --network mainnet-fork'
# then it runs into an issue it says: Gas estimation failed -insufficient funds for transfer
# this is because if we go to get_account() function then it follows else: condition and since we have no account on mainnet with real eth so how could we send funds in some other account
# so we need to tell brownie that when we are working with mainnet-fork then it should create us a fake account with fake eths however we don't want it to deploy MockV3Aggregator.sol because AggregatorV3Interface or pricefeed contracts are already there on testnets and mainnets

# MADE CHANGE2:
  # FORKED_LOCAL_ENVIRONMENTS= ["mainnet-fork"] added in helpful_scripts.py
  # if network.show_active() in FORKED_LOCAL_ENVIRONMENTS or 
  # network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
# AND in our deploy.py it is not gonna be from LOCAL_BLOCKCHAIN_ENVIRONMENTS
# so we will get price_feeds from that address in eth_usd_price_feed

# now still we get an error - list index out of range
# its because brownie's forking doesn't comes with accounts[0] so we need to create our own custom fake accounts right in brownie 
# so we command- 'brownie networks add development mainnet-fork-dev cmd=ganache-cli host=http://127.0.0.1 fork='https://mainnet.infura.io/v3/$WEB3_INFURA_PROJECT_ID' accounts=10 mnemonic= brownie port=8545' 
  # HERE we put another link in strings so that value of our environment variable doesn't comes in its place, set 10 fake accounts for me,
  # performance-wise working with infura could give an issue here so he prefers to fork from an application called alchemy.io, so sign-in > create app (env. = Development, chain= Ethereum, network= Mainnet) > view details > view key > copy http:// >
# and we change the URL so instead command- 'brownie networks add development mainnet-fork-dev cmd=ganache-cli host=http://127.0.0.1 fork=URL from alchemy not in inverted commas accounts=10 mnemonic= brownie port=8545 
# it says now mainnet-fork-dev has been added 

# MADE CHANGE3:
  # In brownie-config.yaml, mainnet-fork has been changed to mainnet-fork-dev:
  # FORKED_LOCAL_ENVIRONMENTS= ["mainnet-fork","mainnet-fork-dev"]

# and now it works with command- 'brownie run scripts/deploy.py --network mainnet-fork-dev'


# with command- 'brownie test --network mainnet-fork-dev'
# we see 1 passed, 1 skipped
# 

# now deploying over github
# git init -b main
# git config user.name "freecodecampvideo"
# git config user.email "pryanshukla0321@gmail.com"
# git add . 
# git status

# either add .env to .gitignore or run command 'git rm --cached .env' and then 'git add .'

# git commit -m 'first commit'