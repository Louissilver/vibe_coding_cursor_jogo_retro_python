# Moon Cresta - Clone em Python

## Sobre o Projeto

Este é um clone do clássico jogo Moon Cresta, desenvolvido em Python com a biblioteca Pygame. O projeto foi criado usando a IDE Cursor com auxílio de IA para gerar um jogo no estilo fixed shooter com mecânicas de progressão únicas.

## Características

- **Sistema de Estágios**: A nave evolui após cada fase completada
- **Três Níveis**: Dificuldade progressiva com diferentes inimigos
- **Gráficos Adaptativos**: Usa sprites personalizados com fallback para formas geométricas
- **Interface Completa**: Score, vida e status do jogador
- **Sistema de Partículas**: Efeitos visuais de explosão

## Tecnologias Utilizadas

- **Python 3.7+**
- **Pygame 2.5.2**
- **IDE Cursor** para desenvolvimento assistido por IA

## Instalação

1. Clone o repositório
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Execução

Existem duas formas de executar o jogo:

1. Via Python diretamente:

```bash
python moon_cresta_game.py
```

2. Via batch script (Windows):

```bash
run_game.bat
```

## Controles

- **Setas**: Movimento da nave
- **Barra de Espaço**: Disparo
- **R**: Reiniciar jogo (após game over/vitória)
- **ESC**: Sair do jogo

## Desenvolvimento com Cursor

O jogo foi desenvolvido utilizando a IDE Cursor, que oferece:

- Geração de código assistida por IA
- Sugestões contextuais
- Integração direta com Pygame
- Debug e execução integrados

### Prompt Utilizado na Criação

O desenvolvimento foi iniciado com o seguinte prompt no Cursor:

```
Crie um jogo em Python usando a biblioteca Pygame no estilo fixed shooter,
como o clássico Moon Cresta. O jogador controla uma nave que deve destruir
inimigos em três fases. Após cada fase, a nave deve acoplar a um novo estágio,
aumentando seu poder de fogo.

Agora no diretório do jogo existem três arquivos, sprint1.png, sprint2.png e sprint3.png.
Gostaria que cada uma dessas imagens fosse o inimigo de cada uma das fases,
respectivamente.
Também gostaria que ao final do jogo fosse possível teclar R para reiniciar o jogo.
Por favor, implemente essas alterações.
```

## Estrutura do Projeto

```
├── moon_cresta_game.py    # Código principal do jogo
├── requirements.txt       # Dependências Python
├── run_game.bat          # Script de execução para Windows
├── README.md             # Documentação
├── sprint1.png           # Sprite inimigo fase 1
├── sprint2.png           # Sprite inimigo fase 2
└── sprint3.png           # Sprite inimigo fase 3
```

## Contribuições

Para contribuir com o projeto:

1. Faça um fork
2. Crie uma branch para sua feature
3. Faça commit das mudanças
4. Push para a branch
5. Abra um Pull Request

## Créditos

Desenvolvido usando a IDE Cursor com tecnologia de IA para geração e assistência de código.

## Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
