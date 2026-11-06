# Explicación — Rerun, sesión y estado de una petición

En S5, el script se vuelve a ejecutar cuando la persona interactúa. Una
variable local puede desaparecer, mientras que `st.session_state` permite
conservar información de la sesión. Eso no significa que debamos guardar todo:
los valores completos del formulario no deben entrar automáticamente en la
telemetría.

La separación que implementará S6 es:

```text
st.session_state: estado observable y agregados de sesión
st.cache_resource: gateway/bundle reutilizable
controller: transiciones y errores
gateway: contrato e inferencia de S4
```

Los umbrales de confianza y latencia son políticas de comunicación de la demo,
no una calibración del modelo.
