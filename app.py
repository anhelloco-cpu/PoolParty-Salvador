<header class="video-container">
    <video autoplay muted loop playsinline class="bg-video">
        <source src="invitacion_neon.mp4" type="video/mp4">
        Tu navegador no soporta videos.
    </video>
    
    <div class="overlay-content">
        <h1 class="neon-text">THE DROP: 15</h1>
        <p>¡Prepárate para la mejor Pool Party!</p>
    </div>
</header>

<style>
.video-container {
    position: relative;
    width: 100%;
    height: 100vh; /* Ocupa toda la pantalla */
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
}

.bg-video {
    position: absolute;
    top: 50%;
    left: 50%;
    min-width: 100%;
    min-height: 100%;
    width: auto;
    height: auto;
    z-index: -1;
    transform: translate(-50%, -50%);
    object-fit: cover; /* Mantiene la proporción sin estirar */
}

.overlay-content {
    text-align: center;
    color: white;
    z-index: 1;
    background: rgba(0, 0, 0, 0.3); /* Un toque oscuro para leer mejor si añades texto */
    padding: 20px;
    border-radius: 15px;
}

.neon-text {
    font-family: 'Orbitron', sans-serif; /* Tipografía futurista */
    text-shadow: 0 0 10px #ff00ff, 0 0 20px #00ffff;
    font-size: 3rem;
}
</style>