import pygame
import sys
import random
import time

# Inicializa Pygame
pygame.init()
pygame.mixer.init()  # Inicializa el módulo de sonido

# Configuración de pantalla
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Juego de Cumpleaños")

# Carga el fondo del juego
background = pygame.image.load("C:\mery\imagenes\fondo.jpg")
background = pygame.transform.scale(background, (800, 600))

# Carga los gráficos (personaje, corazón, la imagen especial y la bandera argentina)
character = pygame.image.load("C:\mery\imagenes\character.gif")
heart = pygame.image.load("C:\mery\imagenes\heart.png")
special_image = pygame.image.load("C:\mery\imagenes\imagen_especial.jpg")
argentina_flag = pygame.image.load("C:\mery\imagenes\argentina_flag.png")

# Carga los archivos de sonido
heart_sound = pygame.mixer.Sound("colision.mp3")
flag_sound = pygame.mixer.Sound("fallo.mp3")

# Cargar música de fondo (asegúrate de que el archivo de música esté en la misma ubicación que tu script)
background_music = "september.mp3"
victory_music = "si_te_vas.mp3"

pygame.mixer.music.load(background_music)

# Establece el volumen de la música de fondo
pygame.mixer.music.set_volume(0.2)

# Escala las imágenes a un tamaño adecuado
character = pygame.transform.scale(character, (100, 100))
heart = pygame.transform.scale(heart, (60, 60))
special_image = pygame.transform.scale(special_image, (800, 600))
argentina_flag = pygame.transform.scale(argentina_flag, (60, 60))

# Variables de posición del personaje
character_x = 400
character_y = 500

# Variables de posición de los corazones
hearts = []
for _ in range(10):
    heart_x = random.randint(50, 750)
    heart_y = random.randint(50, 550)
    hearts.append((heart_x, heart_y))

# Variables de posición de las banderas argentinas
num_argentina_flags = 5
argentina_flags = [(random.randint(50, 750), random.randint(50, 550)) for _ in range(num_argentina_flags)]

# Variables de movimiento
character_speed = 8
heart_speed = 2

# Variables para controlar el juego
score = 0
font = pygame.font.Font(None, 36)
show_special_image = False
victory = False

# Función para verificar la colisión
def check_collision(character_x, character_y, obj_x, obj_y, obj_width, obj_height):
    if (character_x + 100 > obj_x and character_x < obj_x + obj_width) and (character_y + 100 > obj_y and character_y < obj_y + obj_height):
        return True
    return False

# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

# Lógica de movimiento del personaje
    if not victory:  # Verifica si no se ha alcanzado la victoria
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and character_x > 0:
            character_x -= character_speed
        if keys[pygame.K_RIGHT] and character_x < 800 - 100:
            character_x += character_speed
        if keys[pygame.K_UP] and character_y > 0:
            character_y -= character_speed
        if keys[pygame.K_DOWN] and character_y < 600 - 100:
            character_y += character_speed

    # Mueve los corazones en direcciones aleatorias
    for i in range(len(hearts)):
        direction = random.choice(["up", "down", "left", "right"])
        x, y = hearts[i]
        if direction == "up" and y > 0:
            y -= heart_speed
        elif direction == "down" and y < 600 - 60:
            y += heart_speed
        elif direction == "left" and x > 0:
            x -= heart_speed
        elif direction == "right" and x < 800 - 60:
            x += heart_speed
        hearts[i] = (x, y)

    # Mueve las banderas argentinas en direcciones aleatorias
    for i in range(len(argentina_flags)):
        direction = random.choice(["up", "down", "left", "right"])
        x, y = argentina_flags[i]
        if direction == "up" and y > 0:
            y -= heart_speed
        elif direction == "down" and y < 600 - 60:
            y += heart_speed
        elif direction == "left" and x > 0:
            x -= heart_speed
        elif direction == "right" and x < 800 - 60:
            x += heart_speed
        argentina_flags[i] = (x, y)

    # Verifica la colisión entre el personaje y los corazones
    for i in range(len(hearts)):
        heart_x, heart_y = hearts[i]
        if check_collision(character_x, character_y, heart_x, heart_y, 60, 60):
            # Incrementa la puntuación en 10 puntos
            score += 10

            # Reproduce el sonido del corazón
            heart_sound.play()

            # Mueve el corazón a una nueva posición aleatoria
            hearts[i] = (random.randint(50, 750), random.randint(50, 550))

    # Verifica la colisión entre el personaje y las banderas argentinas
    for i in range(len(argentina_flags)):
        argentina_flag_x, argentina_flag_y = argentina_flags[i]
        if check_collision(character_x, character_y, argentina_flag_x, argentina_flag_y, 60, 60):
            # Resta 20 puntos a la puntuación
            score -= 20

            # Reproduce el sonido de la bandera argentina
            flag_sound.play()

            # Mueve la bandera argentina a una nueva posición aleatoria
            argentina_flags[i] = (random.randint(50, 750), random.randint(50, 550))

    # Verifica si la puntuación alcanza 1000 para mostrar la imagen especial y ganar
    if score >= 1000 and not victory:
        show_special_image = True
        victory = True
        pygame.mixer.music.stop()  # Detiene la música de fondo actual
        pygame.mixer.music.load(victory_music)  # Carga la música de victoria
        pygame.mixer.music.play()  # Reproduce la música de victoria

    # Dibuja el fondo
    screen.blit(background, (0, 0))

    if show_special_image:
        # Muestra la imagen especial en toda la pantalla
        screen.blit(special_image, (0, 0))
    else:
        # Dibuja el personaje, los corazones y las banderas argentinas
        screen.blit(character, (character_x, character_y))
        for heart_x, heart_y in hearts:
            screen.blit(heart, (heart_x, heart_y))
        for argentina_flag_x, argentina_flag_y in argentina_flags:
            screen.blit(argentina_flag, (argentina_flag_x, argentina_flag_y))

        # Muestra la puntuación en la pantalla
        text = font.render("Puntuación: " + str(score), True, (255, 255, 255))
        screen.blit(text, (10, 10))

    pygame.display.update()