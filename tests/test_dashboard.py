from pathlib import Path

from streamlit.testing.v1 import AppTest

from flightlab import data, model


def test_dashboard_load_prediction_and_assistant(flights, tmp_path, monkeypatch):
    model.train(flights, {"source": "fixture"}, tmp_path)
    bundle = model.load_model(tmp_path)
    monkeypatch.setattr(data, "load", lambda: (flights, {"source": "fixture"}))
    monkeypatch.setattr(model, "load_model", lambda: bundle)
    path = Path(__file__).resolve().parents[1] / "apps" / "dashboard.py"
    app = AppTest.from_file(path, default_timeout=30).run()
    assert not app.exception
    assert len(app.tabs) == 4
    app.button[0].click().run()
    assert not app.exception
    assert any("Probabilidade" in item.label for item in app.metric)
    app.text_input[0].set_value("Resumo dos dados").run()
    app.button[1].click().run()
    assert not app.exception
    assert any("Resumo local" in item.value for item in app.markdown)
