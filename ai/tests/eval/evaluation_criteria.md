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
- Identifies Desktop as the highest abandonment device
- Reports Desktop abandonment as 56.95%
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