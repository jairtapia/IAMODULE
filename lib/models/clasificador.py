import os
import numpy as np
import joblib

# Ruta absoluta al modelo .pkl ubicado en la misma carpeta
MODEL_PATH = os.path.join(os.path.dirname(__file__), "modelo_apuntes.pkl")

# Singleton: el modelo se carga una sola vez al importar el módulo
_modelo = None


def _cargar_modelo():
    """Carga el modelo desde disco. Se llama sólo la primera vez."""
    global _modelo
    if _modelo is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"No se encontró el modelo en '{MODEL_PATH}'. "
                "Asegúrate de que el archivo 'modelo_apuntes.pkl' esté en lib/models/."
            )
        _modelo = joblib.load(MODEL_PATH)
    return _modelo


def clasificar_texto(texto: str) -> dict:
    """
    Clasifica un texto usando el modelo de apuntes.

    Args:
        texto: El texto / apunte a clasificar.

    Returns:
        Un diccionario con las claves:
            - resultado (str): Categoría predicha.
            - confianza (float): Probabilidad de la clase predicha (0-1).
            - advertencia (str | None): Mensaje si la confianza es baja.
            - todas_las_probabilidades (dict): Probabilidad para cada clase.
    """
    modelo = _cargar_modelo()

    probs = modelo.predict_proba([texto])[0]
    classes = modelo.classes_

    idx_max = int(np.argmax(probs))
    resultado = classes[idx_max]
    confianza = float(probs[idx_max])

    advertencia = None
    if confianza < 0.40:
        advertencia = (
            "La confianza es baja. El apunte podría ser ambiguo "
            "o el modelo necesita más datos similares."
        )

    todas_las_probabilidades = {
        clase: float(prob) for clase, prob in zip(classes, probs)
    }

    return {
        "resultado": resultado,
        "confianza": confianza,
        "advertencia": advertencia,
        "todas_las_probabilidades": todas_las_probabilidades,
    }
