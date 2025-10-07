document.addEventListener('DOMContentLoaded', function() {
    const atv = document.getElementById('atividade')
    const form = document.getElementById('atividade_form')
    const resultado = document.getElementById('resultado')

    if (!form) return;

    form.addEventListener('submit', async function(event) {
        event.preventDefault();
        
        const textoDaNota = atv.value;
        if (!textoDaNota.trim()) {
            alert('Por favor, digite uma nota.');
            return;
        }

        resultado.innerHTML = 'Analisando texto...';

        try {
            const payload = {
                nota: textoDaNota
            };

            const response = await fetch('/predict/note', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            resultado.style.display = 'block';

            if (response.ok) {
                const prob = (data.probabilidade * 100).toFixed(2);
                const classe = data.previsao; 
            
                resultado.innerHTML = `<strong>Previsão:</strong> ${classe} <br>
                                          <strong>Probabilidade de ser 'urgente':</strong> ${prob}%`;
            } else {
                resultado.innerHTML = `<strong>Erro:</strong> ${data.erro}`;
            }

        } catch (error) {
            console.error('Erro na requisição:', error);
            resultado.innerHTML = '<strong>Erro de conexão com o servidor.</strong>';
        }
    });
});

