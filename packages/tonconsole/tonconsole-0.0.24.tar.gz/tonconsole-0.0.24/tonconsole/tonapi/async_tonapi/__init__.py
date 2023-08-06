from .client import AsyncTonapiClient

from .methods.accounts import AccountMethod
from .methods.jettons import JettonMethod
from .methods.nfts import NftMethod
from .methods.traces import TraceMethod


class AsyncTonapi(AsyncTonapiClient):
    def __init__(self, api_key: str, testnet: bool = False):
        """
        :param api_key: You can get an access token here https://tonconsole.com/
        :param testnet: Use true, if you want to switch to testnet
        """
        super(AsyncTonapi, self).__init__(api_key, testnet)

    @property
    def accounts(self) -> AccountMethod:
        return AccountMethod(api_key=self._api_key, testnet=self._testnet)

    @property
    def jettons(self) -> JettonMethod:
        return JettonMethod(api_key=self._api_key, testnet=self._testnet)

    @property
    def nfts(self) -> NftMethod:
        return NftMethod(api_key=self._api_key, testnet=self._testnet)

    @property
    def traces(self) -> TraceMethod:
        return TraceMethod(api_key=self._api_key, testnet=self._testnet)
