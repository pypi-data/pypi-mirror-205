from web3 import Web3

class AddressEthUniswap:
    uniswap_v3_quoter_address=Web3.toChecksumAddress('0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6')
    uniswap_v3_quoter_v2_address=Web3.toChecksumAddress('0x61fFE014bA17989E743c5F6cB21bF9697530B21e')
    uniswap_v3_router_address=Web3.toChecksumAddress('0xE592427A0AEce92De3Edee1F18E0157C05861564')
    uniswap_v3_router_v2_address=Web3.toChecksumAddress('0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45')
    uniswap_v3_factory_address=Web3.toChecksumAddress('0x1F98431c8aD98523631AE4a59f267346ea31F984')

class AddressEthTokens:
    dai=Web3.toChecksumAddress('0x6B175474E89094C44Da98b954EedeAC495271d0F')
    usdc=Web3.toChecksumAddress('0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48')
    usdt=Web3.toChecksumAddress('0xdAC17F958D2ee523a2206206994597C13D831ec7')
    weth=Web3.toChecksumAddress('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2')
    wbtc=Web3.toChecksumAddress('0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599')