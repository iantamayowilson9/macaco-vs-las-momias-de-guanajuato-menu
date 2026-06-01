import pygame
import sys
import random
import os
import math

from src.world_gen import GeneradorMapas
from src.jugador import Macaco, Espada
from src.enemigos import Momia, Zombie, Alien


# ==========================================
# 🛠️ CONFIGURACIÓN E INICIALIZACIÓN INICIAL
# ==========================================
pygame.init()
try:
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
except pygame.error:
    print("⚠️ Advertencia: No se pudo inicializar el audio.")

pygame.mixer.init()

# RESOLUCIÓN HD GLOBAL
ANCHO, ALTO = 1280, 720
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Macaco vs. Las Momias de Guanajuato")
reloj = pygame.time.Clock()


# --- ESTADOS DEL JUEGO ---
estado_juego = "INTRO" 


ruta_base = os.path.dirname(os.path.abspath(__file__))


# ==========================================
# 🎵 SISTEMA DE AUDIO GLOBAL
# ==========================================
ruta_musica_intro = os.path.join(ruta_base, "assets", "intro_music.mp3")
ruta_musica_menu = os.path.join(ruta_base, "assets", "menu_music.mp3") 

def cambiar_musica(ruta_archivo):
    """Maneja el cambio de pistas en streaming de forma segura"""
    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(ruta_archivo)
        pygame.mixer.music.play(-1)
    except pygame.error as e:
        print(f"⚠️ Alerta de audio: No se pudo reproducir {os.path.basename(ruta_archivo)}: {e}")

# Iniciar audio de la intro
cambiar_musica(ruta_musica_intro)


# ==========================================
# 🎬 SISTEMA DE INTRO / VIDEO (PIXEL ART)
# ==========================================
intro_frames = []
frame_actual = 0
frame_timer = 0
FPS_INTRO = 4 

ruta_intro = os.path.join(ruta_base, "assets", "intro")
assets_cargados = False

if os.path.exists(ruta_intro):
    archivos = os.listdir(ruta_intro)
    imagenes_intro = [f for f in archivos if f.lower().endswith('.png') and f.startswith('frame_')]
    imagenes_intro.sort() 
    TOTAL_FRAMES = len(imagenes_intro)
    
    if TOTAL_FRAMES > 0:
        try:
            for nombre_archivo in imagenes_intro:
                ruta_completa_imagen = os.path.join(ruta_intro, nombre_archivo)
                img = pygame.image.load(ruta_completa_imagen).convert_alpha()
                img_escalada = pygame.transform.scale(img, (ANCHO, ALTO)) 
                intro_frames.append(img_escalada)
            assets_cargados = True
            print(f"🎉 ¡Éxito! Se cargaron {TOTAL_FRAMES} frames de la intro en HD.")
        except pygame.error as e:
            print(f"❌ Error al procesar archivos de intro: {e}")
            assets_cargados = False

if not assets_cargados:
    TOTAL_FRAMES = 215 


# ==========================================
# 🎛️ CONFIGURACIÓN DEL MENÚ (OPCIÓN 2: MOSAICO EN MOVIMIENTO)
# ==========================================
opciones_menu = ["Jugar", "Controles", "Salir"]
opcion_seleccionada = 0

splash_texts = [
    "¡Puro Sonidero!",
    "¡Puto el que lo lea!",
    "¡Sublime!",
    "¡Chango Loco!",
    "¡Pura Violencia Sonidera!",
    "¡Guanajuato Se Controla!"
]
splash_text_elegido = random.choice(splash_texts)

COL_WHITE = (255, 255, 255)
COL_YELLOW = (255, 255, 0) 

ruta_assets_menu = os.path.join(ruta_base, "assets", "menu")

# --- CARGA INDEPENDIENTE DE IMÁGENES ---
try:
    # En la parte de carga de assets de tu main.py:
    menu_frame = pygame.image.load(os.path.join(ruta_assets_menu, "menu_frame.png")).convert_alpha()



    # 1. Cargar y Redimensionar LOGO (Ancho ideal 560px)
    logo_raw = pygame.image.load(os.path.join(ruta_assets_menu, "menu_logo.png")).convert_alpha()
    proporcion_logo = logo_raw.get_height() / logo_raw.get_width()
    ANCHO_LOGO_IDEAL = 560
    ALTO_LOGO_IDEAL = int(ANCHO_LOGO_IDEAL * proporcion_logo)
    menu_logo_image = pygame.transform.smoothscale(logo_raw, (ANCHO_LOGO_IDEAL, ALTO_LOGO_IDEAL))
    
    # 2. Cargar Fondo de Tierra de Minecraft
    menu_bg_earth = pygame.image.load(os.path.join(ruta_assets_menu, "menu_bg_earth.png")).convert_alpha()
    
    # 3. Cargar y Redimensionar BOTONES para 720p (460x48)
    ANCHO_BTN_IDEAL, ALTO_BTN_IDEAL = 460, 48
    btn_raw = pygame.image.load(os.path.join(ruta_assets_menu, "menu_button_texture.png")).convert_alpha()
    btn_hover_raw = pygame.image.load(os.path.join(ruta_assets_menu, "menu_button_hover.png")).convert_alpha()
    
    button_texture = pygame.transform.smoothscale(btn_raw, (ANCHO_BTN_IDEAL, ALTO_BTN_IDEAL))
    button_hover_texture = pygame.transform.smoothscale(btn_hover_raw, (ANCHO_BTN_IDEAL, ALTO_BTN_IDEAL))
    print("🎨 Gráficos del menú cargados y escalados con éxito.")
except Exception as e:
    print(f"⚠️ Error al procesar gráficos: {e}")
    menu_logo_image = None
    menu_bg_earth = None
    button_texture = None
    button_hover_texture = None

# 1. ACTUALIZA LA CARGA DE LA FUENTE (Busca esta sección y reemplázala)
archivo_fuente = "Earthbound.otf"  # Nombre cambiado a .otf
ruta_completa_fuente = os.path.join(ruta_assets_menu, archivo_fuente)

if os.path.exists(ruta_completa_fuente):
    try:
        pixel_font = pygame.font.Font(ruta_completa_fuente, 20)      # Botones
        splash_font = pygame.font.Font(ruta_completa_fuente, 24)     # Splash text
        hud_font = pygame.font.Font(ruta_completa_fuente, 28)        # HUD y Game Over
        print("🎉 ¡Fuente Earthbound.otf cargada globalmente!")
    except Exception as e:
        # Respaldo en caso de error
        pixel_font = pygame.font.SysFont("Arial", 22, bold=True)
        splash_font = pygame.font.SysFont("Arial", 26, bold=True)
        hud_font = pygame.font.SysFont("Arial", 28, bold=True)
else:
    pixel_font = pygame.font.SysFont("Arial", 22, bold=True)
    splash_font = pygame.font.SysFont("Arial", 26, bold=True)
    hud_font = pygame.font.SysFont("Arial", 28, bold=True)

def draw_moving_tiled_background(surface, tile_image):
    if not tile_image:
        surface.fill((20, 10, 30))
        return
        
    tile_w, tile_h = tile_image.get_size()
    
    # 1. Solo desplazamos en el eje X para el efecto "cámara lateral"
    # Dividir por 40 ajusta la velocidad: a menor número, más rápido se mueve.
    offset_x = (pygame.time.get_ticks() // 40) % tile_w
    offset_y = 0  # Desactivamos el movimiento vertical
    
    # 2. Dibujamos el mosaico desplazándose a la izquierda
    for y in range(0, ALTO, tile_h):
        for x in range(-tile_w, ANCHO + tile_w, tile_w):
            surface.blit(tile_image, (x - offset_x, y))

def draw_splash_text(surface, text, font, logo_x, logo_y, logo_w, logo_h):
    # 1. Configuraciones visuales
    color_splash = COL_YELLOW
    color_sombra = (0, 0, 0)
    
    # Efecto oscilante de tamaño
    scale_factor = 1.3 + 0.08 * math.sin(pygame.time.get_ticks() * 0.006)
    
    # 2. Renderizar texto
    splash_surface = font.render(text, True, color_splash)
    sombra_surface = font.render(text, True, color_sombra)
    
    # 3. Escalar
    w, h = splash_surface.get_size()
    nuevo_tam = (int(w * scale_factor), int(h * scale_factor))
    scaled_splash = pygame.transform.scale(splash_surface, nuevo_tam)
    scaled_sombra = pygame.transform.scale(sombra_surface, nuevo_tam)
    
    # 4. ROTACIÓN POSITIVA (Para que apunte hacia arriba)
    # Cambiamos a +15 grados para que la izquierda suba
    rotated_splash = pygame.transform.rotate(scaled_splash, 15)
    rotated_sombra = pygame.transform.rotate(scaled_sombra, 15)
    
    # 5. Posicionar cerca de la esquina derecha del logo
    # Ajustamos las coordenadas para que se vea más grande y separado
    pos_x = logo_x + logo_w - 180
    pos_y = logo_y + logo_h - 70
    
    # 6. Dibujar sombra (desplazada 2px a la derecha y abajo)
    surface.blit(rotated_sombra, (pos_x + 3, pos_y + 3))
    # Dibujar texto principal
    surface.blit(rotated_splash, (pos_x, pos_y))

def draw_text_with_outline(surface, text, font, pos, color_texto, color_borde, grosor=1):
    x, y = pos
    # Dibujamos el texto de fondo varias veces para crear el borde
    for dx in range(-grosor, grosor + 1):
        for dy in range(-grosor, grosor + 1):
            if dx != 0 or dy != 0:
                text_outline = font.render(text, True, color_borde)
                surface.blit(text_outline, (x + dx, y + dy))
    
    # Dibujamos el texto principal encima
    text_main = font.render(text, True, color_texto)
    surface.blit(text_main, (x, y))               


# ==========================================
# 🎮 CONFIGURACIÓN DE SPRITES (GAMEPLAY CORE)
# ==========================================
todos_los_sprites = pygame.sprite.Group()
grupo_enemigos = pygame.sprite.Group()
grupo_balas = pygame.sprite.Group()

macaco = Macaco(ANCHO // 2, ALTO // 2)
espada = Espada(macaco)
todos_los_sprites.add(macaco, espada)

oleada_actual = 1
tiempo_oleada = 0
timer_spawn = 0
enemigos_eliminados = 0
puntuacion = 0

def spawnear_enemigo_en_borde():
    borde = random.choice(["TOP", "BOTTOM", "LEFT", "RIGHT"])
    if borde == "TOP": x, y = random.randint(0, ANCHO), -30
    elif borde == "BOTTOM": x, y = random.randint(0, ANCHO), ALTO + 30
    elif borde == "LEFT": x, y = -30, random.randint(0, ALTO)
    else: x, y = ANCHO + 30, random.randint(0, ALTO)
        
    probabilidad = random.random()
    if oleada_actual == 1:
        nuevo_enemigo = Momia(x, y)
    elif oleada_actual == 2:
        nuevo_enemigo = Zombie(x, y) if probabilidad > 0.4 else Momia(x, y)
    else:
        if probabilidad < 0.4: nuevo_enemigo = Zombie(x, y)
        elif probabilidad < 0.7: nuevo_enemigo = Momia(x, y)
        else: nuevo_enemigo = Alien(x, y)
        
    todos_los_sprites.add(nuevo_enemigo)
    grupo_enemigos.add(nuevo_enemigo)

def reiniciar_juego():
    global oleada_actual, tiempo_oleada, timer_spawn, enemigos_eliminados, puntuacion
    oleada_actual = 1
    tiempo_oleada = 0
    timer_spawn = 0
    enemigos_eliminados = 0
    puntuacion = 0
    grupo_enemigos.empty()
    grupo_balas.empty()
    for sprite in list(todos_los_sprites):
        if sprite != macaco and sprite != espada:
            sprite.kill()
    macaco.vida = 3
    macaco.pos = pygame.math.Vector2(ANCHO // 2, ALTO // 2)


# ==========================================
# 🔄 BUCLE PRINCIPAL DEL JUEGO
# ==========================================
jugando = True

# Crear superficie de scanlines una sola vez
filtro_scanlines = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)

for y in range(0, ALTO, 4):
    pygame.draw.line(filtro_scanlines, (0, 0, 0, 40), (0, y), (ANCHO, y))

def aplicar_scanlines(surface):
    surface.blit(filtro_scanlines, (0, 0))

#------------ FILTRO SURFACE -----------------
# Crea una superficie del tamaño de tu pantalla para el filtro
#filtro_surface = pygame.Surface((ANCHO, ALTO))
# Este color será el que tiña tu juego (puedes probar con otros, ej: (20, 0, 50))
#color_filtro = (30, 10, 50)

while jugando:
    reloj.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jugando = False
            
        if event.type == pygame.KEYDOWN:
            if estado_juego == "INTRO":
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    cambiar_musica(ruta_musica_menu) 
                    estado_juego = "MENU"
                    
            elif estado_juego == "MENU":
                if event.key == pygame.K_DOWN:
                    opcion_seleccionada = (opcion_seleccionada + 1) % len(opciones_menu)
                elif event.key == pygame.K_UP:
                    opcion_seleccionada = (opcion_seleccionada - 1) % len(opciones_menu)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if opcion_seleccionada == 0:
                        pygame.mixer.music.stop() 
                        reiniciar_juego()
                        estado_juego = "GAMEPLAY"
                    elif opcion_seleccionada == 1:
                        pass 
                    elif opcion_seleccionada == 2:
                        jugando = False
                        
            elif estado_juego == "GAMEOVER":
                if event.key == pygame.K_RETURN:
                    cambiar_musica(ruta_musica_menu) 
                    estado_juego = "MENU"


    # ------ ESTADO: INTRO ------
    if estado_juego == "INTRO":
        pantalla.fill((0, 0, 0))
        if assets_cargados:
            pantalla.blit(intro_frames[frame_actual], (0, 0))
            frame_timer += 1
            if frame_timer >= FPS_INTRO:
                frame_timer = 0
                frame_actual += 1
                if frame_actual >= TOTAL_FRAMES:
                    cambiar_musica(ruta_musica_menu) 
                    estado_juego = "MENU"
        else:
            txt = hud_font.render(f"REPRODUCIENDO INTRO...", True, COL_WHITE)
            pantalla.blit(txt, (ANCHO // 2 - txt.get_width() // 2, ALTO // 2))
            frame_actual += 1
            if frame_actual >= TOTAL_FRAMES:
                cambiar_musica(ruta_musica_menu)
                estado_juego = "MENU"


    # ------ ESTADO: MENÚ PRINCIPAL (CON MOVIMIENTO INFINITO) ------
    elif estado_juego == "MENU":
        # 1. Dibujar fondo de tierra desplazable (Opción 2 automática)
        draw_moving_tiled_background(pantalla, menu_bg_earth)
        
        logo_y = 50
        if menu_logo_image:
            logo_x = ANCHO // 2 - menu_logo_image.get_width() // 2
            pantalla.blit(menu_logo_image, (logo_x, logo_y))
            
            draw_splash_text(pantalla, splash_text_elegido, splash_font, 
                             logo_x, logo_y, menu_logo_image.get_width(), menu_logo_image.get_height())
        
        # Botones centrados
        btn_start_y = 420
        btn_gap = 8
        
        for i in range(len(opciones_menu)):
            if i == opcion_seleccionada:
                button_surface = button_hover_texture
                text_color = COL_YELLOW
            else:
                button_surface = button_texture
                text_color = COL_WHITE
            
            if button_surface:
                btn_w, btn_h = button_surface.get_size()
                btn_x = ANCHO // 2 - btn_w // 2
                btn_y = btn_start_y + (i * (btn_h + btn_gap))
                pantalla.blit(button_surface, (btn_x, btn_y))
                
                txt_opcion = pixel_font.render(opciones_menu[i], True, text_color)
            

                #Calcular centro de booton
                text_x = btn_x + btn_w // 2 - txt_opcion.get_width() // 2
                text_y = btn_y + btn_h // 2 - txt_opcion.get_height() // 2 - 3

                # 3. Llamamos a la función de borde (usando tus variables calculadas)
                draw_text_with_outline(
                    pantalla, 
                    opciones_menu[i], 
                    pixel_font, 
                    (text_x, text_y), 
                    text_color,   # El color que cambia al hacer hover
                    (0, 0, 0),    # Negro para el borde
                    grosor=2      # Grosor del borde
                )

        txt_copy = pixel_font.render("© 2026 Macaco Games", True, (140, 140, 140))
        pantalla.blit(txt_copy, (ANCHO // 2 - txt_copy.get_width() // 2, ALTO - 45))

        #Filtro de scan
        aplicar_scanlines(pantalla) # <--- AQUÍ LO PONES
        # Dibujar el marco encima de todo
        pantalla.blit(menu_frame, (0, 0))


        # ESTE ES EL MODO DE FILTRO SURFACE
        # Aplicar el filtro de fusión
        # BLEND_RGB_MULT multiplica los colores (oscurece y tiñe)
        # BLEND_RGB_ADD suma los colores (ilumina, efecto neón)
        #filtro_surface.fill(color_filtro)
        #pantalla.blit(filtro_surface, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
        
        # 4. Flip (esto sigue igual)
        pygame.display.flip()


    # ------ ESTADO: GAMEPLAY (1280x720) ------ (esta vacio)
    elif estado_juego == "GAMEPLAY":
        # 1. Limpiar pantalla
        pantalla.fill((0, 0, 0))
        
        # 2. Dibujar un mensaje temporal para confirmar que entramos al modo juego
        mensaje = hud_font.render("MODO JUEGO - EN DESARROLLO", True, (255, 255, 255))
        pantalla.blit(mensaje, (ANCHO // 2 - mensaje.get_width() // 2, ALTO // 2))
        
        # 3. Opción para regresar al menú (presionando ESC)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            cambiar_musica(ruta_musica_menu)
            estado_juego = "MENU"


    # ------ ESTADO: GAME OVER ------
    elif estado_juego == "GAMEOVER":
        pantalla.fill((90, 5, 15))
        txt_go = hud_font.render("GAME OVER - LAS MOMIAS DOMINARON LA PISTA", True, COL_WHITE)
        txt_restart = hud_font.render("Presiona ENTER para regresar al menú principal", True, COL_YELLOW)
        pantalla.blit(txt_go, (ANCHO // 2 - txt_go.get_width() // 2, ALTO // 2 - 40))
        pantalla.blit(txt_restart, (ANCHO // 2 - txt_restart.get_width() // 2, ALTO // 2 + 20))

    pygame.display.flip()

pygame.quit()
sys.exit()