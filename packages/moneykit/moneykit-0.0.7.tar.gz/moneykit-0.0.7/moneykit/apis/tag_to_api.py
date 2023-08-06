import typing_extensions

from moneykit.apis.tags import TagValues
from moneykit.apis.tags.access_token_api import AccessTokenApi
from moneykit.apis.tags.account_numbers_api import AccountNumbersApi
from moneykit.apis.tags.accounts_api import AccountsApi
from moneykit.apis.tags.identity_api import IdentityApi
from moneykit.apis.tags.institutions_api import InstitutionsApi
from moneykit.apis.tags.link_session_api import LinkSessionApi
from moneykit.apis.tags.links_api import LinksApi
from moneykit.apis.tags.products_api import ProductsApi
from moneykit.apis.tags.transactions_api import TransactionsApi
from moneykit.apis.tags.users_api import UsersApi

TagToApi = typing_extensions.TypedDict(
    "TagToApi",
    {
        TagValues.ACCESS_TOKEN: AccessTokenApi,
        TagValues.LINK_SESSION: LinkSessionApi,
        TagValues.LINKS: LinksApi,
        TagValues.INSTITUTIONS: InstitutionsApi,
        TagValues.ACCOUNTS: AccountsApi,
        TagValues.ACCOUNT_NUMBERS: AccountNumbersApi,
        TagValues.TRANSACTIONS: TransactionsApi,
        TagValues.IDENTITY: IdentityApi,
        TagValues.USERS: UsersApi,
        TagValues.PRODUCTS: ProductsApi,
    },
)

tag_to_api = TagToApi(
    {
        TagValues.ACCESS_TOKEN: AccessTokenApi,
        TagValues.LINK_SESSION: LinkSessionApi,
        TagValues.LINKS: LinksApi,
        TagValues.INSTITUTIONS: InstitutionsApi,
        TagValues.ACCOUNTS: AccountsApi,
        TagValues.ACCOUNT_NUMBERS: AccountNumbersApi,
        TagValues.TRANSACTIONS: TransactionsApi,
        TagValues.IDENTITY: IdentityApi,
        TagValues.USERS: UsersApi,
        TagValues.PRODUCTS: ProductsApi,
    }
)
