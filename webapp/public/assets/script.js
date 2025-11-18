// selecting DOM elements used by the phone-like UI
const dropArea = document.querySelector(".drag-area"),
      dragText = dropArea.querySelector("header"),
      browseBtn = document.getElementById('browseBtn'),
      fileInput = document.getElementById('fileInput'),
      icon = dropArea.querySelector(".icon"),
      sensitiveBadge = document.getElementById('sensitiveBadge'),
      nonSensitiveBadge = document.getElementById('nonSensitiveBadge'),
      progressStatus = document.querySelector("#progressStatus"),
      progressBar = document.querySelector("#progressBar"),
      actionsPanel = document.getElementById('actions'),
      blurBtn = document.getElementById('blurBtn'),
      hideBtn = document.getElementById('hideBtn'),
      removeMetaBtn = document.getElementById('removeMetaBtn'),
      deleteBtn = document.getElementById('deleteBtn'),
      scanIndicator = document.getElementById('scanIndicator'),
      companionToggle = document.getElementById('companionToggle'),
      companionBox = document.getElementById('companion'),
      companionMessages = document.getElementById('companionMessages'),
      companionInput = document.getElementById('companionInput'),
      hiddenList = document.getElementById('hiddenList'),
      openHiddenBtn = document.getElementById('openHiddenBtn');

let currentImageFile = null;
let currentDetection = null;

toggle = document.querySelector(".toggle-button");
navlinks = document.querySelector(".navbar-links");

// Navbar toggle button
toggle.addEventListener('click', () => {
  navlinks.classList.toggle('active');
});

// wire browse button to the hidden file input
browseBtn.onclick = () => fileInput.click();
fileInput.addEventListener('change', loadFile);

// wire example buttons
document.querySelectorAll('.example-btn').forEach(btn => {
  btn.addEventListener('click', async (e) => {
    const src = e.currentTarget.getAttribute('data-src');
    await loadExample(src);
  });
});

var loadFile = function(event) {
  var image = document.getElementById('output');
  const photo = event.target.files[0];
  if (photo !== undefined){
    dropArea.classList.add("active");
    sensitiveBadge.style.display = "none";
    nonSensitiveBadge.style.display = "none";
    progressStatus.style.display = "none";
    progressBar.style.display = "none";
    progressBar.style.width = '0%';
    progressBar.innerHTML = '0%';
    scanIndicator.textContent = 'Scanning...';
    currentImageFile = photo;
    let fileType = photo.type; //getting selected file type
  let validExtensions = ["image/jpeg", "image/jpg", "image/png", "image/svg+xml", "image/webp"]; //supported image MIME types
    
    if(validExtensions.includes(fileType)){
      const photoURL = URL.createObjectURL(photo);
      image.src = photoURL;
      image.style.display = "block";
      icon.style.display = "none";
      dragText.style.display = "none";
      progressStatus.style.display = "block";
      progressBar.style.display = "block";
      setTimeout(() => {
        classify();
      }, 150);
    }
    else{
      alert("This is not an Image File!");
      dropArea.classList.remove("active");
      dragText.style.display = "block";
      icon.style.display = "block";
      image.style.display = "none";
    }
  }
};

// Load an example image (fetch from server and feed into the same flow as a file input)
async function loadExample(relativePath){
  try{
    // Ensure path is properly formatted (handle both relative and absolute paths)
    let fetchPath = relativePath;
    if (!fetchPath.startsWith('/') && !fetchPath.startsWith('http')) {
      fetchPath = '/' + fetchPath;
    }
    
    console.log('Loading example from:', fetchPath);
    
    const resp = await fetch(fetchPath);
    if (!resp.ok) {
      throw new Error(`HTTP error! status: ${resp.status}`);
    }
    const blob = await resp.blob();
    if (!blob) {
      throw new Error('Failed to retrieve blob from response');
    }
    const fileName = relativePath.split('/').pop();
    const file = new File([blob], fileName, { type: blob.type || 'image/jpeg' });
    // create a faux event object similar to fileInput change
    const fauxEvent = { target: { files: [file] } };
    // set the input's files where possible (non-standard, but used for consistency)
    try{ const dataTransfer = new DataTransfer(); dataTransfer.items.add(file); fileInput.files = dataTransfer.files; } catch(e) { /* ignore */ }
    loadFile(fauxEvent);
  } catch(e){
    console.error('Failed to load example image', e);
    appendCompanionMessage('Failed to load example image: ' + e.message);
  }
}

// Dark Mode toggle
const chk = document.getElementById('chk');
chk.addEventListener('change', () => {
  document.body.classList.toggle('dark');
});

const classify = async () => {
  var image = document.getElementById('output');
  imagePrediction = classifyImage(image);
  nsfwPrediction = classifyNSFW(image);
  textPrediction = extractText(image)
            .then((text) =>
            {
              return classifyText(text); 
            });
  let image_result = 0;
  let nsfw_result = 0;
  let text_conf = 0;
  await imagePrediction.then((value) =>
    { 
      image_result = value;
      console.log("Image confidence = ", value);
      for (let i = 0; i <= 33; i++) {
        progressBar.style.width = i + '%';
        progressBar.innerHTML = i + '%';
      }
    }
  );
  await nsfwPrediction.then((value) =>
    { 
      nsfw_result = value;
      console.log("NSFW confidence = ", value);
      for (let i = 33; i <= 50; i++) {
        progressBar.style.width = i + '%';
        progressBar.innerHTML = i + '%';
      }
    }
  );
  await textPrediction.then((value) =>
    { 
      text_conf = value;
      console.log("Text confidence = ", value);
    }
  );
  progressStatus.style.display = "none";
  progressBar.style.display = "none";

  // create detection JSON
  const detection = {
  imageId: currentImageFile ? currentImageFile.name : 'unknown',
  timestamp: new Date().toISOString(),
  detectionResults: [],
  aggregatedTags: [],
  privacyRisks: [],
  actionRecommendation: { recommendedAction: 'none', confidence: 0, availableActions: [] },
  provenance: { modelVersion: (window.image_model && window.image_model.version) || 'unknown', onDevice: true, processingTimeMs: 0 }
  };

  // normalize returned values from models (the repo's model returns array or single value)
  const imgScore = Array.isArray(image_result) ? (image_result[0] || 0) : (image_result || 0);
  const nsfwScore = Array.isArray(nsfw_result) ? (nsfw_result[0] || 0) : (nsfw_result || 0);
  const txtScore = Array.isArray(text_conf) ? (text_conf[0] || 0) : (text_conf || 0);

  // Log scores for debugging
  console.log(`Scores - Document: ${Number(imgScore).toFixed(3)}, NSFW: ${Number(nsfwScore).toFixed(3)}, Text: ${Number(txtScore).toFixed(3)}`);

  const finalScore = Math.max(Number(imgScore) || 0, Number(nsfwScore) || 0, Number(txtScore) || 0);
  const isDocument = Number(imgScore) > 0.5;
  const isNSFW = Number(nsfwScore) > 0.5; // Threshold adjusted for better NSFW detection
  
  let detectionLabel = 'non_sensitive';
  if(isDocument) detectionLabel = 'sensitive_document';
  if(isNSFW) detectionLabel = 'nsfw_content';
  if(isDocument && isNSFW) detectionLabel = 'sensitive_document_nsfw';
  
  detection.detectionResults.push({ 
    label: detectionLabel, 
    score: finalScore, 
    sensitive: finalScore > 0.5,
    documentScore: imgScore,
    nsfwScore: nsfwScore,
    textScore: txtScore
  });
  detection.actionRecommendation = { recommendedAction: finalScore > 0.8 ? 'move_to_hidden' : (finalScore > 0.5 ? 'blur' : 'none'), confidence: finalScore, availableActions: ['blur','move_to_hidden','delete','ignore'] };
  currentDetection = detection;

  if(finalScore > 0.5){
    sensitiveBadge.style.display = "block";
    actionsPanel.style.display = 'flex';
    
    let detectionType = '';
    if(isNSFW && isDocument) detectionType = 'NSFW + Sensitive Document';
    else if(isNSFW) detectionType = 'NSFW Content';
    else if(isDocument) detectionType = 'Sensitive Document';
    else detectionType = 'Sensitive';
    
    scanIndicator.textContent = `${detectionType} detected`;
    appendCompanionMessage(`Detected: ${detectionType} (confidence ${ (finalScore*100).toFixed(0) }%). Recommended: ${detection.actionRecommendation.recommendedAction}`);
    
    // AUTO-BLUR sensitive content
    const img = document.getElementById('output');
    if(img) {
      img.style.filter = 'blur(12px)';
      addSensitiveOverlay();
    }
  }
  else{
    nonSensitiveBadge.style.display = "block";
    actionsPanel.style.display = 'none';
    scanIndicator.textContent = 'No sensitive content detected';
    appendCompanionMessage('No sensitive content detected.');
    
    // Remove blur and overlay for non-sensitive images
    const img = document.getElementById('output');
    if(img) {
      img.style.filter = '';
    }
    removeSensitiveOverlay();
  }
}

const extractText = async function(image){
  let prgs = 0;
  let text = await Tesseract.recognize(
              image.src,
              'eng',
              { logger: (m)=> {
                  if(m.status === "recognizing text"){
                    prgs = 50 + Math.ceil(m.progress * 100)/2;
                    progressBar.style.width = prgs + '%';
                    progressBar.innerHTML = prgs + '%';
                  }              
                }
              }
              ).then(({ data: { text } }) => {
                  return text;
              });
  text = text.replace(/[\r\n]+/g," ");
  console.log("Length of text:" , text.length);
  return text;
}

const classifyImage = async function(image){
  try {
    if (!window.image_model) throw new Error('image_model not loaded');
    let tensor = tf.browser.fromPixels(image)
                .resizeBilinear([150, 150])
                .div(tf.scalar(255))
                .expandDims(0);

    const classification = await window.image_model
                          .predict(tensor)
                          .data()
                          .then( (value) => 
                          { return value; }
                          );
    
    // Clean up tensor
    tensor.dispose();
    
    return classification;
  } catch (e) {
    console.warn('Image model error, using fallback:', e);
    // Fallback: heuristic based on filename
    if(currentImageFile && /sensitive|nsfw|nude|spicy|credit|card|id|screen|passport|license/i.test(currentImageFile.name)) return [0.92];
    return [0.05];
  }
}

const classifyNSFW = async function(image){
  try {
    if (!window.nsfw_model) throw new Error('nsfw_model not loaded');
    let tensor = tf.browser.fromPixels(image)
                .resizeBilinear([150, 150])
                .div(tf.scalar(255))
                .expandDims(0);

    const classification = await window.nsfw_model
                          .predict(tensor)
                          .data()
                          .then( (value) => 
                          { 
                            // Model was trained with inverted labels (nsfw=0, safe=1)
                            // Invert the prediction: NSFW score = 1 - model_output
                            return [1.0 - value[0]]; 
                          }
                          );
    
    // Clean up tensor
    tensor.dispose();
    
    return classification;
  } catch (e) {
    console.warn('NSFW model error, using fallback:', e);
    // Fallback: heuristic based on filename
    if(currentImageFile && /nsfw|nude|sexy|porn|spicy|bikini|lingerie|cleavage/i.test(currentImageFile.name)) return [0.95];
    return [0.02];
  }
}

const classifyText = async function(text){
  const max_length = 60;
  const tokens = text.split(" ");
  const word_index = await fetch('./models/text_model/word_index.json')
              .then(response => {
              return response.json();
              });
  let padded = new Array(max_length).fill(0);
  for (let i = 0; i < max_length; i++) {
      let tokenid = word_index[tokens[i].toLowerCase()]
      padded[i] = (tokenid === undefined)? 1 : tokenid;
      if(i == tokens.length-1)
          break;
  }
  let tensor = tf.tensor([padded]);
  
  const classification = await text_model
                          .predict(tensor)
                          .data()
                          .then( (value) => 
                          { return value; }
                          );
  return classification;
}



// Try to load TF.js models; silent fallback to demo mode if not possible.
const setupPage = async() => {
  let loadedCount = 0;
  try{
    scanIndicator.textContent = 'Loading models...';
    console.log('Loading text model...');
    window.text_model = await tf.loadLayersModel('./models/text_model/model.json');
    loadedCount++;
    console.log('✓ Text model loaded (1/3)');
    
    console.log('Loading image model...');
    window.image_model = await tf.loadLayersModel('./models/image_model/model.json');
    loadedCount++;
    console.log('✓ Image model loaded (2/3)');
    
    console.log('Loading NSFW model...');
    window.nsfw_model = await tf.loadLayersModel('./models/nsfw_model/model.json');
    loadedCount++;
    console.log('✓ NSFW model loaded (3/3)');
    
    scanIndicator.textContent = 'Models loaded (Document + NSFW)';
    console.log('✓ All models loaded successfully (3/3)');
  } catch (e){
    console.error(`Failed to load models (${loadedCount}/3 loaded):`, e);
    scanIndicator.textContent = `Partial load (${loadedCount}/3 models) - some features disabled`;
    // keep app usable; classification functions will fallback
  }
}

setupPage();

// Load examples manifest (if present) and render buttons dynamically
async function loadExamplesManifest(){
  const container = document.getElementById('examplesContainer');
  if(!container) return;
  try{
    const resp = await fetch('./assets/images/examples/manifest.json?v=' + Date.now());
    if(!resp.ok) return; // no manifest
    const list = await resp.json();
    if(!Array.isArray(list) || list.length === 0) return;
    list.forEach(p => {
      const btn = document.createElement('button');
      btn.className = 'example-generated-btn';
      const filename = p.split('/').pop();
      btn.textContent = filename;
      btn.onclick = () => loadExample(p);
      container.appendChild(btn);
    });
  } catch(e){ /* silently ignore */ }
}

loadExamplesManifest();

// UI actions
blurBtn.addEventListener('click', () => blurPreview());
hideBtn.addEventListener('click', async () => {
  if(!currentImageFile) return;
  await moveToHidden(currentImageFile, currentDetection);
  appendCompanionMessage('Moved to Hidden folder and encrypted locally.');
  updateHiddenList();
});
deleteBtn.addEventListener('click', () => {
  appendCompanionMessage('Image deleted (demo).');
  // For demo, just clear preview
  const img = document.getElementById('output');
  img.src = '';
  currentImageFile = null;
  currentDetection = null;
  actionsPanel.style.display = 'none';
  sensitiveBadge.style.display = 'none';
  nonSensitiveBadge.style.display = 'none';
  scanIndicator.textContent = 'No scan yet';
});

companionToggle.addEventListener('click', () => {
  companionBox.style.display = companionBox.style.display === 'none' ? 'block' : 'none';
});

companionInput.addEventListener('keydown', (e) => {
  if(e.key === 'Enter'){
    const q = companionInput.value.trim();
    companionInput.value = '';
    handleCompanionQuery(q);
  }
});

function appendCompanionMessage(msg, from='AI'){
  const el = document.createElement('div');
  el.className = 'msg';
  el.textContent = (from === 'AI' ? 'PicShield: ' : 'You: ') + msg;
  companionMessages.appendChild(el);
  companionMessages.scrollTop = companionMessages.scrollHeight;
}

async function handleCompanionQuery(q){
  appendCompanionMessage(q, 'User');
  if(!currentDetection) return appendCompanionMessage('No detection available for this image.');
  // Simple rule-based companion answers
  if(/why|reason/i.test(q)){
    appendCompanionMessage(`This image was flagged as ${currentDetection.detectionResults[0].label} with confidence ${(currentDetection.detectionResults[0].score*100).toFixed(0)}%.`);
  } else if(/what|action/i.test(q)){
    appendCompanionMessage(`Recommended action: ${currentDetection.actionRecommendation.recommendedAction}. Available: ${currentDetection.actionRecommendation.availableActions.join(', ')}`);
  } else if(/share|upload/i.test(q)){
    appendCompanionMessage('I will not upload this photo without your explicit permission. You can choose to allow cloud analysis per-image.');
  } else {
    appendCompanionMessage('I can explain the detection, blur, move to Hidden, or remove metadata. Try: "Why was this flagged?" or "Move to Hidden".');
  }
}

// Add SENSITIVE overlay label on top of blurred image
function addSensitiveOverlay(){
  let overlay = document.getElementById('sensitive-overlay');
  
  // Remove existing overlay if present
  if(overlay) overlay.remove();
  
  // Use the drag-area as the container since that's where the image is
  const dragArea = document.querySelector('.drag-area');
  const img = document.getElementById('output');
  if(!dragArea || !img) return;
  
  // Create overlay element
  overlay = document.createElement('div');
  overlay.id = 'sensitive-overlay';
  overlay.style.cssText = `
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: rgba(255, 0, 0, 0.85);
    color: white;
    padding: 15px 35px;
    font-size: 42px;
    font-weight: bold;
    border-radius: 10px;
    z-index: 1000;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.9);
    pointer-events: none;
    font-family: Arial, sans-serif;
    letter-spacing: 4px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  `;
  overlay.textContent = 'SENSITIVE';
  
  // Ensure container has position relative for absolute positioning to work
  if(window.getComputedStyle(dragArea).position === 'static') {
    dragArea.style.position = 'relative';
  }
  
  dragArea.appendChild(overlay);
}

// Remove SENSITIVE overlay
function removeSensitiveOverlay(){
  const overlay = document.getElementById('sensitive-overlay');
  if(overlay) overlay.remove();
}

// Simple blur preview implementation
function blurPreview(){
  const img = document.getElementById('output');
  if(!img) return;
  if(img.style.filter === 'blur(12px)'){
    img.style.filter = '';
    removeSensitiveOverlay();
    appendCompanionMessage('Preview unblurred.');
  } else {
    img.style.filter = 'blur(12px)';
    addSensitiveOverlay();
    appendCompanionMessage('Preview blurred.');
  }
}

// Minimal IndexedDB helper for storing encrypted files
function openDb(){
  return new Promise((resolve, reject) => {
    const req = indexedDB.open('picshield-db', 1);
    req.onupgradeneeded = () => {
      req.result.createObjectStore('hidden', { keyPath: 'id' });
    };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

async function getOrCreateKey(){
  // store raw key in IndexedDB (for demo). In a production app use WebAuthn/Keystore or wrapped keys.
  const db = await openDb();
  return new Promise((resolve, reject) => {
    const tx = db.transaction('hidden','readwrite');
    const store = tx.objectStore('hidden');
    const g = store.get('__meta_key__');
    g.onsuccess = async () => {
      if(g.result && g.result.key){
        const raw = Uint8Array.from(atob(g.result.key), c => c.charCodeAt(0));
        const k = await crypto.subtle.importKey('raw', raw.buffer, 'AES-GCM', true, ['encrypt','decrypt']);
        resolve(k);
      } else {
        const key = await crypto.subtle.generateKey({ name: 'AES-GCM', length: 256 }, true, ['encrypt','decrypt']);
        const exported = await crypto.subtle.exportKey('raw', key);
        const b64 = btoa(String.fromCharCode(...new Uint8Array(exported)));
        store.put({ id: '__meta_key__', key: b64 });
        tx.oncomplete = () => resolve(key);
      }
    };
    g.onerror = () => reject(g.error);
  });
}

async function moveToHidden(file, detection){
  const db = await openDb();
  const key = await getOrCreateKey();
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const fileBuf = await file.arrayBuffer();
  const encrypted = await crypto.subtle.encrypt({ name: 'AES-GCM', iv }, key, fileBuf);
  const entry = { id: Date.now().toString(), name: file.name, iv: Array.from(iv), data: new Uint8Array(encrypted), detection };
  return new Promise((resolve, reject) => {
    const tx = db.transaction('hidden','readwrite');
    const store = tx.objectStore('hidden');
    store.put(entry);
    tx.oncomplete = () => resolve(entry.id);
    tx.onerror = () => reject(tx.error);
  });
}

async function updateHiddenList(){
  const db = await openDb();
  const tx = db.transaction('hidden','readonly');
  const store = tx.objectStore('hidden');
  const req = store.getAll();
  req.onsuccess = () => {
    const items = req.result.filter(it => it.id !== '__meta_key__');
    if(items.length === 0) {
      hiddenList.textContent = '(empty)';
    } else {
      hiddenList.innerHTML = items.map(i => `
        <div class="hidden-item" data-id="${i.id}" style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
          <span style="flex:1;">${i.name}</span>
          <button onclick="previewHidden('${i.id}')">Preview</button>
          <button onclick="revealHidden('${i.id}')">Reveal</button>
          <button onclick="deleteHidden('${i.id}')">Delete</button>
        </div>
      `).join('');
    }
  };
}

openHiddenBtn.addEventListener('click', async () => updateHiddenList());

// Helpers to fetch a single hidden entry
async function getHiddenEntry(id){
  const db = await openDb();
  return new Promise((resolve, reject) => {
    const tx = db.transaction('hidden','readonly');
    const store = tx.objectStore('hidden');
    const r = store.get(id);
    r.onsuccess = () => resolve(r.result);
    r.onerror = () => reject(r.error);
  });
}

// Decrypt entry and return a Blob
async function decryptEntryToBlob(entry){
  const key = await getOrCreateKey();
  const iv = new Uint8Array(entry.iv);
  // entry.data may be stored as Uint8Array or as plain array
  let enc;
  if(entry.data instanceof Uint8Array) enc = entry.data.buffer;
  else enc = new Uint8Array(entry.data).buffer;
  const decrypted = await crypto.subtle.decrypt({ name: 'AES-GCM', iv }, key, enc);
  return new Blob([decrypted]);
}

// Preview a hidden item in the modal
window.previewHidden = async function(id){
  try{
    const entry = await getHiddenEntry(id);
    if(!entry) return appendCompanionMessage('Hidden item not found.');
    const blob = await decryptEntryToBlob(entry);
    const url = URL.createObjectURL(blob);
    const modal = document.getElementById('hiddenPreviewModal');
    const img = document.getElementById('hiddenPreviewImg');
    img.src = url;
    modal.style.display = 'flex';
    // attach actions
    document.getElementById('revealFromPreview').onclick = async () => { await revealHidden(id); modal.style.display='none'; };
    document.getElementById('deleteFromPreview').onclick = async () => { await deleteHidden(id); modal.style.display='none'; };
    document.getElementById('closeHiddenPreview').onclick = () => { modal.style.display = 'none'; URL.revokeObjectURL(url); };
  } catch(e){ console.error(e); appendCompanionMessage('Failed to preview hidden item.'); }
}

// Reveal (unhide) - decrypt and load back into main preview, then remove from hidden store
window.revealHidden = async function(id){
  try{
    const entry = await getHiddenEntry(id);
    if(!entry) return appendCompanionMessage('Hidden item not found.');
    const blob = await decryptEntryToBlob(entry);
    const file = new File([blob], entry.name, { type: blob.type || 'image/*' });
    // feed into the same loadFile flow
    const fauxEvent = { target: { files: [file] } };
    // remove from DB
    const db = await openDb();
    const tx = db.transaction('hidden','readwrite');
    tx.objectStore('hidden').delete(id);
    tx.oncomplete = () => { updateHiddenList(); appendCompanionMessage(`Revealed ${entry.name}`); };
    loadFile(fauxEvent);
  } catch(e){ console.error(e); appendCompanionMessage('Failed to reveal hidden item.'); }
}

// Delete hidden item permanently
window.deleteHidden = async function(id){
  try{
    const db = await openDb();
    const tx = db.transaction('hidden','readwrite');
    tx.objectStore('hidden').delete(id);
    tx.oncomplete = () => { updateHiddenList(); appendCompanionMessage('Hidden item deleted.'); };
    tx.onerror = () => appendCompanionMessage('Failed to delete hidden item.');
  } catch(e){ console.error(e); appendCompanionMessage('Failed to delete hidden item.'); }
}

// Privacy Center controls
const optPersonalization = document.getElementById('optPersonalization');
const optTelemetry = document.getElementById('optTelemetry');
const clearPersonalization = document.getElementById('clearPersonalization');
const cloudUploadBtn = document.getElementById('cloudUploadBtn');

// Load saved prefs
try {
  const p = localStorage.getItem('picshield_personalization');
  if(p === 'true') optPersonalization.checked = true;
  const t = localStorage.getItem('picshield_telemetry');
  if(t === 'true') optTelemetry.checked = true;
} catch (e) { /* ignore */ }

optPersonalization.addEventListener('change', (e) => {
  localStorage.setItem('picshield_personalization', e.target.checked ? 'true' : 'false');
  appendCompanionMessage(`Local personalization ${e.target.checked ? 'enabled' : 'disabled'}`);
});

optTelemetry.addEventListener('change', (e) => {
  localStorage.setItem('picshield_telemetry', e.target.checked ? 'true' : 'false');
  appendCompanionMessage(`Telemetry ${e.target.checked ? 'enabled' : 'disabled'}`);
});

clearPersonalization.addEventListener('click', () => {
  // demo: clear personalization signals
  localStorage.removeItem('picshield_personalization_data');
  appendCompanionMessage('Local personalization data cleared.');
});

cloudUploadBtn.addEventListener('click', async () => {
  // explicit consent flow for cloud upload (demo only)
  appendCompanionMessage('Cloud upload requested — asking for explicit consent.');
  const ok = confirm('This will upload the selected file to the cloud for analysis. No other photos will be uploaded. Proceed?');
  if(!ok) return appendCompanionMessage('Cloud analysis canceled.');
  // ask user to choose a file to upload
  const filePicker = document.createElement('input');
  filePicker.type = 'file';
  filePicker.accept = 'image/*';
  filePicker.onchange = async (ev) => {
    const f = ev.target.files[0];
    if(!f) return appendCompanionMessage('No file selected.');
    appendCompanionMessage(`Uploading ${f.name} to cloud (demo).`);
    // Demo: we do not actually upload. Show placeholder
    setTimeout(() => appendCompanionMessage('Cloud analysis complete (demo). No data left the device in this demo.)'), 1200);
  };
  filePicker.click();
});

// Examples gallery modal
const loadExamplesBtn = document.getElementById('loadExamplesBtn');
const examplesModal = document.getElementById('examplesModal');
const examplesGallery = document.getElementById('examplesGallery');
const closeExamplesModal = document.getElementById('closeExamplesModal');

loadExamplesBtn.addEventListener('click', async () => {
  // Fetch and render examples in modal
  try{
    const resp = await fetch('./assets/images/examples/manifest.json?v=' + Date.now());
    if(!resp.ok) return appendCompanionMessage('No examples available.');
    const list = await resp.json();
    if(!Array.isArray(list) || list.length === 0) return appendCompanionMessage('No examples found.');
    
    examplesGallery.innerHTML = '';
    list.forEach(path => {
      const container = document.createElement('div');
      container.style.cssText = 'cursor:pointer; border:2px solid #ddd; border-radius:6px; overflow:hidden; background:#f5f5f5;';
      
      const img = document.createElement('img');
      img.src = path;
      img.style.cssText = 'width:100%; height:120px; object-fit:cover; display:block;';
      img.onerror = () => { img.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="120" height="120"%3E%3Crect fill="%23ddd" width="120" height="120"/%3E%3Ctext x="50%25" y="50%25" dominant-baseline="middle" text-anchor="middle" fill="%23999" font-size="12"%3E(404)%3C/text%3E%3C/svg%3E'; };
      
      const label = document.createElement('div');
      label.style.cssText = 'padding:6px; font-size:0.75rem; text-align:center; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; background:#fff;';
      label.textContent = path.split('/').pop();
      
      container.appendChild(img);
      container.appendChild(label);
      container.onclick = () => {
        loadExample(path);
        examplesModal.style.display = 'none';
        appendCompanionMessage(`Loaded example: ${label.textContent}`);
      };
      examplesGallery.appendChild(container);
    });
    
    examplesModal.style.display = 'flex';
  } catch(e){
    console.error('Failed to load examples', e);
    appendCompanionMessage('Failed to load examples.');
  }
});

closeExamplesModal.addEventListener('click', () => {
  examplesModal.style.display = 'none';
});

// Global error handlers to surface errors in the UI for easier debugging
window.addEventListener('error', (ev) => {
  try{
    const msg = ev && ev.message ? ev.message : String(ev.error || ev);
    if(scanIndicator) scanIndicator.textContent = 'Error: ' + msg;
    appendCompanionMessage('JS Error: ' + msg);
    console.error('Global error', ev);
  }catch(e){ console.error(e); }
});

window.addEventListener('unhandledrejection', (ev) => {
  try{
    const reason = ev && ev.reason ? (ev.reason.message || String(ev.reason)) : 'Unhandled rejection';
    if(scanIndicator) scanIndicator.textContent = 'Error: ' + reason;
    appendCompanionMessage('Unhandled promise rejection: ' + reason);
    console.error('Unhandled rejection', ev);
  }catch(e){ console.error(e); }
});
