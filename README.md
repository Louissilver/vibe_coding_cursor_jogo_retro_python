# Moon Cresta - Jogo Retro

Um jogo estilo fixed shooter inspirado no clássico Moon Cresta, desenvolvido em Python com Pygame.

## Características do Jogo

- **Três fases**: Cada fase aumenta a dificuldade e adiciona novos tipos de inimigos
- **Sistema de estágios**: A nave acopla novos estágios após cada fase, aumentando o poder de fogo
- **Inimigos variados**: Diferentes tipos de inimigos com comportamentos únicos
- **Efeitos visuais**: Explosões e fundo estrelado
- **Interface completa**: Score, vida, nível e estágio da nave

## Como Jogar

### Controles

- **Setas direcionais**: Mover a nave
- **Barra de espaço**: Atirar
- **ESC**: Sair do jogo
- **R**: Reiniciar (após game over ou vitória)

### Objetivo

Destrua todos os inimigos em cada fase para progredir. Após cada fase, sua nave será automaticamente melhorada com um novo estágio, aumentando significativamente seu poder de fogo.

### Sistema de Estágios

- **Estágio 1**: Tiro único
- **Estágio 2**: Tiro triplo (principal + 2 laterais)
- **Estágio 3**: Tiro quíntuplo (principal + 4 laterais)

### Tipos de Inimigos

- **Tipo 1**: Inimigos básicos (sprint1.png)
- **Tipo 2**: Inimigos médios (sprint2.png)
- **Tipo 3**: Inimigos avançados (sprint3.png)

_Nota: Se os arquivos de sprite não estiverem disponíveis, o jogo usará formas geométricas como fallback._

## Instalação e Execução

### Pré-requisitos

- Python 3.7 ou superior
- Pygame

### Instalação

1. Clone ou baixe este repositório
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

### Execução

```bash
python moon_cresta_game.py
```

## Estrutura do Projeto

- `moon_cresta_game.py`: Arquivo principal do jogo
- `requirements.txt`: Dependências do projeto
- `sprint1.png`: Sprite do inimigo da fase 1
- `sprint2.png`: Sprite do inimigo da fase 2
- `sprint3.png`: Sprite do inimigo da fase 3
- `README.md`: Este arquivo

## Desenvolvimento

O jogo foi desenvolvido usando:

- **Python 3.x**: Linguagem principal
- **Pygame**: Biblioteca para desenvolvimento de jogos
- **Programação Orientada a Objetos**: Classes bem estruturadas para cada elemento do jogo

## Características Técnicas

- **Resolução**: 800x600 pixels
- **FPS**: 60 frames por segundo
- **Sistema de colisão**: Detecção precisa de colisões
- **Sistema de partículas**: Efeitos de explosão
- **Estados do jogo**: Playing, Level Complete, Victory, Game Over

Divirta-se jogando!
