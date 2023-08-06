# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from moneykit.apis.tag_to_api import tag_to_api

import enum


class TagValues(str, enum.Enum):
    ACCESS_TOKEN = "Access Token"
    LINK_SESSION = "Link Session"
    LINKS = "Links"
    INSTITUTIONS = "Institutions"
    ACCOUNTS = "Accounts"
    ACCOUNT_NUMBERS = "Account Numbers"
    TRANSACTIONS = "Transactions"
    IDENTITY = "Identity"
    USERS = "Users"
    PRODUCTS = "Products"
