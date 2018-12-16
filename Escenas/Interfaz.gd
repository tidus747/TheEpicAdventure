extends CanvasLayer

signal iniciar_juego

func _ready():
	$Intro_song.play()	
	$ScoreLabel.hide()

func mostrar_mensaje(texto):
	$Mensaje.text = texto
	$Mensaje.show()
	$MensajeTimer.start()
	
func ocultar_fondo():
	$Fondo_interfaz.hide()
	
func mostrar_fondo():
	$Fondo_interfaz.show()
	
func game_over():
	$Game_song.stop()
	$Gameover.play()
	mostrar_mensaje("Game Over")
	yield($MensajeTimer, "timeout")
	$Gameover.stop()
	$Button_play.show()
	$Intro_song.play()
	$Mensaje.text = "The Epic Adventure"
	$Licencia.show()
	$Mensaje.show()
	
func update_score(Puntos):
	$ScoreLabel.text = str(Puntos)
	
func _on_MensajeTimer_timeout():
	$Mensaje.hide()
	$Licencia.hide()
	
func _on_Button_play_pressed():
	$Button_play.hide()
	$Fondo_interfaz.hide()
	$Intro_song.stop()
	$Game_song.play()
	emit_signal("iniciar_juego")
