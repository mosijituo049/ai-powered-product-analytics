TOOL_SCHEMAS = {
    "get_checkout_abandonment": {
        "name": "get_checkout_abandonment",
        "description": (
            "Return checkout abandonment KPIs from the GA4 dataset. "
            "This function requires no arguments."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },

    "get_funnel_metrics": {
        "name": "get_funnel_metrics",
        "description": (
            "Return e-commerce funnel metrics from the GA4 dataset. "
            "This function requires no arguments."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },

    "get_abandonment_by_device": {
        "name": "get_abandonment_by_device",
        "description": (
            "Return checkout abandonment metrics broken down by device "
            "category (desktop, mobile, tablet). "
            "This function requires no arguments."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },

    "get_abandonment_by_channel": {
        "name": "get_abandonment_by_channel",
        "description": (
            "Return checkout abandonment metrics broken down by "
            "acquisition channel. "
            "This function requires no arguments."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },

    "get_purchase_prediction": {
        "name": "get_purchase_prediction",
        "description": (
            "Predict the purchase probability for a specific checkout "
            "session. The session_id must be a valid GA4 session ID."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "session_id": {
                    "type": "integer",
                    "description": (
                        "The GA4 session ID to analyze."
                    ),
                },
            },
            "required": ["session_id"],
            "additionalProperties": False,
        },
    },

    "search_project_knowledge": {
        "name": "search_project_knowledge",
        "description": (
            "Search project documentation for definitions, methodology, "
            "and business context. "
            "Do NOT use this tool to retrieve current GA4 metrics, "
            "KPIs, device breakdowns, channel breakdowns, or predictions. "
            "Use the analytics tools for numerical results."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": (
                        "The question or concept to search for "
                        "in the project knowledge base."
                    ),
                },
            },
            "required": ["query"],
            "additionalProperties": False,
        },
    },
}