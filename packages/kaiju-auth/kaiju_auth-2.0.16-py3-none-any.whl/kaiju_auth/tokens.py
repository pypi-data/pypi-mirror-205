from __future__ import annotations

import asyncio
import time
import uuid
from typing import Union, Optional

from jwcrypto import jwk, jwt  # noqa ?

from kaiju_tools.cache import BaseCacheService
from kaiju_tools.exceptions import NotAuthorized
from kaiju_tools.serialization import dumps, loads
from kaiju_tools.services import ContextableService

__all__ = ['KeystoreService', 'JWTService', 'JWT']


class JWT(jwt.JWT):
    """Redefined claim dumps and loads methods."""

    def __init__(self, *args, **kws):
        super().__init__(*args, **kws)
        self._claims_data = None

    @property
    def claims_data(self):
        if self._claims_data is None:
            self._claims_data = loads(self._claims)
        return self._claims_data

    @property
    def claims(self):
        if self._claims is None:
            raise KeyError("'claims' not set")
        return self._claims

    @claims.setter
    def claims(self, c):
        """Set token data."""
        if self._reg_claims and not isinstance(c, dict):
            # decode c so we can set default claims
            c = loads(c)

        if isinstance(c, dict):
            self._add_default_claims(c)
            self._claims = dumps(c)
        else:
            self._claims = c

    def _check_provided_claims(self):
        if self._check_claims is False:
            return
        try:
            claims = loads(self.claims)
            if not isinstance(claims, dict):
                raise ValueError()
        except ValueError:
            if self._check_claims is not None:
                raise jwt.JWTInvalidClaimFormat('Claims check requested but claims is not a json dict')
            return

        self._check_default_claims(claims)

        if self._check_claims is None:
            return

        for name, value in self._check_claims.items():
            if name not in claims:
                raise jwt.JWTMissingClaim('Claim %s is missing' % (name,))

            if name in ['iss', 'sub', 'jti']:
                if value is not None and value != claims[name]:
                    raise jwt.JWTInvalidClaimValue(
                        "Invalid '%s' value. Expected '%s' got '%s'" % (name, value, claims[name])
                    )

            elif name == 'aud':
                if value is not None:
                    if value == claims[name]:
                        continue
                    if isinstance(claims[name], list):
                        if value in claims[name]:
                            continue
                    raise jwt.JWTInvalidClaimValue(
                        "Invalid '%s' value. Expected '%s' to be in '%s'" % (name, claims[name], value)
                    )

            elif name == 'exp':
                if value is not None:
                    self._check_exp(claims[name], value, 0)
                else:
                    self._check_exp(claims[name], time.time(), self._leeway)

            elif name == 'nbf':
                if value is not None:
                    self._check_nbf(claims[name], value, 0)
                else:
                    self._check_nbf(claims[name], time.time(), self._leeway)

            else:
                if value is not None and value != claims[name]:
                    raise jwt.JWTInvalidClaimValue(
                        "Invalid '%s' value. Expected '%s' got '%s'" % (name, value, claims[name])
                    )


class KeystoreService(ContextableService):
    """Public and private key storage."""

    service_name = 'keystore'
    ENC_KEY_SIZE = 256
    ENC_ALGORITHM = 'EC'
    MIN_KEY_TTL = 3600
    KEY_TTL = 3600 * 24
    cache_service_class = BaseCacheService
    cache_key_format = 'keystore.pkey.{kid}'

    def __init__(
        self, app, cache_service: Union[str, cache_service_class] = None, encryption_key_ttl: int = KEY_TTL, logger=None
    ):
        """Initialize.

        :param app:
        :param cache_service: cache service string or instance
        :param encryption_key_ttl: key lifetime in seconds
        :param logger:
        """
        super().__init__(app=app, logger=logger)
        self._encryption_key_ttl = max(self.MIN_KEY_TTL, int(encryption_key_ttl))
        self._kid = None
        self._key = None
        self._pkey = None
        self._pkey_data = None
        self._deadline = None
        self._cache_service_name = cache_service
        self._cache: Optional[BaseCacheService] = None
        self._closed = True
        self._task = None
        self._daemon_sleep_interval = 60

    async def init(self):
        self._cache = self._cache = self.discover_service(self._cache_service_name, cls=self.cache_service_class)
        await self._generate_encryption_key()
        self._closed = False
        self._task = asyncio.create_task(self._loop())

    async def close(self):
        self._closed = True
        self._task.cancel()
        self._task = None

    def closed(self) -> bool:
        return self._closed

    @property
    def deadline(self):
        """Provides more accurate token lifetimes to a client."""
        return self._deadline

    @property
    def key_present(self) -> bool:
        """Return True if a local key pair exists and is still valid."""
        return self._key and time.time() < self._deadline

    async def get_encryption_key(self) -> (str, jwt.JWK):
        """Generate a new key pair if required."""
        if not self.key_present:
            await self._generate_encryption_key()
        return self._kid, self._key

    async def get_public_key(self, kid: str = None) -> Optional[jwk.JWK]:
        """Return local public key by its id or None.

        None returned when:

        - no key with such id exists
        - key deadline is reached
        """
        if self.key_present and (kid == str(uuid.UUID(self._kid)) or kid is None):
            return self._pkey
        cache_kid = self.cache_key_format.format(kid=kid)
        try:
            pkey = await self._cache.get(cache_kid)
            if pkey:
                pkey = loads(pkey)
                pkey = jwk.JWK(**pkey)
                return pkey
        except Exception as exc:
            self.logger.error('Cache service is not available', exc_info=exc)

    async def _generate_encryption_key(self):
        """Generate and set a new key pair and key deadline and push the public key to the shared store (cache)."""
        if self.key_present:
            return
        kid = str(uuid.uuid4())
        key = jwk.JWK.generate(kty=self.ENC_ALGORITHM, size=self.ENC_KEY_SIZE)
        pkey = key._public_params()
        self._pkey = jwk.JWK(**pkey)
        self._pkey_data = dumps(pkey)
        self._kid = kid
        self._key = key
        await self._update_key()

    async def _update_key(self):
        cache_kid = self.cache_key_format.format(kid=self._kid)
        try:
            await self._cache.set(cache_kid, self._pkey_data, ttl=self._encryption_key_ttl)
        except Exception as exc:
            self.logger.error('Cache service is not available', exc_info=exc)
        self._deadline = time.time() + self._encryption_key_ttl

    async def _loop(self):
        while not self._closed:
            await asyncio.sleep(self._daemon_sleep_interval)
            if self.deadline - time.time() < 300:
                await self._update_key()


class JWTService(ContextableService):
    """JWT token generation and validation."""

    service_name = 'jwt'
    TOKEN_ENC_ALG = 'ES256'
    ACCESS_TOKEN_TTL = 600
    REFRESH_TOKEN_TTL = 3600 * 12
    keystore_service_class = KeystoreService

    def __init__(
        self,
        app,
        keystore: Union[str, keystore_service_class] = None,
        access_token_ttl: int = ACCESS_TOKEN_TTL,
        refresh_token_ttl: int = REFRESH_TOKEN_TTL,
        logger=None,
    ):
        """Initialize.

        :param app:
        :param keystore: keystore service
        :param access_token_ttl: access token lifetime sec
        :param refresh_token_ttl: refresh token lifetime sec
        :param logger:
        """
        super().__init__(app=app, logger=logger)
        self._access_token_ttl = max(60, int(access_token_ttl))
        self._refresh_token_ttl = max(self._access_token_ttl, refresh_token_ttl)
        self._keystore = self.discover_service(keystore, cls=self.keystore_service_class)

    def get_token_header(self, token: JWT) -> dict:
        return token.token.jose_header

    def get_token_data(self, token: JWT) -> Optional[dict]:
        return token.claims

    async def generate_access_token(self, ttl=None, **data):
        """Generate a new access token."""
        if ttl is None:
            ttl = self._access_token_ttl
        kid, key = await self._keystore.get_encryption_key()
        return self._generate_token(kid, key, data, ttl=ttl)

    async def generate_refresh_token(self, **data):
        """Generate a new refresh token."""
        kid, key = await self._keystore.get_encryption_key()
        return self._generate_token(kid, key, data, ttl=self._refresh_token_ttl)

    async def generate_token_pair(self, ttl=None, **data):
        """Generate a new access/refresh token pair."""
        if ttl is None:
            ttl = self._access_token_ttl
        kid, key = await self._keystore.get_encryption_key()
        access = self._generate_token(kid, key, data, ttl=ttl)
        refresh = self._generate_token(kid, key, data, ttl=self._refresh_token_ttl)
        return access, refresh

    async def verify_token(self, token: Union[str, JWT]) -> JWT:
        """Verify if given token is valid and properly signed.

        :raises JWError: if token invalid
        :raises JWTExpired: if token has expired
        """
        if type(token) is str:
            _token = token
            try:
                token = JWT(jwt=token)
            except (jwt.JWException, KeyError, ValueError):
                raise NotAuthorized('Invalid authorization token.', service=self.service_name)
        else:
            _token = token.serialize()
        kid = token.token.jose_header.get('kid')
        if not kid:
            raise NotAuthorized('Invalid authorization token.', service=self.service_name)
        try:
            kid = str(uuid.UUID(kid))
        except (ValueError, TypeError, AttributeError):
            raise NotAuthorized('Invalid authorization token.', service=self.service_name)
        pkey = await self._keystore.get_public_key(kid)
        if not pkey:
            raise NotAuthorized('Invalid authorization token.', service=self.service_name)
        try:
            token = JWT(jwt=_token, key=pkey, check_claims={'exp': None})
        except (jwt.JWException, KeyError, ValueError):
            raise NotAuthorized('Invalid authorization token.', service=self.service_name)
        return token

    async def refresh_token(self, refresh_token: Union[str, JWT]):
        """Return a new access token if refresh token is valid."""
        refresh_token = await self.verify_token(refresh_token)
        return await self.generate_token_pair(**refresh_token.claims_data)

    def _generate_token(self, kid: str, key: jwt.JWK, data: dict, ttl: int) -> JWT:
        iat = int(time.time())
        exp = min(iat + ttl, self._keystore.deadline)
        token = JWT(
            header={'typ': 'JWT', 'alg': self.TOKEN_ENC_ALG, 'kid': kid},
            claims={
                **data,
                'iat': iat,
                'exp': exp,
            },
        )
        token.make_signed_token(key)
        return token
