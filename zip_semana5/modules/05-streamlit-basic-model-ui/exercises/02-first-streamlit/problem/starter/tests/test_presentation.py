from model_ui.contracts import PredictionPayload
from model_ui.presentation import confidence_caption, quality_label


def test_basic_presentation_keeps_model_metadata_outside_the_label() -> None:
    prediction = PredictionPayload(
        quality_band="acceptable",
        confidence=0.74,
        model_version="wine-model-v1",
        preprocessing_version="wine-red-features-v1",
    )
    assert quality_label(prediction) == "Resultado aceptable"
    assert confidence_caption(prediction) == "Confianza reportada por el modelo: 74%."
