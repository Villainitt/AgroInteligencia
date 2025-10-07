document.addEventListener('DOMContentLoaded', function() {
    const img = document.getElementById('imagem')
    const resultado = document.getElementById('resultado_img')
    const botao = document.getElementById('btn')

    let arquivoImg = null;

    img.addEventListener('change', function(event) {
        arquivoImg = event.target.files[0];
        if (arquivoImg) {
            console.log(`Arquivo selecionado: ${arquivoImg.name}`);
            resultado.innerHTML = '';
        }
    }); 

    botao.addEventListener('click', async function () {
        if (!arquivoImg) {
            alert('Por favor selecione uma imagem');
            return;
        }

        resultado.innerHTML = "Analisando imagem...";

        try {
            const base64String = await toBase64(arquivoImg);
            const payload = {
                image_base64: base64String
            };

            const response = await fetch ('/predict/leaf_image', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            console.log('Resposta do servidor:', response);

            const data = await response.json();

            console.log('Dados recebidos (objeto data):', data);

            if (response.ok) {
                resultado.innerHTML = `<strong>Previsão:</strong> ${data.previsao} <br>
                                        <strong>Probabilidade</strong> ${(data.probabilidade * 100).toFixed(2)}`;
            } else {
                resultado.innerHTML = `<strong>ERRO:</strong> ${data.erro}`;
            }
        } catch (error) {
            resultado.style.display = 'block';
            resultado.innerHTML = `<strong>Erro de conexão:</strong> não foi possível contatar o servidor`;
            console.error('Erro no fetch', error);
        }

    });

    function toBase64(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = () => {
                const base64 = reader.result.split(',')[1];
                resolve(base64);
            };
            reader.onerror = error => reject(error);
        });
    }

});