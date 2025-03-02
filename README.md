# Proyecto: Ficha Dental

Este es un proyecto web que permite gestionar y visualizar las piezas dentales de los pacientes. Los usuarios pueden editar y guardar cambios en la información de las piezas dentales a través de una interfaz de usuario interactiva.

## Descripción

El proyecto proporciona una vista gráfica de las piezas dentales superiores e inferiores de un paciente. Los lados de las piezas dentales (superior, inferior, derecho e izquierdo) se pueden modificar y se guardan mediante un botón de acción. También se muestra el nombre del paciente al lado de la etiqueta "Ficha Dental".

## Requisitos

- **Navegador Web**: Cualquier navegador moderno (Chrome, Firefox, Safari, Edge).
- **Servidor Web (opcional)**: Si deseas hacer pruebas locales y no usas un servidor backend.
- **Backend (opcional)**: Si tienes una API para recuperar los datos del paciente.

## Tecnologías Utilizadas

- **HTML5**: Para la estructura de la página web.
- **CSS3**: Para el diseño y estilo visual.
- **JavaScript**: Para la lógica interactiva y gestión de eventos.
- **qwebchannel.js**: Usado para la comunicación con un backend (si aplica).

## Instalación

1. **Clonar el Repositorio**:
   Si aún no tienes el proyecto, clónalo en tu máquina local:

   ```bash
   git clone https://github.com/Cdruetta/Ficha-dental-2.git
   ```

2. **Acceder al directorio del proyecto**:

   ```bash
   cd ficha-dental-2
   ```

3. **Abrir el archivo HTML**:
   Si solo necesitas probar la parte visual y no interactuar con una API, simplemente abre el archivo `index.html` en tu navegador.

4. **Configuración del servidor (si aplica)**:
   Si tienes un backend para este proyecto, asegúrate de configurarlo correctamente.

   ### Backend (opcional):

   Si usas un servidor en Python o Node.js para gestionar las solicitudes, sigue los pasos que correspondan para iniciar el servidor.

   Ejemplo con Python (Flask):

   ```bash
   pip install flask
   python app.py
   ```

   O con Node.js:

   ```bash
   npm install
   npm start
   ```

## Uso

1. Al abrir la página, verás una vista de las piezas dentales superiores e inferiores del paciente.
2. La información de cada pieza dental puede ser modificada mediante los "lados" (superior, inferior, derecho e izquierdo).
3. El nombre del paciente se muestra al lado de la etiqueta "Ficha Dental".
4. Para guardar los cambios, presiona el botón **"Guardar Cambios"**.
5. El logo se muestra al final de la página.

## Estructura de Archivos

```
/ficha-dental
│
├── index.html             # Página principal con la interfaz gráfica
├── css
│   └── styles.css         # Estilos personalizados del proyecto
├── js
│   └── app.js             # Lógica de interacción y eventos
├── img
│   └── logo.png           # Logo del proyecto
└── README.md              # Este archivo
```

## Personalización

- **Modificar la interfaz**: Puedes modificar el archivo `styles.css` para ajustar el estilo visual de la página.
- **Modificar los datos del paciente**: En el archivo `app.js`, puedes ajustar la lógica para obtener el nombre del paciente desde una base de datos o API.

## Contribución

Si deseas contribuir al proyecto, por favor sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios.
4. Haz un commit de tus cambios (`git commit -am 'Agregada nueva funcionalidad'`).
5. Haz push a tu rama (`git push origin feature/nueva-funcionalidad`).
6. Crea un Pull Request.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.
