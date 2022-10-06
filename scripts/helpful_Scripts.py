from brownie import accounts, network, config

LOCAL_ETHEREUM_DEVELOPMENT = ['ganache-local', 'development']

def get_account(id = None, index = None):
    if (id):
        return accounts.load(id)
    if (index):
        return accounts[index]
    if (network.show_active() in LOCAL_ETHEREUM_DEVELOPMENT):
        return accounts[0]
    else:
        return accounts.add(config['wallets']['from_key'])