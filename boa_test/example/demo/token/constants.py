"""
Basic settings for an NEP5 Token and crowdsale
"""

# This is the script hash of the address for the owner of the token
# This can be found in ``neo-python`` with the wallet open, use ``wallet`` command
TOKEN_OWNER = b'\x1c\xc9\xc0\\\xef\xff\xe6\xcd\xd7\xb1\x82\x81j\x91R\xec!\x8d.\xc0'

TOKEN_CIRC_KEY = b'in_circulation'

TOKEN_INITIAL_AMOUNT = 2500000 * 100000000  # 2.5m to owners * 10^8

# for now assume 1 dollar per token, and one neo = 40 dollars * 10^8
TOKENS_PER_NEO = 40 * 100000000

# for now assume 1 dollar per token, and one gas = 20 dollars * 10^8
TOKENS_PER_GAS = 20 * 100000000

# maximum amount you can mint in the limited round ( 500 neo/person * 40 Tokens/NEO * 10^8 )
MAX_EXCHANGE_LIMITED_ROUND = 500 * 40 * 100000000

# when to start the crowdsale
BLOCK_SALE_START = 12340

# when to end the initial limited round
LIMITED_ROUND_END = 12340 + 10000

# key for key
KYC_KEY = b'kyc_ok'

# key for limited round contributions
LIMITED_ROUND_KEY = b'r1'
