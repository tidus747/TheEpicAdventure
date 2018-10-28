extends RigidBody2D

export (int) var velocidad_min
export (int) var velocidad_max
var tipo_enemigo = ["zombie_normal","zombie_grande"]
var animacion

func _ready():
	animacion = randi()%tipo_enemigo.size()
	$AnimatedSprite.animation = tipo_enemigo[animacion]
	
	
func _on_VisibilityNotifier2D_screen_exited():
	pass # replace with function body
	
func _dir_movimiento(dir):
	$AnimatedSprite.flip_h = dir < 0
