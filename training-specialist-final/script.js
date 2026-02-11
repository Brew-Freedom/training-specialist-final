// Initial word lists
let positiveWords = ['good','happy','love','great','fantastic'];
let negativeWords = ['bad','sad','hate','terrible','awful'];

// --- Sentiment Analyzer ---
function predictSentiment() {
    const text = document.getElementById('userInput').value.toLowerCase();
    if (!text) { alert("Please enter a sentence."); return; }

    let score = 0;
    positiveWords.forEach(word => { if(text.includes(word)) score++; });
    negativeWords.forEach(word => { if(text.includes(word)) score--; });

    const result = score > 0 ? 'Positive' : score < 0 ? 'Negative' : 'Neutral';
    document.getElementById('result').innerText = `Prediction: ${result}`;
}

// Real-time prediction
document.getElementById('userInput').addEventListener('input', predictSentiment);

// --- Trainable AI ---
function updateWordLists() {
    document.getElementById('positiveList').innerText = positiveWords.join(', ');
    document.getElementById('negativeList').innerText = negativeWords.join(', ');
}

function addWord() {
    const word = document.getElementById('newWord').value.toLowerCase().trim();
    const type = document.getElementById('wordType').value;
    if (!word) { alert("Please enter a word."); return; }

    if(type === 'positive' && !positiveWords.includes(word)) positiveWords.push(word);
    if(type === 'negative' && !negativeWords.includes(word)) negativeWords.push(word);

    document.getElementById('trainFeedback').innerText = 
        `Added "${word}" to ${type} words. Test it in the Sentiment Analyzer!`;
    
    updateWordLists();
    document.getElementById('newWord').value = '';
}

// --- Data Quality Checker ---
function checkDataQuality() {
    const file = document.getElementById('fileInput').files[0];
    if (!file) { alert("Please select a CSV file."); return; }

    const reader = new FileReader();
    reader.onload = function(e) {
        const lines = e.target.result.split('\n');
        const total = lines.length - 1;
        const empty = lines.filter(l => l.trim() === '').length;
        const duplicates = lines.length - new Set(lines).size;

        document.getElementById('qualityResult').innerHTML = `
            <p>Total rows: ${total}</p>
            <p>Empty rows: ${empty}</p>
            <p>Duplicate rows: ${duplicates}</p>
        `;
    };
    reader.readAsText(file);
}

// --- Before/After Demo ---
function runBeforeAfterDemo() {
    const beforeAccuracy = Math.floor(Math.random()*40 + 50);
    const afterAccuracy = Math.floor(Math.random()*20 + 80);

    document.getElementById('beforeAfterResult').innerHTML = `
        <p>Before cleaning dataset: Accuracy ~ ${beforeAccuracy}%</p>
        <p>After cleaning dataset: Accuracy ~ ${afterAccuracy}%</p>
    `;
}

// Initialize word lists
updateWordLists();
