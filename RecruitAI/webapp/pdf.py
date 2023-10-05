from fpdf import FPDF


class PDF(FPDF):

    def __init__(self, *args, with_header: bool, **kwargs):
        super().__init__(*args, **kwargs)
        self.with_header = with_header

    def header(self):
        if self.with_header:
            self.image("webapp/logo_recruit_ai.png", 150, 10, 40)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.set_text_color(128)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def add_text(self, text):
        self.set_font("Arial", size=10)
        self.ln(10)
        self.multi_cell(0, 10, text)
