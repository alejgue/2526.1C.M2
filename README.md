**1. cargar_nivel:**

Esta función se encarga de leer el archivo de nivel indicado en self.level_path y transformarlo en una cuadrícula válida para el juego.

Función:
- Comprueba que la ruta proporcionada corresponde a un archivo existente.
- Lee el contenido completo del fichero utilizando read().
- Divide el texto en líneas con splitlines(), eliminando líneas vacías.
- Valida que todas las filas tengan la misma longitud; si no, lanza un error.
- Asigna el resultado a self.layout y lo devuelve.

Resultado:
El nivel queda representado internamente como una lista de cadenas, donde cada carácter define un tipo de bloque o una celda vacía.

**2. preparar_entidades:**

Esta función inicializa los elementos principales del juego antes de comenzar la partida.

Función:
- Crea la paleta usando self.crear_rect() con las dimensiones definidas en la configuración.
- Centra la paleta en la parte inferior de la pantalla usando midbottom.
- Reinicia las variables de estado del juego: self.score, self.livesy `yo mismoself.end_message.
- Llama a self.reiniciar_bola() para colocar la bola justo encima de la paleta con su velocidad inicial.

Resultado:
El juego queda en estado inicial: paleta centrada, bola preparada para salir y contador de puntos y vidas reiniciado.

**3. crear_bloques:**

Esta función analiza la cuadrícula cargada previamente y genera los bloques que se renderizarán en pantalla.

Función:
- Limpia las listas self.blocks, self.block_colorsy `self.b_self.block_symbols.
- Recorre cada fila y columna de self.layout.
- Ignora el carácter . y valida que no existan símbolos no reconocidos.
- Para cada símbolo de bloque (#, @, %):--Calcula su posición en pantalla mediante self.calcular_posicion_bloque().
    - Añade el rectángulo resultante a self.blocks.
    - Añade su color correspondiente a self.block_colors.
    - Registra el símbolo en self.block_symbols para gestionar la puntuación.

Resultado:
Los bloques quedan generados y listos para ser dibujados y colisionados durante el juego.

**4. procesar_input:**

Esta función gestiona la entrada del usuario para controlar el movimiento de la paleta.

Función:
- Obtiene el estado del teclado mediante self.obtener_estado_teclas().
- Detecta la pulsación de las teclas de movimiento:
    - Izquierda: KEY_LEFT o KEY_A.
    - Derecha: KEY_RIGHT o KEY_D.
- Actualiza la posición horizontal de la paleta utilizando self.PADDLE_SPEED.
- Aplica límites para evitar que la paleta pueda salir de la pantalla.

Resultado:
La paleta se mueve a la izquierda o a la derecha solo cuando el usuario mantiene pulsadas las teclas correspondientes, y nunca puede salirse de los límites de la pantalla.

**5. actualizar_bola:**

Esta función se encarga del movimiento de la bola y todas las colisiones que se producen durante la partida.

Función:
- Actualiza la posición de la bola sumando su vector de velocidad (self.ball_velocity) a su posición actual (self.ball_pos), y obtiene su rectángulo de colisión mediante self.obtener_rect_bola().
- Colisión con paredes laterales: Detecta si la bola toca los bordes izquierdo o derecho de la pantalla
- Colisión con techo: Si la bola golpea la parte superior de la pantalla, invierte su componente vertical (self.ball_velocity.y *= -1) y reajusta su posición.
- Caída de la bola: Cuando la bola cae por debajo de la pantalla (ball_rect.top >= self.SCREEN_HEIGHT), resta una vida, reinicia la bola sobre la paleta.
- Colisión con la paleta: Verifica si la bola impacta con la paleta mientras desciende (self.ball_velocity.y > 0). En caso afirmativo:
    - Reposiciona la bola justo encima de la paleta para evitar que atraviese.
    - Calcula la distancia relativa del punto de impacto respecto al centro de la paleta.
    - Aplica un ángulo de rebote que varía según dónde golpee la bola
    - Multiplica  self.BALL_SPEED para mantener velocidad constante.
- Colisión con bloques: Recorre todos los bloques activos comprobando colisiones
- Si las vidas llegan a cero, establece el mensaje "GAME OVER" y llama a self.pantalla_fin().
- Si no quedan bloques en pantalla, determina el mensaje apropiado: si es el último nivel (level_5.txt), muestra "¡JUEGO TERMINADO! ¡Gracias por jugar!", de lo contrario "¡Pasaste el Nivel!", y llama a self.pantalla_fin().

Resultado:
La bola se mueve de forma fluida, rebota en todas las superficies, destruye bloques al impactar y se detecta las condiciones de victoria o derrota.

**6. dibujar_bloque_con_borde:**

Esta función mejora la presentación visual de los bloques añadiéndoles un borde negro que los hace más definidos y atractivos.

Función:
- Define el grosor del borde (3 píxeles) y su color (negro).
- Dibuja primero un rectángulo negro del tamaño completo del bloque, que actuará como el borde exterior.
- Utiliza el método .inflate() de pygame para crear un rectángulo interior reducido en el doble del grosor del borde por cada dimensión (lo que deja visible el marco negro).
- Dibuja el rectángulo interior con el color original del bloque, creando así el efecto de borde.

Resultado:
Cada bloque se renderiza con un borde negro de 3 píxeles que lo rodea completamente

**7. dibujar_escena**

Esta función pinta cada elemento en el orden correcto para que se visualice adecuadamente.

Función:
- Dibuja la imagen de fondo cargada (self.background_img) usando blit() en la posición (0, 0). Si la imagen no está disponible, rellena la pantalla con el color de fondo predeterminado. 
- Itera sobre las listas paralelas self.blocks y self.block_colors utilizando zip(), y dibuja cada bloque llamando a self.dibujar_bloque_con_borde() para incluir el efecto de borde.
- Renderiza la paleta como un rectángulo sólido con self.dibujar_rectangulo() usando self.PADDLE_COLOR.
- Dibuja la bola como un círculo mediante self.dibujar_circulo(), usando la posición actual self.ball_pos, el radio definido self.BALL_RADIUS y el color self.BALL_COLOR.
- Muestra información vital del juego en la esquina superior izquierda:
Puntuación actual en la posición (10, 10).
Número de vidas restantes en la posición (10, 40).

Resultado:
La pantalla muestra el juego completo: fondo personalizado o color sólido, todos los bloques activos con sus bordes, la paleta controlada por el jugador, la bola en movimiento, y los indicadores de puntuación y vidas siempre visibles.

**8. cargar_audio_y_fondo:**

Esta función añade música ambiental y fondos visuales específicos para cada nivel.

Función:
- Extrae el número del nivel desde el nombre del archivo (por ejemplo, level_3.txt → 3) utilizando .stem.split('_')[-1].
- Asigna archivos de audio y fondo según el número de nivel:
    - Niveles 1-2: Música level_1-2.mp3 y fondo background1-2.png
    - Niveles 3-4: Música level_3-4.mp3 y fondo background3-4.png
    - Nivel 5+: Música level_5.mp3 y fondo background5.png
- Intenta cargar la imagen correspondiente usando pygame.image.load(), la convierte con .convert() para optimizar el rendimiento, y la redimensiona al tamaño exacto de la pantalla (SCREEN_WIDTH x SCREEN_HEIGHT) con pygame.transform.scale(). Si falla, captura la excepción y muestra una advertencia, permitiendo que el juego continúe con el fondo de color sólido.
- Carga de música: Detiene cualquier música que esté sonando con pygame.mixer.music.stop(), carga el nuevo archivo de audio con pygame.mixer.music.load(), establece el volumen definido (self.music_volume), e inicia la reproducción en bucle infinito (loops=-1). Si hay error, muestra advertencia y el juego continúa sin música.

Resultado:
Cada nivel tiene su propia ambientación visual y sonora.

**9. pantalla_fin**

Esta función gestiona las pantallas de finalización del juego, proporcionando diferentes opciones al jugador según el resultado obtenido.

Función:
- Crea fuentes de pygame para el mensaje principal (tamaño 60) y los botones (tamaño 40), inicializa un reloj para controlar los FPS, y detiene la música con pygame.mixer.music.stop().
- Analiza el mensaje recibido para identificar tres estados posibles:
    - game_over = True si el mensaje es "GAME OVER"
    - juego_completo = True si el mensaje es "¡JUEGO TERMINADO! ¡Gracias por jugar!"
    - Nivel completado en cualquier otro caso

- Renderizado de textos: Geera superficies de texto para el mensaje principal y tres botones posibles: "Next Level", "Retry" y "Quit".
- Posicionamiento de botones: Calcula la posición central de la pantalla y crea rectángulos para los botones. La disposición varía según el estado:
    - Game Over o Juego Completo: Muestra botones "Retry" (arriba) y "Quit" (abajo)
    - Nivel completado: Muestra botones "Next Level" (arriba) y "Quit" (abajo)
- Bucle de pantalla de fin: Entra en un bucle independiente que:
- Evento de cierre de ventana: Si el usuario cierra la ventana, establece self.running = False y retorna.

Resultado:
El jugador recibe feedback visual claro sobre su progreso y puede elegir entre reintentar el nivel actual, avanzar al siguiente (si ganó), o salir del juego. 

**10. run**

Esta es la función principal del juego, implementando el bucle de juego clásico (game loop).

Función:
- Inicialización: Ejecuta en secuencia:

self.inicializar_pygame(): Inicializa pygame, crea la ventana y el reloj de FPS.
self.cargar_nivel(): Lee y valida el archivo de nivel.
self.preparar_entidades(): Posiciona paleta y bola, reinicia puntuación y vidas.
self.crear_bloques(): Genera los rectángulos de bloques según la cuadrícula.
self.cargar_audio_y_fondo(): Carga música y fondo visual del nivel.
Establece self.running = True para iniciar el bucle principal.


- Bucle principal (while self.running:): Se ejecuta continuamente mientras el juego está activo:

Procesamiento de eventos: Itera sobre todos los eventos de pygame:

Si detecta EVENT_QUIT (cerrar ventana), establece self.running = False
Si detecta EVENT_KEYDOWN con la tecla ESCAPE, también establece self.running = False


- Input del jugador: Llama a self.procesar_input() para gestionar el movimiento de la paleta según las teclas presionadas.
- Ejecuta self.actualizar_bola() que mueve la bola, resuelve todas las colisiones y verifica condiciones de fin de juego.
- Renderizado: Invoca self.dibujar_escena() que pinta todos los elementos del juego en pantalla.
Sincronización de pantalla: Llama a self.actualizar_pantalla() para hacer visible lo dibujado (equivalente a pygame.display.flip()).
- Finalización: Una vez que self.running es False y el bucle termina, llama a self.finalizar_pygame() para cerrar pygame limpiamente y liberar recursos.

Resultado:
El juego funciona de manera fluida y estable, procesando entrada del usuario, actualizando la lógica del juego y renderizando gráficos a 60 FPS constantes, hasta que el jugador decide salir o completa/pierde todos los niveles.