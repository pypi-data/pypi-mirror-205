from acb.config.settings import AppSettings


class SentrySettings(AppSettings):
    enabled = ac.app.sentry_enabled
    dsn = "https://ea3f99402f144c2badf512c55d3d7bb7@o310698.ingest.sentry.io/1777286"
    sample_rate = 1.0 if not deployed else 0.5
