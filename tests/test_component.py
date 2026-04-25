"""Tests for synmerco-autogpt."""

import pytest
from synmerco_autogpt import SynmercoCommands, SynmercoComponent, is_autogpt_available
from synmerco_autogpt._client import validate_did, validate_amount, validate_sha256, SynmercoHTTPClient, SynmercoAPIError
from synmerco_autogpt._registry import TOOLS


def test_registry_count():
    assert len(TOOLS) >= 44

def test_no_duplicate_names():
    names = [t["name"] for t in TOOLS]
    assert len(names) == len(set(names))

def test_commands_instantiates():
    c = SynmercoCommands(api_key="test")
    assert c is not None

def test_commands_has_all_methods():
    c = SynmercoCommands(api_key="test")
    for t in TOOLS:
        assert hasattr(c, t["name"]), f"Missing method: {t['name']}"

def test_commands_methods_callable():
    c = SynmercoCommands(api_key="test")
    assert callable(getattr(c, "lookup_trust_score"))
    assert callable(getattr(c, "create_escrow"))
    assert callable(getattr(c, "semantic_search"))

def test_list_commands():
    c = SynmercoCommands(api_key="test")
    cmds = c.list_commands()
    assert len(cmds) >= 44
    assert all("name" in cmd and "description" in cmd for cmd in cmds)

def test_component_instantiates():
    comp = SynmercoComponent(api_key="test")
    assert comp is not None
    assert comp.cmds is not None

def test_component_get_commands():
    comp = SynmercoComponent(api_key="test")
    cmds = list(comp.get_commands())
    assert len(cmds) >= 44
    names = [c[0] for c in cmds]
    assert "lookup_trust_score" in names
    assert "create_escrow" in names

def test_validate_did():
    assert validate_did("did:key:z6MkTest") == "did:key:z6MkTest"
    with pytest.raises(ValueError): validate_did("bad")

def test_validate_amount():
    assert validate_amount(500) == 500
    with pytest.raises(ValueError): validate_amount(10)

def test_validate_sha256():
    assert validate_sha256("ab" * 32) == "ab" * 32
    with pytest.raises(ValueError): validate_sha256("short")

def test_client_defaults():
    c = SynmercoHTTPClient()
    assert "synmerco" in c.base_url

def test_autogpt_availability_flag():
    assert isinstance(is_autogpt_available(), bool)

def test_error_formatting():
    e = SynmercoAPIError(401, "unauthorized", "Bad key")
    assert "401" in str(e)
