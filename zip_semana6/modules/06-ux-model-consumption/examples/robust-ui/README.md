# Ejemplo ejecutable — evolución de la UI de S5

Este ejemplo es la versión avanzada de la interfaz que se construyó en S5.
Conserva el formulario y el gateway de inferencia de la práctica anterior y
añade las decisiones de operación de la sesión:

- estado persistente para recordar el último resultado y permitir reintentar;
- `st.cache_resource` para no reconstruir el gateway en cada rerun;
- estados explícitos de carga, éxito y error;
- mensajes de recuperación, confianza y latencia;
- telemetría agregada sin guardar el payload completo de entrada.

La referencia docente se organiza así:

```text
app.py
  -> PredictionController
       -> InferenceGateway
            -> DemoGateway o bundle de S4
       -> PredictionView / UserFacingError
       -> TelemetrySnapshot
```

## Comportamientos que se deben observar

1. Al pulsar el botón de la app de S5, una petición emite `loading` y termina
   en `success` o `error`.
2. La vista conserva la categoría, la confianza, la latencia y las versiones.
3. La confianza baja muestra una recomendación de revisión.
4. Un error de contrato no muestra traceback ni los valores introducidos.
5. La telemetría conserva contadores, códigos, latencias y versiones, pero no
   el payload.

El `PackagedBundleGateway` localiza el módulo de S4 y delega en su contrato y
función `infer_wine_quality()`. Esta es la costura que S7 puede implementar con
HTTP sin cambiar `PredictionController` ni la presentación. La práctica no
crea una segunda interfaz: se ejecuta sobre la misma entrada que S5 y prepara
el desacoplamiento que se necesitará en S7.
