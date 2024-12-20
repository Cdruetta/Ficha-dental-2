let backend;

// Inicializar comunicación con Python
new QWebChannel(qt.webChannelTransport, function (channel) {
  backend = channel.objects.backend;

  // Cargar datos iniciales desde Python
  backend
    .cargar_datos_dentales()
    .then(function (datos) {
      console.log("Datos recibidos:", datos);
      inicializarDientes(datos);
    })
    .catch(function (error) {
      console.error("Error al cargar datos: ", error);
    });
});

function inicializarDientes(datos) {
  const superior = document.getElementById("dientes-superiores");
  const inferior = document.getElementById("dientes-inferiores");

  // Asignar los números de los dientes
  const dientesSuperiores = [18, 17, 16, 15, 14, 13, 12, 11, 21, 22, 23, 24, 25, 26, 27, 28];
  const dientesInferiores = [48, 47, 46, 45, 44, 43, 42, 41, 31, 32, 33, 34, 35, 36, 37, 38];

  // Agregar los dientes superiores
  dientesSuperiores.forEach((numero) => {
    superior.appendChild(crearDiente(numero));
  });

  // Agregar los dientes inferiores
  dientesInferiores.forEach((numero) => {
    inferior.appendChild(crearDiente(numero));
  });

  // Marcar los dientes según los datos de la base de datos
  datos.forEach(([diente, cara, estado]) => {
    const dienteElemento = document.querySelector(`[data-nombre="${diente}"]`);
    if (dienteElemento) {
      const lado = dienteElemento.querySelector(`[data-cara="${cara}"]`);
      if (lado) {
        if (estado === "caries") {
          lado.classList.add("seleccionado");
          lado.classList.add("bloqueado");
        }
      }

      // Marcar el centro si está seleccionado
      if (cara === "centro" && estado === "caries") {
        const centro = dienteElemento.querySelector(".centro");
        centro.classList.add("seleccionado");
        centro.classList.add("bloqueado");
      }
    }
  });
}


function crearDiente(nombre) {
  const diente = document.createElement("div");
  diente.classList.add("diente");
  diente.dataset.nombre = nombre;

  // Crear los 4 lados de la pieza dental
  const ladoArriba = crearLado("arriba", diente);
  const ladoAbajo = crearLado("abajo", diente);
  const ladoIzquierda = crearLado("izquierda", diente);
  const ladoDerecha = crearLado("derecha", diente);

  // Crear el centro de la pieza dental
  const centro = document.createElement("div");
  centro.classList.add("centro");
  diente.appendChild(centro);

  // Añadir los lados a la pieza dental
  diente.appendChild(ladoArriba);
  diente.appendChild(ladoAbajo);
  diente.appendChild(ladoIzquierda);
  diente.appendChild(ladoDerecha);

  // Hacer el centro seleccionable si no está bloqueado
  centro.onclick = function () {
    if (!centro.classList.contains("bloqueado")) {
      centro.classList.toggle("seleccionado");
    }
  };

  // Hacer los lados seleccionables si no están bloqueados
  ladoArriba.onclick = function () {
    if (!ladoArriba.classList.contains("bloqueado")) {
      ladoArriba.classList.toggle("seleccionado");
    }
  };

  ladoAbajo.onclick = function () {
    if (!ladoAbajo.classList.contains("bloqueado")) {
      ladoAbajo.classList.toggle("seleccionado");
    }
  };

  ladoIzquierda.onclick = function () {
    if (!ladoIzquierda.classList.contains("bloqueado")) {
      ladoIzquierda.classList.toggle("seleccionado");
    }
  };

  ladoDerecha.onclick = function () {
    if (!ladoDerecha.classList.contains("bloqueado")) {
      ladoDerecha.classList.toggle("seleccionado");
    }
  };

  return diente;
}

function crearLado(cara, diente) {
  const lado = document.createElement("div");
  lado.classList.add("lado", `lado-${cara}`);
  lado.dataset.cara = cara;

  return lado;
}

function guardarCambios() {
  const datos = [];
  document.querySelectorAll(".lado.seleccionado").forEach((lado) => {
    const nombreDiente = lado.closest(".diente").dataset.nombre; // Este debería ser un número
    const cara = lado.dataset.cara;
    datos.push([nombreDiente, cara, "caries"]);
  });

  // Guardar el estado del centro
  document.querySelectorAll(".centro.seleccionado").forEach((centro) => {
    const nombreDiente = centro.closest(".diente").dataset.nombre; // Este también debería ser un número
    datos.push([nombreDiente, "centro", "caries"]);
  });

  // Enviar los datos a Python para guardar en la base de datos
  backend
    .guardar_datos_dentales(datos)
    .then(() => {
      alert("Cambios guardados con éxito");
    })
    .catch((error) => {
      console.error("Error al guardar los datos", error);
    });
}
// Función para obtener el ID del diente a partir del nombrefunction obtenerIdDiente(nombreDiente) {
function obtenerIdDiente(nombreDiente) {
    const regex = /\d+/; // Expresión regular para extraer los números
    const match = nombreDiente.match(regex); // Extrae los números del nombre del diente
    if (match) {
      return match[0].padStart(2, '0'); // Asegura que tenga 2 caracteres
    }
    return "00"; // Retorna "00" si no encuentra un número
  }



