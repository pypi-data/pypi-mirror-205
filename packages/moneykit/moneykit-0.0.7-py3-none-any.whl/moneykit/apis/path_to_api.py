import typing_extensions

from moneykit.apis.paths.auth_introspect import AuthIntrospect
from moneykit.apis.paths.auth_token import AuthToken
from moneykit.apis.paths.institutions import Institutions
from moneykit.apis.paths.institutions_institution_id import InstitutionsInstitutionId
from moneykit.apis.paths.institutions_institution_id_styling import InstitutionsInstitutionIdStyling
from moneykit.apis.paths.link_session import LinkSession
from moneykit.apis.paths.link_session_exchange_token import LinkSessionExchangeToken
from moneykit.apis.paths.links_id import LinksId
from moneykit.apis.paths.links_id_accounts import LinksIdAccounts
from moneykit.apis.paths.links_id_accounts_account_id import LinksIdAccountsAccountId
from moneykit.apis.paths.links_id_accounts_numbers import LinksIdAccountsNumbers
from moneykit.apis.paths.links_id_identity import LinksIdIdentity
from moneykit.apis.paths.links_id_products import LinksIdProducts
from moneykit.apis.paths.links_id_transactions import LinksIdTransactions
from moneykit.apis.paths.links_id_transactions_sync import LinksIdTransactionsSync
from moneykit.apis.paths.users_id_accounts import UsersIdAccounts
from moneykit.apis.paths.users_id_links import UsersIdLinks
from moneykit.apis.paths.users_id_transactions import UsersIdTransactions
from moneykit.apis.paths.well_known_jwks_json import WellKnownJwksJson
from moneykit.paths import PathValues

PathToApi = typing_extensions.TypedDict(
    "PathToApi",
    {
        PathValues.LINKS_ID_ACCOUNTS: LinksIdAccounts,
        PathValues.LINKS_ID_ACCOUNTS_NUMBERS: LinksIdAccountsNumbers,
        PathValues.LINKS_ID_ACCOUNTS_ACCOUNT_ID: LinksIdAccountsAccountId,
        PathValues.AUTH_TOKEN: AuthToken,
        PathValues.AUTH_INTROSPECT: AuthIntrospect,
        PathValues.LINKS_ID_IDENTITY: LinksIdIdentity,
        PathValues.INSTITUTIONS: Institutions,
        PathValues.INSTITUTIONS_INSTITUTION_ID: InstitutionsInstitutionId,
        PathValues.INSTITUTIONS_INSTITUTION_ID_STYLING: InstitutionsInstitutionIdStyling,
        PathValues.LINKSESSION: LinkSession,
        PathValues.LINKSESSION_EXCHANGETOKEN: LinkSessionExchangeToken,
        PathValues.LINKS_ID: LinksId,
        PathValues.LINKS_ID_TRANSACTIONS: LinksIdTransactions,
        PathValues.LINKS_ID_TRANSACTIONS_SYNC: LinksIdTransactionsSync,
        PathValues.USERS_ID_TRANSACTIONS: UsersIdTransactions,
        PathValues.USERS_ID_ACCOUNTS: UsersIdAccounts,
        PathValues.USERS_ID_LINKS: UsersIdLinks,
        PathValues._WELLKNOWN_JWKS_JSON: WellKnownJwksJson,
        PathValues.LINKS_ID_PRODUCTS: LinksIdProducts,
    },
)

path_to_api = PathToApi(
    {
        PathValues.LINKS_ID_ACCOUNTS: LinksIdAccounts,
        PathValues.LINKS_ID_ACCOUNTS_NUMBERS: LinksIdAccountsNumbers,
        PathValues.LINKS_ID_ACCOUNTS_ACCOUNT_ID: LinksIdAccountsAccountId,
        PathValues.AUTH_TOKEN: AuthToken,
        PathValues.AUTH_INTROSPECT: AuthIntrospect,
        PathValues.LINKS_ID_IDENTITY: LinksIdIdentity,
        PathValues.INSTITUTIONS: Institutions,
        PathValues.INSTITUTIONS_INSTITUTION_ID: InstitutionsInstitutionId,
        PathValues.INSTITUTIONS_INSTITUTION_ID_STYLING: InstitutionsInstitutionIdStyling,
        PathValues.LINKSESSION: LinkSession,
        PathValues.LINKSESSION_EXCHANGETOKEN: LinkSessionExchangeToken,
        PathValues.LINKS_ID: LinksId,
        PathValues.LINKS_ID_TRANSACTIONS: LinksIdTransactions,
        PathValues.LINKS_ID_TRANSACTIONS_SYNC: LinksIdTransactionsSync,
        PathValues.USERS_ID_TRANSACTIONS: UsersIdTransactions,
        PathValues.USERS_ID_ACCOUNTS: UsersIdAccounts,
        PathValues.USERS_ID_LINKS: UsersIdLinks,
        PathValues._WELLKNOWN_JWKS_JSON: WellKnownJwksJson,
        PathValues.LINKS_ID_PRODUCTS: LinksIdProducts,
    }
)
