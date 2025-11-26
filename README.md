1.cargar_nivel:
Esta función se encarga de leer el archivo de nivel indicado en self.level_path y transformarlo en una cuadrícula válida para el juego.
Función:
-Comprueba que la ruta proporcionada corresponde a un archivo existente.
-Lee el contenido completo del fichero utilizando read().
-Divide el texto en líneas con splitlines(), eliminando líneas vacías.
-Valida que todas las filas tengan la misma longitud; si no, lanza un error.
-Asigna el resultado a self.layout y lo devuelve.
Resultado:
El nivel queda representado internamente como una lista de cadenas, donde cada carácter define un tipo de bloque o una celda vacía.

2.preparar_entidades:
Esta función inicializa los elementos principales del juego antes de comenzar la partida.
Función:
-Crea la paleta usando self.crear_rect() con las dimensiones definidas en la configuración.
-Centra la paleta en la parte inferior de la pantalla usando midbottom.
-Reinicia las variables de estado del juego: self.score, self.livesy `yo mismoself.end_message.
-Llama a self.reiniciar_bola() para colocar la bola justo encima de la paleta con su velocidad inicial.
Resultado:
El juego queda en estado inicial: paleta centrada, bola preparada para salir y contador de puntos y vidas reiniciado.

3.crear_bloques:
Esta función analiza la cuadrícula cargada previamente y genera los bloques que se renderizarán en pantalla.
Función:
-Limpia las listas self.blocks, self.block_colorsy `self.b_self.block_symbols.
-Recorre cada fila y columna de self.layout.
-Ignora el carácter . y valida que no existan símbolos no reconocidos.
-Para cada símbolo de bloque (#, @, %):--Calcula su posición en pantalla mediante self.calcular_posicion_bloque().
--Añade el rectángulo resultante a self.blocks.
--Añade su color correspondiente a self.block_colors.
--Registra el símbolo en self.block_symbols para gestionar la puntuación.
Resultado:
Los bloques quedan generados y listos para ser dibujados y colisionados durante el juego.

4.procesar_input:
Esta función gestiona la entrada del usuario para controlar el movimiento de la paleta.
Función:
-Obtiene el estado del teclado mediante self.obtener_estado_teclas().
-Detecta la pulsación de las teclas de movimiento:
--Izquierda: KEY_LEFT o KEY_A.
--Derecha: KEY_RIGHT o KEY_D.
-Actualiza la posición horizontal de la paleta utilizando self.PADDLE_SPEED.
-Aplica límites para evitar que la paleta pueda salir de la pantalla.
Resultado:
La paleta se mueve a la izquierda o a la derecha solo cuando el usuario mantiene pulsadas las teclas correspondientes, y nunca puede salirse de los límites de la pantalla.