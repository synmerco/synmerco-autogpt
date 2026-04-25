"""SynmercoCommands — 46 commands for AI agent commerce.

Works standalone or as an AutoGPT CommandProvider component.
"""

from __future__ import annotations

import json
from typing import Any

from synmerco_autogpt._client import (
    SynmercoHTTPClient, SynmercoAPIError,
    validate_did, validate_amount, validate_sha256,
)
from synmerco_autogpt._registry import TOOLS


def _call(http: SynmercoHTTPClient, tool_name: str, **kwargs) -> str:
    tdef = next((t for t in TOOLS if t["name"] == tool_name), None)
    if not tdef:
        return json.dumps({"error": f"Unknown tool: {tool_name}"})
    for fname, fmeta in tdef.get("fields", {}).items():
        val = kwargs.get(fname)
        if val is None: continue
        ft = fmeta.get("type", "str")
        if ft == "did": kwargs[fname] = validate_did(val)
        elif ft == "amount": kwargs[fname] = validate_amount(val)
        elif ft == "sha256": kwargs[fname] = validate_sha256(val)
    path = tdef["path"]
    for pp in tdef.get("path_params", []):
        path = path.replace("{" + pp + "}", str(kwargs.pop(pp, "")))
    try:
        if tdef["method"] == "GET":
            return json.dumps(http.get(path, **kwargs), indent=2, default=str)
        else:
            return json.dumps(http.post(path, kwargs), indent=2, default=str)
    except SynmercoAPIError as e:
        return f"Synmerco API error: {e}"
    except Exception as e:
        return f"Error: {e}"


class SynmercoCommands:
    """46 Synmerco commands. Works standalone or inside AutoGPT."""

    def __init__(self, api_key: str | None = None, base_url: str | None = None, timeout: float = 30.0):
        self._http = SynmercoHTTPClient(api_key=api_key, base_url=base_url, timeout=timeout)

    def lookup_trust_score(
        self,
        did: str,
    ) -> str:
        """Look up any AI agent's trust score, reputation tier, transaction history, and on-chain verification status. Free, no auth required."""
        kwargs: dict = {}
        if did is not None: kwargs["did"] = did
        return _call(self._http, "lookup_trust_score", **kwargs)

    def search_agents(
        self,
        capability: str | None = None,
        minScore: int | None = None,
        availability: str | None = None,
    ) -> str:
        """Search for AI agents by capability, minimum trust score, and availability. Free, no auth required."""
        kwargs: dict = {}
        if capability is not None: kwargs["capability"] = capability
        if minScore is not None: kwargs["minScore"] = minScore
        if availability is not None: kwargs["availability"] = availability
        return _call(self._http, "search_agents", **kwargs)

    def compare_agents(
        self,
        did1: str,
        did2: str,
    ) -> str:
        """Compare trust scores and transaction history of two AI agents side by side. Free, no auth required."""
        kwargs: dict = {}
        if did1 is not None: kwargs["did1"] = did1
        if did2 is not None: kwargs["did2"] = did2
        return _call(self._http, "compare_agents", **kwargs)

    def estimate_fees(
        self,
        amountCents: int,
    ) -> str:
        """Calculate Synmerco fees for a given transaction amount. Shows platform fee, insurance, referral split, and net to seller. Free, no auth required."""
        kwargs: dict = {}
        if amountCents is not None: kwargs["amountCents"] = amountCents
        return _call(self._http, "estimate_fees", **kwargs)

    def get_platform_info(
        self,
    ) -> str:
        """Get Synmerco platform information including supported chains, fees, features, and documentation links. Free, no auth required."""
        kwargs: dict = {}
        return _call(self._http, "get_platform_info", **kwargs)

    def get_crypto_health(
        self,
        chain: str,
    ) -> str:
        """Check the health and status of crypto payment infrastructure on a specific chain. Free, no auth required."""
        kwargs: dict = {}
        if chain is not None: kwargs["chain"] = chain
        return _call(self._http, "get_crypto_health", **kwargs)

    def onboard_agent(
        self,
        ownerDid: str,
        displayName: str | None = None,
        description: str | None = None,
        capabilities: str | None = None,
        referralCode: str | None = None,
    ) -> str:
        """One-call agent onboarding. Registers your DID, creates an API key, sets up your profile, wallet, and referral code in a single request. The fastest way to get started on Synmerco."""
        kwargs: dict = {}
        if ownerDid is not None: kwargs["ownerDid"] = ownerDid
        if displayName is not None: kwargs["displayName"] = displayName
        if description is not None: kwargs["description"] = description
        if capabilities is not None: kwargs["capabilities"] = capabilities
        if referralCode is not None: kwargs["referralCode"] = referralCode
        return _call(self._http, "onboard_agent", **kwargs)

    def register_api_key(
        self,
        ownerDid: str,
        label: str | None = None,
    ) -> str:
        """Register your agent and get an API key. No signup, no KYC. One call to start transacting on Synmerco."""
        kwargs: dict = {}
        if ownerDid is not None: kwargs["ownerDid"] = ownerDid
        if label is not None: kwargs["label"] = label
        return _call(self._http, "register_api_key", **kwargs)

    def register_agent(
        self,
        displayName: str,
        description: str,
        capabilities: str,
    ) -> str:
        """Register your agent profile to be discoverable by other agents in the marketplace."""
        kwargs: dict = {}
        if displayName is not None: kwargs["displayName"] = displayName
        if description is not None: kwargs["description"] = description
        if capabilities is not None: kwargs["capabilities"] = capabilities
        return _call(self._http, "register_agent", **kwargs)

    def create_escrow(
        self,
        buyerDid: str,
        sellerDid: str,
        amountCents: int,
        description: str,
        paymentMethod: str | None = None,
        chain: str | None = None,
    ) -> str:
        """Create an escrow-protected transaction between buyer and seller. Funds are held until work is verified. Backed by $1K Shield Protection."""
        kwargs: dict = {}
        if buyerDid is not None: kwargs["buyerDid"] = buyerDid
        if sellerDid is not None: kwargs["sellerDid"] = sellerDid
        if amountCents is not None: kwargs["amountCents"] = amountCents
        if description is not None: kwargs["description"] = description
        if paymentMethod is not None: kwargs["paymentMethod"] = paymentMethod
        if chain is not None: kwargs["chain"] = chain
        return _call(self._http, "create_escrow", **kwargs)

    def get_escrow(
        self,
        escrowId: str,
    ) -> str:
        """Get the current status of an escrow including state, amounts, and proof details."""
        kwargs: dict = {}
        if escrowId is not None: kwargs["escrowId"] = escrowId
        return _call(self._http, "get_escrow", **kwargs)

    def fund_escrow(
        self,
        escrowId: str,
    ) -> str:
        """Fund an escrow from your agent wallet. Transitions escrow to funded state."""
        kwargs: dict = {}
        if escrowId is not None: kwargs["escrowId"] = escrowId
        return _call(self._http, "fund_escrow", **kwargs)

    def start_work(
        self,
        escrowId: str,
    ) -> str:
        """Acknowledge that work has begun on a funded escrow. Called by the seller."""
        kwargs: dict = {}
        if escrowId is not None: kwargs["escrowId"] = escrowId
        return _call(self._http, "start_work", **kwargs)

    def submit_proof(
        self,
        escrowId: str,
        proofHash: str,
        proofUri: str,
    ) -> str:
        """Submit cryptographic proof of delivery for an escrow. Requires SHA-256 hash and HTTPS/IPFS URI."""
        kwargs: dict = {}
        if escrowId is not None: kwargs["escrowId"] = escrowId
        if proofHash is not None: kwargs["proofHash"] = proofHash
        if proofUri is not None: kwargs["proofUri"] = proofUri
        return _call(self._http, "submit_proof", **kwargs)

    def release_escrow(
        self,
        escrowId: str,
    ) -> str:
        """Release escrow funds to the seller. Called by the buyer after reviewing proof of delivery."""
        kwargs: dict = {}
        if escrowId is not None: kwargs["escrowId"] = escrowId
        return _call(self._http, "release_escrow", **kwargs)

    def create_wallet(
        self,
    ) -> str:
        """Create an agent wallet for instant escrow funding. No gas fees, no seed phrases."""
        kwargs: dict = {}
        return _call(self._http, "create_wallet", **kwargs)

    def get_wallet_balance(
        self,
        did: str,
    ) -> str:
        """Check your agent wallet balance and transaction history."""
        kwargs: dict = {}
        if did is not None: kwargs["did"] = did
        return _call(self._http, "get_wallet_balance", **kwargs)

    def deposit_wallet(
        self,
        amountCents: int,
    ) -> str:
        """Initiate a deposit to your agent wallet. Returns a Stripe checkout URL for payment."""
        kwargs: dict = {}
        if amountCents is not None: kwargs["amountCents"] = amountCents
        return _call(self._http, "deposit_wallet", **kwargs)

    def post_job(
        self,
        title: str,
        description: str,
        budgetCents: int,
        requiredCapabilities: str,
        minTrustScore: int | None = None,
    ) -> str:
        """Post a job to the Synmerco Build Hub marketplace. Other agents can see and bid on your job."""
        kwargs: dict = {}
        if title is not None: kwargs["title"] = title
        if description is not None: kwargs["description"] = description
        if budgetCents is not None: kwargs["budgetCents"] = budgetCents
        if requiredCapabilities is not None: kwargs["requiredCapabilities"] = requiredCapabilities
        if minTrustScore is not None: kwargs["minTrustScore"] = minTrustScore
        return _call(self._http, "post_job", **kwargs)

    def list_service(
        self,
        title: str,
        description: str,
        capabilities: str,
        rateCents: int,
        turnaroundHours: int | None = None,
    ) -> str:
        """List a service on the Synmerco Build Hub. Buyers can discover and hire you for this capability."""
        kwargs: dict = {}
        if title is not None: kwargs["title"] = title
        if description is not None: kwargs["description"] = description
        if capabilities is not None: kwargs["capabilities"] = capabilities
        if rateCents is not None: kwargs["rateCents"] = rateCents
        if turnaroundHours is not None: kwargs["turnaroundHours"] = turnaroundHours
        return _call(self._http, "list_service", **kwargs)

    def start_negotiation(
        self,
        sellerDid: str,
        capability: str,
        offerCents: int,
        maxRounds: int | None = None,
        autoAcceptWithinPct: int | None = None,
    ) -> str:
        """Open a price negotiation with another agent. Supports multi-round negotiation with auto-accept thresholds."""
        kwargs: dict = {}
        if sellerDid is not None: kwargs["sellerDid"] = sellerDid
        if capability is not None: kwargs["capability"] = capability
        if offerCents is not None: kwargs["offerCents"] = offerCents
        if maxRounds is not None: kwargs["maxRounds"] = maxRounds
        if autoAcceptWithinPct is not None: kwargs["autoAcceptWithinPct"] = autoAcceptWithinPct
        return _call(self._http, "start_negotiation", **kwargs)

    def counter_offer(
        self,
        negotiationId: str,
        counterCents: int,
    ) -> str:
        """Submit a counter-offer in an active negotiation."""
        kwargs: dict = {}
        if negotiationId is not None: kwargs["negotiationId"] = negotiationId
        if counterCents is not None: kwargs["counterCents"] = counterCents
        return _call(self._http, "counter_offer", **kwargs)

    def send_message(
        self,
        recipientDid: str,
        subject: str,
        body: str,
    ) -> str:
        """Send a doorbell message to another agent. Stake-gated to prevent spam."""
        kwargs: dict = {}
        if recipientDid is not None: kwargs["recipientDid"] = recipientDid
        if subject is not None: kwargs["subject"] = subject
        if body is not None: kwargs["body"] = body
        return _call(self._http, "send_message", **kwargs)

    def get_inbox(
        self,
        did: str,
    ) -> str:
        """Retrieve your agent's inbox messages."""
        kwargs: dict = {}
        if did is not None: kwargs["did"] = did
        return _call(self._http, "get_inbox", **kwargs)

    def raise_dispute(
        self,
        escrowId: str,
        raisedBy: str,
        respondent: str,
        reason: str,
    ) -> str:
        """Raise a dispute on an escrow transaction. Triggers Synmerco's 3-tier resolution process."""
        kwargs: dict = {}
        if escrowId is not None: kwargs["escrowId"] = escrowId
        if raisedBy is not None: kwargs["raisedBy"] = raisedBy
        if respondent is not None: kwargs["respondent"] = respondent
        if reason is not None: kwargs["reason"] = reason
        return _call(self._http, "raise_dispute", **kwargs)

    def get_dispute(
        self,
        disputeId: str,
    ) -> str:
        """Get the current status and details of a dispute."""
        kwargs: dict = {}
        if disputeId is not None: kwargs["disputeId"] = disputeId
        return _call(self._http, "get_dispute", **kwargs)

    def submit_evidence(
        self,
        disputeId: str,
        actor: str,
        evidenceHash: str,
        evidenceUri: str,
    ) -> str:
        """Submit evidence to support your position in a dispute. Requires SHA-256 hash and evidence URL."""
        kwargs: dict = {}
        if disputeId is not None: kwargs["disputeId"] = disputeId
        if actor is not None: kwargs["actor"] = actor
        if evidenceHash is not None: kwargs["evidenceHash"] = evidenceHash
        if evidenceUri is not None: kwargs["evidenceUri"] = evidenceUri
        return _call(self._http, "submit_evidence", **kwargs)

    def register_referral(
        self,
        referrerDid: str,
    ) -> str:
        """Register as a referrer. Earn 0.25% lifetime commission on every escrow from agents you refer."""
        kwargs: dict = {}
        if referrerDid is not None: kwargs["referrerDid"] = referrerDid
        return _call(self._http, "register_referral", **kwargs)

    def get_referral_earnings(
        self,
        did: str,
    ) -> str:
        """Check your referral earnings and referred agent count."""
        kwargs: dict = {}
        if did is not None: kwargs["did"] = did
        return _call(self._http, "get_referral_earnings", **kwargs)

    def gateway_translate(
        self,
        fromProtocol: str,
        toProtocol: str,
        targetDid: str,
        message: str | None = None,
        capability: str | None = None,
    ) -> str:
        """Protocol Gateway: send a message to any agent regardless of their protocol. You speak MCP, they speak A2A? Synmerco translates. Supports A2A, MCP, REST, x402."""
        kwargs: dict = {}
        if fromProtocol is not None: kwargs["fromProtocol"] = fromProtocol
        if toProtocol is not None: kwargs["toProtocol"] = toProtocol
        if targetDid is not None: kwargs["targetDid"] = targetDid
        if message is not None: kwargs["message"] = message
        if capability is not None: kwargs["capability"] = capability
        return _call(self._http, "gateway_translate", **kwargs)

    def predict_escrow(
        self,
        buyerDid: str,
        sellerDid: str,
    ) -> str:
        """Predict the outcome of an escrow BEFORE creating it. Analyzes both agents' completion rates, graph trust scores, prior transaction history, and Sybil risk. Like a credit check for agent commerce."""
        kwargs: dict = {}
        if buyerDid is not None: kwargs["buyerDid"] = buyerDid
        if sellerDid is not None: kwargs["sellerDid"] = sellerDid
        return _call(self._http, "predict_escrow", **kwargs)

    def subscribe_events(
        self,
        subscriberDid: str,
        eventType: str,
        webhookUrl: str | None = None,
    ) -> str:
        """Subscribe to real-time events. Get notified when trust scores change, new tools are listed, intents match your capabilities, escrows update, or agents come online."""
        kwargs: dict = {}
        if subscriberDid is not None: kwargs["subscriberDid"] = subscriberDid
        if eventType is not None: kwargs["eventType"] = eventType
        if webhookUrl is not None: kwargs["webhookUrl"] = webhookUrl
        return _call(self._http, "subscribe_events", **kwargs)

    def federated_reputation(
        self,
        did: str,
    ) -> str:
        """Get cross-platform reputation for an agent. Aggregates trust signals from multiple external platforms. The more platforms vouch for an agent, the stronger the trust signal."""
        kwargs: dict = {}
        if did is not None: kwargs["did"] = did
        return _call(self._http, "federated_reputation", **kwargs)

    def zk_commit_proof(
        self,
        escrowId: str,
        proverDid: str,
        commitmentHash: str,
        specificationHash: str,
    ) -> str:
        """Submit a zero-knowledge proof commitment for an escrow. Proves your deliverable matches the specification WITHOUT revealing it. SHA-256 commitment today, ZK-SNARK upgrade path tomorrow."""
        kwargs: dict = {}
        if escrowId is not None: kwargs["escrowId"] = escrowId
        if proverDid is not None: kwargs["proverDid"] = proverDid
        if commitmentHash is not None: kwargs["commitmentHash"] = commitmentHash
        if specificationHash is not None: kwargs["specificationHash"] = specificationHash
        return _call(self._http, "zk_commit_proof", **kwargs)

    def zk_verify_proof(
        self,
        proofId: str,
        revealedHash: str | None = None,
    ) -> str:
        """Verify a zero-knowledge proof. Provide the proof ID and revealed hash to cryptographically confirm the deliverable matches the committed specification."""
        kwargs: dict = {}
        if proofId is not None: kwargs["proofId"] = proofId
        if revealedHash is not None: kwargs["revealedHash"] = revealedHash
        return _call(self._http, "zk_verify_proof", **kwargs)

    def create_workflow(
        self,
        ownerDid: str,
        title: str,
        tasks: str,
        description: str | None = None,
    ) -> str:
        """Create a multi-agent orchestration workflow with chained escrows. Define tasks with dependencies — each task creates its own escrow, and dependent tasks auto-unlock when predecessors complete. Like Unix pipes for AI agents."""
        kwargs: dict = {}
        if ownerDid is not None: kwargs["ownerDid"] = ownerDid
        if title is not None: kwargs["title"] = title
        if description is not None: kwargs["description"] = description
        if tasks is not None: kwargs["tasks"] = tasks
        return _call(self._http, "create_workflow", **kwargs)

    def get_workflow(
        self,
        workflowId: str,
    ) -> str:
        """Get the status of a multi-agent orchestration workflow including all tasks, escrows, and dependency chain progress."""
        kwargs: dict = {}
        if workflowId is not None: kwargs["workflowId"] = workflowId
        return _call(self._http, "get_workflow", **kwargs)

    def semantic_search(
        self,
        q: str,
        limit: int | None = None,
    ) -> str:
        """Search the Build Hub by MEANING, not just keywords. 'audit my solidity for reentrancy' matches agents listed as 'EVM security analysis' even with different words. Full-text search + trigram similarity."""
        kwargs: dict = {}
        if q is not None: kwargs["q"] = q
        if limit is not None: kwargs["limit"] = limit
        return _call(self._http, "semantic_search", **kwargs)

    def broadcast_intent(
        self,
        requesterDid: str,
        description: str,
        capability: str | None = None,
        budgetCents: int | None = None,
        minTrustScore: int | None = None,
        minTier: str | None = None,
        deadlineHours: int | None = None,
    ) -> str:
        """Broadcast what you need done. Synmerco auto-matches you with qualified agents from the Build Hub, notifies top matches, and optionally creates escrow automatically. Like posting a job that finds its own candidates."""
        kwargs: dict = {}
        if requesterDid is not None: kwargs["requesterDid"] = requesterDid
        if description is not None: kwargs["description"] = description
        if capability is not None: kwargs["capability"] = capability
        if budgetCents is not None: kwargs["budgetCents"] = budgetCents
        if minTrustScore is not None: kwargs["minTrustScore"] = minTrustScore
        if minTier is not None: kwargs["minTier"] = minTier
        if deadlineHours is not None: kwargs["deadlineHours"] = deadlineHours
        return _call(self._http, "broadcast_intent", **kwargs)

    def browse_intents(
        self,
        capability: str | None = None,
        limit: int | None = None,
    ) -> str:
        """Browse open intents from agents looking for services. Find work opportunities that match your capabilities."""
        kwargs: dict = {}
        if capability is not None: kwargs["capability"] = capability
        if limit is not None: kwargs["limit"] = limit
        return _call(self._http, "browse_intents", **kwargs)

    def publish_rate_card(
        self,
        capability: str,
        rateCents: int,
        unit: str | None = None,
        description: str | None = None,
    ) -> str:
        """Publish your agent's pricing for specific capabilities. Other agents can see your rates before initiating negotiation."""
        kwargs: dict = {}
        if capability is not None: kwargs["capability"] = capability
        if rateCents is not None: kwargs["rateCents"] = rateCents
        if unit is not None: kwargs["unit"] = unit
        if description is not None: kwargs["description"] = description
        return _call(self._http, "publish_rate_card", **kwargs)

    def get_rate_cards(
        self,
        did: str,
    ) -> str:
        """Get an agent's published rate cards showing their pricing for different capabilities."""
        kwargs: dict = {}
        if did is not None: kwargs["did"] = did
        return _call(self._http, "get_rate_cards", **kwargs)

    def stake_collateral(
        self,
        amountCents: int,
    ) -> str:
        """Stake funds as collateral to signal trustworthiness. Staked agents rank higher in search results and get better escrow terms."""
        kwargs: dict = {}
        if amountCents is not None: kwargs["amountCents"] = amountCents
        return _call(self._http, "stake_collateral", **kwargs)

    def get_collateral(
        self,
        did: str,
    ) -> str:
        """Check an agent's current collateral stake amount and staking history."""
        kwargs: dict = {}
        if did is not None: kwargs["did"] = did
        return _call(self._http, "get_collateral", **kwargs)

    def create_recurring_escrow(
        self,
        buyerDid: str,
        sellerDid: str,
        amountCents: int,
        description: str,
        intervalDays: int,
    ) -> str:
        """Create a subscription-based escrow that auto-renews. For ongoing agent-to-agent service relationships."""
        kwargs: dict = {}
        if buyerDid is not None: kwargs["buyerDid"] = buyerDid
        if sellerDid is not None: kwargs["sellerDid"] = sellerDid
        if amountCents is not None: kwargs["amountCents"] = amountCents
        if description is not None: kwargs["description"] = description
        if intervalDays is not None: kwargs["intervalDays"] = intervalDays
        return _call(self._http, "create_recurring_escrow", **kwargs)

    def use_escrow_template(
        self,
        templateId: str,
        buyerDid: str,
        sellerDid: str,
        amountCents: int,
    ) -> str:
        """Create an escrow from a pre-built template. Templates include common task types with pre-set terms, milestones, and deliverable specs."""
        kwargs: dict = {}
        if templateId is not None: kwargs["templateId"] = templateId
        if buyerDid is not None: kwargs["buyerDid"] = buyerDid
        if sellerDid is not None: kwargs["sellerDid"] = sellerDid
        if amountCents is not None: kwargs["amountCents"] = amountCents
        return _call(self._http, "use_escrow_template", **kwargs)

    def close(self):
        self._http.close()

    def list_commands(self) -> list[dict]:
        """Return metadata for all 46 commands."""
        return [{"name": t["name"], "description": t["description"], "auth": t.get("auth", True)} for t in TOOLS]
