from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
INDEX = (ROOT / "plugins/cogentnexus-rotation/src/index.ts").read_text(encoding="utf-8")
TICKETS = (ROOT / "plugins/cogentnexus-rotation/src/ticket-store.ts").read_text(encoding="utf-8")


class PluginContinuityContractTests(unittest.TestCase):
    def test_delivery_receipts_are_order_independent_and_ticket_scoped(self):
        for marker in (
            "earlyDeliveryReceipts",
            "ticketedRuns",
            'directResult === "unchanged" && ticketedRuns.has(runId)',
            'directState === "awaiting_delivery" && earlyReceipt',
            'directState === "unchanged"',
            "waitForIdle",
        ):
            self.assertIn(marker, INDEX)

    def test_post_compaction_guard_promotes_original_direct_ticket(self):
        for marker in (
            '[CogentNexus Continuation: post-compaction]',
            "promotePendingDirectForSession",
            "hasPendingDirectExecutionForSession",
            'status=\'waiting\',workflow_eligible=1',
            "post_compaction_promoted",
        ):
            self.assertIn(marker, INDEX if marker in INDEX else TICKETS)

    def test_response_ready_delivery_is_not_compaction_promoted(self):
        self.assertIn("response_ready_at IS NULL", TICKETS)
        self.assertIn("delivery_confirmed_at", TICKETS)
        self.assertIn("recoverUndeliveredDirect", TICKETS)


if __name__ == "__main__":
    unittest.main()
