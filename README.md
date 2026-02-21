# Taller_Desarrollo_en_Contenedores_MLOPS_PUJ
## Proyecto MLOps: Clasificación de Pingüinos con Arquitectura Desacoplada

Este proyecto implementa una arquitectura de Machine Learning desacoplada orientada a MLOps, utilizando Python y Docker Compose. El objetivo es demostrar buenas prácticas en el ciclo de vida de modelos, separación de entrenamiento e inferencia, y automatización de despliegue.

### 1. Descripción y Objetivo
El proyecto permite entrenar modelos de clasificación de pingüinos en un entorno JupyterLab y servir predicciones mediante una API REST basada en FastAPI. Ambos servicios están desacoplados y comparten artefactos de modelos a través de un volumen Docker, facilitando la actualización y recarga automática de modelos.

### 2. Arquitectura
La arquitectura se compone de dos servicios principales:

```
┌───────────────┐      Volumen compartido      ┌───────────────┐
│ JupyterLab   │ <--------------------------> │ FastAPI       │
│ Entrenamiento│        /models               │ Inferencia    │
└───────────────┘                              └───────────────┘
```
- **JupyterLab**: Entrenamiento y guardado de modelos (.pkl)
- **FastAPI**: Inferencia y recarga automática de modelos
- **Volumen Docker**: Carpeta `models` compartida entre ambos servicios
- **Docker Compose**: Orquestación de servicios y volumen
- **Model Registry**: Basado en filesystem, con escritura atómica

### 3. Estructura del Repositorio

```
Taller_Desarrollo_en_Contenedores_MLOPS_PUJ/
├── docker-compose.yaml
├── main.py
├── model_registry.py
├── predict.py
├── requirements.txt
├── train.ipynb
├── datasets/
│   └── penguins_size.csv
├── docker/
│   ├── Dockerfile.api
│   └── Dockerfile.jupyter
├── logs/
├── models/
├── models_performance/
│   ├── decision_tree_results.txt
│   ├── knn_results.txt
│   └── svm_results.txt
```

### 4. Requisitos
- Docker
- Docker Compose
- Python 3.11 (para desarrollo local)

### 5. Instrucciones para levantar el proyecto

1. Clona el repositorio:
	 ```bash
	 git clone <url-del-repositorio>
	 cd Taller_Desarrollo_en_Contenedores_MLOPS_PUJ
	 ```
2. Levanta los servicios con Docker Compose:
	 ```bash
	 docker compose up --build
	 ```
3. Accede a JupyterLab en [http://localhost:8888](http://localhost:8888)
4. Accede a la API en [http://localhost:8000/docs](http://localhost:8000/docs)

### 6. Entrenamiento de modelos desde Jupyter
Abre el notebook `train.ipynb` en JupyterLab. Ejecuta las celdas para entrenar modelos de clasificación (Decision Tree, KNN, SVM) y guardarlos en la carpeta `models/` como archivos `.pkl`. El guardado utiliza escritura atómica para evitar corrupción.

### 7. Consumo de la API
La API FastAPI expone un endpoint `/predict` para realizar inferencias. Puedes probarlo desde Swagger UI o mediante requests:

#### Ejemplo de request:
```bash
curl -X POST "http://localhost:8000/predict" \
		 -H "Content-Type: application/json" \
		 -d '{"model": "decision_tree", "features": [0.5, 1.2, 3.4, 2.1]}'
```

#### Ejemplo de respuesta:
```json
{
	"prediction": "Adelie",
	"probability": 0.92
}
```

### 8. Mecanismo de Hot Reload de Modelos
La API monitorea el timestamp de los archivos de modelos en el volumen compartido. Cuando detecta una actualización, recarga el modelo automáticamente sin reiniciar el contenedor, permitiendo despliegue continuo y experimentación.

### 9. Buenas Prácticas Implementadas
- Escritura atómica de modelos para evitar corrupción
- Separación clara entre entrenamiento (Jupyter) e inferencia (API)
- Volumen Docker compartido para artefactos
- Model registry simple basado en filesystem
- Dockerfiles separados para cada servicio

### 10. Posibles Mejoras Futuras
- Versionado de modelos y registro avanzado
- Integración de CI/CD para entrenamiento y despliegue
- Monitoreo de modelos en producción
- Validación de datos y drift detection
- Autenticación y autorización en la API

### 11. Ejemplos de Requests a la API
#### Obtener predicción:
```bash
curl -X POST "http://localhost:8000/predict" \
		 -H "Content-Type: application/json" \
		 -d '{"model": "knn", "features": [0.7, 1.0, 2.9, 1.8]}'
```

#### Swagger UI:
Accede a [http://localhost:8000/docs](http://localhost:8000/docs) para probar la API de forma interactiva.

### 12. Troubleshooting Común
- **Error: modelo no encontrado**
	- Verifica que el modelo esté guardado en la carpeta `models/` y que el nombre sea correcto.
- **La API no recarga el modelo**
	- Asegúrate de que el archivo del modelo se haya actualizado (timestamp cambiado).
- **Problemas de permisos en volumen**
	- Verifica configuración de Docker y permisos de carpeta.
- **JupyterLab no inicia**
	- Revisa logs del contenedor y dependencias en `requirements.txt`.

---
Este proyecto es ideal para portafolio o evaluación técnica en MLOps, mostrando buenas prácticas de desacoplamiento, automatización y robustez en el ciclo de vida de modelos.
