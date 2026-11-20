import gradio as gr
import torch
from transformers import pipeline

# Detectar automáticamente GPU si está disponible, o usar CPU
device = 0 if torch.cuda.is_available() else -1

# Crear el pipeline de clasificación de imágenes con el modelo solicitado
clasificador = pipeline(
    task="image-classification",
    model="google/mobilenet_v2_1.0_224",
    device=device,
)


def clasificar(imagen):
    """Recibe una imagen y devuelve un diccionario con las 3 etiquetas más probables
    y su porcentaje correspondiente.
    """
    if imagen is None:
        return {}

    resultados = clasificador(imagen, top_k=3)

    etiquetas_porcentaje = {}
    for item in resultados:
        etiqueta = item["label"]
        porcentaje = round(item["score"] * 100, 2)
        etiquetas_porcentaje[etiqueta] = f"{porcentaje}%"

    return etiquetas_porcentaje


# Interfaz de Gradio
demo = gr.Interface(
    fn=clasificar,
    inputs=gr.Image(type="pil", label="Sube una imagen"),
    outputs=gr.JSON(label="Top 3 etiquetas más probables"),
    title="Clasificador de imágenes con MobileNet V2",
    description="Sube una imagen para obtener las 3 etiquetas más probables con su porcentaje usando google/mobilenet_v2_1.0_224.",
)

if __name__ == "__main__":
    demo.launch()