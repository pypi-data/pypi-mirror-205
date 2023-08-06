# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from moneykit.apis.path_to_api import path_to_api

import enum


class PathValues(str, enum.Enum):
    LINKS_ID_ACCOUNTS = "/links/{id}/accounts"
    LINKS_ID_ACCOUNTS_NUMBERS = "/links/{id}/accounts/numbers"
    LINKS_ID_ACCOUNTS_ACCOUNT_ID = "/links/{id}/accounts/{account_id}"
    AUTH_TOKEN = "/auth/token"
    AUTH_INTROSPECT = "/auth/introspect"
    LINKS_ID_IDENTITY = "/links/{id}/identity"
    INSTITUTIONS = "/institutions"
    INSTITUTIONS_INSTITUTION_ID = "/institutions/{institution_id}"
    INSTITUTIONS_INSTITUTION_ID_STYLING = "/institutions/{institution_id}/styling"
    LINKSESSION = "/link-session"
    LINKSESSION_EXCHANGETOKEN = "/link-session/exchange-token"
    LINKS_ID = "/links/{id}"
    LINKS_ID_TRANSACTIONS = "/links/{id}/transactions"
    LINKS_ID_TRANSACTIONS_SYNC = "/links/{id}/transactions/sync"
    USERS_ID_TRANSACTIONS = "/users/{id}/transactions"
    USERS_ID_ACCOUNTS = "/users/{id}/accounts"
    USERS_ID_LINKS = "/users/{id}/links"
    _WELLKNOWN_JWKS_JSON = "/.well-known/jwks.json"
    LINKS_ID_PRODUCTS = "/links/{id}/products"
