from PyPDF2 import PdfReader
from pdf2image import convert_from_path
from PyPDF2.errors import PdfReadError
import os

class PDFToolkit:
    def __init__(self):
        pass

    def pdf2image(pdfPath, outputPath, imageFormat):
        """
        Converte um arquivo PDF em uma ou mais imagens no formato especificado e salva na pasta de saída.

        :param pdfPath: o caminho completo do arquivo PDF a ser convertido
        :param outputPath: o caminho completo da pasta onde as imagens convertidas serão salvas
        :param imageFormat: o formato das imagens de saída (por exemplo, 'png', 'jpeg', etc.)
        :return: nenhum

        Exemplo de uso:
        pdf_toolkit = PDFToolkit()
        pdf_toolkit.convert_pdf_to_images('/caminho/para/arquivo.pdf', '/caminho/para/pasta', 'jpeg')

        Esta função converte um arquivo PDF em uma ou mais imagens no formato especificado e salva na pasta de saída. O nome das imagens de saída é gerado automaticamente a partir do nome do arquivo PDF e do número da página. Se o arquivo PDF contém várias páginas, a função gera uma imagem para cada página. As imagens são salvas na pasta de saída com o nome no formato 'nome_do_arquivo_pdf_número_da_página.extensão'.
        """
        # Verifica se o arquivo PDF existe
        if not os.path.isfile(pdfPath):
            raise ValueError(f'O arquivo PDF {pdfPath} não foi encontrado.')

        # Verifica se o arquivo PDF é válido e pode ser convertido
        with open(pdfPath, 'rb') as f:
            try:
                PdfReader(f)
            except PdfReadError:
                raise ValueError(f'O arquivo PDF {pdfPath} é inválido e não pode ser convertido.')

        # Converte o arquivo PDF em imagens
        fileName = os.path.splitext(os.path.basename(pdfPath))[0]
        pages = convert_from_path(pdfPath)
        for i, page in enumerate(pages):
            page.save(os.path.join(outputPath, f'{fileName}_{i+1}.{imageFormat}'), f'{imageFormat}')
