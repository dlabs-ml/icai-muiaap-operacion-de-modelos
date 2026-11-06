# Activo de clase — calidad de vino

La Práctica 5.2 reutiliza el contrato de las semanas 3 y 4. Las muestras se
consultan en:

[inference_samples.csv](../../../semana3/assets/03-wine-quality/inference_samples.csv)

No se copia el CSV para evitar que las semanas evolucionen con datos distintos.
El formulario usa las once columnas canónicas y el gateway delega en S4 la
validación, el preprocesado y la inferencia.

## Bundle obligatorio

Cada pareja debe utilizar el directorio de su bundle real de S4, que contiene
al menos `manifest.json` y `model.joblib`. La aplicación recibe esa ubicación
mediante:

```powershell
$env:MODEL_UI_BUNDLE = 'RUTA_AL_BUNDLE_DE_S4'
```

No existe una predicción sustitutiva para ejecutar o entregar la aplicación sin
ese artefacto. Los dobles de inferencia se usan únicamente dentro de los tests
automáticos para comprobar el comportamiento de la interfaz.
