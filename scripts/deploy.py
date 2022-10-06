from brownie import XQuantumMarket, config, network
from scripts.helpful_Scripts import get_account

def deployer():
    account = get_account()
    xquantumMarket = XQuantumMarket.deploy(
        {'from':account}, 
        publish_source = config['networks'][network.show_active()].get('verify', False)
        )
    print(f'smartContract deployed at https://goerli.etherscan.io/address/{xquantumMarket}')
    return xquantumMarket

def getInfo():
    """ @dev::: brownie keeps all instances of deployed contracts within build/contracts
    thus we can access most recent deployments. """
    xquantumMarket = XQuantumMarket[-1]
    balance = xquantumMarket.getBalance()
    merchant = xquantumMarket.Merchant()
    products = xquantumMarket.getProducts()

    print([balance, merchant, products])

def setPrice(product, newPrice):
    xquantumMarket = XQuantumMarket[-1]
    txn = xquantumMarket.setPrice(product, newPrice, {'from': get_account()})
    txn.wait(1)
    print(f'price for {product} has been set to {newPrice*1/10**9} eth.')

def buyProduct(price, product):
    account = get_account()
    xquantumMarket = XQuantumMarket[-1]
    txn = xquantumMarket.buyProduct(product, {'from': account, 'value': price})
    txn.wait(1)
    print(f'{account} has bought {product}')

def withdraw():
    xquantumMarket = XQuantumMarket[-1]
    txn = xquantumMarket.withdraw({'from':get_account()})
    txn.wait(1)
    print('Transactional withdraw has been successful !')

def main():
    """ here below you can comment/uncomment different functions
    depending over how you want to interact with the smartContract. """
    # deployer()
    # getInfo()
    # setPrice('T-shirt', 5000000)
    # buyProduct(5000000 * 1/10**9, 'T-shirt')
    # withdraw()