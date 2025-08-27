# Como Adicionar Músicas ao Jogo

## Formato Suportado
- **MP3**: Formato recomendado para melhor compatibilidade

## Localização
Coloque seus arquivos de música na pasta `src/audio/`

## Configuração
Para adicionar uma nova música:

1. Adicione o arquivo de música na pasta `src/audio/`
2. Abra o arquivo `src/config.py`
3. Adicione o caminho da música na lista `AUDIO_FILES`:

```python
AUDIO_FILES = [
    'src/audio/03_Sonne.mp3',
    'src/audio/sua_nova_musica.mp3',  # Adicione aqui
    'src/audio/outra_musica.mp3',     # E aqui
]
```

## Exemplo de Estrutura
```
src/audio/
├── 03_Sonne.mp3
├── sua_nova_musica.mp3
├── outra_musica.mp3
└── README.md
```

## Dicas
- Use nomes descritivos para os arquivos
- Certifique-se de que os arquivos são válidos e não estão corrompidos
- O jogo selecionará automaticamente uma música aleatória a cada execução
- Se uma música falhar ao carregar, o jogo tentará carregar outra automaticamente
