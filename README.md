# KIRA - Herramienta de Búsqueda de URLs

## ¿Qué es KIRA?

KIRA es una herramienta diseñada para explorar y analizar sitios web. Su principal función es encontrar todas las páginas y recursos accesibles dentro de un sitio web dado. Esto puede ser útil para varios propósitos, incluyendo:

1. Auditoría de seguridad
2. Mapeo de la estructura de un sitio web
3. Identificación de contenido oculto o no enlazado
4. Búsqueda de posibles páginas de administración


## ¿Cómo funciona?

1. **Exploración**: KIRA comienza con una URL que tú le proporcionas y explora todas las páginas enlazadas dentro de ese sitio.
2. **Profundidad**: Puedes especificar qué tan "profundo" quieres que KIRA explore. Por ejemplo, una profundidad de 2 significa que explorará la página inicial, las páginas enlazadas directamente desde ella, y las páginas enlazadas desde esas.
3. **Búsqueda de Admin**: KIRA puede intentar encontrar páginas de administración probando rutas comunes como '/admin', '/login', etc.
4. **Resultados**: Al final, KIRA te proporciona una lista de todas las URLs encontradas.


## Cómo usar KIRA

1. **Iniciar KIRA**:
Abre una terminal o línea de comandos y escribe:

```plaintext
python kira.py https://www.ejemplo.com
```

Reemplaza "[https://www.ejemplo.com](https://www.ejemplo.com)" con el sitio web que quieres analizar.


2. **Opciones adicionales**:

1. Para cambiar la profundidad de búsqueda:

```plaintext
python kira.py https://www.ejemplo.com --depth 3
```


2. Para cambiar el número de procesos paralelos (para búsquedas más rápidas):

```plaintext
python kira.py https://www.ejemplo.com --workers 10
```





3. **Durante la ejecución**:

1. KIRA te preguntará si quieres buscar páginas de administración.
2. Si dices que sí, te preguntará si tienes una lista personalizada de rutas para probar.



4. **Resultados**:

1. KIRA guardará todas las URLs encontradas en un archivo de texto.
2. El nombre del archivo será basado en el sitio web analizado, por ejemplo: "ejemplo.com_1.txt"





## Consideraciones éticas y legales

1. **Permiso**: Asegúrate de tener permiso para analizar el sitio web. Analizar sitios sin autorización puede ser ilegal.
2. **Uso responsable**: Esta herramienta está diseñada para fines de auditoría y seguridad. No la uses para actividades maliciosas o no autorizadas.
3. **Impacto**: KIRA realiza múltiples solicitudes a un sitio web. En sitios grandes o con configuraciones de seguridad estrictas, esto podría ser interpretado como un ataque o causar problemas de rendimiento.
4. **Privacidad**: Si encuentras información sensible o privada, repórtala al propietario del sitio de manera responsable.


## Limitaciones

- KIRA solo puede encontrar páginas que estén enlazadas o que sigan patrones comunes (en el caso de páginas de administración).
- No puede acceder a contenido protegido por contraseñas o detrás de formularios de inicio de sesión.
- Algunos sitios web pueden tener medidas para prevenir este tipo de exploración automática.


## Soporte

Si tienes preguntas sobre cómo usar KIRA o encuentras algún problema, por favor contacta al equipo de soporte técnico.
