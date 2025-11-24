const fileInput   = document.getElementById('fileInput');
const selectBtn   = document.getElementById('selectBtn');
const settingsSec = document.getElementById('settingsSec');
const progressSec = document.getElementById('progressSec');
const resultSec   = document.getElementById('resultSec');

let selectedFile = null;
let fileId       = null;

/* 1. Выбор файла */
selectBtn.onclick = () => fileInput.click();
fileInput.onchange = (e) => {
  const file = e.target.files[0];
  if(!file) return;
  selectedFile = file;

  // Показать инфо
  document.getElementById('fileName').textContent = file.name;
  document.getElementById('fileSize').textContent = formatBytes(file.size);
  document.querySelector('.file-info').classList.remove('hidden');
  settingsSec.classList.remove('hidden');
};

/* 2. Старт сжатия */
document.getElementById('startBtn').onclick = async () => {
  if(!selectedFile) return;

  settingsSec.classList.add('hidden');
  progressSec.classList.remove('hidden');
  animateProgress();

  const body = new FormData();
  body.append('file', selectedFile);

  try{
    const r = await fetch('http://localhost:8000/api/compress',{
      method:'POST',
      body
    });
    const data = await r.json();
    fileId = data.fileId;

    showResult(data);
  }catch(err){
    alert('Ошибка сжатия: '+err);
    location.reload();
  }
};

/* 3. Анимация прогресса */
function animateProgress(){
  let w = 0;
  const intv = setInterval(()=>{
    w += Math.random()*15;
    if(w>90) w=90;
    document.getElementById('progressFill').style.width = w+'%';
    document.getElementById('progressText').textContent = Math.round(w)+' %';
    if(fileId){ clearInterval(intv); finishProgress(); }
  },200);
}
function finishProgress(){
  document.getElementById('progressFill').style.width = '100%';
  document.getElementById('progressText').textContent = '100 %';
}

/* 4. Показ результата */
function showResult(data){
  setTimeout(()=>{
    progressSec.classList.add('hidden');
    resultSec.classList.remove('hidden');

    document.getElementById('origSize').textContent   = formatBytes(selectedFile.size);
    document.getElementById('newSize').textContent    = formatBytes(data.compressedSize);
    document.getElementById('savedPercent').textContent = (data.compressionRatio*100).toFixed(1)+'%';
  },400);
}

/* 5. Скачивание */
document.getElementById('downloadBtn').onclick = () => {
  if(!fileId) return;
  const a = document.createElement('a');
  a.href = `http://localhost:8000/api/download/${fileId}`;
  a.download = `compressed_${selectedFile.name}`;
  a.click();
};

/* helpers */
function formatBytes(b){
  const k=1024, s=['Б','КБ','МБ','ГБ'];
  let i=Math.floor(Math.log(b)/Math.log(k));
  return (b/Math.pow(k,i)).toFixed(2)+' '+s[i];
}