# 🤖 Módulo de Inteligencia Artificial (Backend API)

Este proyecto es una API construida con **FastAPI** (Python) que sirve como el cerebro de nuestra aplicación. Se encarga de procesar imágenes y texto utilizando modelos de Inteligencia Artificial.

---

## 🚀 Guía de Inicio Rápido (Para Estudiantes)

Sigue estos pasos cuidadosamente para poner en marcha el servidor en tu computadora.

### 1. Requisitos Previos

Asegúrate de tener instalado **Python** (versión 3.9 o superior recommended).
Para verificar si lo tienes, abre una terminal (PowerShell o CMD) y escribe:
```powershell
python --version
```

### 2. Configurar el Entorno Virtual

Es importante aislar las librerías del proyecto para no afectar tu sistema.

1.  Abre la terminal en la carpeta del proyecto (`IA_Module`).
2.  Crea el entorno virtual ejecutando:
    ```powershell
    python -m venv venv
    ```
    *(Esto creará una carpeta llamada `venv`)*.

3.  **Activa** el entorno virtual:
    *   **En Windows (PowerShell):**
        ```powershell
        .\venv\Scripts\Activate
        ```
    *   **En Windows (CMD):**
        ```cmd
        venv\Scripts\activate.bat
        ```
    *   *(Sabrás que funcionó porque verás `(venv)` al principio de la línea de comandos)*.

### 3. Instalar Dependencias

Con el entorno activado, instala las librerías necesarias:

```powershell
pip install -r requirements.txt
```

*(Esto puede tardar un poco la primera vez)*.

### 4. Configurar Variables de Entorno

El servidor necesita cierta configuración para funcionar.

1.  Busca el archivo llamado `.env.example`.
2.  Haz una copia de ese archivo y renómbralo a `.env` (sin el `.example`).
3.  Abre el archivo `.env` con un editor de texto (Notepad, VS Code).
    *   Si no vas a usar la API de Google (Gemini), puedes dejar la línea `GOOGLE_API_KEY` comentada o vacía por ahora.

### 5. Ejecutar el Servidor 🏃‍♂️

Ahora estamos listos para encender el motor. Ejecuta:

```powershell
uvicorn main:app --reload
```

Si todo sale bien, verás algo como:
`INFO:     Uvicorn running on http://127.0.0.1:8000`

### 6. Verificar que funciona

Abre tu navegador web e ingresa a:
👉 [http://localhost:8000/docs](http://localhost:8000/docs)

Deberías ver una página azul con el título "AI Module API". ¡Esa es la documentación interactiva!

---

## 📚 Cómo probar la API (Documentación Interactiva)

FastAPI genera automáticamente una página donde puedes probar todos los "endpoints" (funciones) del servidor sin necesidad de programar nada extra.

### Paso a paso para hacer una prueba:

1.  **Entra a la documentación**: [http://localhost:8000/docs](http://localhost:8000/docs)
2.  Verás una lista de bloques de colores (GET, POST). Cada uno es una función de la IA.
3.  **Haz clic** en la flecha de un endpoint, por ejemplo: `POST /api/v1/ai/process`.
4.  Presiona el botón gris que dice **Try it out** (Pruébalo) en la esquina derecha.
5.  Se habilitará un cuadro de texto (Request body). Puedes editar el JSON para enviar datos.
    *   *Ejemplo de prueba:*
        ```json
        {
          "prompt": "Hola, ¿cómo estás?",
          "model": "default-model"
        }
        ```
6.  Haz clic en el botón azul grande **Execute**.
7.  Mira abajo en la sección **Responses**.
    *   Si todo salió bien, verás un `Code 200` y el resultado de la IA en el cuerpo de la respuesta (`Response body`).

### Ejemplo 2: Subir una imagen o PDF (Endpoint de Extracción)

Este es un poco diferente porque enviamos archivos.

1.  Busca el endpoint: `POST /api/v1/extraction/text`.
2.  Haz clic en **Try it out**.
3.  Verás un campo que dice **file**. Haz clic en "Choose File" (o "Seleccionar archivo") y busca una imagen o PDF en tu computadora.
4.  (Opcional) En el campo **mode**, puedes escribir `standard` (por defecto) o `gemini` si configuraste la API Key.
5.  Dale a **Execute**.
6.  El servidor leerá tu archivo y te devolverá el texto extraído en el JSON de respuesta.

¡Es así de fácil interactuar con tu backend! no necesitas Postman ni crear un frontend todavía.


