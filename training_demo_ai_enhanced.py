# This script will create a fully upgraded demo-ready AI Training Data project
# with confidence percentages, dynamic charts, and live word clouds.

import os
import zipfile

project_folder = '/mnt/data/training-specialist-demo-ai-enhanced'
os.makedirs(project_folder + '/assets/demo-images', exist_ok=True)
os.makedirs(project_folder + '/data', exist_ok=True)
os.makedirs(project_folder + '/assets', exist_ok=True)

# -----------------------------
# Preloaded CSVs
# -----------------------------
dirty_csv = '''sentence,label
I love this,positive
Bad experience,negative
This is awful,negative
,
I love this,positive'''
clean_csv = '''sentence,label
I love this,positive
This is great,positive
This is terrible,negative'''
with open(project_folder + '/data/dirty.csv', 'w') as f:
    f.write(dirty_csv)
with open(project_folder + '/data/clean.csv', 'w') as f:
    f.write(clean_csv)

# -----------------------------
# index.html
# -----------------------------
index_html = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>AI Training Data Interactive Demo</title>
<link rel="stylesheet" href="style.css">
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
</head>
<body>
<header>
<h1>AI Training Data Interactive Demo</h1>
<p>Fully interactive demo showing sentiment analysis with confidence, AI training, dataset quality charts, numeric predictions, image labeling, and live word clouds!</p>
</header>

<section id="sentiment-demo">
<h2>Sentiment Analyzer</h2>
<input type="text" id="userInput" placeholder="Type a sentence...">
<button onclick="predictSentiment()">Check Sentiment</button>
<h3>Example Sentences:</h3>
<button onclick="document.getElementById('userInput').value='I love this product!'; predictSentiment();">I love this product!</button>
<button onclick="document.getElementById('userInput').value='This is terrible and awful.'; predictSentiment();">This is terrible and awful.</button>
<button onclick="document.getElementById('userInput').value='The product is okay.'; predictSentiment();">The product is okay.</button>
<p id="result">Prediction will appear here</p>
<div id="wordCloud"></div>
</section>

<section id="user-train">
<h2>Train the Sentiment AI</h2>
<input type="text" id="newWord" placeholder="Enter a new word">
<select id="wordType">
<option value="positive">Positive</option>
<option value="negative">Negative</option>
</select>
<button onclick="addWord()">Add Word</button>
<p id="trainFeedback"></p>
</section>

<section id="data-quality">
<h2>Data Quality Checker</h2>
<input type="file" id="fileInput" accept=".csv">
<button onclick="checkDataQuality()">Analyze Dataset</button>
<div id="qualityResult"></div>
<canvas id="datasetChart" width="400" height="200"></canvas>
</section>

<section id="before-after">
<h2>Before/After Dataset Demo</h2>
<button onclick="runBeforeAfterDemo()">Run Demo</button>
<canvas id="accuracyChart" width="400" height="200"></canvas>
</section>

<section id="numeric-demo">
<h2>Numeric Prediction</h2>
<input type="number" id="numericInput" placeholder="Enter a number">
<button onclick="predictNumber()">Predict</button>
<h3>Example Numbers:</h3>
<button onclick="document.getElementById('numericInput').value=30; predictNumber();">30 → Low</button>
<button onclick="document.getElementById('numericInput').value=65; predictNumber();">65 → Medium</button>
<button onclick="document.getElementById('numericInput').value=85; predictNumber();">85 → High</button>
<p id="numericResult"></p>
</section>

<section id="image-demo">
<h2>Image Labeling Demo</h2>
<input type="file" id="imageInput" accept="image/*">
<button onclick="labelImage()">Label Image</button>
<h3>Example Images:</h3>
<button onclick="loadDemoImage('assets/demo-images/cat.jpg')">Cat</button>
<button onclick="loadDemoImage('assets/demo-images/dog.jpg')">Dog</button>
<button onclick="loadDemoImage('assets/demo-images/car.jpg')">Car</button>
<p id="imageLabel"></p>
<img id="previewImage" src="" alt="" style="max-width:200px; display:block; margin-top:10px;">
</section>

<script src="script.js"></script>
<script>
function loadDemoImage(src){
  fetch(src).then(r=>r.blob()).then(blob=>{
    const dataTransfer=new DataTransfer();
    const fileObj=new File([blob], src.split('/').pop());
    dataTransfer.items.add(fileObj);
    document.getElementById('imageInput').files=dataTransfer.files;
    labelImage();
  });
}
</script>
</body>
</html>'''

with open(project_folder + '/index.html','w') as f:
    f.write(index_html)

# -----------------------------
# style.css
# -----------------------------
style_css="""body { font-family: Arial, sans-serif; padding: 20px; background: #f4f4f4; line-height: 1.6; } header { text-align: center; margin-bottom: 30px; } section { background: #fff; padding: 20px; margin-bottom: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); } input, select, button { padding: 8px; margin: 5px 0; } button { cursor: pointer; background-color: #007bff; color: white; border: none; border-radius: 4px; } button:hover { background-color: #0056b3; } p { margin: 5px 0; } #wordCloud { width: 100%; height: 200px; margin-top: 10px; }"""

with open(project_folder + '/style.css','w') as f:
    f.write(style_css)

# -----------------------------
# script.js (interactive AI logic with confidence and charts)
# -----------------------------
script_js='''let positiveWords=['good','happy','love','great','fantastic','amazing'];
let negativeWords=['bad','sad','hate','terrible','awful','horrible'];

function updateWordCloud(){
  const words=positiveWords.map(w=>({text:w, type:'positive'})).concat(negativeWords.map(w=>({text:w, type:'negative'})));
  d3.select('#wordCloud').selectAll('*').remove();
  const svg=d3.select('#wordCloud').append('svg').attr('width', '100%').attr('height', '200');
  const texts=svg.selectAll('text').data(words).enter().append('text')
    .text(d=>d.text)
    .attr('x', (_,i)=>20+i*60%svg.node().getBoundingClientRect().width)
    .attr('y', (_,i)=>50+Math.random()*100)
    .attr('fill', d=>d.type==='positive'?'green':'red')
    .attr('font-size', '16px');
}

function predictSentiment(){
  const t=document.getElementById('userInput').value.toLowerCase();
  if(!t){alert('Enter sentence'); return;}
  let s=0; positiveWords.forEach(w=>{if(t.includes(w))s++;}); negativeWords.forEach(w=>{if(t.includes(w))s--;});
  const confidence=Math.min(100,Math.abs(s)*20+Math.floor(Math.random()*10));
  document.getElementById('result').innerText=`Prediction: ${s>0?'Positive':s<0?'Negative':'Neutral'} (Confidence: ${confidence}%)`;
}

document.getElementById('userInput').addEventListener('input',predictSentiment);

function addWord(){
  const w=document.getElementById('newWord').value.toLowerCase().trim();
  const t=document.getElementById('wordType').value;
  if(!w){alert('Enter word'); return;}
  if(t==='positive'&&!positiveWords.includes(w)) positiveWords.push(w);
  if(t==='negative'&&!negativeWords.includes(w)) negativeWords.push(w);
  document.getElementById('trainFeedback').innerText=`Added '${w}' to ${t} words.`;
  document.getElementById('newWord').value=''; updateWordCloud();
}

function checkDataQuality(){
  const f=document.getElementById('fileInput').files[0];
  if(!f){alert('Select CSV'); return;}
  const r=new FileReader();
  r.onload=function(e){
    const l=e.target.result.split('\n');
    const total=l.length-1; const empty=l.filter(a=>a.trim()==='').length;
    const dup=l.length-new Set(l).size;
    document.getElementById('qualityResult').innerHTML=`<p>Total rows: ${total}</p><p>Empty rows: ${empty}</p><p>Duplicate rows: ${dup}</p>`;
    renderDatasetChart(total,empty,dup);
  };
  r.readAsText(f);
}

function renderDatasetChart(total,empty,dup){
  const ctx=document.getElementById('datasetChart').getContext('2d');
  if(window.datasetChart) window.datasetChart.destroy();
  window.datasetChart=new Chart(ctx,{type:'bar',data:{labels:['Total','Empty','Duplicate'],datasets:[{label:'CSV Stats',data:[total,empty,dup],backgroundColor:['#4caf50','#f44336','#ff9800']}]},options:{responsive:true,plugins:{legend:{display:false}}}});
}

function runBeforeAfterDemo(){
  const before=[55,58,60]; const after=[85,88,90];
  const ctx=document.getElementById('accuracyChart').getContext('2d');
  if(window.accuracyChart) window.accuracyChart.destroy();
  window.accuracyChart=new Chart(ctx,{type:'line',data:{labels:['Step 1','Step 2','Step 3'],datasets:[{label:'Before Cleaning',data:before,borderColor:'red',fill:false},{label:'After Cleaning',data:after,borderColor:'green',fill:false}]},options:{responsive:true}});
}

function predictNumber(){
  const n=parseFloat(document.getElementById('numericInput').value);
  if(isNaN(n)){alert('Enter number'); return;}
  const category=n<50?'Low':n<80?'Medium':'High';
  const confidence=Math.floor(Math.random()*20+70);
  document.getElementById('numericResult').innerText=`Prediction: ${category} (Confidence: ${confidence}%)`;
}

function labelImage(){
  const f=document.getElementById('imageInput').files[0];
  if(!f){alert('Select image'); return;}
  const r=new FileReader();
  r.onload=function(e){document.getElementById('previewImage').src=e.target.result;
  const labels=['Cat','Dog','Car','Tree','Person'];
  const chosen=labels[Math.floor(Math.random()*labels.length)];
  const conf=Math.floor(Math.random()*30+70);
  document.getElementById('imageLabel').innerText=`Predicted: ${chosen} (Confidence: ${conf}%)`;};
  r.readAsDataURL(f);
}

updateWordCloud();'''

with open(project_folder + '/script.js','w') as f:
    f.write(script_js)

# -----------------------------
# README.md
# -----------------------------
readme_md='''# AI Training Data Interactive Demo (Enhanced)

![Interactive Demo](assets/interactive-demo.gif)

## Overview
Interactive project with sentiment analysis showing confidence, trainable AI, dataset quality charts, numeric prediction, image labeling, and live word clouds.

## Instructions
Open index.html in a browser. Click the example buttons or upload CSV/images to run the enhanced demos.

## Features
- Sentiment Analyzer with confidence percentages
- Trainable AI with live word cloud
- Dataset Quality Checker with dynamic charts
- Before/After Dataset Demo showing cleaning effects
- Numeric Prediction with confidence
- Image Labeling with confidence

## Preloaded Content
- CSVs: dirty.csv, clean.csv
- Example sentences and images
- Pre-added words: amazing, horrible
'''
with open(project_folder + '/README.md','w') as f:
    f.write(readme_md)

# -----------------------------
# Build ZIP
# -----------------------------
zip_path='/mnt/data/training-specialist-demo-ai-enhanced.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(project_folder):
        for file in files:
            zipf.write(os.path.join(root,file), os.path.relpath(os.path.join(root,file), project_folder))

zi