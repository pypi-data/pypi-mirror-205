class Loggers(BaseModel):
    log_format: str = str()
    configs: dict = dict()
    uvicorn = ["uvicorn.access", "uvicorn.error"]
    cache = ["starlette_cache", "httpx_caching"]
    sql = [
        "sqlalchemy.engine",
        "sqlalchemy.orm",
        "sqlalchemy.pool",
        "sqlalchemy.dialects",
    ]
    format = adict(
        time="<b><e>[</e> <w>{time:YYYY-MM-DD HH:mm:ss.SSS}</w> <e>]</e></b>",
        level=" <level>{level:>8}</level>",
        sep=" <b><w>in</w></b> ",
        name="{name:>20}",
        line="<b><e>[</e><w>{line:^5}</w><e>]</e></b>",
        message="  <level>{message}</level>",
    )
    level_per_module = {m: "DEBUG" if v is True else "INFO" for (m, v) in debug.items()}

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self.log_format = "".join(self.format.values())
        self.configs = dict(
            filter=self.level_per_module,
            format=self.log_format,
            enqueue=True,
            backtrace=True,
        )

    async def init(self) -> None:
        logger.remove()
        logging.getLogger("uvicorn").handlers.clear()
        logger.add(sys.stderr, **self.configs)
        logger.level("DEBUG", color="<cyan>")
        if debug.log:
            logger.debug("debug")
            logger.info("info")
            logger.warning("warning")
            logger.error("error")
            logger.critical("critical")
            await apformat(self.level_per_module)


loggers = Loggers()
