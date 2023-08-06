from starlette_exporter import PrometheusMiddleware, handle_metrics

from matter_observability.config import Config
from matter_observability.exceptions import MisConfigurationError
from .request_id import process_request_id


def configure_middleware(app, skip_paths=None):
    metrics_path = "/internal/metrics"

    app.middleware("http")(process_request_id)

    if Config.ENABLE_METRICS:
        if bool(Config.INSTANCE_NAME) is False:
            raise MisConfigurationError("Environment variable: INSTANCE_NAME is not valid")

        app.add_middleware(
            PrometheusMiddleware,
            app_name=Config.INSTANCE_NAME,
            group_paths=True,
            skip_paths=[metrics_path] + skip_paths if skip_paths else [metrics_path],
        )
        app.add_route(metrics_path, handle_metrics)
