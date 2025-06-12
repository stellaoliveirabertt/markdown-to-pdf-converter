# Conversor Markdown para PDF

## Descrição
Ferramenta web desenvolvida em Flask para converter arquivos Markdown (.md) em PDFs profissionais com formatação elegante.

## Funcionalidades
- Interface web moderna com drag-and-drop
- Suporte a arquivos .md e .markdown
- Conversão com formatação CSS profissional
- Suporte a tabelas, código, listas, citações
- Validação de arquivos (tipo e tamanho)
- Download automático do PDF gerado
- Limite de 10MB por arquivo

## Tecnologias Utilizadas
- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Conversão**: markdown + weasyprint
- **Estilização**: CSS customizado para PDFs

## Estrutura do Projeto
```
markdown-to-pdf-converter/
├── src/
│   ├── main.py              # Aplicação Flask principal
│   ├── routes/
│   │   ├── converter.py     # Lógica de conversão
│   │   └── user.py          # Rotas de usuário (template)
│   ├── static/
│   │   └── index.html       # Interface web
│   ├── models/              # Modelos de dados
│   └── database/            # Banco de dados SQLite
├── venv/                    # Ambiente virtual Python
└── requirements.txt         # Dependências
```

## Como Executar

### 1. Instalar Dependências
```bash
cd markdown-to-pdf-converter
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Executar a Aplicação
```bash
python src/main.py
```

### 3. Acessar a Ferramenta
Abra o navegador em: http://localhost:5000

## API Endpoints

### POST /api/convert
Converte arquivo Markdown para PDF

**Parâmetros:**
- `file`: Arquivo Markdown (.md ou .markdown)

**Resposta:**
- Arquivo PDF para download

**Exemplo de uso:**
```bash
curl -X POST -F "file=@documento.md" http://localhost:5000/api/convert -o documento.pdf
```

## Recursos da Conversão

### Formatação Suportada
- **Cabeçalhos** (H1-H6) com bordas coloridas
- **Texto**: negrito, itálico, código inline
- **Listas**: ordenadas e não ordenadas
- **Tabelas** com estilização alternada
- **Código**: blocos com syntax highlighting
- **Citações** com borda lateral
- **Links** funcionais
- **Imagens** responsivas
- **Separadores** (hr)

### Estilização PDF
- Fonte: DejaVu Sans (compatível com Unicode)
- Margens: 2cm em todas as bordas
- Numeração de páginas automática
- Quebras de página inteligentes
- Layout responsivo

## Validações
- Tipos de arquivo: .md, .markdown
- Tamanho máximo: 10MB
- Codificação: UTF-8
- Tratamento de erros robusto

## Segurança
- Validação de tipos de arquivo
- Sanitização de nomes de arquivo
- Limpeza automática de arquivos temporários
- Limite de tamanho de upload

## Dependências Principais
- Flask: Framework web
- flask-cors: Suporte a CORS
- markdown: Parser de Markdown
- weasyprint: Geração de PDF
- werkzeug: Utilitários web

## Autor
Aqui vai uma sugestão de como você pode se adicionar como autora e explicar a motivação do projeto de forma clara e com personalidade:

---

## Autoria

Desenvolvido por [Stella Moreira](https://www.linkedin.com/in/stellaoliveiram/) com o apoio de ferramentas de IA.

> Cansada de pagar por conversores limitados ou cheios de anúncios, resolvi criar uma alternativa gratuita, elegante e funcional — feita com carinho (e um pouco de indignação) por quem também precisa dessas ferramentas no dia a dia.


## Licença
Código aberto para uso educacional e comercial.
