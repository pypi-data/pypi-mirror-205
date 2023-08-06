import logging
from urllib.error import HTTPError

from prometheus_client import push_to_gateway, CollectorRegistry

from matter_observability.config import Config
from matter_observability.exceptions import MisConfigurationError

registry = CollectorRegistry()
job_name = f"batch_{Config.INSTANCE_NAME}"


def publish_metrics():
    if Config.ENABLE_METRICS:
        if Config.PROMETHEUS_PUSH_GATEWAY_HOST is None:
            raise MisConfigurationError("Environment variable: PROMETHEUS_PUSH_GATEWAY_HOST is not set")

        try:
            push_to_gateway(
                f"{Config.PROMETHEUS_PUSH_GATEWAY_HOST}:9091",
                job=job_name,
                registry=registry,
                timeout=1,  # The connection timeout
            )
        except (OSError, HTTPError) as ex:
            logging.warning(f"Observability: Unable to send metrics to the Push Gateway: {str(ex)}")
