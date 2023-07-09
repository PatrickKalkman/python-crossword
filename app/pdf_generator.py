from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


class PDFGenerator:
    def __init__(self, filename="./crosswords/crossword.pdf", img_filename="./crosswords/crossword.png"):
        self.filename = filename
        self.grid_image = img_filename
        self.styles = getSampleStyleSheet()

    def create_pdf(self, assignment, crossword, crossword_cue_generator):
        doc = SimpleDocTemplate(self.filename, pagesize=landscape(letter))
        elements = []

        crossword_image = Image(self.grid_image, 300, 300)
        elements.append(crossword_image)
        elements.append(Paragraph("", self.styles["Normal"]))

        for variable, word in sorted(assignment.items(), key=lambda item: crossword.get_variable_number(item[0])):
            cue = crossword_cue_generator.generate(word)
            text = f"{crossword.get_variable_number(variable)}: {variable.direction} => {cue}"
            elements.append(Paragraph(text, self.styles["Normal"]))

        doc.build(elements)
