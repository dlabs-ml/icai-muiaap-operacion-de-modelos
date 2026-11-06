# Datos de apoyo — Semana 6

La interfaz parte del formulario de S5 y reutiliza las once características y
las cinco muestras de `../../../semana3/assets/03-wine-quality/inference_samples.csv`.
No se duplica el CSV para mantener una única fuente de verdad entre las semanas
3, 4, 5 y 6.

En modo real, el gateway delega la validación en el contrato Pydantic y la
inferencia del bundle de la semana 4. La demo ofrece también un gateway
determinista para enseñar estado, caché, confianza baja, errores y reintento
sin depender de un modelo binario ni de una descarga externa.
