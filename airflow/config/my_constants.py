import os

CLIENT_ID = "airflow"
CLIENT_SECRET = os.environ.get("AIRFLOW_CLIENT_SECRET")
OIDC_ISSUER = "http://keycloak:8080/realms/nemo"

PROVIDER_NAME = "keycloak"
OIDC_BASE_URL = "{oidc_issuer}/protocol/openid-connect".format(oidc_issuer=OIDC_ISSUER)
OIDC_TOKEN_URL = "{oidc_base_url}/token".format(oidc_base_url=OIDC_BASE_URL)
OIDC_AUTH_URL = "{oidc_base_url}/auth".format(oidc_base_url=OIDC_BASE_URL)