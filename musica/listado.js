const files = [
    "intro.mp3",
    "bingchilling_beat.wav",
    "bingchilling.wav",
    "pena_artistica_beat.wav",
    "pena_artistica_1.wav",
    "pena_artistica_2.wav",
    "pena_artistica_final.wav",
    "been_tealing_p1.wav",
    "been_tealing_p2.wav",
    "been_tealing_beat.wav",
    "been_tealing_final.mp3",
    "yo_tu_mama_cuando.wav",
    "carti_type_beat.mp3",
    "carti_type_beat_sin_carti.mp3",
    "mejorbeatdelahistoria.mp3",
    "peo.mp3",
    "me_costo_demasiado_hacer_este_beat.mp3",
    "me_costo_demasiado_hacer_este_beat_(ft.santos).mp3",
    "este_me_costo_menos.mp3",
    "freddy_mi_amigo_(CLEAN).mp3",
    "freddy_mi_amigo.mp3",
    "santos_traidor.mp3",
    "bagatela1.wav",
    "bagatela2.wav",
    "bagatela3.wav",
    "bagatela4.mp3"
];
console.log(files.join(", "))

document.addEventListener("DOMContentLoaded", function(event) {
    for (var i = 0; i < files.length; i++){
        document.getElementById("audios").innerHTML += "<br><audio controls><source src=musica/"+files[i]+" type=\"audio/"+files[i].slice(-3,files[i].length)+"\"></audio> "+files[i].slice(0,-4)+"<hr>"
    }
});
