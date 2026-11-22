const selectLang = document.getElementById("targetLang");
const statusText = document.getElementById("status");

// Muat bahasa yang terakhir disimpan saat popup dibuka
chrome.storage.local.get(["targetLang"], (result) => {
  if (result.targetLang) {
    selectLang.value = result.targetLang;
  }
});

// Simpan bahasa baru setiap kali pengguna mengubah pilihan
selectLang.addEventListener("change", () => {
  const bahasaDipilih = selectLang.value;
  chrome.storage.local.set({ targetLang: bahasaDipilih }, () => {
    statusText.textContent = "Bahasa tersimpan!";
    setTimeout(() => {
      statusText.textContent = "";
    }, 1500);
  });
});