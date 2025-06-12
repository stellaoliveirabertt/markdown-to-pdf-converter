import os
import tempfile
import markdown
import weasyprint
from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename

converter_bp = Blueprint('converter', __name__)

ALLOWED_EXTENSIONS = {'md', 'markdown'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_file_size(file):
    """Validate file size"""
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    return size <= MAX_FILE_SIZE

@converter_bp.route('/convert', methods=['POST'])
def convert_markdown_to_pdf():
    try:
        # Check if file is present in request
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo foi enviado'}), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo foi selecionado'}), 400
        
        # Validate file extension
        if not allowed_file(file.filename):
            return jsonify({'error': 'Tipo de arquivo não suportado. Use arquivos .md ou .markdown'}), 400
        
        # Validate file size
        if not validate_file_size(file):
            return jsonify({'error': 'Arquivo muito grande. O tamanho máximo é 10MB'}), 400
        
        # Read markdown content
        markdown_content = file.read().decode('utf-8')
        
        # Convert markdown to HTML
        html_content = markdown.markdown(
            markdown_content,
            extensions=[
                'markdown.extensions.tables',
                'markdown.extensions.fenced_code',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
                'markdown.extensions.nl2br'
            ]
        )
        
        # Create complete HTML document with CSS styling
        complete_html = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Documento PDF</title>
            <style>
                @page {{
                    size: A4;
                    margin: 2cm;
                    @bottom-center {{
                        content: counter(page) " / " counter(pages);
                        font-size: 10pt;
                        color: #666;
                    }}
                }}
                
                body {{
                    font-family: 'DejaVu Sans', Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 100%;
                    margin: 0;
                    padding: 0;
                }}
                
                h1, h2, h3, h4, h5, h6 {{
                    color: #2c3e50;
                    margin-top: 1.5em;
                    margin-bottom: 0.5em;
                    page-break-after: avoid;
                }}
                
                h1 {{
                    font-size: 2.2em;
                    border-bottom: 3px solid #3498db;
                    padding-bottom: 0.3em;
                }}
                
                h2 {{
                    font-size: 1.8em;
                    border-bottom: 2px solid #3498db;
                    padding-bottom: 0.2em;
                }}
                
                h3 {{
                    font-size: 1.4em;
                    color: #34495e;
                }}
                
                p {{
                    margin-bottom: 1em;
                    text-align: justify;
                }}
                
                code {{
                    background-color: #f8f9fa;
                    padding: 2px 4px;
                    border-radius: 3px;
                    font-family: 'Courier New', monospace;
                    font-size: 0.9em;
                    color: #e74c3c;
                }}
                
                pre {{
                    background-color: #f8f9fa;
                    border: 1px solid #e9ecef;
                    border-radius: 5px;
                    padding: 1em;
                    overflow-x: auto;
                    page-break-inside: avoid;
                }}
                
                pre code {{
                    background-color: transparent;
                    padding: 0;
                    color: #333;
                }}
                
                blockquote {{
                    border-left: 4px solid #3498db;
                    margin: 1em 0;
                    padding-left: 1em;
                    color: #666;
                    font-style: italic;
                    background-color: #f8f9fa;
                    padding: 1em;
                    border-radius: 0 5px 5px 0;
                }}
                
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin: 1em 0;
                    page-break-inside: avoid;
                }}
                
                th, td {{
                    border: 1px solid #ddd;
                    padding: 8px 12px;
                    text-align: left;
                }}
                
                th {{
                    background-color: #3498db;
                    color: white;
                    font-weight: bold;
                }}
                
                tr:nth-child(even) {{
                    background-color: #f8f9fa;
                }}
                
                ul, ol {{
                    margin: 1em 0;
                    padding-left: 2em;
                }}
                
                li {{
                    margin-bottom: 0.5em;
                }}
                
                a {{
                    color: #3498db;
                    text-decoration: none;
                }}
                
                a:hover {{
                    text-decoration: underline;
                }}
                
                img {{
                    max-width: 100%;
                    height: auto;
                    display: block;
                    margin: 1em auto;
                    border-radius: 5px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                
                hr {{
                    border: none;
                    border-top: 2px solid #3498db;
                    margin: 2em 0;
                }}
                
                .page-break {{
                    page-break-before: always;
                }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        # Create temporary files
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as html_file:
            html_file.write(complete_html)
            html_file_path = html_file.name
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as pdf_file:
            pdf_file_path = pdf_file.name
        
        try:
            # Convert HTML to PDF using WeasyPrint
            weasyprint.HTML(filename=html_file_path).write_pdf(pdf_file_path)
            
            # Generate output filename
            original_filename = secure_filename(file.filename)
            pdf_filename = original_filename.rsplit('.', 1)[0] + '.pdf'
            
            # Send the PDF file
            return send_file(
                pdf_file_path,
                as_attachment=True,
                download_name=pdf_filename,
                mimetype='application/pdf'
            )
            
        finally:
            # Clean up temporary files
            try:
                os.unlink(html_file_path)
            except:
                pass
            # Note: PDF file will be cleaned up by Flask after sending
            
    except UnicodeDecodeError:
        return jsonify({'error': 'Erro ao decodificar o arquivo. Verifique se o arquivo está em UTF-8'}), 400
    except Exception as e:
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500

