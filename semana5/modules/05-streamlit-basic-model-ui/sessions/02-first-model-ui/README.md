# Clase 2 — Taller: frontal Wine sobre el bundle S4

**Duración:** 120 minutos de práctica guiada

La pareja aplica al proyecto Wine el patrón practicado con Churn. El starter es
autocontenido: ya incluye los once `FIELD_SPECS`. La Práctica 5.1 no entrega
ningún archivo que deba copiarse.

## Prerrequisito

Cada pareja necesita su bundle real de S4 y configura el directorio mediante:

```powershell
$env:MODEL_UI_BUNDLE = 'RUTA_AL_BUNDLE_DE_S4'
```

La aplicación no ofrece predicciones sustitutivas. Los dobles de gateway
existen únicamente bajo `tests/`.

## Secuencia

1. Localizar y validar el bundle de S4.
2. Revisar los once `FIELD_SPECS` proporcionados.
3. Implementar los widgets dentro de un único `st.form`.
4. Comprobar cero llamadas al editar y una tras el submit.
5. Usar únicamente `InferenceGateway.predict(values)`.
6. Mostrar `quality_band`, `confidence`, `model_version` y
   `preprocessing_version`.
7. Reproducir un bundle ausente y mostrar un mensaje accionable sin detalles
   internos.
8. Ejecutar tests y completar la matriz QA.
9. Anotar dos límites para S6 sin implementar estado, caché, FSM ni telemetría.

## Entrega

- código del starter completado;
- configuración documentada de `MODEL_UI_BUNDLE`;
- suite y formato verdes;
- evidencia de una inferencia con el bundle real;
- evidencia del tratamiento de bundle ausente;
- matriz QA: arranque con bundle, edición sin envío, submit válido y bundle
  ausente.

## Relación con 5.1

Se transfiere el patrón `formulario → submit → una inferencia →
resultado/error`. No se reutilizan los cuatro campos, la regla, los labels ni
ningún archivo del caso Churn.
