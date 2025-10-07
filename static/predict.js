document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('pred_form')
    const resultadoDiv = document.getElementById('resultado')

    if (!form) return;

    form.addEventListener('submit', async function(event) {
        event.preventDefault();

        const dadosRecebidos = {
            precipitacao: parseFloat(document.getElementById('precipitacao').value),
            temperatura_max: parseFloat(document.getElementById('temperatura_max').value),
            temperatura_min: parseFloat(document.getElementById('temperatura_min').value),
            elevacao: parseFloat(document.getElementById('elevacao').value)
        };

        try {
            const response = await fetch('/predict/soildata', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(dadosRecebidos)
            });

            const resultado = await response.json();
            
            resultadoDiv.style.display = 'block';

            if (response.ok) {
                const prob = (resultado.probabilidade * 100).toFixed(2);
                if (resultado.previsao === 'rendimento_alto') {
                    resultadoDiv.className = 'alto'; 
                    resultadoDiv.innerHTML = `<strong>Previsão:</strong> Rendimento Alto<br><strong>Probabilidade:</strong> ${prob}%`;
                } else {
                    resultadoDiv.className = 'baixo';
                    resultadoDiv.innerHTML = `<strong>Previsão:</strong> Rendimento Baixo<br><strong>Probabilidade de ser alto:</strong> ${prob}%`;
                }
            } else {
                resultadoDiv.className = 'baixo';
                resultadoDiv.innerHTML = `<strong>ERRO:</strong> ${resultado.erro}`;
            }
        } catch (error) {
            resultadoDiv.style.display = 'block';
            resultadoDiv.className = 'baixo';
            resultadoDiv.innerHTML = `<strong>Erro de conexão:</strong> Não foi possível contatar o servidor.`;
            console.error('Erro no fetch:', error);
        }
        
    });

});