// static/js/scripts.js
// Validation-only script + simple SPA page switcher

// helper
const $ = id => document.getElementById(id);

// validators
function isDigitsOnly(s){ return /^\d+$/.test(String(s)); }
function isTenDigits(s){ return /^\d{10}$/.test(String(s)); }

// clear listed element texts
function clearAllMessages(){
  ['accNameErr','accMobileErr','accPasswordErr','accConfirmErr','accSuccess',
   'trNameErr','trPasswordErr','trAmountErr','trSuccess','balancesSummary'].forEach(id=>{
    const el = $(id);
    if(el) el.textContent = '';
  });
}

// SPA page switcher (only toggles sections that exist in the current document)
function showPage(id) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  const target = document.getElementById(id);
  if (target) target.classList.add('active');
}

// small helper to safely set text
function setText(id, text){
  const el = $(id);
  if(el) el.textContent = text;
}

// prevent double-submit helper
function disableButton(btn){
  if(!btn) return;
  btn.disabled = true;
  btn.dataset._origText = btn.textContent;
  btn.textContent = 'Submitting...';
}

// restore submit button (not strictly necessary after redirect)
function restoreButton(btn){
  if(!btn) return;
  btn.disabled = false;
  if(btn.dataset._origText) btn.textContent = btn.dataset._origText;
}

// clear specific error on input (nice UX)
function attachClearOnInput(ids){
  ids.forEach(id=>{
    const el = $(id);
    if(el) el.addEventListener('input', () => {
      const err = document.getElementById(id + 'Err');
      if(err) err.textContent = '';
    });
  });
}

// ---------- Account form validation (works on both index or separate page) ----------
(function setupAccountValidation(){
  const accountForm = $('accountForm');
  if(!accountForm) return;

  attachClearOnInput(['accName','accMobile','accPassword','accConfirm']);

  accountForm.addEventListener('submit', function(e){
    // collect inputs safely
    const name = ($('accName')||{value:''}).value.trim();
    const mobile = ($('accMobile')||{value:''}).value.trim();
    const pass = ($('accPassword')||{value:''}).value.trim();
    const confirm = ($('accConfirm')||{value:''}).value.trim();

    // clear
    setText('accNameErr','');
    setText('accMobileErr','');
    setText('accPasswordErr','');
    setText('accConfirmErr','');
    setText('accSuccess','');

    let valid = true;

    if(name === '') { setText('accNameErr','Enter your name'); valid = false; }
    if(!isTenDigits(mobile)) { setText('accMobileErr','Mobile must be exactly 10 digits'); valid = false; }
    if(!isDigitsOnly(pass)) { setText('accPasswordErr','Password must contain digits only'); valid = false; }
    if(pass !== confirm) { setText('accConfirmErr','Passwords do not match'); valid = false; }

    if(!valid){
      e.preventDefault();
      // keep submit button enabled so user can fix
    } else {
      // allow native submit: disable submit button to avoid double click
      const submitBtn = accountForm.querySelector('button[type="submit"]');
      disableButton(submitBtn);
      setText('accSuccess','Validation passed — submitting...');
      // do NOT call e.preventDefault()
    }
  });
})();

// ---------- Transfer form validation ----------
(function setupTransferValidation(){
  const transferForm = $('transferForm');
  if(!transferForm) return;

  attachClearOnInput(['trName','trPassword','trAmount']);

  transferForm.addEventListener('submit', function(e){
    const name = ($('trName')||{value:''}).value.trim();
    const password = ($('trPassword')||{value:''}).value.trim();
    const amountRaw = ($('trAmount')||{value:''}).value;

    // clear
    setText('trNameErr','');
    setText('trPasswordErr','');
    setText('trAmountErr','');
    setText('trSuccess','');

    let ok = true;
    if(name === '') { setText('trNameErr','Enter your name'); ok = false; }
    if(password === '') { setText('trPasswordErr','Enter password'); ok = false; }
    else if(!isDigitsOnly(password)) { setText('trPasswordErr','Password must be digits only'); ok = false; }

    const amount = Number(amountRaw);
    if(!amountRaw || isNaN(amount) || amount <= 0) { setText('trAmountErr','Enter a valid amount (> 0)'); ok = false; }

    if(!ok){
      e.preventDefault();
    } else {
      const submitBtn = transferForm.querySelector('button[type="submit"]');
      disableButton(submitBtn);
      setText('trSuccess','Validation passed — submitting...');
      // allow native submit
    }
  });
})();
//######################################3
// document.addEventListener("DOMContentLoaded", () => {
//   const ctx = document.getElementById("weeklyChart");
//   if (!ctx) return;

//   const weeks = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
//   const amounts = window.weeklyAmounts || [0, 0, 0, 0, 0, 0, 0];

//   new Chart(ctx, {
//     type: "bar",
//     data: {
//       labels: weeks,
//       datasets: [{
//         label: "Weekly Spend",
//         data: amounts
//       }]
//     },
//     options: {
//       responsive: true,
//       plugins: {
//         tooltip: {
//           enabled: true
//         }
//       }
//     }
//   });
// });



//############3333

// Expose showPage globally in case template uses inline onclick handlers
window.showPage = showPage;
