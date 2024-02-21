from aiohttp import ClientSession, TCPConnector


def http_session(verify_ssl: bool = True) -> ClientSession:
    """
    Returns a new aiohttp client instance.

    Usage:

        with http_session() as session:
            async with session.get('http://python.org') as response:
                print("Status:", response.status)
    """
    return ClientSession(
        connector=TCPConnector(limit_per_host=5, verify_ssl=verify_ssl)
    )
