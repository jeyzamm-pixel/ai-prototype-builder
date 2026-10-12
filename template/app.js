(function () {
  var D = window.DANE || {};
  var $ = function (id) { return document.getElementById(id); };
  var ma = {
    hero: !!D.hero, oferta: !!(D.oferta && D.oferta.length), opinie: !!(D.opinie && D.opinie.length),
    pokaz: !!(D.pokaz && D.pokaz.length), czat: !!D.czat, kreator: !!(D.kreator && D.kreator.kroki && D.kreator.kroki.length)
  };
  // Sekcja bez danych sama znika.
  Object.keys(ma).forEach(function (k) {
    document.querySelectorAll('[data-sekcja="' + k + '"]').forEach(function (el) { if (!ma[k]) el.remove(); });
  });
  document.title = D.firma || 'Prototyp';
  if (ma.hero) { $('h-nad').textContent = D.hero.nad || D.firma; $('h-tytul').textContent = D.hero.tytul; $('h-opis').textContent = D.hero.opis || ''; }
  if (ma.oferta) D.oferta.forEach(function (t) { var li = document.createElement('li'); li.textContent = t; $('oferta-lista').appendChild(li); });
  if (ma.opinie) D.opinie.forEach(function (o) {
    var d = document.createElement('div'); d.className = 'opinia';
    var t = document.createElement('span'); t.textContent = o.tekst; var a = document.createElement('small'); a.textContent = o.autor;
    d.appendChild(t); d.appendChild(document.createElement('br')); d.appendChild(a); $('opinie-lista').appendChild(d);
  });
  if (ma.pokaz) D.pokaz.forEach(function (t) { var li = document.createElement('li'); li.textContent = t; $('pokaz-lista').appendChild(li); });
  $('stopka').textContent = D.stopka || '';

  if (ma.czat) {
    $('czat-nazwa').textContent = 'Asystent: ' + D.firma;
    var log = $('czat-log');
    var say = function (t, kto) { var m = document.createElement('div'); m.className = 'm ' + kto; m.textContent = t; log.appendChild(m); log.scrollTop = log.scrollHeight; };
    // Czat bez LLM: odpowiedzi ze słów kluczowych z dane.js.
    var odpowiedz = function (q) {
      q = q.toLowerCase();
      var o = D.czat.odpowiedzi.filter(function (r) { return r.slowa.some(function (s) { return q.indexOf(s) >= 0; }); })[0];
      return o ? o.tekst : D.czat.domyslna;
    };
    var pytaj = function (q) { say(q, 'u'); say(odpowiedz(q), 'b'); };
    say(D.czat.powitanie, 'b');
    D.czat.podpowiedzi.forEach(function (p) {
      var b = document.createElement('button'); b.type = 'button'; b.textContent = p; b.onclick = function () { pytaj(p); }; $('czat-pod').appendChild(b);
    });
    $('czat-form').onsubmit = function (e) { e.preventDefault(); var v = $('czat-in').value.trim(); if (v) { pytaj(v); $('czat-in').value = ''; } };
  }

  if (ma.kreator) {
    var krok = 0, odp = [];
    var rysuj = function () {
      var k = D.kreator.kroki[krok];
      $('k-krok').textContent = 'Krok ' + (krok + 1) + ' z ' + D.kreator.kroki.length + ': ' + k.pytanie;
      $('k-opcje').textContent = '';
      k.opcje.forEach(function (o) {
        var b = document.createElement('button'); b.type = 'button'; b.textContent = o;
        b.onclick = function () { odp.push(o); krok++; krok < D.kreator.kroki.length ? rysuj() : koniec(); };
        $('k-opcje').appendChild(b);
      });
    };
    var koniec = function () {
      $('k-opcje').textContent = ''; $('k-krok').textContent = 'Podsumowanie';
      $('k-wynik').textContent = odp.join(', ') + '. Zgłoszenie wysyłamy teraz. Cenę poda człowiek po rozmowie.';
      // Kreator naprawdę wysyła zgłoszenie (webhook z dane.js), ale nigdy nie podaje ceny.
      if (D.kreator.webhook) fetch(D.kreator.webhook, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ firma: D.firma, odpowiedzi: odp }) }).catch(function () {});
      window.__zgloszenie = { firma: D.firma, odpowiedzi: odp };
    };
    $('b-kreator').onclick = function () { krok = 0; odp = []; $('k-wynik').textContent = ''; $('kreator').hidden = false; rysuj(); };
  }
  window.__sekcje = ma;
})();
