# Funnel Definition

## E-commerce Funnel

The project uses a five-stage e-commerce funnel:

1. Page View
2. View Item
3. Add to Cart
4. Begin Checkout
5. Purchase

The funnel is analyzed at the session level.

## Page View

Page View is the first stage of the e-commerce funnel.

It represents a session containing page view activity.

This stage is used as the initial population for the funnel analysis.

## View Item

View Item represents a session where the user viewed a product or item.

This stage indicates product-level engagement after visiting the application.

## Add to Cart

Add to Cart represents a session where the user added a product to the shopping cart.

This stage indicates stronger purchase intent than simply viewing an item.

## Begin Checkout

Begin Checkout represents a session where the user initiated the checkout process.

In the session-level analysis, checkout initiation is identified using:

`begin_checkout > 0`

This stage defines the population used for the checkout abandonment analysis.

## Purchase

Purchase represents a session where the user completed a purchase.

In the session-level analytical model, purchase is represented by:

`purchased = TRUE`

## Funnel Conversion

For each funnel stage, the project calculates the number of sessions reaching that stage and its overall conversion rate.

The funnel stages are ordered as:

`Page View → View Item → Add to Cart → Begin Checkout → Purchase`

## Funnel Drop-off

Stage drop-off is calculated by comparing the number of sessions at the current stage with the number of sessions at the previous stage.

Formula:

`(1 - current stage sessions / previous stage sessions) × 100`

The first funnel stage has no previous stage and therefore has a drop-off rate of zero.

## Checkout Abandonment and Funnel

Checkout abandonment is analyzed after users have reached the Begin Checkout stage.

A checkout session is considered abandoned when checkout was initiated but the session did not result in a purchase.

Therefore, checkout abandonment analysis focuses specifically on users who entered the checkout stage rather than all website sessions.