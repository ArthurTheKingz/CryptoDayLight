function buscar() {
  const crypto = document.getElementById('crypto').value.trim().toLowerCase();
  if (!crypto) {
    alert('Digite uma criptomoeda');
    return;
  }

  fetch(`/api/price?crypto=${crypto}`)
    .then(res => res.json())
    .then(data => {
      if (data.error) {
        document.getElementById('resultado').innerHTML = data.error;
      } else {
        document.getElementById('resultado').innerHTML = `
          <h3>${data.name} (${data.symbol})</h3>
          💰 Preço: $${data.price_usd} USD<br>
          💶 Preço: €${data.price_eur} EUR<br>
          💵 Preço: R$${data.price_brl} BRL<br>
          📈 Variação 24h: ${data.change24h}%<br>
          🏦 MarketCap: $${data.marketCap}<br>
          🔥 Volume 24h: $${data.volume24h}<br>
        `;
      }
    })
    .catch(() => {
      document.getElementById('resultado').innerHTML = '❌ Erro na consulta';
    });
}