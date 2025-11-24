# MOBO_Ingeniero_IA_Jr_Enrique_Rios_Flores

Este repositorio contiene el proyecto MOBO para Ingeniero IA Jr por Enrique Rios Flores.

## Resumen General del Proyecto

El proyecto **MOBO_Ingeniero_IA_Jr_Enrique_Rios_Flores** es una aplicación de chatbot de IA desarrollada en Python utilizando FastAPI como framework principal. Está diseñado para proporcionar una interfaz de chat interactiva con funcionalidades avanzadas como RAG (Retrieval-Augmented Generation) y soporte para herramientas MCP (Model Context Protocol). 
Todo el proyecto está hecho con una arquitectura de microservicios dockerizados.

Pensando también en los problemas planteados en el examen teorico quise pantear un mcp para la 

NOTA: Al Tener una Arquitectura de microservicios y logica del codigo desacoplada puede ser que el primer build de la app sea un poco tardado. La mayor parte del tiempo se la lleva al descarga de sentence-transformers.
 
## Cómo arrancar el proyecto

### Prerrequisitos
- Docker y Docker Compose instalados en tu sistema.
- Conexión a internet para descargar imágenes y dependencias.

### Instrucciones
1. Clona o navega al directorio raíz del proyecto.
2. Ejecuta el siguiente comando para construir y levantar todos los servicios:

   ```bash
   docker compose up
   ```

   NOTA: Al tener una arquitectura de microservicios y lógica del código desacoplada, el primer build puede ser un poco tardado.

3. Una vez que todos los servicios estén corriendo, accede a la interfaz web en `http://localhost:3000`.
4. Para gestionar la base de datos, usa Mongo Express en `http://localhost:8081` (usuario: admin, contraseña: express123, deje un boton en la interfaz principal para poder acceder facilmente).

## Arquitectura

### 1. API Principal y Interfaz de Usuario
- **Archivo principal**: `main.py` contiene la aplicación FastAPI que actúa como el punto de entrada principal.
- **Interfaz web**: Ofrece una interfaz HTML básica y simple accesible en el puerto 3000. Incluye:
  - Un área de chat para enviar mensajes y recibir respuestas del bot.
  - Opciones configurables:
    - **RAG (Retrieval-Augmented Generation)**: Se puede activar/desactivar. Permite elegir entre 4 roles contextuales (ADMIN, DEV, HR, ALL) para enriquecer las respuestas con documentos relevantes recuperados de una base de datos vectorial.
    - **MCP Server**: Checkbox para habilitar herramientas adicionales, como obtener tasas de cambio de USD desde una API externa.
  - Un botón para acceder a Mongo Express (puerto 8081) para visualizar la base de datos.
- **Funcionalidad del chat**:
  - Los mensajes del usuario se procesan para generar respuestas de IA usando clientes de IA (por defecto, OpenRouter con modelo Gemini 2.5 Flash).
  - Si RAG está habilitado, se codifica el mensaje en embeddings y se busca similitud en FAISS para agregar contexto relevante.
  - Si MCP está habilitado, se incluyen herramientas como funciones para consultas externas.
  - Todas las interacciones se registran en MongoDB para auditoría.

### 2. Arquitectura y Servicios
El proyecto está dockerizado con múltiples servicios interconectados en una red puente (`ai_api_network`):
- **MongoDB**: Base de datos principal (puerto 27017) para almacenar interacciones de chat, usuarios y documentos (embeddings generados por el servicio de faiss).
- **API (FastAPI)**: Servicio principal que expone la interfaz web y maneja la lógica de chat.
- **FAISS**: Servicio de búsqueda vectorial (puerto 8001) para RAG. Maneja embeddings de documentos y búsquedas de similitud.
- **MCP Server**: Servicio micro (puerto 8002) que proporciona herramientas adicionales para el chatbot.
- **Mongo Express** (opcional): Interfaz web para gestionar MongoDB (puerto 8081). Este servicio se habilito para poder ver la base de datos de MongoDB de una forma facil y clara.

### 3. Clientes y Servicios Auxiliares
- **Clientes de IA**: Soporte para múltiples proveedores (OpenAI, Claude, OpenRouter) a través de una fábrica de clientes. (Para fines de pruebas sólo está habilitado el cliente con Openrouter, dejo una api key restringida con cierto butget para poder probar e proyecto)
- **Cliente FAISS**: Interfaz para búsquedas vectoriales.
- **Cliente MongoDB**: Para operaciones en la base de datos.
- **Cliente MCP**: Para integrar herramientas MCP.

### 4. Configuración y Datos
- **Configuración**: Centralizada en `src/config/settings.py`.
- **Documentos RAG**: Almacenados en `docs/`, con archivos específicos por rol (ADMIN, DEV, HR, ALL).
- **Embeddings**: Procesados en el servicio FAISS.

### 5. Dependencias y Despliegue
- **Dependencias**: Gestionadas con `pyproject.toml`.
- **Despliegue**: Usa Docker Compose para orquestar servicios.

### 6. Flujo de Datos General
- El usuario interactúa vía la interfaz web.
- La API procesa el mensaje, agrega contexto RAG y herramientas MCP si están habilitadas.
- Se genera la respuesta usando un cliente de IA.
- La interacción se guarda en MongoDB.

Este proyecto demuestra una arquitectura modular para un chatbot con capacidades de IA avanzadas.