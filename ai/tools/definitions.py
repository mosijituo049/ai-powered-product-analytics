from ai.tools.analyst import (
    get_abandonment_by_channel,
    get_abandonment_by_device,
    get_checkout_abandonment,
    get_funnel_metrics,
    get_purchase_prediction,
)
from ai.tools.rag import search_project_knowledge

TOOLS = [
    get_checkout_abandonment,
    get_funnel_metrics,
    get_abandonment_by_device,
    get_abandonment_by_channel,
    get_purchase_prediction,
    search_project_knowledge,
]