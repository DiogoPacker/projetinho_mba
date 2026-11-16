import json
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from flightlab.assistant import answer


def test_local_mode_does_not_call_provider(flights):
    client = Mock()
    result = answer("Resumo", flights, client=client)
    assert result["mode"] == "local_summary"
    client.responses.create.assert_not_called()


def test_llm_receives_aggregates_and_not_raw_rows(flights, monkeypatch):
    monkeypatch.setenv("FLIGHTLAB_ENABLE_LLM", "true")
    client = Mock()
    client.responses.create.return_value = SimpleNamespace(output_text="Taxa: 40% (delay_rate).")
    result = answer("Qual a taxa?", flights, use_llm=True, client=client)
    payload = client.responses.create.call_args.kwargs
    context = json.loads(payload["input"])
    assert context["aggregates"]["delay_rate"] == pytest.approx(0.4)
    assert "tailnum" not in payload["input"]
    assert payload["store"] is False
    assert result["mode"] == "llm"


def test_question_validation(flights):
    with pytest.raises(ValueError):
        answer("  ", flights)


def test_public_demo_disables_llm_even_with_a_client(flights, monkeypatch):
    monkeypatch.setenv("FLIGHTLAB_ENABLE_LLM", "false")
    client = Mock()
    with pytest.raises(ValueError, match="desativado"):
        answer("Resumo", flights, use_llm=True, client=client)
    client.responses.create.assert_not_called()
    assert answer("Resumo", flights)["mode"] == "local_summary"
