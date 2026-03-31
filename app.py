"""
Ejercicio 1: Superpoderes y Personalización del Agente
Autores: Angie Yesenia Giraldo Gavilan, Cesar Augusto Florez Castaño, Jhonatan Rojas Diaz
"""

import random
import requests
from smolagents import CodeAgent, HfApiModel, tool, FinalAnswerTool
import gradio as gr

# ============================================================
# 🔧 HERRAMIENTA 1 (Camino A): Calculador de Áreas
# ============================================================
@tool
def calcular_area(figura: str, valor1: float, valor2: float = 0) -> str:
    """
    Calcula el área de una figura geométrica.

    Args:
        figura: Nombre de la figura. Puede ser 'rectangulo', 'triangulo' o 'circulo'.
        valor1: Para rectángulo y triángulo es la base. Para círculo es el radio.
        valor2: Para rectángulo es la altura. Para triángulo es la altura. No aplica al círculo.

    Returns:
        Un string con el resultado del área calculada.
    """
    figura = figura.lower()
    import math

    if figura == "rectangulo":
        area = valor1 * valor2
        return f"El área del rectángulo con base {valor1} y altura {valor2} es: {area:.2f}"

    elif figura == "triangulo":
        area = (valor1 * valor2) / 2
        return f"El área del triángulo con base {valor1} y altura {valor2} es: {area:.2f}"

    elif figura == "circulo":
        area = math.pi * (valor1 ** 2)
        return f"El área del círculo con radio {valor1} es: {area:.2f}"

    else:
        return f"Figura '{figura}' no reconocida. Usa: rectangulo, triangulo o circulo."


# ============================================================
# 🔧 HERRAMIENTA 2 (Camino B): Clima actual con API externa
# ============================================================
@tool
def obtener_clima(ciudad: str) -> str:
    """
    Obtiene el clima actual de una ciudad usando la API gratuita de wttr.in.

    Args:
        ciudad: Nombre de la ciudad en español o inglés (ej: 'Medellin', 'Bogota', 'London').

    Returns:
        Un string con la información del clima actual de la ciudad.
    """
    try:
        # wttr.in es una API pública y gratuita, no requiere clave
        url = f"https://wttr.in/{ciudad}?format=3&lang=es"
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            return f"🌤️ Clima en {ciudad}: {response.text.strip()}"
        else:
            return f"No pude obtener el clima de {ciudad}. Intenta con otro nombre de ciudad."

    except Exception as e:
        return f"Error al consultar el clima: {str(e)}"


# ============================================================
# 🎯 MODIFICACIÓN DEL FinalAnswerTool
# Objetivo: Personalizar la respuesta final del agente
# ============================================================
class MiFinalAnswerTool(FinalAnswerTool):
    """
    Versión personalizada del FinalAnswerTool.
    Agrega un prefijo, firma y conteo de caracteres a cada respuesta.
    """

    # Sobrescribimos el método forward que es el que genera la respuesta
    def forward(self, answer: str) -> str:
        # 1️⃣ Contamos cuántos caracteres tiene la respuesta original
        num_caracteres = len(answer)

        # 2️⃣ Construimos la respuesta con prefijo, contenido y firma
        respuesta_formateada = (
            f"🤖 Agente dice:\n\n"          # Prefijo con emoji
            f"{answer}\n\n"                  # Respuesta original del agente
            f"📊 Esta respuesta tiene {num_caracteres} caracteres.\n"  # Conteo de caracteres
            f"--- Procesado por Angie, Cesar y Jhonatan ---"           # Firma del equipo
        )

        return respuesta_formateada


# ============================================================
# 🚀 CONFIGURACIÓN DEL AGENTE
# ============================================================

# Modelo que usará el agente (gratuito en HF Spaces)
modelo = HfApiModel(model_id="Qwen/Qwen2.5-Coder-32B-Instruct")

# Creamos el agente con las herramientas personalizadas
agente = CodeAgent(
    tools=[
        calcular_area,       # Herramienta 1: Calculador de áreas
        obtener_clima,       # Herramienta 2: Clima con API
        MiFinalAnswerTool(), # FinalAnswerTool modificado
    ],
    model=modelo,
    max_steps=5,
)


# ============================================================
# 🖥️ INTERFAZ GRADIO
# ============================================================
def responder(pregunta):
    resultado = agente.run(pregunta)
    return resultado

interfaz = gr.Interface(
    fn=responder,
    inputs=gr.Textbox(
        label="¿Qué quieres preguntarle al agente?",
        placeholder="Ej: ¿Cuál es el área de un rectángulo de base 5 y altura 3?"
    ),
    outputs=gr.Textbox(label="Respuesta del Agente"),
    title="🤖 Agente Inteligente - Ejercicio 1",
    description=(
        "Agente con superpoderes:\n"
        "📐 Puede calcular áreas de figuras geométricas\n"
        "🌤️ Puede consultar el clima de cualquier ciudad\n\n"
        "Autores: Angie Giraldo | Cesar Florez | Jhonatan Rojas"
    ),
    examples=[
        ["¿Cuál es el área de un triángulo con base 6 y altura 4?"],
        ["¿Qué clima hace hoy en Medellín?"],
        ["Calcula el área de un círculo con radio 7"],
        ["¿Cómo está el tiempo en Bogotá?"],
    ]
)

if __name__ == "__main__":
    interfaz.launch()
