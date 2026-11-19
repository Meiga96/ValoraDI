Con las valoraciones Valora(5, 4, 3) y Valora(3, 4, 5), y los pesos de por defecto, ¿cuánto valen las tres medias y la nota global?
¿Qué devuelve Pesos(50, 30, 30).aviso? ¿Y Pesos(50, 30, 30).validos?
¿Por qué texto_global está en el modelo y no en la ventana?
-----------------------------------------------------------
Respuestas
Medias: docente 4.0, materiales 4.0 y clases 4.0. Nota global: (4.0 · 40 + 4.0 · 30 + 4.0 · 30) / 100 = 4.0.
"Sobran 10 puntos: la suma pasa de 100 %", porque suman 110; y False.
Porque escribir la nota con un decimal, o una raya si no hay, también es una decisión del cálculo. Así la ventana solo copia el texto, y la regla se prueba con pytest.