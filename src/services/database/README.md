# Servicio de Base de Datos

## Descripción General

Este servicio se encarga de gestionar la base de datos no relacional MongoDB. Proporciona funcionalidades para almacenar y recuperar datos relacionados con el procesamiento de documentos y las interacciones del usuario.

## Colecciones Principales

### 1. Colección `documents`
- **Propósito**: Almacena todos los chunks de texto que posteriormente se convierten en embeddings.
- **Nota**: FAISS no tiene memoria persistente, por lo que esta colección sirve como almacenamiento permanente de los datos procesados.

### 2. Colección `interactions`
- **Propósito**: Guarda las interacciones del usuario con el sistema.
- **Razón de implementación**: Esta funcionalidad se alinea con el caso resuelto en el primer examen teórico, proporcionando un historial de interacciones para análisis y mejoras.

## Visualización de Datos

Para visualizar el contenido de la base de datos de manera opcional, se puede utilizar un segundo servicio llamado **MongoExpress**. Este servicio permite una interfaz gráfica para explorar las colecciones.

- **Acceso**: En la aplicación principal, hay un botón etiquetado "View DB" que tiene los parámetros hardcodeados para conectarse directamente.

## Notas Adicionales

- El servicio está diseñado para integrarse con otros componentes del sistema, como FAISS para embeddings y el servicio MCP para procesamiento.
- Asegúrese de que MongoDB esté ejecutándose y configurado correctamente antes de iniciar este servicio.