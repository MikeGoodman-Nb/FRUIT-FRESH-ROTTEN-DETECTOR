function triggerUpload() {
  document.getElementById("fileInput").click();
}

// SAAT PILIH FOTO
document.getElementById("fileInput").addEventListener("change", function () {
  const file = this.files[0];
  const previewImage = document.getElementById("previewImage");
  const uploadBtn = document.getElementById("uploadBtn");
  const processBtn = document.getElementById("processBtn");
  const changeBtn = document.getElementById("changeBtn");
  const resultText = document.getElementById("result");
  const analysisBox = document.getElementById("analysisBox");

  if (!file) return;

  const reader = new FileReader();
  reader.onload = function (e) {
    previewImage.src = e.target.result;

    uploadBtn.style.display = "none";
    processBtn.style.display = "block";
    changeBtn.style.display = "block";

    resultText.innerText = "";
    analysisBox.style.display = "none"; // sembunyikan analisis jika pilih foto baru
  };

  reader.readAsDataURL(file);
});

// RESET FOTO
function resetImage() {
  const fileInput = document.getElementById("fileInput");
  const previewImage = document.getElementById("previewImage");
  const uploadBtn = document.getElementById("uploadBtn");
  const processBtn = document.getElementById("processBtn");
  const changeBtn = document.getElementById("changeBtn");
  const resultText = document.getElementById("result");
  const analysisBox = document.getElementById("analysisBox");

  previewImage.src = "assets/Image.png";
  resultText.innerText = "";
  fileInput.value = "";

  uploadBtn.style.display = "block";
  processBtn.style.display = "none";
  changeBtn.style.display = "none";

  analysisBox.style.display = "none";

  fileInput.click(); // langsung buka file explorer
}

// PROSES PREDIKSI
async function uploadImage() {
  const fileInput = document.getElementById("fileInput");
  const processBtn = document.getElementById("processBtn");
  const changeBtn = document.getElementById("changeBtn");
  const analysisBox = document.getElementById("analysisBox");
  const categoryBox = document.getElementById("categoryBox");
  const confidenceFill = document.getElementById("confidenceFill");
  const confidenceValue = document.getElementById("confidenceValue");
  const resultText = document.getElementById("result");

  if (!fileInput.files.length) {
    resultText.innerText = "Please choose an image.";
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  try {
    resultText.innerText = "Processing...";

    const response = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      resultText.innerText = "Server error.";
      return;
    }

    const data = await response.json();

    // SEMBUNYIKAN tombol
    processBtn.style.display = "none";
    changeBtn.style.display = "none";

    // TAMPILKAN BOX ANALISIS
    analysisBox.style.display = "block";

    // 1. Tentukan kategori final
    let category = "";
    if (data.class === "fresh") {
      category = "Segar";
    } else if (data.class === "rotten") {
      category = "Tidak Layak";
    } else {
      category = "Layu"; // fallback
    }

    categoryBox.innerText = "Kategori: " + category;

    // 2. Bar confidence gradasi
    const conf = parseFloat(data.confidence);
    const percent = conf * 100;

    confidenceFill.style.width = percent + "%";

    // Warna gradasi: hijau → kuning → merah
    confidenceFill.style.background = `
      linear-gradient(90deg,
      green 0%,
      yellow 50%,
      red 100%)
    `;

    confidenceValue.innerText = `Confidence Score: ${percent.toFixed(2)}%`;

    resultText.innerText = "";
  } catch (err) {
    resultText.innerText = "Connection error.";
  }
}
