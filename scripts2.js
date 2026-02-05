/* script.js
   JS is used ONLY for:
   1) switching visible page (login <-> create)
   2) validating create-account password (exactly 6 digits) and confirm match
   Nothing else is performed by JS.
*/

(function () {
  // Page switching
  const toCreateBtn = document.getElementById('toCreateBtn');
  const toLoginBtn = document.getElementById('toLoginBtn');
  const loginPage = document.getElementById('loginPage');
  const createPage = document.getElementById('createPage');

  function showCreate() {
    loginPage.classList.remove('active');
    loginPage.setAttribute('aria-hidden', 'true');
    createPage.classList.add('active');
    createPage.setAttribute('aria-hidden', 'false');
  }

  function showLogin() {
    createPage.classList.remove('active');
    createPage.setAttribute('aria-hidden', 'true');
    loginPage.classList.add('active');
    loginPage.setAttribute('aria-hidden', 'false');
  }

  toCreateBtn && toCreateBtn.addEventListener('click', showCreate);
  toLoginBtn && toLoginBtn.addEventListener('click', showLogin);

  // Password validation only (exactly 6 digits) on create-account form
  const accountForm = document.getElementById('accountForm');
  if (accountForm) {
    accountForm.addEventListener('submit', function (evt) {
      // Clear previous errors
      document.getElementById('accPasswordErr').innerText = '';
      document.getElementById('accConfirmErr').innerText = '';
      document.getElementById('accMobileErr').innerText = '';

      const pass = document.getElementById('accPassword').value.trim();
      const confirm = document.getElementById('accConfirm').value.trim();
      const mobile = document.getElementById('accMobile').value.trim();

      // Optional: check mobile minimal format here (not required by you, but helpful)
      if (mobile && (!/^\d{10}$/.test(mobile))) {
        evt.preventDefault();
        document.getElementById('accMobileErr').innerText = 'Enter a valid 10-digit mobile number.';
        return;
      }

      if (!/^\d{6}$/.test(pass)) {
        evt.preventDefault();
        document.getElementById('accPasswordErr').innerText = 'Password must be exactly 6 digits.';
        return;
      }

      if (pass !== confirm) {
        evt.preventDefault();
        document.getElementById('accConfirmErr').innerText = 'Passwords do not match.';
        return;
      }

      // If validation passes, allow normal form submission to server.
    });
  }
})();
