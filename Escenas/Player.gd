extends Area2D

# Variables globales para nuestro personaje
export(int) var velocidad # Con el comando insertado de esta forma pondremos directamente la variable sobre el inspector
var velocidad_correr
var velocidad_caminar
var movimiento = Vector2() # Esta variable sirve para darle movimiento al personaje 
var limite
signal golpe # Un signal funciona como un evento dentro del juego

func _ready():
	# Called when the node is added to the scene for the first time.
	# Initialization here
	hide()
	limite = get_viewport_rect().size # Guardamos el valor del tamaño en límite
	velocidad_correr = 2.5 * velocidad
	velocidad_caminar = velocidad

func _process(delta):
	movimiento = Vector2() # Reiniciamos la variable para que no incremente constantemente el movimiento
	if Input.is_action_pressed("ui_right"):
		movimiento.x += 1
	if Input.is_action_pressed("ui_left"):
		movimiento.x -= 1
	if Input.is_action_pressed("ui_up"):
		movimiento.y -= 1
	if Input.is_action_pressed("ui_down"):
		movimiento.y += 1
		
	# Modificamos la velocidad de movimiento
	if Input.is_action_pressed("ui_run"):
		velocidad = velocidad_correr
	else:
		velocidad = velocidad_caminar
		
	if movimiento.length() > 0 : # Verificamos si se está moviendo para normalizar la velocidad
		movimiento = movimiento.normalized() * velocidad
		
	position += movimiento * delta
	position.x = clamp(position.x, 0, limite.x)
	position.y = clamp(position.y, 0, limite.y)
	
	if movimiento.x != 0: # Si nos estamos moviendo en el eje X
		$Sprites_player.animation = "correr"
		$Sprites_player.flip_h = movimiento.x < 0
	elif movimiento.y == 0:
		$Sprites_player.animation = "idle"
		
		
	
		
		
func _on_Player_body_entered(body):
	hide()
	emit_signal("golpe")
	$collision_player.disabled = true # Desactivamos la colisión con el jugador cuando colisiona con algún objeto
	
func inicio(pos):
	position = pos
	show()
	$collision_player.disabled = false
