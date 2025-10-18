## Leitor de Tela em Python

Este projeto implementa um leitor de tela básico em Python, utilizando as seguintes bibliotecas:

* **pyautogui:** Para capturar a tela.
* **google.generativeai:** Para interagir com o modelo Gemini e obter descrições das imagens.
* **os:** Para manipulação de arquivos e diretórios.
* **time:** Para controle de tempo.
* **uuid:** Para gerar identificadores únicos para os arquivos temporários.
* **gtts:** Para converter texto em fala.
* **playsound:** Para reproduzir o áudio gerado.
* **keyboard:** Para detectar o pressionamento de teclas.

### Funcionalidades

* Captura a tela quando o usuário pressiona Ctrl+Shift.
* Envia a imagem capturada para o modelo Gemini.
* Recebe uma descrição da imagem do modelo.
* Converte a descrição em fala utilizando gTTS.
* Reproduz a fala gerada para o usuário.

### Pré-requisitos

* Python 3.x
* Bibliotecas listadas acima (instale com `pip install pyautogui google-generative-ai gtts playsound keyboard`)
* Uma chave de API válida para o Google Generative AI.
* Configure a variável de ambiente `GOOGLE_API_KEY` com sua chave de API.

### Como usar

1. Clone ou baixe este repositório.
2. Instale as dependências: `pip install -r requirements.txt`
3. Execute o script: `python screen_reader.py`
4. Pressione Ctrl+Shift para capturar a tela e ouvir a descrição.

### Observações

* O script cria uma pasta `temp` para armazenar arquivos temporários.
* Certifique-se de ter uma conexão com a internet para utilizar o modelo Gemini.
* O modelo Gemini pode levar alguns segundos para gerar a descrição.
* A qualidade da descrição depende da complexidade da imagem capturada.

### Melhorias Possíveis

* Adicionar suporte para outros idiomas além do português.
* Implementar recursos de acessibilidade mais avançados, como navegação por elementos da tela.
* Otimizar o desempenho para telas maiores ou com muitos elementos.
* Adicionar uma interface gráfica para facilitar a configuração e o uso.

**Aviso:** Este é um projeto experimental e pode conter bugs ou limitações. Use por sua conta e risco.

**Contribuições são bem-vindas!** Se você tiver alguma sugestão, correção ou melhoria, sinta-se à vontade para abrir uma issue ou pull request.

**Licença:** Este projeto é licenciado sob a licença MIT. Consulte o arquivo LICENSE para mais detalhes.