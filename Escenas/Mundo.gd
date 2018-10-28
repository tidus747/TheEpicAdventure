extends Node
export (PackedScene) var Enemigo
var Score = 0
var signox
var signoy

func _ready():
	randomize()
	
func nuevo_juego():
	Score = 0
	$Player.inicio($PosicionDeInicio.position) #Posicion de inicio del jugador
	$InicioTimer.start()
	$Interfaz.mostrar_mensaje("Listo!")
	$Interfaz.update_score(Score)

func game_over():
	$ScoreTimer.stop()
	$EnemigoTimer.stop()
	$Interfaz.game_over()


func _on_InicioTimer_timeout():
	$EnemigoTimer.start()
	$ScoreTimer.start()


func _on_ScoreTimer_timeout():
	Score += 1
	$Interfaz.update_score(Score)
	

func _on_EnemigoTimer_timeout():
	# Seleccionamos un punto en el camino
	$Camino/enemigo_posicion.set_offset(randi())
	
	var E = Enemigo.instance()
	add_child(E)
	
	# Seleccionar una direccion
	var d = $Camino/enemigo_posicion.rotation + PI/2
	
	E.position = $Camino/enemigo_posicion.position
	
	#d += rand_range(-PI/4, PI/4) 
	#E.rotation = d
	
	if $Player.position.x >= E.position.x:
		signox = 1
	else:
		signox = -1
	
	if $Player.position.y >= E.position.y:
		signoy = 1
	else:
		signoy = -1
			
	E._dir_movimiento(signox)
	E.set_linear_velocity(Vector2(signox*rand_range(E.velocidad_min, E.velocidad_max),signoy*rand_range(E.velocidad_min, E.velocidad_max)/rand_range(2,4)).rotated(0))
