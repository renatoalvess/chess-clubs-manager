# Chess Club Manager

**Descrição:**  
Um sistema de gerenciamento de clubes de xadrez feito em Flask, Python e MySQL, que inclui funcionalidades como cadastro de clubes, jogadores, histórico de partidas, ranking, login de usuários e cálculos de rating.  

Desenvolvido no decorrer do Projeto de Extensão da faculdade, o projeto Xadrez Lógico abordava o ensinamento de xadrez e lógica a alunos do ensino fundamental e a comunidade local.  
O sistema inicialmente iria organizar o andamento dos clubes de xadrez escolares locais, bem como as partidas entre os jogadores e ranqueamentos.  

A seção de cards e notícias é apenas um template inicial e requer continuidade.  

## Funcionalidades  

- Cadastro de clubes e jogadores  
- Histórico de partidas  
- Sistema de ranking  
- Login e autenticação de usuários  
- Cálculo de rating  

## Tecnologias Utilizadas  

- Flask  
- Python  
- MySQL  
- HTML/CSS  
- JavaScript  

## Instalação  

**Pré-requisitos:**  
- Python 3.8 ou superior  
- MySQL  

**Passos:**  
```bash
# 1. Clone o repositório:
git clone https://github.com/seu-usuario/chess-clubs-manager.git

# 2. Instale as dependências:
cd chess-clubs-manager
pip install -r requirements.txt

# 3. Configure o banco de dados:
# Crie um banco de dados MySQL e configure as credenciais no arquivo config.py.
# Configure a credencial do admin no script criar_admin.py e ajuste no arquivo config.py:
python criar_admin.py

# 4. Inicie a aplicação:
python app.py
