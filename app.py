import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Bingo",
    page_icon="🎱",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container {padding: 0.5rem 1rem 0rem 1rem; max-width: 100%;}
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    div[data-testid="stAppViewContainer"] {padding: 0;}
    iframe {display: block;}
    </style>
    """,
    unsafe_allow_html=True,
)

BINGO_HTML = """
<!DOCTYPE html>
<html>
<head>
<style>
  html, body {
    margin: 0;
    padding: 0;
    background: transparent;
    height: 100%;
  }

  #bingo-wrap {
    font-family: 'Segoe UI', Arial, sans-serif;
    background: radial-gradient(circle at top, #1e2a52, #0a0f24);
    color: white;
    padding: 30px 40px;
    border-radius: 20px;
    text-align: center;
    width: 100%;
    max-width: 100%;
    height: 100%;
    margin: auto;
    box-sizing: border-box;
    transition: all 0.3s ease;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  #bingo-wrap.fs-active {
    max-width: 100vw;
    width: 100vw;
    height: 100vh;
    border-radius: 0;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  .columns {
    display: flex;
    justify-content: center;
    align-items: stretch;
    gap: 26px;
    margin: 16px 0;
  }

  .fs-active .columns { gap: 2vw; margin: 2vh 0; }

  .col {
    flex: 1;
    max-width: 240px;
    padding: 36px 12px;
    border-radius: 20px;
    background: rgba(255,255,255,0.05);
    border: 2px solid rgba(255,255,255,0.1);
    display: flex;
    align-items: center;
    justify-content: center;
    transition: box-shadow 0.2s ease, background 0.2s ease;
  }

  .fs-active .col { max-width: 17vw; padding: 3vh 1vw; }

  @keyframes flash {
    0%   { box-shadow: 0 0 0 rgba(255,255,255,0); background: rgba(255,255,255,0.05); }
    35%  { box-shadow: 0 0 40px rgba(255,255,255,0.55); background: rgba(255,255,255,0.18); }
    100% { box-shadow: 0 0 0 rgba(255,255,255,0); background: rgba(255,255,255,0.05); }
  }

  .col.flash { animation: flash 1s ease-out; }

  .col .letter {
    font-size: 6.5em;
    font-weight: bold;
    line-height: 1;
  }

  .fs-active .col .letter { font-size: 7.5vw; }

  .colB .letter { color: #ff5f6d; }
  .colI .letter { color: #ffc371; }
  .colN .letter { color: #47cf73; }
  .colG .letter { color: #36a2eb; }
  .colO .letter { color: #d264ff; }

  #current-area {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 150px;
    margin: 12px 0;
  }

  .fs-active #current-area { height: 16vh; margin: 1.5vh 0; }

  #current {
    font-size: 7em;
    font-weight: bold;
    color: white;
    letter-spacing: 4px;
    text-shadow: 0 0 30px rgba(255,255,255,0.6);
  }

  .fs-active #current { font-size: 9vw; }

  @keyframes pop {
    0% { transform: scale(0.3); opacity: 0; }
    60% { transform: scale(1.2); opacity: 1; }
    100% { transform: scale(1); }
  }

  #current.pop { animation: pop 0.4s ease-out; }

  .called-num {
    display: inline-block;
    margin: 3px;
    padding: 8px 14px;
    border-radius: 8px;
    font-size: 1.05em;
    background: rgba(255,255,255,0.08);
  }

  .fs-active .called-num { font-size: 1.3vw; padding: 0.6vh 1vw; }

  #history {
    max-height: 110px;
    overflow-y: auto;
    margin-top: 14px;
    padding: 10px;
    background: rgba(0,0,0,0.2);
    border-radius: 10px;
  }

  .fs-active #history { max-height: 12vh; }

  .btns {
    margin-top: 16px;
    margin-bottom: 4px;
    display: flex;
    justify-content: center;
    gap: 22px;
    flex-wrap: wrap;
  }

  .fs-active .btns { margin-top: 2vh; }

  button {
    padding: 22px 44px;
    font-size: 1.5em;
    border: none;
    border-radius: 36px;
    cursor: pointer;
    font-weight: bold;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
  }

  .fs-active button { padding: 1.8vh 2.5vw; font-size: 1.6vw; }

  button:hover { transform: translateY(-2px) scale(1.03); }

  #startBtn { background: linear-gradient(90deg, #47cf73, #2fae5b); color: white; }
  #pauseBtn { background: linear-gradient(90deg, #ffb347, #ff8c00); color: white; }
  #resetBtn { background: linear-gradient(90deg, #ff5f6d, #c9184a); color: white; }
  #fullBtn  { background: linear-gradient(90deg, #36a2eb, #1976d2); color: white; }
</style>
</head>

<body>

<div id="bingo-wrap">
  <div class="columns" id="columns"></div>

  <div id="current-area">
    <div id="current">--</div>
  </div>

  <div id="history"></div>

  <div class="btns">
    <button id="startBtn">▶ Iniciar</button>
    <button id="pauseBtn">⏸ Pausar</button>
    <button id="resetBtn">🔄 Reiniciar</button>
    <button id="fullBtn">⛶ Pantalla completa</button>
  </div>
</div>

<script>
(function() {
  const letters = ['B','I','N','G','O'];
  const NUM_MIN = 0;
  const NUM_MAX = 80;

  const columnsDiv = document.getElementById('columns');
  const current = document.getElementById('current');
  const historyDiv = document.getElementById('history');
  const startBtn = document.getElementById('startBtn');
  const pauseBtn = document.getElementById('pauseBtn');
  const resetBtn = document.getElementById('resetBtn');
  const fullBtn = document.getElementById('fullBtn');
  const wrap = document.getElementById('bingo-wrap');

  let pool = [];
  let timer = null;
  let running = false;

  function buildColumns() {
    columnsDiv.innerHTML = '';
    letters.forEach(L => {
      const col = document.createElement('div');
      col.className = 'col col' + L;
      const letterDiv = document.createElement('div');
      letterDiv.className = 'letter';
      letterDiv.textContent = L;
      col.appendChild(letterDiv);
      columnsDiv.appendChild(col);
    });
  }

  function shuffle(arr) {
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  }

  function resetGame() {
    clearInterval(timer);
    running = false;
    pool = [];
    letters.forEach(L => {
      for (let n = NUM_MIN; n <= NUM_MAX; n++) {
        pool.push({ letter: L, num: n });
      }
    });
    shuffle(pool);
    historyDiv.innerHTML = '';
    current.textContent = '--';
    current.className = '';
  }

  function callNumber() {
    if (pool.length === 0) {
      clearInterval(timer);
      running = false;
      current.textContent = 'FIN';
      return;
    }
    const { letter: L, num: n } = pool.pop();

    current.classList.remove('pop');
    void current.offsetWidth; // reinicia la animación
    current.textContent = L + n;
    current.classList.add('pop');

    const col = document.querySelector('.col' + L);
    if (col) {
      col.classList.remove('flash');
      void col.offsetWidth;
      col.classList.add('flash');
    }

    const tag = document.createElement('span');
    tag.className = 'called-num';
    tag.textContent = L + n;
    historyDiv.appendChild(tag);
    historyDiv.scrollTop = historyDiv.scrollHeight;
  }

  startBtn.addEventListener('click', () => {
    if (running) return;
    running = true;
    callNumber();
    timer = setInterval(callNumber, 4000);
  });

  pauseBtn.addEventListener('click', () => {
    running = false;
    clearInterval(timer);
  });

  resetBtn.addEventListener('click', resetGame);

  // --- Pantalla completa cross-browser ---
  // Streamlit renderiza este HTML dentro de un iframe con srcdoc (mismo origen),
  // así que intentamos primero poner en fullscreen la ventana padre (la pestaña
  // completa del navegador) y si falla, hacemos fallback al propio iframe.
  function requestFS(el) {
    if (el.requestFullscreen) return el.requestFullscreen();
    if (el.webkitRequestFullscreen) return el.webkitRequestFullscreen();
    if (el.mozRequestFullScreen) return el.mozRequestFullScreen();
    if (el.msRequestFullscreen) return el.msRequestFullscreen();
  }

  function exitFS(doc) {
    if (doc.exitFullscreen) return doc.exitFullscreen();
    if (doc.webkitExitFullscreen) return doc.webkitExitFullscreen();
    if (doc.mozCancelFullScreen) return doc.mozCancelFullScreen();
    if (doc.msExitFullscreen) return doc.msExitFullscreen();
  }

  function isFS(doc) {
    return doc.fullscreenElement || doc.webkitFullscreenElement ||
           doc.mozFullScreenElement || doc.msFullscreenElement;
  }

  fullBtn.addEventListener('click', () => {
    let targetDoc = document;
    let targetEl = wrap;
    try {
      if (window.top && window.top.document && window.top !== window) {
        targetDoc = window.top.document;
        targetEl = window.top.document.documentElement;
      }
    } catch (e) {
      // origen distinto: nos quedamos con el iframe local
      targetDoc = document;
      targetEl = wrap;
    }

    if (!isFS(targetDoc)) {
      const req = requestFS(targetEl);
      if (req && req.catch) {
        req.catch(() => { requestFS(wrap); });
      }
    } else {
      exitFS(targetDoc);
    }
  });

  ['fullscreenchange','webkitfullscreenchange','mozfullscreenchange','MSFullscreenChange']
    .forEach(evt => {
      document.addEventListener(evt, () => {
        wrap.classList.toggle('fs-active', !!isFS(document));
      });
      try {
        if (window.top && window.top.document) {
          window.top.document.addEventListener(evt, () => {
            wrap.classList.toggle('fs-active', !!isFS(window.top.document));
          });
        }
      } catch (e) { /* cross-origin, ignorar */ }
    });

  buildColumns();
  resetGame();
})();
</script>

</body>
</html>
"""

components.html(BINGO_HTML, height=780, scrolling=False)
