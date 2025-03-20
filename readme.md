# Grade GUI

Este é um aplicativo GUI desenvolvido em Python para gerenciar disciplinas e notas, utilizando **Tkinter** para a interface gráfica e **SQLite** como banco de dados.

## Funcionalidades

- **Inserir Disciplina**: Adicione novas disciplinas ao banco de dados.
- **Consultar Disciplinas**: Visualize todas as disciplinas cadastradas.
- **Inserir Notas**: Insira ou atualize notas para disciplinas específicas.
- **Consultar Grade**: Visualize as disciplinas com suas respectivas notas e cálculos de média.
- **Eliminar Disciplina**: Exclua disciplinas e suas notas associadas.
- **Executar Consulta SQL**: Execute consultas SQL diretamente no banco de dados.

## Requisitos

- **Python 3.8 ou superior**
- Bibliotecas Python:
  - `tkinter` (integrada ao Python)
  - `sqlite3` (integrada ao Python)
  - `pyinstaller` (apenas para criar o executável)

## Estrutura do Projeto
```
grade/
├── main.py          # Arquivo principal que inicia a aplicação GUI
├── database.py      # Módulo para interações com o banco de dados SQLite
├── gui.py           # Módulo que define a interface gráfica usando Tkinter
├── utils.py         # Funções auxiliares para cálculos e validações
├── assets/          # Diretório para arquivos de mídia (ícones, imagens, etc.)
└── README.md        # Documentação do projeto
```

## Como Executar

1. Clone este repositório:
    ```bash
    git clone https://github.com/seu-usuario/grade-gui.git
    cd grade-gui
    ```

2. Instale as dependências necessárias:
    ```bash
    pip install -r requirements.txt
    ```

3. Execute o aplicativo:
    ```bash
    python main.py
    ```

## Criar Executável

Para criar um executável standalone, utilize o **PyInstaller**:
```bash
pyinstaller --onefile --windowed main.py
```
O executável será gerado na pasta `dist/`.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).