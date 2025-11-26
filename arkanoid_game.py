"""Plantilla del juego Arkanoid para el hito M2.

Completa los métodos marcados con TODO respetando las anotaciones de tipo y la
estructura de la clase. El objetivo es construir un prototipo jugable usando
pygame que cargue bloques desde un fichero de nivel basado en caracteres.
"""
from arkanoid_core import ArkanoidGame, arkanoid_method, pygame, Vector2
import random as rnd
# --------------------------------------------------------------------- #
# Métodos a completar por el alumnado
# --------------------------------------------------------------------- #

@arkanoid_method
def cargar_nivel(self) -> list[str]:   
    """Lee el fichero de nivel y devuelve la cuadrícula como lista de filas."""
    # Comprueba que `self.level_path` existe y es fichero.
    ruta_fichero_nivel = self.level_path

    if not ruta_fichero_nivel.is_file():
        mensaje = f"No se encuentra el archivo: {ruta_fichero_nivel}"
        print(mensaje)  

    # Lee su contenido, filtra líneas vacías y valida que todas tienen el mismo ancho.
    with ruta_fichero_nivel.open("r", encoding="utf-8") as f:
       # Lee todo el contenido del archivo como una sola cadena
       texto_entero = f.read()   
       # Obtiene las lineas sin espacios y las separa
       lineas = [
           linea.strip() 
           for linea in texto_entero.splitlines() 
           if linea.strip()
       ]  
       # Comprueba el ancho de las lineas
       longitudes = [len(linea) for linea in lineas]  
       if len(set(longitudes)) > 1:   
           raise ValueError("Las filas del nivel no tienen el mismo ancho")  
    # Guarda el resultado en `self.layout` y devuélvelo.
    self.layout = lineas
    return self.layout
    
   

@arkanoid_method
def preparar_entidades(self, reiniciar_score: bool = False) -> None:
    """Posiciona paleta y bola, y reinicia puntuación y vidas."""
    # - Ajusta el tamaño de `self.paddle` y céntrala usando `midbottom`.
    self.paddle = self.crear_rect(0, 0, *self.PADDLE_SIZE)
    self.paddle.midbottom = (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT - self.PADDLE_OFFSET)
    
    # - Reinicia `self.score`, `self.lives` y `self.end_message`.
    if reiniciar_score:
        self.score = 0
    self.lives = 3  
    self.end_message = ""

    # - Llama a `self.reiniciar_bola()` para colocar la bola sobre la paleta.
    self.reiniciar_bola()

@arkanoid_method
def crear_bloques(self) -> None:
    """Genera los rectángulos de los bloques en base a la cuadrícula."""
    # Limpia `self.blocks`, `self.block_colors` y `self.block_symbols`.
    self.blocks.clear()
    self.block_colors.clear()
    self.block_symbols.clear()
    # Recorre `self.layout` para detectar símbolos de bloque.
    bloque_simbolos = self.BLOCK_COLORS.keys()  # Símbolos que representan bloques
    caracteres_validos = bloque_simbolos | {"."}
    for fila, conjunto_caracter in enumerate(self.layout, start=0):
        for columna, caracter in enumerate(conjunto_caracter, start=0): 
            if caracter not in caracteres_validos:
                raise ValueError(
                    f"Carácter '{caracter}' no definido "
                    "en el archivo de nivel."
                )
            
            if caracter == ".":
                continue

            # Usa `self.calcular_posicion_bloque` y rellena las listas paralelas.
            if caracter in bloque_simbolos:
                rectangulo = self.calcular_posicion_bloque(fila, columna)  
                self.blocks.append(rectangulo) 
                self.block_colors.append(self.BLOCK_COLORS[caracter])
                self.block_symbols.append(caracter)
    

@arkanoid_method
def procesar_input(self) -> None:
    """Gestiona la entrada de teclado para mover la paleta."""
    # - Obtén el estado de teclas con `self.obtener_estado_teclas()`.
    # - Desplaza la paleta con `self.PADDLE_SPEED` si se pulsan las teclas izquierda/derecha.
    # - Limita la posición para que no salga de la pantalla.
    movimiento=0
    velocidad=self.PADDLE_SPEED 
    teclas=self.obtener_estado_teclas()
    #Detectar la dirección del movminiento de la paleta
    if teclas[self.KEY_LEFT] or teclas[self.KEY_A]:
        movimiento= -velocidad
    elif teclas[self.KEY_RIGHT] or teclas[self.KEY_D]:
        movimiento= velocidad

    #Mover la paleta

    if movimiento!=0:
        self.paddle.x +=movimiento
        #Limitar movimiento de la paleta
        if self.paddle.x <0:
            self.paddle.x =0
        if self.paddle.x > self.SCREEN_WIDTH - self.paddle.width:
            self.paddle.x = self.SCREEN_WIDTH - self.paddle.width

@arkanoid_method
def actualizar_bola(self) -> None:
    """Actualiza la posición de la bola y gestiona colisiones."""
    # Mueve la bola según su velocidad.
    self.ball_pos += self.ball_velocity
    ball_rect = self.obtener_rect_bola()
    # Gestiona colisiones con paredes, paleta y bloques.
    
    if ball_rect.left <= 0:
        self.ball_velocity.x *= -1
        self.ball_pos.x = ball_rect.width / 2 + 1

    elif ball_rect.right >= self.SCREEN_WIDTH:
        self.ball_velocity.x *= -1
        self.ball_pos.x = self.SCREEN_WIDTH - ball_rect.width / 2 - 1

    if ball_rect.top <= 0:
        self.ball_velocity.y *= -1
        self.ball_pos.y = ball_rect.height / 2 + 1

    if ball_rect.top >= self.SCREEN_HEIGHT:
        self.lives -= 1
        self.reiniciar_bola()
        return

    if ball_rect.colliderect(self.paddle) and self.ball_velocity.y > 0:

        self.ball_pos.y = self.paddle.top - ball_rect.height / 2 - 1
        ball_rect = self.obtener_rect_bola()

        distancia_relativa = (ball_rect.centerx - self.paddle.centerx) / (self.paddle.width / 2)
        distancia_relativa = max(-1, min(1, distancia_relativa))

        MAX_ANGULO = 60
        angulo = distancia_relativa * MAX_ANGULO

        direccion = Vector2(0, -1).rotate(angulo)

        self.ball_velocity = direccion.normalize() * self.BALL_SPEED

    nuevos_bloques = []
    nuevos_colores = []
    nuevos_simbolos = []
    colision_bloque = False

    for rect, color, symbol in zip(self.blocks, self.block_colors, self.block_symbols):
        if not colision_bloque and ball_rect.colliderect(rect):
            self.ball_velocity.y *= -1
            self.score += self.BLOCK_POINTS[symbol]
            colision_bloque = True
        else:
            nuevos_bloques.append(rect)
            nuevos_colores.append(color)
            nuevos_simbolos.append(symbol)

    self.blocks = nuevos_bloques
    self.block_colors = nuevos_colores
    self.block_symbols = nuevos_simbolos
# Controla fin de nivel cuando no queden bloques y resta vidas si la bola cae.

    if self.lives <= 0:
        self.pantalla_fin("GAME OVER")

    if len(self.blocks) == 0:
        self.pantalla_fin("¡Pasaste el Nivel!")
@arkanoid_method
def dibujar_bloque_con_borde(self, rect: pygame.Rect, color: tuple[int, int, int]) -> None:
    """Dibuja un bloque con un borde negro simple."""
    
    GROSOR_BORDE = 3           # Define el grosor del borde en píxeles
    COLOR_BORDE = (0, 0, 0)  # Negro
    
    # 1. Dibujar el rectángulo exterior (el borde) con el color negro
    self.dibujar_rectangulo(rect, COLOR_BORDE)
    
    # 2. Crear el rectángulo interior (cuerpo)
    # .inflate() reduce el rectángulo en el doble del grosor del borde
    cuerpo_rect = rect.inflate(-GROSOR_BORDE * 2, -GROSOR_BORDE * 2)
    
    # 3. Dibujar el cuerpo interior con el color original del bloque
    self.dibujar_rectangulo(cuerpo_rect, color)

@arkanoid_method
def dibujar_escena(self) -> None:
    """Renderiza fondo, bloques, paleta, bola y HUD."""
    # Fondo
    if self.background_img and self.screen:
        # Dibuja la imagen en la posición (0, 0)
        self.screen.blit(self.background_img, (0, 0))
    else:
        # Fondo (fallback si la imagen falla)
        self.screen.fill(self.BACKGROUND_COLOR)

    # Bloques
    for rect, color in zip(self.blocks, self.block_colors):
        self.dibujar_bloque_con_borde(rect, color)

    # Paleta
    self.dibujar_rectangulo(self.paddle, self.PADDLE_COLOR)

    # Bola
    self.dibujar_circulo(self.ball_pos, self.BALL_RADIUS, self.BALL_COLOR)

    # HUD: puntuación y vidas
    self.dibujar_texto(f"Puntos: {self.score}", (10, 10))
    self.dibujar_texto(f"Vidas: {self.lives}", (10, 40))
    # Actualiza pantalla aquí para asegurarse de que se dibuje antes de la siguiente iteración
    self.actualizar_pantalla()

    if self.end_message:
        ancho = self.SCREEN_WIDTH // 2
        alto = self.SCREEN_HEIGHT // 2
        self.dibujar_texto(self.end_message, (ancho - 80, alto - 20), grande=True)
        self.game_over_sound = pygame.mixer.Sound("others/Game_over.mp3")
        self.game_over_sound.set_volume(100)
        pygame.mixer.music.stop()
        pygame.mixer.quit()

@arkanoid_method
def cargar_audio_y_fondo(self) -> None:
    try:
        # Extrae el número del nombre del archivo (ej: 'level_1.txt' -> 1)
        level_num_str = self.level_path.stem.split('_')[-1]
        level_num = int(level_num_str)
    except (ValueError, IndexError):
        level_num = 1 # Valor por defecto si el nombre no sigue el patrón
    
    music_file = None
    background_file = None
    
    if level_num in [1, 2]:
        music_file = "others/level_1-2.mp3"
        background_file = "others/background1-2.png"
    elif level_num in [3, 4]:
        music_file = "others/level_3-4.mp3"
        background_file = "others/background3-4.png"
    elif level_num >= 5:
        music_file = "others/level_5.mp3"
        background_file = "others/background5.png"
      
    self.background_img = None
    if background_file:
        try:
            # Carga la imagen
            img = pygame.image.load(background_file).convert() 
            
            # Redimensionar la imagen al tamaño de la pantalla
            self.background_img = pygame.transform.scale(
                img, 
                (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
            )
        except pygame.error as e:
            print(f"Advertencia: No se pudo cargar el fondo {background_file}. Error: {e}")
            # Si falla, self.background_img se mantiene en None y se usa BACKGROUND_COLOR.

    if music_file:
        try:
            # Detiene la música actual si está sonando
            pygame.mixer.music.stop() 
            
            # Carga la nueva canción
            pygame.mixer.music.load(music_file)
            
            # Establece volumen y reproduce en bucle
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(loops=-1)
        except pygame.error as e:
            print(f"Advertencia: No se pudo cargar la música {music_file}. Error: {e}")


@arkanoid_method
def pantalla_fin(self, mensaje: str) -> None:
    """Pantalla simple de fin: muestra mensaje, Retry y Next Level."""
    fuente = pygame.font.SysFont(None, 60)
    fuente_btn = pygame.font.SysFont(None, 40)
    #fuente_score = pygame.font.SysFont(None, 40)

    clock = pygame.time.Clock()

    game_over = (mensaje=="GAME OVER")

    # Crear los textos
    txt_mensaje = fuente.render(mensaje, True, (255, 255, 255))
    txt_next = fuente_btn.render("Next Level", True, (255, 255, 255))
    txt_retry = fuente_btn.render("Retry", True, (255, 255, 255))
    txt_quit = fuente_btn.render("Quit", True, (255, 255, 255))

    #txt_puntuacion = None
    #if not game_over:
    #    texto_score = f"PUNTUACIÓN: {self.score}"
    #    txt_puntuacion = fuente_score.render(texto_score, True, (255, 255, 255))

    # Rectángulos de botones
    ancho_btn = 240
    alto_btn = 50
    centro_x = self.SCREEN_WIDTH // 2
    
    next_rect = None 
    retry_rect = None 
    
    pos_central_arriba = self.SCREEN_HEIGHT // 2 - 35
    pos_central_abajo = self.SCREEN_HEIGHT // 2 + 35
    
    if game_over:
        retry_rect = pygame.Rect(centro_x - ancho_btn // 2, pos_central_arriba, ancho_btn, alto_btn)
        quit_rect = pygame.Rect(centro_x - ancho_btn // 2, pos_central_abajo, ancho_btn, alto_btn)
    else: 
        next_rect = pygame.Rect(centro_x - ancho_btn // 2, pos_central_arriba, ancho_btn, alto_btn)
        quit_rect = pygame.Rect(centro_x - ancho_btn // 2, pos_central_abajo, ancho_btn, alto_btn)



    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_rect and retry_rect.collidepoint(event.pos):
                    # Reiniciar el juego
                    reinicio_completo = (mensaje == "GAME OVER" or mensaje == "¡JUEGO TERMINADO! ¡Gracias por jugar!")

                    if mensaje == "¡JUEGO TERMINADO! ¡Gracias por jugar!":
                        self.level_path = self.level_path.with_name("level_1.txt")
                        self.cargar_nivel()

                    # Reiniciar este nivel    
                    self.preparar_entidades(reiniciar_score=reinicio_completo)
                    self.crear_bloques()
                    self.cargar_audio_y_fondo()
                    return
                
                if next_rect and next_rect.collidepoint(event.pos):
                    # Pasar al siguiente nivel directamente
                    actual = self.level_path
                    try:
                        n = int(actual.stem.split("_")[-1])
                        siguiente = actual.with_name(f"level_{n+1}.txt")
                        if siguiente.exists():
                            self.level_path = siguiente
                            self.cargar_nivel()
                            self.preparar_entidades()
                            self.crear_bloques()
                            self.cargar_audio_y_fondo()
                        else:
                            # Fin de todos los niveles
                            self.pantalla_fin("¡JUEGO TERMINADO! ¡Gracias por jugar!") 
                        return
                    except:
                        print("Nombre de nivel no soportado.")
                        return
                        
                if quit_rect.collidepoint(event.pos):
                    # Quita el juego
                    self.running = False
                    return

        # Fondo negro
        self.screen.fill((0, 0, 0))

        # Posición base para el mensaje principal (ej: "¡HAS GANADO!")
        pos_y_mensaje = self.SCREEN_HEIGHT // 3
        
        self.screen.blit(
            txt_mensaje,
            (centro_x - txt_mensaje.get_width()//2, pos_y_mensaje)
        )
        
        # Dibujar la puntuación solo si no es Game Over
        #if txt_puntuacion:
        #    self.screen.blit(
        #        txt_puntuacion,
        #        (centro_x - txt_puntuacion.get_width()//2, pos_y_mensaje + 60) 
        #    )
        
        # Botón Next level
        if next_rect:
            pygame.draw.rect(self.screen, (80, 80, 80), next_rect)
            next_text_x = next_rect.centerx - txt_next.get_width() // 2
            next_text_y = next_rect.centery - txt_next.get_height() // 2
            self.screen.blit(txt_next, (next_text_x, next_text_y))

        # Botón Retry
        if retry_rect:
            pygame.draw.rect(self.screen, (80, 80, 80), retry_rect)
            retry_text_x = retry_rect.centerx - txt_retry.get_width() // 2
            retry_text_y = retry_rect.centery - txt_retry.get_height() // 2
            self.screen.blit(txt_retry, (retry_text_x, retry_text_y))

        # Botón Quit
        pygame.draw.rect(self.screen, (80, 80, 80), quit_rect)
        quit_text_x = quit_rect.centerx - txt_quit.get_width() // 2
        quit_text_y = quit_rect.centery - txt_quit.get_height() // 2
        self.screen.blit(txt_quit, (quit_text_x, quit_text_y))

        pygame.display.flip()
        clock.tick(30)




@arkanoid_method
def run(self) -> None:
    """Ejecuta el bucle principal del juego."""
    # Inicializar pygame y cargar el nivel
    self.inicializar_pygame()
    self.cargar_nivel()
    self.preparar_entidades()
    self.crear_bloques()
    self.cargar_audio_y_fondo()
    self.running = True
    

    while self.running:
        # Procesar eventos
        for event in self.iterar_eventos():
            if event.type == self.EVENT_QUIT:
                self.running = False
            elif event.type == self.EVENT_KEYDOWN and event.key == self.KEY_ESCAPE:
                self.running = False
        

        # Entrada del jugador
        self.procesar_input()

        # Actualización de la bola y colisiones
        self.actualizar_bola()

        # Dibujar escena completa
        self.dibujar_escena()

        # Actualizar pantalla
        self.actualizar_pantalla()

        # Limitar FPS
        self.clock.tick(self.FPS)

    # Salida del juego
    self.finalizar_pygame()

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
