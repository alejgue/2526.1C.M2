"""Plantilla del juego Arkanoid para el hito M2.

Completa los métodos marcados con TODO respetando las anotaciones de tipo y la
estructura de la clase. El objetivo es construir un prototipo jugable usando
pygame que cargue bloques desde un fichero de nivel basado en caracteres.
"""
from arkanoid_core import *
# --------------------------------------------------------------------- #
# Métodos a completar por el alumnado
# --------------------------------------------------------------------- #

#@arkanoid_method
def cargar_nivel(self) -> list[str]:    #YOOOOOYOOOOO
    """Lee el fichero de nivel y devuelve la cuadrícula como lista de filas."""
    ruta_fichero_nivel = self.level_path

    if not ruta_fichero_nivel.is_file():
        mensaje = f"No se encuentra el archivo: {ruta_fichero_nivel}"
        print(mensaje)         # - Comprueba que `self.level_path` existe y es fichero.
    with ruta_fichero_nivel.open("r", encoding="utf-8") as f:
       texto_entero = f.read()   #Lee todo el contenido del archivo como una sola cadena y luego la divide
       lineas = [linea.strip() for linea in texto_entero.splitlines() if linea.strip()]    #Obtiene las lineas sin espacios y separados por l
       longitudes = [len(linea) for linea in lineas]    # Comprueba el ancho de las lineas
       if len(set(longitudes)) > 1:   
           raise ValueError("Las filas del nivel no tienen el mismo ancho")  
    # - Lee su contenido, filtra líneas vacías y valida que todas tienen el mismo ancho.
    self.layout = lineas
    return self.layout
    # - Guarda el resultado en `self.layout` y devuélvelo.
   

@arkanoid_method
def preparar_entidades(self) -> None:
    """Posiciona paleta y bola, y reinicia puntuación y vidas."""
    # - Ajusta el tamaño de `self.paddle` y céntrala usando `midbottom`.
    # - Reinicia `self.score`, `self.lives` y `self.end_message`.
    # - Llama a `self.reiniciar_bola()` para colocar la bola sobre la paleta.
    raise NotImplementedError

@arkanoid_method
def crear_bloques(self) -> None:    #YOOOOOYOOOOO
    """Genera los rectángulos de los bloques en base a la cuadrícula."""
    # - Limpia `self.blocks`, `self.block_colors` y `self.block_symbols`.
    self.blocks.clear()
    self.block_colors.clear()
    self.block_symbols.clear()
    # - Recorre `self.layout` para detectar símbolos de bloque.
    bloque_simbolos = self.BLOCK_COLORS.keys()   # Definimos el conjunto de símbolos que representan un bloque (claves del diccionario de colores)
    caracteres_validos = bloque_simbolos | {"."}
    for fila, conjunto_caracter in enumerate(self.layout, start=1):
        for columna, caracter in enumerate(conjunto_caracter, start=1): 
            if caracter not in caracteres_validos:
                raise ValueError(f"Carácter '{caracter}' no definido en el archivo de nivel.")
            
            if caracter == ".":
                continue
            
            if caracter in bloque_simbolos:
                rectangulo = self.calcular_posicion_bloque(fila, columna)  
                self.blocks.append(rectangulo) 
                self.block_colors.append(self.BLOCK_COLORS[caracter])
                self.block_symbols.append(caracter)
    # - Usa `self.calcular_posicion_bloque` y rellena las listas paralelas.
    

@arkanoid_method
def procesar_input(self) -> None:
    """Gestiona la entrada de teclado para mover la paleta."""
    # - Obtén el estado de teclas con `self.obtener_estado_teclas()`.
    # - Desplaza la paleta con `self.PADDLE_SPEED` si se pulsan las teclas izquierda/derecha.
    # - Limita la posición para que no salga de la pantalla.
    raise NotImplementedError

@arkanoid_method
def actualizar_bola(self) -> None:
    """Actualiza la posición de la bola y gestiona colisiones."""
    # - Mueve la bola según su velocidad.
    self.ball_pos += self.ball_velocity
    ball_rect = self.obtener_rect_bola()

    # - Comprueba colisiones con paredes, paleta y bloques.
    if ball_rect.left <= 0 or ball_rect.right >= self.SCREEN_WIDTH:
        self.ball_velocity.x *= -1

    if ball_rect.top <= 0:
        self.ball_velocity.y *= -1

    if ball_rect.top >= self.SCREEN_HEIGHT:
        self.lives -= 1
        self.reiniciar_bola()
        return

    if ball_rect.colliderect(self.paddle):
        self.ball_velocity.y = -abs(self.ball_velocity.y)

    nuevos_bloques = []
    nuevos_colores = []
    nuevos_simbolos = []

    for rect, color, symbol in zip(self.blocks, self.block_colors, self.block_symbols):
        if ball_rect.colliderect(rect):
            self.ball_velocity.y *= -1
            self.score += self.BLOCK_POINTS[symbol]
        else:
            nuevos_bloques.append(rect)
            nuevos_colores.append(color)
            nuevos_simbolos.append(symbol)

    # - Actualiza velocidad, puntuación y vidas según corresponda.
    self.blocks = nuevos_bloques
    self.block_colors = nuevos_colores
    self.block_symbols = nuevos_simbolos

@arkanoid_method
def dibujar_escena(self) -> None:
    """Renderiza fondo, bloques, paleta, bola y HUD."""
    # - Rellena el fondo y dibuja cada bloque con `self.dibujar_rectangulo`.
    # - Pinta la paleta y la bola con las utilidades proporcionadas.
    # - Muestra puntuación, vidas y mensajes usando `self.dibujar_texto`.
    raise NotImplementedError

@arkanoid_method
def run(self) -> None:
    """Ejecuta el bucle principal del juego."""
    # - Inicializa recursos (`self.inicializar_pygame`, `self.cargar_nivel`, etc.).
    # - Procesa eventos de `self.iterar_eventos()` y llama a los métodos de actualización/dibujo.
    # - Refresca la pantalla con `self.actualizar_pantalla()` y cierra con `self.finalizar_pygame()`.
    raise NotImplementedError


def main() -> None:
    """Permite ejecutar el juego desde la línea de comandos."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Plantilla del hito M2: Arkanoid con pygame.",
    )
    parser.add_argument(
        "level",
        type=str,
        help="Ruta al fichero de nivel (texto con # para bloques y . para huecos).",
    )
    args = parser.parse_args()

    game = ArkanoidGame(args.level)
    game.run()
    


if __name__ == "__main__":
    main()
