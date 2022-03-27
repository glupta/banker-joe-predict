from web3 import Web3
import time
import requests
import json
import plot

TEN_POWER_EIGHT = 100000000
a = [56950.56, 57577.07, 56990.52, 57261.51, 57362.04, 57054.35,
       56782.  , 56933.02, 57163.87, 56907.34, 57099.38, 56963.49,
       57160.66, 57100.2 , 57646.49, 58536.41, 58614.49, 58430.45,
       57994.97, 57461.32, 57427.91, 56788.54, 56987.82, 57057.39,
       57184.07, 57009.3 , 57201.4 , 56954.34, 56300.12, 56475.  ,
       56907.99, 56653.05, 56810.42, 56944.93, 56683.64, 56547.88,
       56309.51, 56521.13, 56450.66, 57097.77, 56516.95, 56329.  ,
       56576.77, 56719.46, 56616.27, 57028.12, 56858.7 , 56841.7 ,
       56484.26, 56513.44, 56494.53, 56257.74]
       
b = [56318.89, 56587.4 , 56725.86, 56847.27, 56733.7 , 56581.05, 56815.6 , 56826.8 ,
       56959.77, 56789.76, 56863.2 , 56239.08, 55975.33, 54997.17,
       54982.31, 54881.63, 53838.66, 53453.99, 53610.  , 53409.48,
       53601.05, 53041.33, 52982.5 , 53112.4 , 52000.01, 50256.61,
       47538.02, 47482.79, 47242.75, 47500.58, 47475.49, 47370.51,
       46489.66, 47053.32, 47387.01, 47828.28, 48203.74, 47842.98,
       48241.04, 48866.13, 49249.99, 49256.25, 48705.09, 49207.85,
       49152.46, 48944.69, 49017.8 , 49056.97, 49170.78, 48948.98,
       49424.  , 49464.63, 49289.17, 49474.55, 48990.83, 49233.73,
       49236.24, 49382.34, 49297.52, 48926.21, 47951.57, 48488.09,
       49262.21, 49089.19, 48902.44, 48814.67, 49158.84, 49214.1 ]

def load_price():
    banker_joe = '0xC22F01ddc8010Ee05574028528614634684EC29e'
    avax_api_key = 'KEWX5BVU54DNUBX5BZ1VRYH8I96C445GSV'
    user_wallet = '0x65DAC8B5D5D31b1150d8a5a5A14Ed0e3A6827da8'

    response = {}

    #get AVAX balance on Banker Joe
    javax_query = 'https://api.snowtrace.io/api?module=account&action=tokenbalance&contractaddress='+banker_joe+'&address='+user_wallet+'&tag=latest&apikey='+avax_api_key
    javax_response = requests.get(javax_query).json()
    print('javax',javax_response, 'wallet',user_wallet)
    avax_balance = int(javax_response['result']) / TEN_POWER_EIGHT / 50
    response['avax_balance'] = avax_balance

    #if iData supplied, provide next hardcoded price. Otherwise, get current price from Chainlink
    if iData:
        btcPrices = [53453.99, 50610.0, 53409.48, 53601.05, 53041.33, 52982.5, 53112.4, 52000.01, 50256.61, 47538.02, 47482.79, 47242.75, 47500.58, 47475.49, 47370.51, 46489.66, 47053.32, 47387.01, 47828.28, 48203.74, 47842.98]
        response['price_data'] = btcPrices[int(iData)]
    else:
        avalanche_url = 'https://api.avax-test.network/ext/bc/C/rpc'
        provider = Web3(Web3.HTTPProvider(avalanche_url))
        abi = '[{"inputs":[{"internalType":"address","name":"_aggregator","type":"address"},{"internalType":"address","name":"_accessController","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"int256","name":"current","type":"int256"},{"indexed":true,"internalType":"uint256","name":"roundId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"updatedAt","type":"uint256"}],"name":"AnswerUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"roundId","type":"uint256"},{"indexed":true,"internalType":"address","name":"startedBy","type":"address"},{"indexed":false,"internalType":"uint256","name":"startedAt","type":"uint256"}],"name":"NewRound","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"OwnershipTransferRequested","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"inputs":[],"name":"acceptOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"accessController","outputs":[{"internalType":"contract AccessControllerInterface","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"aggregator","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_aggregator","type":"address"}],"name":"confirmAggregator","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"description","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_roundId","type":"uint256"}],"name":"getAnswer","outputs":[{"internalType":"int256","name":"","type":"int256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint80","name":"_roundId","type":"uint80"}],"name":"getRoundData","outputs":[{"internalType":"uint80","name":"roundId","type":"uint80"},{"internalType":"int256","name":"answer","type":"int256"},{"internalType":"uint256","name":"startedAt","type":"uint256"},{"internalType":"uint256","name":"updatedAt","type":"uint256"},{"internalType":"uint80","name":"answeredInRound","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_roundId","type":"uint256"}],"name":"getTimestamp","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"latestAnswer","outputs":[{"internalType":"int256","name":"","type":"int256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"latestRound","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"latestRoundData","outputs":[{"internalType":"uint80","name":"roundId","type":"uint80"},{"internalType":"int256","name":"answer","type":"int256"},{"internalType":"uint256","name":"startedAt","type":"uint256"},{"internalType":"uint256","name":"updatedAt","type":"uint256"},{"internalType":"uint80","name":"answeredInRound","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"latestTimestamp","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"","type":"uint16"}],"name":"phaseAggregators","outputs":[{"internalType":"contract AggregatorV2V3Interface","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"phaseId","outputs":[{"internalType":"uint16","name":"","type":"uint16"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_aggregator","type":"address"}],"name":"proposeAggregator","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"proposedAggregator","outputs":[{"internalType":"contract AggregatorV2V3Interface","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint80","name":"_roundId","type":"uint80"}],"name":"proposedGetRoundData","outputs":[{"internalType":"uint80","name":"roundId","type":"uint80"},{"internalType":"int256","name":"answer","type":"int256"},{"internalType":"uint256","name":"startedAt","type":"uint256"},{"internalType":"uint256","name":"updatedAt","type":"uint256"},{"internalType":"uint80","name":"answeredInRound","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"proposedLatestRoundData","outputs":[{"internalType":"uint80","name":"roundId","type":"uint80"},{"internalType":"int256","name":"answer","type":"int256"},{"internalType":"uint256","name":"startedAt","type":"uint256"},{"internalType":"uint256","name":"updatedAt","type":"uint256"},{"internalType":"uint80","name":"answeredInRound","type":"uint80"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_accessController","type":"address"}],"name":"setController","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_to","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"version","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'
        addr = '0x31CF013A08c6Ac228C94551d535d5BAfE19c602a'
        contract = provider.eth.contract(address=addr, abi=abi)
        latestData = contract.functions.latestRoundData().call()
        currentPrice = latestData[1] / TEN_POWER_EIGHT
        print('currentPrice', currentPrice)
        response['price_data'] = currentPrice

    model = 'model.pkl'
    data = a+b
    get_predictions(model, data)
    return json.dumps(response)