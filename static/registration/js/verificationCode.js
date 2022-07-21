const initTimer = (limitationTtl) => {
  const resendButton = $('#resend-code');

  const countDownDate = new Date(Date.now() + limitationTtl * 1000);

  let timeLeft;
  const updateUI = () => {
    const now = new Date().getTime();
    timeLeft = countDownDate - now;

    const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);

    const timer = `${minutes.toString()}:${seconds.toString()}`
    resendButton.text(timer);
  }

  updateUI();
  resendButton.prop('disabled', true);
  const timerInterval = setInterval(() => {
    updateUI();
    if (timeLeft < 0) {
      clearInterval(timerInterval);
      resendButton.prop('disabled', false);
      resendButton.text('ارسال دوباره کد');
    }
  }, 1000);
}

$(function () {
  const resendButton = $('#resend-code');
  const retryAfter = resendButton.data('retry-after');
  if (retryAfter > 0)
    initTimer(retryAfter);

  resendButton.click((e) => {
    $.ajax({
      url: '/users/send_code/',
      success(res) {
        initTimer(120);
      },
      error(err) {
        if (err.status === 429) {
          initTimer(err.getResponseHeader('Retry-After'));
        }
      },
    });
  });
});