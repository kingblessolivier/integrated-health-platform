"""
Pure consent logic (no DB) — unit-tested in tests.py. Consent is enforced *in addition to*
technical authorisation (docs/08): a patient may revoke a specific actor's access.
"""


def consent_permits(records, actor_id) -> bool:
    """`records` is an iterable of (actor_id, status). Deny if the actor has a 'revoked'
    consent for this patient; otherwise allow."""
    for record_actor, status in records:
        if str(record_actor) == str(actor_id) and status == "revoked":
            return False
    return True
