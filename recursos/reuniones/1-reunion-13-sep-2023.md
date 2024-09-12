## Requisitos
* Crear Partida
* Unir jugador
* Iniciar partida
* Crear Mazo
* Repartir cartas
* Robar carta del mazo
* Jugar carta (sin aplicar efecto si no es un lanzallamas)
* Efecto lanzallamas al jugarlo
* Finalizar partida (solo se finaliza cuando queda un solo jugador vivo)
* Aclaración: un jugador solo juega cartas durante su turno, no se pide implementar cartas de defensa.
Esto quiere decir que al jugar un lanzallamas el jugador objetivo siempre muere.

## Comentarios y consultas
* Pedir nombre al ingreso, o antes de comenzar cada partida. ---> nos gusta mas antes de ingresar a cada partida
* Cómo identificar jugadores con mismo nombre dentro de una mesa ----> Jugador con Nombre/ID único por partida. Consultar si todo ok(?)
* Cómo sincronizar los eventos? Comunicación a través de Sockets o el jugador cada cierto tiempo pide el estado actual
* Clase maso?
* Herencia
* Contratos de API?
* Clase configuración de la partida (?)


# Tickets 1er Sprint

## Ambos
Definir endpoints de la API (puede dividirse en más tickets según la complejidad).
Definir un borrador de las interfaces de usuario.

## Backend
Crear la estructura del proyecto en Fast API.
Crear la estructura de la base de datos.
Implementar la clase "Partida".
Implementar la clase "Estado del Juego".
Implementar la clase "Jugador".
Implementar la clase "Carta".
Crear la clase (o solo la funcionalidad) de mazo.
Implementar la funcionalidad de repartir cartas: asociar instancias de cartas con instancias de jugadores y registrarlas en la base de datos.
Comunicar carta(s) al jugador (esto depende de la metodología de comunicación elegida).
Agregar métodos para la gestión de turnos y fases del turno. Modificar el estado de la partida y la base de datos.
Agregar método para robar carta y registrarla en la base de datos. Asociar una instancia de carta a una instancia de jugador (pensar en cómo identificar cartas de manera única).
Agregar método para jugar carta y registrarla en la base de datos. Desasociar la carta del jugador y marcarla como descartada u otro método para llevar registro.
Agregar funcionalidad "lanzallamas": modificar el estado de la partida y la base de datos.
Agregar métodos de chequeo para el fin de partida.
Limpiar recursos y eliminar todo lo de la base de datos al finalizar la partida.

## Frontend
Crear la estructura del proyecto en React.
Crear la página principal (sin funcionalidad, solo botones y estructura).
Mostrar partidas disponibles.
Crear la estructura de la página "partida".
Crear botones para crear partida y unirse a partida.
Crear formulario "crear partida" y desarrollar la funcionalidad correspondiente.
Implementar la funcionalidad de "unirse partida".
Crear la estructura del lobby (jugadores dentro de la partida, sala de espera).
Crear botón y funcionalidad para iniciar la partida.
Mostrar carta(s).
Agregar botón y funcionalidad para robar carta.
Agregar botón y funcionalidad para jugar carta.
Agregar botones y funcionalidad necesarios para seleccionar el jugador al cual aplicar "lanzallamas".
Avisar/mostrar resultados de la partida.
Programar la secuencia de fin de partida y el regreso a la página principal.




----------------------------------------------------------------------------------------------------------------

### Borrador 

## Tickets 1er Sprint

### Ambos
* Definir endpoints API:
 + Crear endpoint para "Crear Partida" (POST /api/partidas).
 + Crear endpoint para "Unir Jugador" (POST /api/partidas/{id}/jugadores).
 + Definir estructura JSON de respuesta para ambos.
Definir un borrador de las interfaces


### Backend
Crear la estructura del proyecto en Fast API
Crear la estructura de la base de datos
Crear clase partida
Crear clase estado del juego
Crear clase jugador 
Crear clase carta
Crear la clase (o solo la funcionalidad) de maso (?)
Funcionalidad repartir: asociar instancias de cartas con instancia de jugadores y registrarlo en la base de datos
Comunicar carta(s) al jugador. Esto depende de cual va a ser la metodología de comunicación.
Agregar métodos para gestión de turno y fase del turno. Modifica estado de la partida y BD
Agregar método robar carta y registrar en la BD. Asocia una instancia carta a una instancia jugador (pensar en como identificar cartas unívocamente)
Agregar método jugar carta y registrar en la BD. Desasocia la carta del jugador y (la marca como descartada / otro método que encontremos para llevar registro)
Agregar funcionalidad "lanzallamas". Modificar estado de la partida && BD
Agregar métodos de chequeo fin de partida
Limpiar recursos y eliminar todo lo de la BD


### Frontend
Crear estructura del proyecto en react
Crear página principal(sin funcionalidad, botones y estructura)
Mostrar partidas disponibles
Crear estructura página "partida"
Crear botones crear partida, unirse partida
Crear formulario "crear partida" / Funcionalidad de "crear partida" 
Funcionalidad de "unirse partida"
Crear estructura lobby (jugadores dentro de la partida, sala de espera)
Crear botón y funcionalidad "iniciar partida"
Mostrar carta(s)
Agregar botón y funcionalidad robar carta
Agregar botón y funcionalidad jugar carta
Agregar botones y funcionalidad necesarios para seleccionar jugador al cual aplicarle "lanzallamas"
Avisar/mostrar resultados de la partida
Programar secuencia de fin de partida y regreso a página principal