from pydantic import BaseSettings


class Settings(BaseSettings):
    TESTING: bool = False
    PRODUCTION: bool = False

    MONGO_USER: str = "trader"
    MONGO_PASS: str = "trader"
    MONGO_HOST: str = "trader.uzfplyn.mongodb.net"
    MONGO_DB: str = "trader"

    BINANCE_API_KEY: str
    BINANCE_SECRET: str
    OKX_API_KEY: str
    OKX_SECRET_KEY: str
    OKX_PASSPHRASE: str

    MEXC_KEY: str
    MEXC_SECRET: str
    # MONITOR_URL: str

    class Config:
        case_sensitive = True


settings = Settings()
