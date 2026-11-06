from pathlib import Path

from streamlit.testing.v1 import AppTest


def test_historial_solo_cambia_al_enviar_o_vaciar(monkeypatch):
    app = Path(__file__).with_name("05_practica_starter.py")
    monkeypatch.syspath_prepend(str(app.parent))
    at = AppTest.from_file(str(app)).run()
    assert not at.exception
    assert at.metric, "La app debe mostrar el contador al arrancar"
    assert at.metric[0].value == "0"
    assert not at.dataframe
    at.slider(key="tenure_months").set_value(18).run()
    assert at.metric[0].value == "0"
    for count in range(1, 4):
        # AppTest envía el cambio y el submit en la misma ejecución.
        at.slider(key="tenure_months").set_value(18)
        next(b for b in at.button if b.label == "Predecir y guardar").click().run()
        assert not at.exception
        assert at.metric[0].value == str(count)
        assert len(at.dataframe[0].value) == count
        assert at.session_state.history[-1]["tenure_months"] == 18
    at.checkbox(key="show_help").check().run()
    assert at.metric[0].value == "3"
    assert len(at.dataframe[0].value) == 3
    next(b for b in at.button if b.label == "Vaciar historial").click().run()
    assert at.metric[0].value == "0"
    assert not at.dataframe
