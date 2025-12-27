// Cookie Consent Logic
document.addEventListener('DOMContentLoaded', () => {
  const consentBanner = document.getElementById('cookie-consent');
  const btnAccept = document.getElementById('btn-accept');
  const btnDecline = document.getElementById('btn-decline');

  if (!consentBanner || !btnAccept || !btnDecline) return;

  // Check if user has already made a choice
  const consent = localStorage.getItem('cookie-consent');

  if (!consent) {
    // Show banner
    consentBanner.classList.remove('hidden');
  }

  btnAccept.addEventListener('click', () => {
    localStorage.setItem('cookie-consent', 'accepted');
    consentBanner.classList.add('hidden');
  });

  btnDecline.addEventListener('click', () => {
    localStorage.setItem('cookie-consent', 'declined');
    consentBanner.classList.add('hidden');
  });
});
