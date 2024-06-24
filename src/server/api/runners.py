from core.logger import SubLogger

logger = SubLogger("Runners")


def register_runners_api(app, Server):
    @app.get("/runner/{slug}/stat")
    async def get_stat(slug: str):
        result = Server.get_stat(slug)
        logger.success(f"Get {slug} stat {result}")
        return result

    @app.post("/runner/{slug}/stat")
    async def put_stat(slug: str, stat: dict):
        logger.success(f"Put stat {slug} {stat}")
        Server.set_stat(slug, int(stat["id"]), stat)

    @app.get("/runner/{slug}/guide")
    async def get_guide(slug: str):
        result = Server.get_guide(slug)
        logger.success(f"Get {slug} guide {result}")
        return result
