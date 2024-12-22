
document.addEventListener("DOMContentLoaded", function() {
    const weatherContainer = document.getElementById("weather-info-container");

    if (weatherContainer) {
        // Vérifie si les données météo sont disponibles et ajoute la classe pour animer
        if (weatherContainer.classList.contains("weather-block-horizontal")) {
            // Si le bloc est déjà dans le DOM, lance l'animation après un petit délai
            setTimeout(() => {
                weatherContainer.classList.add("show-weather");
            }, 100);  // Délai pour laisser le temps au navigateur de re-render
        }
    }
});
  