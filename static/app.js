// All page behaviour lives here so the Content-Security-Policy can forbid inline scripts.
document.addEventListener("DOMContentLoaded", function () {
  var file = document.getElementById("file"), fname = document.getElementById("fname");
  if (file) file.addEventListener("change", function () {
    fname.textContent = file.files[0] ? file.files[0].name : "Choose a CSV file";
  });
  var thr = document.getElementById("thr"), tv = document.getElementById("tv");
  if (thr) thr.addEventListener("input", function () { tv.textContent = parseFloat(thr.value).toFixed(2); });
  var form = document.getElementById("f"), go = document.getElementById("go");
  if (form) form.addEventListener("submit", function () { go.textContent = "Analysing…"; });
  var pb = document.getElementById("printBtn");
  if (pb) pb.addEventListener("click", function () { window.print(); });
  document.querySelectorAll("form[data-confirm]").forEach(function (f) {
    f.addEventListener("submit", function (e) { if (!confirm(f.dataset.confirm)) e.preventDefault(); });
  });
});
