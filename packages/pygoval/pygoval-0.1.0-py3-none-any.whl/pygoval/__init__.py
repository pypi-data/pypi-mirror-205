from .proto import api_pb2 as api
import aiohttp


from .channel import Channel, Channel0, ChannelStatus
from .exceptions import GovalException, ConnectionMetadataExeption, ChannelClosed
from .client import ConnectionMetadata, Client

__all__ = (
    # pygoval.proto
    "api",
    # pygoval.client
    "ConnectionMetadata",
    "Client",
    # pygoval.channel
    "Channel",
    "Channel0",
    "ChannelStatus",
    # pygoval.exceptions
    "ChannelClosed",
    "GovalException",
    "ConnectionMetadataExeption",
)


async def fetch_token(replId: str, sid: str) -> ConnectionMetadata:
    async with aiohttp.ClientSession(
        headers={
            "X-Requested-With": "PyGoval (github.com/PotentialStyx/pygoval)",
            "User-Agent": "PyGoval (github.com/PotentialStyx/pygoval)",
            "origin": "https://replit.com",
        },
        cookies={"connect.sid": sid},
    ) as session:
        async with session.post(
            f"https://replit.com/data/repls/{replId}/get_connection_metadata"
        ) as response:
            return await response.json()
