from opentelemetry import trace, metrics
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

# Configure resources
resource = Resource(attributes={
    SERVICE_NAME: "billjard-backend"
})

# Configure Tracer
trace_provider = TracerProvider(resource=resource)
trace_provider.add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces"))
)
trace.set_tracer_provider(trace_provider)

# Configure Meter Provider for metrics
reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(endpoint="http://localhost:4318/v1/metrics")
)
meter_provider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(meter_provider)

# Create Meter instance
meter = metrics.get_meter("billjard-backend", version="1.0.0")

# Define metrics
request_counter = meter.create_counter(
    name="http_requests_total",
    description="Total number of HTTP requests",
    unit="1"
)

active_users_gauge = meter.create_observable_gauge(
    name="active_users",
    callbacks=[],
    description="Number of active users currently online"
)

response_latency_histogram = meter.create_histogram(
    name="http_response_latency",
    description="Latency of HTTP responses",
    unit="ms"
)

# # Functions to add callbacks (example for gauge)
# def track_active_users():
#     # Replace with your actual logic to get active users count
#     active_users = 42
#     return [metrics.Observation(1, active_users)]
#
# # Register gauge callback
# active_users_gauge.callbacks = [track_active_users]
