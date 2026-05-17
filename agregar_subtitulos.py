"""
Script para agregar subtítulos quemados a los clips de inglés.
Ajusta los tiempos en el diccionario SUBTITLES antes de ejecutar.
"""

from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import os

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURACIÓN DE SUBTÍTULOS
# Formato: { nombre_archivo: [(inicio_seg, fin_seg, "texto"), ...] }
# Ajusta inicio/fin según tus videos después de verlos.
# ─────────────────────────────────────────────────────────────────────────────

SUBTITLES = {
    "video ingles1.mp4": [
        (0.5, 6.0, "We always patrol the university every morning\nto keep students safe."),
    ],
    "video ingles 2.mp4": [
        (0.5, 5.5, "He usually eats his delicious lunch twice a day."),
    ],
    "video ingles 3.mp4": [
        (0.5, 6.5, "He frequently drinks fresh water\nbecause it is very hot at midday."),
    ],
    "video ingles 4.mp4": [
        (0.5, 8.0, "My dog never stays awake in the afternoon;\nhe always takes a long nap."),
    ],
    "video ingles 5.mp4": [
        # Escenario 5 — reemplaza con tu frase y ajusta los tiempos
        (0.5, 6.0, "Tu frase del escenario 5 aquí."),
    ],
    "video ingles 6.mp4": [
        # Escenario 6 — reemplaza con tu frase y ajusta los tiempos
        (0.5, 6.0, "Tu frase del escenario 6 aquí."),
    ],
}

# ─────────────────────────────────────────────────────────────────────────────
# ESTILO
# ─────────────────────────────────────────────────────────────────────────────

FONT       = "Arial"          # Cambia a "Montserrat-Regular" si lo tienes instalado
FONTSIZE   = 42               # Tamaño en píxeles — ajusta según resolución del video
COLOR      = "white"
STROKE_COLOR = "black"
STROKE_WIDTH = 2              # Grosor del borde negro
MARGIN_Y   = 60               # Distancia desde el borde inferior en píxeles

# ─────────────────────────────────────────────────────────────────────────────
# PROCESAMIENTO
# ─────────────────────────────────────────────────────────────────────────────

output_folder = "videos_con_subtitulos"
os.makedirs(output_folder, exist_ok=True)


def make_subtitle_clip(text, video_size, start, end):
    """Crea un TextClip centrado en la parte inferior con borde negro."""
    txt = (
        TextClip(
            text,
            font=FONT,
            fontsize=FONTSIZE,
            color=COLOR,
            stroke_color=STROKE_COLOR,
            stroke_width=STROKE_WIDTH,
            method="caption",
            align="center",
            size=(int(video_size[0] * 0.9), None),  # 90 % del ancho del video
        )
        .set_start(start)
        .set_end(end)
        .set_position(("center", video_size[1] - MARGIN_Y - FONTSIZE * text.count("\n") - FONTSIZE))
    )
    return txt


for filename, segments in SUBTITLES.items():
    if not os.path.exists(filename):
        print(f"[ADVERTENCIA] No se encontró: {filename} — se omite.")
        continue

    print(f"Procesando: {filename}")
    video = VideoFileClip(filename)

    subtitle_clips = [
        make_subtitle_clip(text, video.size, start, end)
        for start, end, text in segments
    ]

    final = CompositeVideoClip([video] + subtitle_clips)

    out_name = os.path.join(output_folder, f"subtitulado_{filename}")
    final.write_videofile(
        out_name,
        codec="libx264",
        audio_codec="aac",
        fps=video.fps,
        preset="slow",       # "slow" = mejor calidad; cámbialo a "fast" si prefieres velocidad
        ffmpeg_params=["-crf", "18"],  # 18 = calidad casi sin pérdida (0–51, menor = mejor)
        threads=4,
        logger="bar",
    )

    video.close()
    final.close()
    print(f"  → Guardado en: {out_name}\n")

print("¡Listo! Todos los videos procesados están en la carpeta:", output_folder)
