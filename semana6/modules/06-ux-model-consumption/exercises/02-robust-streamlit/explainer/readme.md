# Explicación — Evolucionar, no rehacer, la app de S5

El starter representa el estado final de la práctica de S5 antes del refactor.
La interfaz ya sabe dibujar el formulario. S6 introduce una capa que controla
el ciclo de vida de la petición:

```text
formulario S5
      ↓
session_state + controller
      ↓
InferenceGateway → bundle de S4
      ↓
UiState / PredictionView / UserFacingError
```

`st.cache_resource` es para el gateway o el bundle reutilizable. No debe
convertirse en una caché de respuestas por usuario. `st.session_state` conserva
estado observable de la sesión, no sustituye a un almacén de datos ni autoriza
a registrar el formulario completo.

El controlador no importa Streamlit para que sus transiciones puedan probarse
con un reloj y un gateway falso. En S7, el mismo controlador podrá consumir un
gateway HTTP.
