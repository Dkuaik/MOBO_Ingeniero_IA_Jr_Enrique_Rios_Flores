# Clientes del Proyecto

## Descripción General

Para todos los microservicios de este proyecto, se crearon diferentes clientes para facilitar la comunicación entre ellos. Se habilitaron funcionalidades para desacoplar el código y trabajar de manera independiente en cada servicio, permitiendo que interactúen sin crear un código espagueti.

## Arquitectura de los Clientes IA

Me gustaría destacar la idea detrás de `ia_clients`. Este módulo funciona de la siguiente manera:

- **Interfaz**: Sirve como una capa de abstracción para inyectar dependencias.
- **Implementaciones de Clientes**: Se crean las implementaciones específicas de los clientes (para fines de la prueba técnica, solo funciona el de OpenRouter).
- **Client Factory**: Es el encargado de crear las instancias de los clientes.

De esta forma, en cualquier parte del código podemos solicitar un cliente que se comunique con Claude, OpenAI u OpenRouter (y se puede expandir fácilmente sin afectar el código existente). Esto nos permite comunicarnos siempre de la misma manera con el cliente de IA, pero con diferentes implementaciones, lo que brinda flexibilidad para extender el número de clientes sin romper nada.

Para los fines de la prueba tecnica sólo el cliente de OpenRouter es utilizable