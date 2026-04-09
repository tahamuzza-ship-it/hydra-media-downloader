async function getTranscript(videoId) {
  // Opción 1: Probar con yewtu.be (Invidious)
  try {
    const response = await fetch(`https://yewtu.be/api/v1/captions/${videoId}`);
    if (response.ok) {
      const data = await response.json();
      if (data.captions) {
        return data.captions;
      }
    }
  } catch (e) {
    console.log("yewtu.be falló:", e.message);
  }

  // Opción 2: Probar con pipedapi (alternativa)
  try {
    const response = await fetch(`https://pipedapi.kavin.rocks/transcripts/${videoId}`);
    if (response.ok) {
      const data = await response.json();
      if (data.transcripts && data.transcripts.length > 0) {
        return data.transcripts.map(t => t.text).join(' ');
      }
    }
  } catch (e) {
    console.log("pipedapi falló:", e.message);
  }

  // Opción 3: Probar con un proxy de YouTube
  try {
    const proxyUrl = `https://cors-anywhere.herokuapp.com/https://www.youtube.com/watch?v=${videoId}`;
    const response = await fetch(proxyUrl);
    // Esto es más complejo, requiere parsear HTML
  } catch (e) {
    console.log("proxy falló:", e.message);
  }

  throw new Error('No se pudo obtener la transcripción');
}
