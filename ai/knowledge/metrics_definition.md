# Metrics Definition

## Checkout Session

A checkout session is a session where the user initiated checkout.

In the analytical model, checkout sessions are identified using:

`begin_checkout > 0`

The checkout KPI query uses sessions from `int_sessions` where `begin_checkout > 0`.

## Purchase Session

A purchase session is a checkout session where:

`purchased = TRUE`

## Abandoned Checkout Session

An abandoned checkout session is a checkout session where:

`checkout_abandoned = TRUE`

The project treats a checkout session as abandoned when the user initiated checkout but did not complete a purchase.

## Checkout Abandonment Rate

Checkout abandonment rate measures the proportion of checkout sessions that were abandoned.

Formula:

`abandoned checkout sessions / checkout sessions × 100`

The project calculates this metric using:

- `checkout_sessions`
- `abandoned_sessions`

The current numerical value should be retrieved from the analytics tools rather than stored as a fixed value in this knowledge document.

## Purchase Conversion

Purchase conversion measures the proportion of relevant sessions that resulted in a purchase.

In the checkout analysis, purchase sessions are identified using:

`purchased = TRUE`

## Overall Conversion Rate

Overall conversion rate measures the proportion of sessions reaching a funnel stage relative to the initial funnel population.

The funnel model contains an `overall_conversion_rate` metric for each funnel stage.

## Stage Drop-off Rate

Stage drop-off rate measures the proportion of sessions lost between one funnel stage and the previous stage.

Formula:

`(1 - current stage sessions / previous stage sessions) × 100`

The funnel metrics query calculates this value using the number of sessions at the current stage and the previous funnel stage.

## Session Duration

Session duration represents the duration of a user session in seconds.

It is one of the behavioral features used in the project.

## Engagement per Event

Engagement per event is an engineered session-level feature.

Formula:

`total engagement time / total events`

It represents the average engagement time associated with each event within a session.

## Item View Rate

Item view rate is an engineered session-level feature.

Formula:

`item views / pageviews`

It represents the proportion of page views associated with item views.

## Checkout Ratio

Checkout ratio is an engineered session-level feature.

Formula:

`begin checkout / add to cart`

It represents the relationship between checkout initiation and add-to-cart activity within a session.

## Purchase Probability

Purchase probability is the probability produced by the purchase intent machine learning model.

It represents a model prediction, not an actual purchase outcome.

When reporting this metric, describe it as a predicted purchase probability.