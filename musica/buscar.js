function Buscar(){
	proyecto = document.getElementById('text').value + ".wav";
	if (proyecto == ".wav"){
		return prompt("Escribe algo");
	}
	window.location.href = proyecto;
}
