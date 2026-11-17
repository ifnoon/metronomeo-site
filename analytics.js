(() => {
  const measurement = 'G-DNJX7KFH00';
  const key = 'metronomeo-analytics';
  let active = false;
  const readChoice = () => { try { return localStorage.getItem(key); } catch { return null; } };
  function enable() {
    if (active) return;
    active = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window['ga-disable-' + measurement] = false;
    window.gtag('js', new Date());
    window.gtag('config', measurement, {allow_google_signals: false, allow_ad_personalization_signals: false, page_location: location.origin + location.pathname});
    const script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=' + measurement;
    document.head.append(script);
  }
  function choose(value) {
    try { localStorage.setItem(key, value); } catch {}
    document.querySelector('.analytics-choice')?.remove();
    if (value === 'yes') enable();
    else {
      window['ga-disable-' + measurement] = true;
      document.cookie.split(';').forEach(cookie => {
        const name = cookie.split('=')[0].trim();
        if (!name.startsWith('_ga')) return;
        ['', ';domain=' + location.hostname, ';domain=.' + location.hostname].forEach(domain => {
          document.cookie = name + '=;Max-Age=0;path=/' + domain + ';SameSite=Lax';
        });
      });
    }
  }
  function showChoice() {
    if (document.querySelector('.analytics-choice')) return;
    const aside = document.createElement('aside');
    aside.className = 'analytics-choice';
    aside.setAttribute('aria-label', 'Website analytics preferences');
    aside.innerHTML = '<p>Help us improve this site with optional analytics. <a href="/privacy.html#website">Privacy</a></p><div><button type="button" data-choice="no">No thanks</button><button type="button" data-choice="yes">Allow analytics</button></div>';
    aside.querySelectorAll('button').forEach(button => button.addEventListener('click', () => choose(button.dataset.choice)));
    document.body.append(aside);
  }
  const choice = readChoice();
  if (choice === 'yes') enable();
  else if (choice === null) showChoice();
  document.querySelectorAll('a[href*="apps.apple.com/app/metronomeo/"]').forEach(link => {
    link.addEventListener('click', () => {
      if (active && !window['ga-disable-' + measurement]) window.gtag('event', 'app_store_click', {link_url: link.href, link_text: link.textContent.trim(), transport_type: 'beacon'});
    });
  });
  const preferences = document.createElement('button');
  preferences.type = 'button';
  preferences.className = 'analytics-settings';
  preferences.textContent = 'Cookie settings';
  preferences.addEventListener('click', showChoice);
  const footer = document.querySelector('footer');
  if (footer) footer.append(preferences);
  else { const area = document.createElement('footer'); area.className = 'wrap'; area.append(preferences); document.body.append(area); }
})();
