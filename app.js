// FarmGuard X - Plant Pathology AI Core Application Script (Offline-First PWA)

document.addEventListener('DOMContentLoaded', () => {

  // Register Service Worker for Offline Functionality
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('./sw.js')
      .then((reg) => {
        console.log('[FarmGuard X] Service Worker registered successfully:', reg.scope);
      })
      .catch((err) => {
        console.warn('[FarmGuard X] Service Worker registration failed:', err);
      });
  }

  // Network Status Monitor
  const offlineStatusBadge = document.getElementById('offlineStatusBadge');
  function updateOnlineStatus() {
    if (navigator.onLine) {
      if (offlineStatusBadge) {
        offlineStatusBadge.className = 'offline-badge';
        offlineStatusBadge.innerHTML = '🟢 Offline Engine Ready';
      }
    } else {
      if (offlineStatusBadge) {
        offlineStatusBadge.className = 'offline-badge is-offline';
        offlineStatusBadge.innerHTML = '⚡ Offline Mode Active';
      }
      showToast('📶 You are offline. FarmGuard X is running from local cache.');
    }
  }

  window.addEventListener('online', updateOnlineStatus);
  window.addEventListener('offline', updateOnlineStatus);
  updateOnlineStatus();

  // Preset Pathology Database
  const presets = {
    tomato_late_blight: {
      crop: "Tomato",
      prediction: "Tomato Late Blight",
      confidence: 97.4,
      category: "⚠️ High Severity Fungal Pathogen Detected",
      categoryColor: "var(--rose-danger)",
      symptoms: ["Dark brown spots", "Yellow leaf edges"],
      cause: "Phytophthora infestans",
      causeDetails: "Water mold / Oomycete pathogen spread via damp spores.",
      organicTitle: "Neem oil spray",
      organicDesc: "Apply cold-pressed Neem Oil emulsion (5ml per 1L of water with 1ml liquid soap). Spray thoroughly during early morning or evening hours every 3 days to suffocate spores and reduce fungal spread.",
      chemicalTitle: "Copper fungicide",
      chemicalDesc: "Apply Copper Hydroxide or Copper Oxychloride spray (2g per 1L water) every 5–7 days. Copper acts as a protective barrier on leaf tissue preventing germ tube penetration. Observe a 1-day harvest interval after application.",
      bioTitle: "Trichoderma Bio-Control & Canopy Pruning",
      bioDesc: "Perform soil root drenching with Trichoderma harzianum bio-fungicide to colonize roots. Prune bottom 30cm of lower leaves with dark brown spots to stop soil-splash spore inoculation.",
      precautions: "Avoid watering leaves",
      precautionsDetails: "Use drip irrigation to keep foliage dry and suppress sporulation.",
      expectedRecovery: "7–14 days",
      image: "assets/tomato_late_blight.jpg",
      box: { top: "25%", left: "20%", width: "55%", height: "50%" }
    },
    healthy_tomato: {
      crop: "Tomato",
      prediction: "Healthy Tomato Foliage",
      confidence: 99.1,
      category: "✅ Normal Growth & Vigorous Canopy",
      categoryColor: "var(--emerald-light)",
      symptoms: ["No lesion spots detected", "Vibrant green chlorosis test passed"],
      cause: "Optimal Nutrient Balance & High Solar Insolation",
      causeDetails: "Plant immune system active with zero pathogen load.",
      organicTitle: "Preventative Seaweed Extract",
      organicDesc: "Apply foliar seaweed kelp extract every 14 days to enhance thermal tolerance and cellular cell wall strength.",
      chemicalTitle: "No Chemical Action Needed",
      chemicalDesc: "Chemical fungicides are not required. Maintain standard micronutrient drip schedule.",
      bioTitle: "Mycorrhizal Inoculant",
      bioDesc: "Inoculate soil with beneficial endomycorrhizal fungi for enhanced phosphorus uptake.",
      precautions: "Maintain steady moisture",
      precautionsDetails: "Continue monitoring soil tensiometer levels to ensure steady hydration.",
      expectedRecovery: "Optimal Status",
      image: "assets/healthy_tomato.jpg",
      box: { top: "15%", left: "15%", width: "70%", height: "70%" }
    },
    corn_rust: {
      crop: "Corn",
      prediction: "Corn Common Rust",
      confidence: 94.8,
      category: "⚠️ Moderate Fungal Rust Outbreak",
      categoryColor: "var(--amber-warning)",
      symptoms: ["Reddish-brown pustules", "Upper leaf rust coating"],
      cause: "Puccinia sorghi",
      causeDetails: "Fungal spores airborne under high humidity and 16-24°C temperatures.",
      organicTitle: "Sulfur Dusting Spray",
      organicDesc: "Apply organic elemental sulfur dust on foliage during low-wind morning hours.",
      chemicalTitle: "Azoxystrobin Fungicide",
      chemicalDesc: "Apply QoI inhibitor fungicide at 150ml/acre to halt spore germination.",
      bioTitle: "Crop Airflow Management",
      bioDesc: "Improve row spacing and remove wild grass hosts from field perimeter.",
      precautions: "Ensure crop spacing",
      precautionsDetails: "Improve canopy air circulation and crop row spacing.",
      expectedRecovery: "10–18 days",
      image: "assets/tomato_late_blight.jpg",
      box: { top: "30%", left: "25%", width: "45%", height: "45%" }
    },
    potato_early_blight: {
      crop: "Potato",
      prediction: "Potato Early Blight",
      confidence: 92.5,
      category: "⚠️ Moderate Alternaria Lesions",
      categoryColor: "var(--amber-warning)",
      symptoms: ["Concentric ring spots", "Lower leaf chlorosis"],
      cause: "Alternaria solani",
      causeDetails: "Fungal pathogen targeting older foliage under stress.",
      organicTitle: "Compost Tea Spray",
      organicDesc: "Spray aerated compost tea weekly to populate leaf surface with beneficial microbes.",
      chemicalTitle: "Mancozeb 75% WP",
      chemicalDesc: "Apply protectant contact fungicide at 2g/L water every 7 days.",
      bioTitle: "Bacillus subtilis Foliar Shield",
      bioDesc: "Apply bio-fungicide Bacillus subtilis strain QST 713 to colonize foliage.",
      precautions: "Rotate crops annually",
      precautionsDetails: "Avoid planting Solanaceae crops in the same soil back-to-back.",
      expectedRecovery: "10–14 days",
      image: "assets/tomato_late_blight.jpg",
      box: { top: "20%", left: "30%", width: "50%", height: "50%" }
    }
  };

  let currentPreset = 'tomato_late_blight';

  // DOM Elements
  const dropZone = document.getElementById('dropZone');
  const previewImg = document.getElementById('previewImg');
  const scannerCard = document.getElementById('scannerCard');
  const triggerScanBtn = document.getElementById('triggerScanBtn');
  const boundingBox = document.getElementById('boundingBox');

  const predictionTitle = document.getElementById('predictionTitle');
  const predictionCategory = document.getElementById('predictionCategory');
  const confidenceValue = document.getElementById('confidenceValue');
  const gaugeCircle = document.getElementById('gaugeCircle');
  const symptomsList = document.getElementById('symptomsList');
  const likelyCauseText = document.getElementById('likelyCauseText');
  const precautionsText = document.getElementById('precautionsText');
  const expectedRecoveryText = document.getElementById('expectedRecoveryText');

  const organicTitle = document.getElementById('organicTitle');
  const organicDesc = document.getElementById('organicDesc');
  const chemicalTitle = document.getElementById('chemicalTitle');
  const chemicalDesc = document.getElementById('chemicalDesc');
  const bioTitle = document.getElementById('bioTitle');
  const bioDesc = document.getElementById('bioDesc');

  // Sidebar Navigation Smooth Scroll & Active Highlight
  document.querySelectorAll('.app-sidebar .nav-item').forEach(nav => {
    nav.addEventListener('click', (e) => {
      e.preventDefault();
      document.querySelectorAll('.app-sidebar .nav-item').forEach(n => n.classList.remove('active'));
      nav.classList.add('active');

      const targetId = nav.getAttribute('data-target');
      const targetElem = document.getElementById(targetId);
      if (targetElem) {
        targetElem.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // Trigger Scanning Sequence
  function runNeuralScan(presetKey) {
    currentPreset = presetKey || currentPreset;
    const data = presets[currentPreset];

    scannerCard.classList.add('is-scanning');
    showToast('⚡ Initializing Offline AI Scanning Engine...');

    setTimeout(() => {
      // Update Preview Image & Bounding Box
      previewImg.src = data.image;
      boundingBox.style.top = data.box.top;
      boundingBox.style.left = data.box.left;
      boundingBox.style.width = data.box.width;
      boundingBox.style.height = data.box.height;
      boundingBox.querySelector('.bounding-box-label').textContent = `${data.cause} (${data.confidence}%)`;

      // Update Hero Diagnosis Data
      predictionTitle.textContent = data.prediction;
      predictionCategory.textContent = data.category;
      predictionCategory.style.color = data.categoryColor;

      // Animate Confidence Counter
      animateConfidence(data.confidence);

      // Render Symptoms
      symptomsList.innerHTML = data.symptoms
        .map(s => `<li><span class="symptom-tag">• ${s}</span></li>`)
        .join('');

      likelyCauseText.textContent = data.cause;
      precautionsText.textContent = data.precautions;
      expectedRecoveryText.textContent = data.expectedRecovery;

      if (organicTitle) organicTitle.textContent = data.organicTitle;
      if (organicDesc) organicDesc.textContent = data.organicDesc;
      if (chemicalTitle) chemicalTitle.textContent = data.chemicalTitle;
      if (chemicalDesc) chemicalDesc.textContent = data.chemicalDesc;
      if (bioTitle) bioTitle.textContent = data.bioTitle;
      if (bioDesc) bioDesc.textContent = data.bioDesc;

      scannerCard.classList.remove('is-scanning');
      showToast(`✅ Diagnosis Complete: ${data.prediction} detected (${data.confidence}% confidence)`);

      // Recalculate dosage
      calculateDosage();
    }, 1500);
  }

  // Confidence Gauge Animation
  function animateConfidence(targetScore) {
    let currentScore = 0;
    const interval = setInterval(() => {
      currentScore += 2.5;
      if (currentScore >= targetScore) {
        currentScore = targetScore;
        clearInterval(interval);
      }
      confidenceValue.textContent = `${currentScore.toFixed(1)}%`;
      const offset = 251.2 - (251.2 * currentScore / 100);
      gaugeCircle.style.strokeDashoffset = offset;
    }, 30);
  }

  // Preset Chips Clicking
  document.querySelectorAll('.preset-chips .chip').forEach(chip => {
    chip.addEventListener('click', () => {
      document.querySelectorAll('.preset-chips .chip').forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      const presetKey = chip.getAttribute('data-preset');
      runNeuralScan(presetKey);
    });
  });

  // Re-Scan Trigger Button
  triggerScanBtn.addEventListener('click', () => runNeuralScan(currentPreset));

  // Drag & Drop File Handling
  dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
  });

  dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragover');
  });

  dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleUploadedFile(files[0]);
    }
  });

  dropZone.addEventListener('click', () => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.onchange = (e) => {
      if (e.target.files.length > 0) {
        handleUploadedFile(e.target.files[0]);
      }
    };
    input.click();
  });

  function handleUploadedFile(file) {
    const reader = new FileReader();
    reader.onload = (event) => {
      previewImg.src = event.target.result;
      showToast('📸 Custom image loaded. Running AI model analysis...');
      runNeuralScan('tomato_late_blight');
    };
    reader.readAsDataURL(file);
  }

  // Treatment Tabs Interactivity (Organic vs Chemical vs Bio)
  const treatmentTabs = document.querySelectorAll('.treatment-tabs .tab-btn');
  const treatmentContents = document.querySelectorAll('.treatment-content');
  const treatmentTypeSelect = document.getElementById('treatmentType');

  treatmentTabs.forEach(btn => {
    btn.addEventListener('click', () => {
      treatmentTabs.forEach(b => b.classList.remove('active'));
      treatmentContents.forEach(c => c.classList.remove('active'));
      
      btn.classList.add('active');
      const tabTarget = btn.getAttribute('data-treatment-tab');
      const targetContent = document.getElementById(`tab-${tabTarget}`);
      if (targetContent) {
        targetContent.classList.add('active');
      }

      // Sync calculator dropdown
      if (tabTarget === 'organic') {
        treatmentTypeSelect.value = 'neem';
      } else if (tabTarget === 'chemical') {
        treatmentTypeSelect.value = 'copper';
      }
      calculateDosage();

      showToast(`Switched view to ${btn.textContent.trim()}`);
    });
  });

  // Dosage Calculator Logic
  const landAreaInput = document.getElementById('landArea');
  const areaUnitSelect = document.getElementById('areaUnit');
  const calcOutput = document.getElementById('calcOutput');
  const waterMixOutput = document.getElementById('waterMixOutput');

  function calculateDosage() {
    const area = parseFloat(landAreaInput.value) || 1;
    const unit = areaUnitSelect.value;
    const treatment = treatmentTypeSelect.value;

    let acresMultiplier = 1;
    if (unit === 'hectares') acresMultiplier = 2.47105;
    if (unit === 'sqm') acresMultiplier = 0.000247105;

    const totalAcres = area * acresMultiplier;

    if (treatment === 'copper') {
      const chemicalKg = (totalAcres * 0.5).toFixed(2);
      const waterLiters = Math.round(totalAcres * 200);
      calcOutput.textContent = `${chemicalKg} kg`;
      waterMixOutput.textContent = `Mix with ${waterLiters} Liters of water (Rate: 2g/L)`;
    } else {
      const neemLiters = (totalAcres * 0.6).toFixed(2);
      const waterLiters = Math.round(totalAcres * 120);
      calcOutput.textContent = `${neemLiters} Liters`;
      waterMixOutput.textContent = `Mix with ${waterLiters} Liters of water + emulsifier`;
    }
  }

  landAreaInput.addEventListener('input', calculateDosage);
  areaUnitSelect.addEventListener('change', calculateDosage);
  treatmentTypeSelect.addEventListener('change', calculateDosage);

  // Spray Application Log Modal & Table Logic
  const openLogModalBtn = document.getElementById('openLogModalBtn');
  const closeLogModalBtn = document.getElementById('closeLogModalBtn');
  const cancelLogBtn = document.getElementById('cancelLogBtn');
  const logModal = document.getElementById('logModal');
  const sprayLogForm = document.getElementById('sprayLogForm');
  const sprayLogTableBody = document.getElementById('sprayLogTableBody');
  const logEntryCount = document.getElementById('logEntryCount');

  let logCount = 2;

  function toggleLogModal(show) {
    logModal.style.display = show ? 'flex' : 'none';
  }

  if (openLogModalBtn) openLogModalBtn.addEventListener('click', () => toggleLogModal(true));
  if (closeLogModalBtn) closeLogModalBtn.addEventListener('click', () => toggleLogModal(false));
  if (cancelLogBtn) cancelLogBtn.addEventListener('click', () => toggleLogModal(false));

  sprayLogForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const product = document.getElementById('logTreatmentProduct').value;
    const field = document.getElementById('logFieldBlock').value;
    const volume = document.getElementById('logVolume').value;

    const now = new Date();
    const dateStr = now.toISOString().split('T')[0] + ' (Just Now)';

    const newRow = document.createElement('tr');
    newRow.style.borderBottom = '1px solid rgba(255,255,255,0.04)';
    newRow.innerHTML = `
      <td style="padding: 8px;">${dateStr}</td>
      <td style="padding: 8px; color: var(--emerald-light); font-weight:600;">${product}</td>
      <td style="padding: 8px;">${field}</td>
      <td style="padding: 8px;">${volume}</td>
      <td style="padding: 8px;"><span class="symptom-tag" style="background:rgba(16,185,129,0.15); color:var(--emerald-light); border-color:var(--border-accent);">Completed</span></td>
    `;

    sprayLogTableBody.insertBefore(newRow, sprayLogTableBody.firstChild);
    logCount++;
    logEntryCount.textContent = `${logCount} Recorded Applications`;

    toggleLogModal(false);
    showToast(`📝 Logged application of ${product} to ${field}`);
  });

  // Task Checklist Interactivity & LocalStorage
  const taskChecks = document.querySelectorAll('.task-check');
  const checklistCount = document.getElementById('checklistCount');

  function updateChecklistProgress() {
    const total = taskChecks.length;
    const checkedCount = Array.from(taskChecks).filter(c => c.checked).length;
    checklistCount.textContent = `${checkedCount}/${total} Done`;
  }

  taskChecks.forEach(check => {
    check.addEventListener('change', () => {
      updateChecklistProgress();
      showToast(check.checked ? 'Task marked as completed ✅' : 'Task pending ⏳');
    });
  });

  // Search Disease Database
  const searchInput = document.getElementById('searchDatabase');
  const tableRows = document.querySelectorAll('#directoryTableBody tr');

  searchInput.addEventListener('input', (e) => {
    const query = e.target.value.toLowerCase();
    tableRows.forEach(row => {
      const text = row.textContent.toLowerCase();
      row.style.display = text.includes(query) ? '' : 'none';
    });
  });

  // Export / Print Report
  document.getElementById('printReportBtn').addEventListener('click', () => {
    window.print();
  });

  // Toast Notification System
  function showToast(message) {
    const toastContainer = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="color: var(--emerald-light);">
        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
        <polyline points="22 4 12 14.01 9 11.01"></polyline>
      </svg>
      <span>${message}</span>
    `;
    toastContainer.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(100%)';
      setTimeout(() => toast.remove(), 300);
    }, 3500);
  }

  // Initial Calculation
  calculateDosage();
  updateChecklistProgress();

});
