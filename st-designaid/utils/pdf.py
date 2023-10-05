from fpdf.fpdf import FPDF
import base64

def sanitise_text(text):
    return text.encode('latin-1', 'replace').decode('latin-1')

def split_text(pdf, text, width):
    """Split a text string into chunks that each have a width less than the specified width."""
    lines = []
    words = text.split(' ')
    current_line = ''

    for word in words:
        test_line = current_line + word + ' '
        test_width = pdf.get_string_width(test_line)

        if test_width <= width:
            current_line += word + ' '
        else:
            lines.append(current_line)
            current_line = word + ' '

    if current_line:
        lines.append(current_line)

    return lines

def multi_cell(pdf, w, h, txt, font_family, font_style, font_size, border=0, align='L', fill=False):
    """Handle text wrapping for the FPDF library with custom font settings."""
    pdf.set_font(font_family, font_style, font_size)
    lines = split_text(pdf, txt, w)
    
    for line in lines:
        pdf.cell(w, h, line, border, 1, align, fill)

def create_download_link(val, filename):
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'
