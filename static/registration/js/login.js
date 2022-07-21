$(function () {
  // load stored credentials from localStorage
  const rememberMe = $('#remember-me');
  const phoneNumber = $('#id_username');
  const password = $('#id_password');
  const storedRememberMe = localStorage.getItem('loginRememberMe');
  const storedPhoneNumber = localStorage.getItem('loginPhoneNumber');
  const storedPassword = localStorage.getItem('loginPassword');
  phoneNumber.val(storedPhoneNumber);
  password.val(storedPassword);
  rememberMe.prop('checked', Boolean(storedRememberMe));

  const loginForm = $('#login-form');
  loginForm.submit(() => {
    if (rememberMe.prop('checked')) {
      localStorage.setItem('loginPhoneNumber', phoneNumber.val());
      localStorage.setItem('loginPassword', password.val());
      localStorage.setItem('loginRememberMe', '1');
    } else {
      localStorage.removeItem('loginPhoneNumber');
      localStorage.removeItem('loginPassword');
      localStorage.removeItem('loginRememberMe');
    }
  });
});