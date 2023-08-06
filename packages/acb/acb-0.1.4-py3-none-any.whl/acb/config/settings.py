import typing as t
from pathlib import Path
from pprint import pprint

from aiopath import AsyncPath
from pydantic import BaseSettings
from acb.actions import dump
from acb.actions import hash
from acb.actions import load
from acb.adapters import SecretManager
from addict import Dict as adict


class AppConfig(BaseSettings):
    deployed = False
    basedir = Path().cwd()
    tmp = basedir / "tmp"
    config_path = basedir / "config.py"
    settings: list = None
    secrets: dict = None
    debug: bool = True
    deployed: bool = True if basedir.name == "app" else False

    async def init(self, deployed: bool = False):
        self.deployed = True if self.basedir.name == "app" else False
        # deployed = True if basedir.name == "srv" else False
        self.secrets = await SecretManager().init()
        print(f"{str(self.config_path.resolve())}")
        self.deployed = deployed
        self.debug = False if deployed else True
        pprint(self.settings)
        pprint(self.secrets)
        classes = dict()
        for s in [s for s in self.settings if "Settings" in s.__class__.__name__]:
            print(s, type(s))
            settings_module = s.__class__.__name__.replace("Settings", "").lower()
            print(settings_module)
            classes["settings_module"] = s()
        self.__init__(**classes)
        print("done")
        return self

    class Config:
        extra = "allow"


class AppSettings(BaseSettings):
    formatted: bool = False
    yml_settings: t.Any = None
    values: dict = None
    cls_name: str = None

    class Config:
        extra = "allow"
        arbitrary_types_allowed = True
        json_loads = load.json
        json_dumps = dump.json

    def __init__(self, **values: t.Any) -> None:
        super().__init__(**values)
        # name = self.__class__.__name__.replace("Settings", "").lower()
        # settings = ac.basedir / "settings"
        # for path in [
        #     p for p in settings.iterdir() if p.suffix == ".yml" and p.stem == name
        # ]:
        #     self.yml_settings = path.read_text()
        #     self.values = load.yml(self.yml_settings)
        #     current_hash = hash.crc32c(self.yml_settings)
        #     new_settings = dump.yml(values)
        #     new_hash = hash.crc32c(new_settings)
        #     if not ac.deployed and not self.formatted and current_hash != new_hash:
        #         print(f"Changes detected in {path} - formatting...")
        #         path.write_text(new_settings)
        #         self.formatted = True
        #     super().__init__(**values)

    # @classmethod
    # async def add_settings(self):
    #     setattr(ac, self.cls_name, self)

    async def __call__(self, ac) -> None:
        print("call")
        self.cls_name = self.__class__.__name__.replace("Settings", "").lower()
        settings = ac.basedir / "settings"
        for path in [
            AsyncPath(p)
            for p in settings.iterdir()
            if p.suffix == ".yml" and p.stem == self.cls_name
        ]:
            self.yml_settings = await path.read_text()
            self.values = await load.yml(self.yml_settings)
            current_hash = hash.crc32c(self.yml_settings)
            new_settings = await dump.yml(self.values)
            new_hash = await hash.acrc32c(new_settings)
            if not ac.deployed and not self.formatted and current_hash != new_hash:
                print(f"Changes detected in {path} - formatting...")
                await path.write_text(new_settings)
                self.formatted = True
                # pprint(self.values)
            super().__init__(**self.values)
        # setattr(ac, self.cls_name, self)


class App(AppSettings):
    project = "splashstand-255421"
    name = str
    # path = basedir
    title = "SplashStand"
    timezone = "US/Pacific"
    domain: t.Optional[str]
    localhost = "localhost"
    url = "splashstand.net"
    pwa_name = "SplashStand"
    framework = "bulma"
    store_enabled = True
    mail_provider = "mailgun"
    sentry_enabled = True
    facebook_login_enabled = False
    google_login_enabled = True
    fontawesome_pro = True
    ios_id: t.Optional[str]
    datetime_format = "MM-DD-YYYY h:mm A"
    about: t.Optional[str]
    pages = dict()
    social_media = list()
    favicon: t.Optional[str]
    icon: t.Optional[str]
    contact = adict(
        email=t.Optional[str], phone=t.Optional[str], address=t.Optional[str]
    )
    copyright: t.Optional[str]
    theme_color = "ffffff"
    bgcolor = adict(app="ffffff", resize="ffffff")
    permanent_session_lifetime: int = 2_678_400
    wtf_csrf_time_limit: int = 172_800
    roles: list = ["admin", "owner", "contributor", "user"]
    media_types: list = ["image", "video", "audio"]
    video_exts: list = [".webm", ".m4v", ".mp4"]
    image_exts: list = [".jpeg", ".jpg", ".png", ".webp"]
    audio_exts: list = [".m4a", ".mp4"]
    allowed_exts: list = [
        ".html",
        ".scss",
        ".json",
        ".js",
        ".xml",
        ".yml",
        ".py",
        ".ini",
        ".gz",
        ".pickle",
        ".txt",
    ]
    gmail = adict(
        enabled=True,
        mx_servers=[
            "1 aspmx.l.google.com.",
            "5 alt1.aspmx.l.google.com.",
            "5 alt2.aspmx.l.google.com.",
            "10 alt3.aspmx.l.google.com.",
            "10 alt4.aspmx.l.google.com.",
        ],
    )
    hashlib = "blake2b"
    bulma_extensions = [
        "bulma-checkradio",
        "bulma-divider",
        "bulma-pageloader",
        "bulma-pricingtable",
    ]
    codemirror = adict(version="5.58.3", theme="cobalt")
    fontawesome = adict(version="5.15.1", kit="274806bd44")
    jquery_version = "3.5.1"
    # ckeditor_fields = ["text", "description", "about", "intro", "info"]
    # datetime_fields = ["date", "published", "created", "released", "born"]
    favicon_sizes = ["32", "128", "152", "167", "180", "192", "196"]

    class IconSizes(BaseModel):
        square = (["120", "152", "180"],)
        android = (["192", "512"],)
        ios = [
            ("1242x2688", "414", "896", "3"),
            ("828x1792", "414", "896", "2"),
            ("1125x2436", "375", "812", "3"),
            ("1242x2208", "414", "736", "3"),
            ("750x1334", "375", "667", "2"),
            ("2048x2732", "1024", "1366", "2"),
            ("1668x2388", "834", "1194", "2"),
            ("1668x2224", "834", "1112", "2"),
            ("1536x2048", "768", "1024", "2"),
        ]

    icon_sizes = IconSizes()

    class Header(BaseSettings):
        dimensions = ("1920x1080",)
        logo_dimensions = ("1024x240",)

    header = Header()

    class NotificationIcons(BaseSettings):
        info = "info-circle"
        success = "check-circle"
        danger = "exclamation-circle"
        warning = "exclamation-triangle"

    notification_icons = NotificationIcons()

    bitly = adict(
        access_token="3a68d5dab21a094e0d76c6cbf3d428f21b21976d",
        group_guid="o_3j8qhptjn4",
        domain="bit.ly",
        url="https://api-ssl.bitly.com/v4",
    )

    def __init__(self, **data: t.Any) -> None:
        super().__init__(**data)
        self.title = self.title.title()
        self.localhost = "host.docker.internal" if debug.docker else self.localhost
        self.domain = (
            f"{self.name}.splashstand.net" if deployed else f"{self.localhost}:5000"
        )
        self.url = f"https://{self.name}.{self.domain}"
