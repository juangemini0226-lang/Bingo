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
    .block-container {padding-top: 1rem; padding-bottom: 0rem; max-width: 1100px;}
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
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
  }

  #bingo-wrap {
    font-family: 'Segoe UI', Arial, sans-serif;
    background: radial-gradient(circle at top, #1e2a52, #0a0f24);
    color: white;
    padding: 20px 20px 10px 20px;
    border-radius: 20px;
    text-align: center;
    width: 100%;
    max-width: 1250px;
    margin: auto;
    box-sizing: border-box;
    transition: all 0.3s ease;
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
    gap: 16px;
    margin: 20px 0;
  }

  .fs-active .columns { gap: 1.8vw; margin: 2vh 0; }

  .col {
    flex: 1;
    max-width: 220px;
    padding: 16px 10px;
    border-radius: 16px;
    background: rgba(255,255,255,0.05);
    border: 2px solid rgba(255,255,255,0.1);
  }

  .fs-active .col { max-width: 16vw; padding: 1.4vh 0.8vw; }

  .col .letter {
    font-size: 2.4em;
    font-weight: bold;
    margin-bottom: 10px;
  }

  .fs-active .col .letter { font-size: 3.4vw; }

  .colB .letter { color: #ff5f6d; }
  .colI .letter { color: #ffc371; }
  .colN .letter { color: #47cf73; }
  .colG .letter { color: #36a2eb; }
  .colO .letter { color: #d264ff; }

  #current-area {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 70px;
    margin: 10px 0;
  }

  .fs-active #current-area { height: 9vh; margin: 1.5vh 0; }

  #current {
    font-size: 2.4em;
    font-weight: bold;
    color: white;
    letter-spacing: 2px;
    text-shadow: 0 0 18px rgba(255,255,255,0.5);
  }

  .fs-active #current { font-size: 4vw; }

  @keyframes pop {
    0% { transform: scale(0.3); opacity: 0; }
    60% { transform: scale(1.2); opacity: 1; }
    100% { transform: scale(1); }
  }

  #current.pop { animation: pop 0.4s ease-out; }

  .called-num {
    display: inline-block;
    margin: 2px;
    padding: 6px 10px;
    border-radius: 8px;
    font-size: 0.9em;
    background: rgba(255,255,255,0.08);
  }

  .fs-active .called-num { font-size: 1.3vw; padding: 0.6vh 1vw; }

  #history {
    max-height: 90px;
    overflow-y: auto;
    margin-top: 10px;
    padding: 8px;
    background: rgba(0,0,0,0.2);
    border-radius: 10px;
  }

  .fs-active #history { max-height: 12vh; }

  .btns {
    margin-top: 14px;
    margin-bottom: 4px;
    display: flex;
    justify-content: center;
    gap: 15px;
    flex-wrap: wrap;
  }

  .fs-active .btns { margin-top: 2vh; }

  button {
    padding: 12px 26px;
    font-size: 1em;
    border: none;
    border-radius: 30px;
    cursor: pointer;
    font-weight: bold;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
  }

  .fs-active button { padding: 1.2vh 2vw; font-size: 1.1vw; }

  button:hover { transform: translateY(-2px) scale(1.03); }

  #startBtn { background: linear-gradient(90deg, #47cf73, #2fae5b); color: white; }
  #pauseBtn { background: linear-gradient(90deg, #ffb347, #ff8c00); color: white; }
  #resetBtn { background: linear-gradient(90deg, #ff5f6d, #c9184a); color: white; }
  #fullBtn  { background: linear-gradient(90deg, #36a2eb, #1976d2); color: white; }

  .col .grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 2px;
    font-size: 0.62em;
  }

  .fs-active .col .grid { font-size: 0.9vw; }

  .col .grid span {
    padding: 2px 0;
    border-radius: 4px;
    opacity: 0.35;
  }

  .col .grid span.used {
    opacity: 1;
    background: rgba(255,255,255,0.25);
    font-weight: bold;
  }
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
  const ranges = {
    B: [0, 16],
    I: [17, 32],
    N: [33, 48],
    G: [49, 64],
    O: [65, 80]
  };

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
      const [lo, hi] = ranges[L];
      const col = document.createElement('div');
      col.className = 'col col' + L;
      const letterDiv = document.createElement('div');
      letterDiv.className = 'letter';
      letterDiv.textContent = L;
      col.appendChild(letterDiv);
      const grid = document.createElement('div');
      grid.className = 'grid';
      for (let n = lo; n <= hi; n++) {
        const span = document.createElement('span');
        span.textContent = n;
        span.id = 'num-' + n;
        grid.appendChild(span);
      }
      col.appendChild(grid);
      columnsDiv.appendChild(col);
    });
  }

  function letterFor(n) {
    for (const L of letters) {
      if (n >= ranges[L][0] && n <= ranges[L][1]) return L;
    }
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
    for (let n = 0; n <= 80; n++) pool.push(n);
    shuffle(pool);
    historyDiv.innerHTML = '';
    current.textContent = '--';
    current.className = '';
    document.querySelectorAll('.grid span').forEach(s => s.classList.remove('used'));
  }

  function callNumber() {
    if (pool.length === 0) {
      clearInterval(timer);
      running = false;
      current.textContent = 'FIN';
      return;
    }
    const n = pool.pop();
    const L = letterFor(n);

    current.classList.remove('pop');
    void current.offsetWidth; // reinicia la animación
    current.textContent = L + n;
    current.classList.add('pop');

    const numSpan = document.getElementById('num-' + n);
    if (numSpan) numSpan.classList.add('used');

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

components.html(BINGO_HTML, height=900, scrolling=False)
