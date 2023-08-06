try:
    from qwak.inner import wire_dependencies

    from qwak_inference.batch_client.batch_client import BatchInferenceClient
    from qwak_inference.feedback_client import FeedbackClient

    wire_dependencies()
except ImportError:
    # We are conditional loading these clients since the skinny does
    # not support them due to the pandas, numpy, joblib, etc. dependencies
    pass

from qwak_inference.realtime_client import RealTimeClient

__all__ = ["BatchInferenceClient", "FeedbackClient", "RealTimeClient"]

__version__ = "0.0.11.rc0"
