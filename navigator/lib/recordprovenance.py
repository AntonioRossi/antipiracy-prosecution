"""Representational typed-command provenance for verification records.

The values in this module identify the command contract that produced a
record.  They are audit metadata, not a signature or a claim that record
contents are cryptographically unforgeable.
"""


ATTESTATION_PRODUCER_COMMAND = "navigator/build.py attest/v1"


def attestation_producer_problems(record):
    """Return defects in an attestation's exact producer-command marker."""
    if not isinstance(record, dict):
        return ["attestation record is not an object"]
    if record.get("producerCommand") != ATTESTATION_PRODUCER_COMMAND:
        return [
            "attestation producerCommand must be exactly %r"
            % ATTESTATION_PRODUCER_COMMAND
        ]
    return []
