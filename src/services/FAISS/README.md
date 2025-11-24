# Servicio FAISS

## Descripción General

Este servicio se encarga de generar embeddings para el procesamiento de documentos y consultas de usuarios. Utiliza FAISS (Facebook AI Similarity Search) para realizar búsquedas por similitud semántica.

## Momentos de Ejecución

El servicio genera embeddings en dos momentos clave:

### 1. Al Iniciar la Aplicación
- **Proceso**: Revisa la carpeta `docs` y procesa todos los documentos disponibles, se pueden configurar 2 parametros principalmente el overlaping y el tamaño del chunk.
- **Sistema de Roles**: Los documentos siguen una nomenclatura con prefijos como `ALL`, `DEV`, `RH`, `ADMIN`. Esta convención permite implementar un sistema de roles personalizado.
  - Los roles pueden ser cambiados desde la interfaz del chat.
  - Programáticamente, a través de un `rol_id`, los usuarios solo tienen acceso a ciertos embeddings, asegurando la privacidad de la documentación.

### 2. Durante las Consultas del Usuario
- **Proceso**: Cuando un usuario escribe una petición, se genera un embedding de la consulta.
- **Búsqueda**: Posteriormente, se realiza una búsqueda por similitud semántica para encontrar documentos relevantes y asegurandonos de que el rol_id pueda acceder a esos embeddings.

## Notas Técnicas

- Los embeddings se almacenan en FAISS para búsquedas eficientes.
- El sistema de roles garantiza que la información sensible esté protegida según el nivel de acceso del usuario.
- Asegúrese de que la carpeta `docs` contenga los documentos con la nomenclatura correcta antes de iniciar el servicio.
