import logging
import sys
import os

# Import the `configure_azure_monitor()` function from the
# `azure.monitor.opentelemetry` package.
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace
from opentelemetry.trace import (
    get_tracer_provider,
)


if os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING"):
    # Configure OpenTelemetry to use Azure Monitor with the
    # APPLICATIONINSIGHTS_CONNECTION_STRING environment variable.
    configure_azure_monitor(enable_live_metrics=True, logger_name=__name__)

    tracer = trace.get_tracer(__name__, tracer_provider=get_tracer_provider())


logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout)
