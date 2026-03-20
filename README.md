# 🏙️ Ciudad en Equilibrio - Simulador de Gestión Urbana

**Ciudad en Equilibrio** es una aplicación interactiva en Python y Streamlit que invita a los usuarios a gestionar una ciudad campestre sostenible: controlando Economía, Medio Ambiente, Energía y Bienestar Social.

## 🌱 Objetivo

Simular la toma de decisiones sistémicas en una ciudad rural-modernizada, manteniendo equilibrio entre:

- Economía (ingresos y crecimiento)
- Medio Ambiente (naturaleza, turismo y recursos naturales)
- Energía (infraestructura y suministro)
- Bienestar Social (salud, educación y felicidad)

Se trabaja con rondas (10 rondas o colapso) y se gestionan eventos positivos/negativos y decisiones estratégicas.

## 🎮 Experiencia UI/UX

La interfaz está diseñada con estilo campestre + pixel art:

- paleta suaves (verdes, marrones, beige, azul cielo)
- luz cálida (amanecer/atardecer)
- texturas madera/pasto/tierra
- paneles semi-translúcidos (vidrio/pergamino)
- botones orgánicos, hover brillo/escalado y animaciones suaves
- clima dinámico (Sol, Nublado, Lluvia)
- modo día/noche
- minimapa UI pixel en esquina

## ✨ Características principales

- rondas fijas (10) + colapso cuando algún indicador llega a 0
- decisiones con cooldown, multiplicadores y efectos (+1..+10 / -1..-10)
- eventos 70% positivos y 30% negativos por dificultad
- calculo de puntaje y estado de la ciudad
- logros, misiones y ranking (SQLite)
- responsive (PC, tablet, móvil)

## 🧩 Estructura de carpetas

- `app.py`: entrada principal
- `router.py`: navegación entre pantallas
- `screen_*`: vistas (inicio, login, lobby, juego, fin, logros, etc.)
- `ui_styles.py`: temas y estilos globales
- `screen_juego.py`: lógica principal del juego
- `config.py`: parámetros y datos (decisiones, eventos, estados)
- `db.py`: conexión y consultas SQLite
- `questions*`: banco de preguntas y lógica de selección

## 🔧 Requisitos

- Python 3.9+
- pip

### Dependencias

```bash
pip install -r requirements.txt
```

## ▶️ Ejecutar local

```bash
cd "c:\Users\User\OneDrive\Escritorio\ING. SISTEMAS DANIEL MAURICIO QUINTERO\SEMESTRE 4\PENSAMIENTO SISTEMICO\CIUDAD PYTHON"
streamlit run app.py
```

## 🗂️ Base de datos inicial

- `database.sqlite3` contiene tablas:
  - `grupos`, `estudiantes`, `progresojuego`, `cooldowndecisiones`, `ranking`, `logros_grupo`, `misiones_pendientes`, `misiones_canjeadas`, `estrellas_grupo`
- `screen_inicio.py` ejecuta `init_db()`.

## 🛠️ Personalización y desarrollo

- `config.py` permite ajustar fácilmente:
  - `TOTAL_RONDAS`, `COOLDOWN`, `TIEMPO_PREGUNTA`, `MEZCLA_PREGUNTAS`
  - `DECISIONES`, `EVENTOS_POR_DIFICULTAD`, `ESTADOS_CIUDAD`, `ATRIBUTOS`, `MISIONES`, `LOGROS`
- agrega nuevas preguntas en `questions_bank.py`.

## 🗣️ Sugerencias futuras

- modo multijugador/turnos real con websockets
- agregar mapamundi con coordenadas y eventos locales
- sistema de resultados exportables (`csv`, `json`)
- sonidos ambientales (aves, viento, riachuelo) con `st.audio` o `components.html`

## 📦 Licencia

Este proyecto se comparte libremente y puede copiarse, modificarse y redistribuirse.
