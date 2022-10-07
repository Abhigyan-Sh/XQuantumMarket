from brownie import ( 
  network, 
  accounts, 
  exceptions, 
  XQuantumMarket )
import pytest

from scripts.helpful_Scripts import get_account, LOCAL_ETHEREUM_DEVELOPMENT
from web3 import Web3

def test_onlyOwner_can_setPrice():
  account= get_account(index = 2)
  """ since brownie keeps a tract of recent deployments on a test network """
  xquantumMarket = XQuantumMarket[-1]
  with pytest.raises(exceptions.VirtualMachineError):
    txn = xquantumMarket.setPrice("Bag", 5000000, {'from':account})
    txn.wait(1)

def test_updationOf_product_n_productToPrice():
  account= get_account()
  xquantumMarket = XQuantumMarket[-1]
  txn = xquantumMarket.setPrice("Bag", 5000000, {'from':account})
  txn.wait(1)

  account= get_account(index = 2)
  products = xquantumMarket.getProducts()
  priceOfProduct = xquantumMarket.ProductToPrice("Bag")
  assert products[0] == "Bag"
  assert priceOfProduct == 5000000

def test_only_bought_when_payedSufficientForProduct():
  account= get_account()
  xquantumMarket = XQuantumMarket[-1]
  with pytest.raises(exceptions.VirtualMachineError):
    # expected payment was 5000000 gwei or 5000000 * 1/10**9 eth
    txn = xquantumMarket.buyProduct("Bag", {'from':account, 'value': 4900000 * 1/10**9})
    txn.wait(1)

def test_updationOf_Buyer_BuyerToProduct_n_getBalance():
  account= get_account()
  xquantumMarket = XQuantumMarket[-1]
  txn = xquantumMarket.buyProduct(5000000 * 1/10**9, "Bag", {'from':account})
  txn.wait(1)
  """ Buyer is an array but since a getter function wraps 
  it hence putting (0) and not [0] """
  buyer = xquantumMarket.Buyer(0)
  BuyerToProduct = xquantumMarket.BuyerToProduct(account, 0)
  balance = xquantumMarket.getBalance()
  assert buyer == account
  assert BuyerToProduct == "Bag"
  assert balance == 5000000 # returns balance in gwei

def test_onlyOwner_can_withdraw():
  if network.show_active() not in LOCAL_ETHEREUM_DEVELOPMENT:
    pytest.skip('Only for local testing.')
  account = get_account(index = 2)
  xquantumMarket = XQuantumMarket[-1]

  with pytest.raises(exceptions.VirtualMachineError):
    xquantumMarket.withdraw({'from':account})

def purchaseHistoryOfSingleAccount():
  account= get_account()
  xquantumMarket = XQuantumMarket[-1]
  txn = xquantumMarket.setPrice("shirt", 3000000, {'from':account})
  txn.wait(1)
  BuyersProduct1 = xquantumMarket.BuyerToProduct(account, 0)
  BuyersProduct2 = xquantumMarket.BuyerToProduct(account, 1)
  assert BuyersProduct1 == 'Bag'
  assert BuyersProduct2 == 'shirt'