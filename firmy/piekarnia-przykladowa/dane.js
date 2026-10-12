window.DANE = {
  firma: 'Piekarnia Przykładowa',
  hero: { nad: 'Piekarnia rzemieślnicza', tytul: 'Chleb, na który się czeka', opis: 'Pieczemy codziennie od rana. Chleb na zakwasie, bułki, drożdżówki i torty na zamówienie.' },
  oferta: ['Chleb na zakwasie', 'Bułki i drożdżówki', 'Torty na zamówienie', 'Zamówienia na rano'],
  opinie: [
    { tekst: 'Najlepszy żytni w okolicy, zawsze jeszcze ciepły.', autor: 'Ania, klientka' },
    { tekst: 'Tort na urodziny gotowy dokładnie na czas.', autor: 'Marek, klient' }
  ],
  pokaz: ['Pokazujemy Państwa firmę w działającym prototypie.', 'Można w nim zadać pytanie asystentowi.', 'Kreator zbiera zamówienie i wysyła je do właściciela.'],
  czat: {
    powitanie: 'Dzień dobry! Jestem asystentem Piekarni Przykładowej. W czym pomóc?',
    podpowiedzi: ['Godziny otwarcia', 'Tort na zamówienie'],
    odpowiedzi: [
      { slowa: ['godzin', 'otwar'], tekst: 'Jesteśmy czynni od poniedziałku do soboty od szóstej rano.' },
      { slowa: ['tort', 'zamówieni'], tekst: 'Torty przyjmujemy z trzydniowym wyprzedzeniem.' }
    ],
    domyslna: 'Zostaw numer, oddzwonimy jeszcze dziś.'
  },
  kreator: { kroki: [
    { pytanie: 'Co zamawiasz?', opcje: ['Tort', 'Chleb na rano', 'Ciasta na przyjęcie', 'Dla firmy'] },
    { pytanie: 'Na kiedy?', opcje: ['Jutro', 'W tym tygodniu', 'Później'] }
  ] },
  stopka: 'Piekarnia Przykładowa, ul. Przykładowa 1, Miasto Testowe. Prototyp demonstracyjny.'
};
