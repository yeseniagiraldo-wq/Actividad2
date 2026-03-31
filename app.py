"""
Ejercicio 1: Superpoderes y Personalización del Agente
Autores: Angie Yesenia Giraldo Gavilan, Cesar Augusto Florez Castaño, Jhonatan Rojas Diaz
"""
import os
from huggingface_hub import login

hf_token = os.environ.get("HF_TOKEN")
if hf_token:
    login(token=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)


import raimport random
import requests
from smolagents import CodeAgent, InferenceClientModel, tool, FinalAnswerTool
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


