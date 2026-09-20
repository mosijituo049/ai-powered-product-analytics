# Evaluation Criteria

## Case 1 — Overall checkout abandonment

### PASS
- Calls `get_checkout_abandonment`
- Reports the overall abandonment rate as 56.33%
- Does not invent unsupported numerical values

### FAIL
- Does not call the required tool
- Reports an incorrect value
- Agent reaches maximum iterations

## Case 2 — Highest abandonment device

### PASS
- Calls `get_abandonment_by_device`
- Calls `get_checkout_abandonment`
- Identifies Tablet as the highest abandonment device
- Reports Tablet abandonment as 57.20%
- Reports overall abandonment as 56.33%

### FAIL
- Does not call the required tools
- Identifies the wrong device
- Reports incorrect values
- Agent reaches maximum iterations

## Case 3 — Channel abandonment

### PASS
- Calls `get_abandonment_by_channel`
- Reports the abandonment rate for each acquisition channel
- Does not invent unsupported channels or values

### FAIL
- Does not call the required tool
- Reports incorrect channel values
- Invents unsupported channels
- Agent reaches maximum iterations

## Case 4 — Definition question

### PASS
- Does not call analytics tools
- Provides a correct definition of checkout abandonment
- Does not introduce unsupported dataset-specific information

### FAIL
- Calls an analytics tool unnecessarily
- Mixes unrelated GA4 metrics into the answer
- Provides an incorrect definition

## Case 5 — Causal question

### PASS
- Does not claim that the available data proves a cause
- Clearly states that the available data is insufficient to determine why users abandon checkout
- Distinguishes observed data from causal explanations

### FAIL
- Claims that a device, channel, or other factor caused abandonment
- Invents explanations not supported by the available data
- Presents correlation or descriptive metrics as causal evidence

## Case 6 — Definition and overall abandonment

### PASS
- Calls `search_project_knowledge`
- Calls `get_checkout_abandonment`
- Uses project knowledge for the definition
- Reports the current overall abandonment rate as 56.33%
- Does not mix project knowledge and analytics facts incorrectly

### FAIL
- Does not call the required tools
- Uses analytics data to answer the project definition
- Reports an incorrect abandonment rate
- Invents unsupported information
- Agent reaches maximum iterations


## Case 7 — Device abandonment and definition

### PASS
- Calls `get_abandonment_by_device`
- Calls `search_project_knowledge`
- Reports the device-level abandonment rates from tool data
- Uses project knowledge for the definition
- Does not invent unsupported values

### FAIL
- Does not call the required tools
- Uses the wrong source for the definition
- Reports incorrect device-level values
- Invents unsupported information
- Agent reaches maximum iterations


## Case 8 — Purchase prediction

### PASS
- Calls `get_purchase_prediction`
- Reports the prediction returned by the tool
- Reports the purchase probability returned by the tool
- Does not invent prediction values

### FAIL
- Does not call the required tool
- Reports an incorrect prediction or probability
- Invents unsupported prediction values
- Agent reaches maximum iterations


## Case 9 — Derived metric grounding

### PASS
- Calls `get_purchase_prediction`
- Reports `checkout_ratio` as 0.0 for session 6636007571
- Uses the derived metric returned by the tool as the authoritative value
- Does not recalculate `checkout_ratio` from `begin_checkout` and `add_to_cart`

### FAIL
- Reports `checkout_ratio` as 2.0
- Recalculates the derived metric independently
- Ignores the value returned by the tool
- Claims that `begin_checkout / add_to_cart` equals 2.0

### Known failure
- Current known failure: the LLM may report `checkout_ratio` as 2.0 even though the tool returns 0.0.
- This case is intentionally retained as a regression case until the grounding issue is fixed.


## Case 10 — Non-existent session

### PASS
- Calls `get_purchase_prediction`
- Does not invent a prediction or probability
- Clearly states that the session data is unavailable or not found

### FAIL
- Invents a prediction
- Invents a purchase probability
- Provides unsupported session features
- Agent reaches maximum iterations


## Case 11 — Unsupported country breakdown

### PASS
- Does not invent a country-level abandonment rate
- Clearly explains that the available analytics tools do not provide the requested country-level metric
- Does not present an unsupported numerical value as fact

### FAIL
- Invents a Japan abandonment rate
- Provides an unsupported numerical value
- Treats an unrelated metric as a country-level abandonment rate


## Case 12 — Device and channel comparison

### PASS
- Calls `get_abandonment_by_device`
- Calls `get_abandonment_by_channel`
- Reports the returned device-level and channel-level metrics accurately
- Does not invent additional categories

### FAIL
- Does not call the required tools
- Uses only one of the two required tools
- Reports incorrect values
- Invents unsupported categories
- Agent reaches maximum iterations


## Case 13 — Funnel analysis

### PASS
- Calls `get_funnel_metrics`
- Uses the returned funnel metrics
- Identifies the largest stage drop-off according to the tool data
- Reports the corresponding metric accurately

### FAIL
- Does not call the required tool
- Identifies the wrong funnel stage
- Reports an incorrect metric
- Invents unsupported funnel values
- Agent reaches maximum iterations


## Case 14 — Project knowledge

### PASS
- Calls `search_project_knowledge`
- Uses project-specific knowledge to answer the question
- Does not invent project information

### FAIL
- Does not use project knowledge when required
- Invents project-specific information
- Uses unsupported external information as project facts


## Case 15 — Unsupported general benchmark

### PASS
- Does not invent a worldwide e-commerce abandonment benchmark
- Clearly distinguishes project-specific information from unsupported external information
- States that the requested benchmark is not available in the project knowledge

### FAIL
- Invents a worldwide benchmark
- Presents an unsupported external statistic as fact
- Treats project data as a worldwide industry benchmark