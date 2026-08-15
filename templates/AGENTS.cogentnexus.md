## CogentNexus - Managed Runtime

CogentNexus is enabled for this workspace. Every eligible owner message is committed to the durable Ticket store before model inference, then routed through the lightest reliable execution lane.

1. Preserve the user's message and session identity in the Ticket store before inference.
2. DIRECT conversation remains lightweight; do not create a staged workflow unless complexity, interruption, or risk requires it.
3. If a direct turn is interrupted, the Host Controller may promote the committed Ticket to durable recovery without requiring the user to repeat it.
4. Durable work must resume from committed evidence and must not repeat external side effects blindly.
5. A terminal user-visible request must end as delivered, cancelled, or explicitly failed; never silently disappear.
6. Host PASSTHROUGH removes this managed block and disables CogentNexus interception so OpenClaw behaves normally.

Keep private reasoning private. User intent, authorization, safety rules, and higher-priority instructions always take precedence.
