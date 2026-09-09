#!/usr/bin/env python3
"""Final CogentNexus-OpenClaw Host overlay with provider-neutral lifecycle."""
from __future__ import annotations

from datetime import datetime, timezone

import host_provider_v092 as base
import provider_event_liveness_v092 as provider_event_liveness

provider_event_liveness.patch_provider_events(base.provider_events)

legacy = base.legacy
providers = base.providers
provider_events = base.provider_events
ORIGINAL_ENABLE_MANAGED = legacy.enable
ORIGINAL_RESTART_MANAGED = legacy.restart_managed
BASE_PROVIDER_RUNTIME = base.provider_aware_runtime


def _parse_utc(value):
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def progress_for_call(root, target, started_at):
    """Match provider proof-of-life to a call using normalized UTC time."""
    progress = provider_events.latest_progress(root, target)
    if not isinstance(progress, dict):
        return None
    event_time = _parse_utc(progress.get("at"))
    started_time = _parse_utc(started_at)
    if event_time is None or started_time is None or event_time < started_time:
        return None
    return progress


# Different valid UTC spellings (`Z` vs `+00:00`) are not lexicographically
# ordered by time, so keep the proven normalized evidence matcher.
base._progress_for_call = progress_for_call


def provider_event_aware_runtime(root, *args, timeout=180, check=True):
    """Delegate runtime lifecycle without taking provider/process ownership.

    Provider/model/auth routing and provider process lifecycle belong to
    OpenClaw in v0.9.5. Legacy ``--provider`` syntax is handled by the lower
    compatibility façade and must not cause this final Host layer to select,
    start, stop, probe, or attach a provider adapter.
    """
    return BASE_PROVIDER_RUNTIME(root, *args, timeout=timeout, check=check)


legacy.runtime = provider_event_aware_runtime


def enable_managed(root):
    """Preserve cleanup of any legacy watcher after transactional enable failure."""
    try:
        return ORIGINAL_ENABLE_MANAGED(root)
    except Exception:
        try:
            provider_events.stop_adapter(root)
        except Exception:
            # Compatibility cleanup must never mask the original transactional
            # activation failure. A later migration/reconciliation pass can retry.
            pass
        raise


def restart_managed(root):
    """Restart the CNX/OpenClaw runtime boundary without provider authority."""
    return ORIGINAL_RESTART_MANAGED(root)


legacy.enable = enable_managed
legacy.restart_managed = restart_managed


if __name__ == "__main__":
    raise SystemExit(legacy.main())
