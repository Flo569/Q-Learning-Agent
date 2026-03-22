import json
import queue
import threading
import time

from flask import Flask, Response, render_template_string

from q_learning.utils.settings import Settings

SPEED_DELAY = [0.45, 0.09, 0.03, 0.008, 0.004, 0.0]


class Visualizer:

    def __init__(self, host="0.0.0.0", port=8080):
        self.running = False
        self.host = host
        self.port = port
        self.event_queue: queue.Queue = queue.Queue(maxsize=600)
        self.control: dict = {"running": False, "reset": False, "speed": 2}

        self.app = Flask(__name__)
        self.setup_routes()

    def init(self, filename: str):
        try:
            self.event_queue.put_nowait({
                "type": "maze",
                "layout": Settings.layout,
                "filename": filename
            })
        except queue.Full:
            pass

    def shutdown(self):
        try:
            self.event_queue.put_nowait({"type": "training_done"})
        except queue.Full:
            pass

    def start(self):
        """Startet Flask-Server in eigenem Thread"""
        self.running = True
        thread = threading.Thread(target=self.run_server, daemon=True)
        thread.start()

    def stop(self):
        """Stoppt Visualizer (nur Flag; Flask Thread läuft weiter)"""
        self.running = False

    def update(self, agent_pos: tuple, episode: int, steps: int, epsilon: float, reward: int,
               score: int, bonus_pos: list, trail: list, done: bool, success: bool):
        """Empfängt Schritt-Daten vom Environment und pusht in Event-Queue"""
        if not self.running:
            return
        try:
            x, y = agent_pos
            self.event_queue.put_nowait({
                "type": "step",
                "x": x, "y": y,
                "episode": episode,
                "step": steps,
                "epsilon": epsilon,
                "reward": reward,
                "score": score,
                "bonus_pos": [[b[0], b[1]] for b in bonus_pos],
                "trail": trail[-25:],
                "done": done,
                "won": done and success,
            })

            # speed throttle
            d = SPEED_DELAY[max(0, min(len(SPEED_DELAY) - 1, self.control["speed"] - 1))]
            if d > 0:
                time.sleep(d)
        except queue.Full:
            pass

    def run_server(self):
        """Startet Flask-App"""
        self.app.run(host=self.host, port=self.port, threaded=True, use_reloader=False)

    def pause(self):
        while not self.control["running"]:
            time.sleep(0.05)
            if self.control["reset"]:
                return
        if self.control["reset"]:
            return

    def restart_training(self):
        self.control["reset"] = False
        self.control["running"] = False
        while not self.event_queue.empty():
            try:
                self.event_queue.get_nowait()
            except queue.Empty:
                break

    # ---------------------------------------------------------------------------
    # Flask routes
    # ---------------------------------------------------------------------------

    def setup_routes(self):

        @self.app.route("/stream")
        def stream():
            def generate():
                while True:
                    try:
                        event = self.event_queue.get(timeout=5)
                        yield f"data: {json.dumps(event)}\n\n"
                    except queue.Empty:
                        yield 'data: {"type":"ping"}\n\n'

            return Response(generate(), mimetype="text/event-stream",
                            headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})

        @self.app.route("/control/<action>")
        def control(action: str):
            if action == "run":
                self.control["running"] = True
            elif action == "pause":
                self.control["running"] = False
            elif action == "reset":
                self.control["reset"] = True
                self.control["running"] = False
                self.restart_training()
            elif action.startswith("speed"):
                self.control["speed"] = int(action[-1])
            return "ok"

        @self.app.route("/")
        def index():
            return render_template_string(_HTML,
                                          alpha=Settings.alpha,
                                          gamma=Settings.gamma,
                                          epsilon_main=Settings.epsilon_main,
                                          epsilon_decay=Settings.epsilon_decay,
                                          epsilon_min=Settings.epsilon_min,
                                          episodes=Settings.episodes,
                                          )

# ---------------------------------------------------------------------------
# HTML / CSS / JS
# ---------------------------------------------------------------------------
_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Q-Learning Visualizer</title>
<style>
  *{box-sizing:border-box;margin:0;padding:0}
  body{background:#0d0d1a;color:#e2e8f0;font-family:'JetBrains Mono',monospace;display:flex;flex-direction:column;align-items:center;min-height:100vh;padding:20px 12px}
  h1{font-size:15px;letter-spacing:.12em;color:#94a3b8;margin-bottom:6px;text-transform:uppercase;display:flex;align-items:center;gap:10px}
  #log-badge{font-size:10px;color:#4ade80;background:#0a1f0a;border:0.5px solid #166534;border-radius:4px;padding:2px 8px;letter-spacing:.04em}
  #maze-name{font-size:11px;color:#22d3c5;letter-spacing:.06em;margin-bottom:10px;min-height:16px}
  #wrap{display:flex;gap:18px;align-items:flex-start;flex-wrap:wrap;justify-content:center}
  #canvas{border:1px solid #1e2a3a;border-radius:6px;image-rendering:pixelated}
  #panel{width:195px;display:flex;flex-direction:column;gap:8px}
  .card{background:#111827;border:0.5px solid #1e2a3a;border-radius:8px;padding:9px 13px}
  .card .lbl{font-size:10px;color:#64748b;letter-spacing:.06em;margin-bottom:2px}
  .card .val{font-size:22px;font-weight:500;color:#e2e8f0;font-variant-numeric:tabular-nums}
  #bars{
  height:36px;
  display:flex;
  align-items:flex-end;
  gap:1px;
  padding-top:4px;
  overflow:hidden;
}

.bar{
  flex:1;
  min-width:0;
  border-radius:1px 1px 0 0;
}
  #controls{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-top:10px}
  button{background:transparent;border:0.5px solid #334155;color:#94a3b8;border-radius:6px;padding:5px 14px;font-size:12px;font-family:inherit;cursor:pointer;transition:background .15s}
  button:hover{background:#1e2a3a;color:#e2e8f0}
  button.active{background:#0d3349;color:#22d3c5;border-color:#22d3c5}
  #milestone{font-size:12px;color:#fbbf24;background:#1a1500;border:0.5px solid #92400e;border-radius:6px;padding:4px 12px;opacity:0;transition:opacity .4s;margin-left:auto}
  #milestone.show{opacity:1}
  #params{margin-top:10px;background:#111827;border:0.5px solid #1e2a3a;border-radius:8px;padding:10px 13px;width:100%;max-width:510px}
  #params .ph{font-size:10px;color:#64748b;letter-spacing:.06em;margin-bottom:8px}
  .prow{display:flex;align-items:center;gap:8px;margin-bottom:5px;font-size:12px}
  .prow label{width:120px;color:#94a3b8;flex-shrink:0}
  .prow input[type=range]{flex:1;accent-color:#22d3c5;opacity:.45;cursor:not-allowed}
  .prow .pval{width:52px;text-align:right;color:#e2e8f0;font-variant-numeric:tabular-nums}
  .lgnd{display:flex;gap:10px;flex-wrap:wrap;margin-top:6px}
  .lgnd span{font-size:10px;color:#64748b;display:flex;align-items:center;gap:4px}
  .lgnd i{width:10px;height:10px;border-radius:2px;display:inline-block;flex-shrink:0}
</style>
</head>
<body>
<h1>Q-Learning Visualizer <span id="log-badge"
      style="color: {{ ' #4ade80 ' if csv_active else ' #f87171 ' }};
             background: {{ ' #0a1f0a ' if csv_active else ' #1f0a0a ' }};
             border-color: {{ ' #166534 ' if csv_active else ' #7f1d1d ' }}">
  {{ 'CSV logging active' if csv_active else 'CSV logging off' }}
</span></h1>
<div id="maze-name">Press Run to start…</div>
<div id="wrap">
  <canvas id="canvas"></canvas>
  <div id="panel">
    <div class="card"><div class="lbl">MAZE</div><div class="val" style="font-size:13px;padding-top:2px" id="v-maze">–</div></div>
    <div class="card"><div class="lbl">EPISODE</div><div class="val" id="v-ep">–</div></div>
    <div class="card"><div class="lbl">STEP</div><div class="val" id="v-stp">–</div></div>
    <div class="card"><div class="lbl">ε EPSILON</div><div class="val" id="v-eps">–</div></div>
    <div class="card"><div class="lbl">WIN RATE</div><div class="val" id="v-wr">–</div></div>
    <div class="card"><div class="lbl">LAST 100 EPISODES</div><div id="bars"></div></div>
    <div class="card">
      <div class="lbl">LEGEND</div>
      <div class="lgnd">
        <span><i style="background:#1e4d2b"></i>Start</span>
        <span><i style="background:#7c1515"></i>Goal</span>
        <span><i style="background:#4a3000"></i>Bonus</span>
        <span><i style="background:#0c0c22"></i>Wall</span>
        <span><i style="background:#22d3c5;border-radius:50%"></i>Agent</span>
        <span><i style="background:rgba(34,211,197,.45)"></i>Trail</span>
      </div>
    </div>
  </div>
</div>

<div id="controls">
  <button onclick="setRun(true)">▶ Run</button>
  <button onclick="setRun(false)">❚❚ Pause</button>
  <button onclick="doReset()">↺ Reset</button>
  <span style="font-size:11px;color:#64748b;margin-left:4px">Speed:</span>
  <button class="active" id="s1" onclick="setSpeed(1)">·</button>
  <button id="s2" onclick="setSpeed(2)">··</button>
  <button id="s3" onclick="setSpeed(3)">···</button>
  <button id="s4" onclick="setSpeed(4)">····</button>
  <button id="s5" onclick="setSpeed(5)">·····</button>
  <button id="s6" onclick="setSpeed(6)">Max</button>
  <span id="milestone"></span>
</div>

<div id="params">
  <div class="ph">HYPERPARAMETERS — change values in settings.py, then Reset to apply</div>
  <div class="prow"><label>α alpha</label><input type="range" min=".01" max="1" step=".01" value="{{ alpha }}" disabled><span class="pval">{{ alpha }}</span></div>
  <div class="prow"><label>γ gamma</label><input type="range" min=".01" max="1" step=".01" value="{{ gamma }}" disabled><span class="pval">{{ gamma }}</span></div>
  <div class="prow"><label>ε start</label><input type="range" min=".01" max="1" step=".01" value="{{ epsilon_main }}" disabled><span class="pval">{{ epsilon_main }}</span></div>
  <div class="prow"><label>ε decay</label><input type="range" min=".9" max=".9999" step=".0001" value="{{ epsilon_decay }}" disabled><span class="pval">{{ epsilon_decay }}</span></div>
  <div class="prow"><label>ε min</label><input type="range" min=".001" max=".5" step=".001" value="{{ epsilon_min }}" disabled><span class="pval">{{ epsilon_min }}</span></div>
  <div style="font-size:10px;color:#475569;margin-top:6px">
    Episodes per maze: {{ episodes }} &nbsp;|&nbsp;
    Logs written to: /logs/
  </div>
</div>

<script>
const cvs=document.getElementById('canvas'),ctx=cvs.getContext('2d');
const CS=38;
let layout=[],ROWS=0,COLS=0,agX=0,agY=0,bonusSet=new Set(),trail=[];
let wins=[],ep=0,stp=0,eps=0,currentMaze='–';

function setRun(r){fetch('/control/'+(r?'run':'pause'));}
function doReset(){fetch('/control/reset').then(()=>location.reload());}
function setSpeed(s){
  fetch('/control/speed'+s);
  for(let i=1;i<=6;i++)document.getElementById('s'+i).classList.toggle('active',i===s);
}

function draw(){
  if(!ROWS)return;
  ctx.clearRect(0,0,cvs.width,cvs.height);
  const trailMap=new Map();
  trail.forEach(([tx,ty],i)=>trailMap.set(tx+','+ty,i));
  for(let y=0;y<ROWS;y++){
    for(let x=0;x<COLS;x++){
      const v=layout[y][x],isAg=agX===x&&agY===y;
      const isBon=bonusSet.has(x+','+y);
      const ti=trailMap.has(x+','+y)?trailMap.get(x+','+y):-1;
      let col='#141428';
      if(v===3)col='#0c0c22';
      else if(isAg)col='#22d3c5';
      else if(v===2)col='#7c1515';
      else if(v===1)col='#1e4d2b';
      else if(isBon)col='#4a3000';
      else if(ti>=0){const a=.15+(ti+1)/Math.max(trail.length,1)*.7;col=`rgba(34,211,197,${a.toFixed(2)})`;}
      ctx.fillStyle=col;ctx.fillRect(x*CS,y*CS,CS,CS);
      const cx=x*CS+CS/2,cy=y*CS+CS/2;
      if(isAg){
        ctx.beginPath();ctx.arc(cx,cy,9,0,Math.PI*2);
        ctx.fillStyle='#22d3c5';ctx.fill();
        ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
      } else if(v===2){
        ctx.beginPath();ctx.arc(cx,cy,6,0,Math.PI*2);
        ctx.fillStyle='#e53e3e';ctx.fill();
      } else if(v===1){
        ctx.fillStyle='#2dba52';ctx.fillRect(cx-5,cy-5,10,10);
      } else if(isBon){
        ctx.beginPath();ctx.arc(cx,cy,5,0,Math.PI*2);
        ctx.fillStyle='#eab308';ctx.fill();
        ctx.strokeStyle='#f5d060';ctx.lineWidth=1.5;ctx.stroke();
      }
    }
  }
  ctx.strokeStyle='rgba(255,255,255,0.04)';ctx.lineWidth=.5;
  for(let i=0;i<=COLS;i++){ctx.beginPath();ctx.moveTo(i*CS,0);ctx.lineTo(i*CS,ROWS*CS);ctx.stroke();}
  for(let i=0;i<=ROWS;i++){ctx.beginPath();ctx.moveTo(0,i*CS);ctx.lineTo(COLS*CS,i*CS);ctx.stroke();}
}

function updateStats(){
  document.getElementById('v-maze').textContent=currentMaze;
  document.getElementById('v-ep').textContent=ep.toLocaleString();
  document.getElementById('v-stp').textContent=stp;
  document.getElementById('v-eps').textContent=eps.toFixed(3);
  const wr=wins.length?wins.reduce((a,b)=>a+b,0)/wins.length:0;
  document.getElementById('v-wr').textContent=(wr*100).toFixed(1)+'%';
  document.getElementById('bars').innerHTML=wins.map(w=>`<div class="bar" style="height:${w?100:28}%;background:${w?'#22d3c5':'rgba(229,83,62,.7)'}"></div>`).join('');
}

let lastMilestone=0;
function checkMilestone(episode){
  if(episode%100===0&&episode!==lastMilestone){
    lastMilestone=episode;
    const wr=wins.length?Math.round(wins.reduce((a,b)=>a+b,0)/wins.length*100):0;
    const m=document.getElementById('milestone');
    m.textContent=`Milestone — Ep ${episode} — ${wr}% wins`;
    m.classList.add('show');setTimeout(()=>m.classList.remove('show'),3000);
  }
}

const es=new EventSource('/stream');
es.onmessage=ev=>{
  const d=JSON.parse(ev.data);
  if(d.type==='ping')return;
  if(d.type==='maze'){
    layout=d.layout;ROWS=layout.length;COLS=layout[0].length;
    cvs.width=COLS*CS;cvs.height=ROWS*CS;
    currentMaze=d.filename;wins=[];ep=0;stp=0;
    document.getElementById('maze-name').textContent='Training: '+d.filename;
    draw();updateStats();
  }
  if(d.type==='step'){
    agX=d.x;agY=d.y;ep=d.episode;stp=d.step;eps=d.epsilon;
    trail=d.trail||[];
    bonusSet=new Set((d.bonus_pos||[]).map(([bx,by])=>bx+','+by));
    if(d.done){wins.push(d.won?1:0);if(wins.length>100)wins.shift();checkMilestone(d.episode);}
    draw();updateStats();
  }
  if(d.type==='training_done'){
    document.getElementById('maze-name').textContent='All mazes complete — logs written to /logs/';
    document.getElementById('log-badge').textContent='CSV logs saved';
  }
};
</script>
</body>
</html>
"""
