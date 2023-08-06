from aiopath import AsyncPath
from addict import Dict as adict

theme = adict(
    app=adict(
        base=adict(templates=AsyncPath("theme") / "app" / "base" / "templates"),
        templates=AsyncPath("theme") / "app" / ac.app.framework / "templates",
        style=AsyncPath("theme") / "app" / ac.app.framework / "style",
    ),
    admin=adict(
        base=adict(templates=AsyncPath("theme") / "admin" / "base" / "templates"),
        templates=AsyncPath("theme") / "admin" / ac.admin.framework / "templates",
        style=AsyncPath("theme") / "admin" / ac.admin.framework / "style",
    ),
)
