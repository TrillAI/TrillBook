"""Build the square, nine-page AI picture book (requires reportlab)."""
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader

ROOT = Path(__file__).resolve().parent
SIZE = 720
SENTENCES = [
    "Artificial intelligence, or AI, includes computer systems that learn patterns from examples.",
    "During training, an AI model adjusts its settings to get better at a task.",
    "A language model learns patterns in text and predicts what bits of text might come next.",
    "When you type a prompt, or instruction, the model uses those patterns to create a response.",
    "AI can help brainstorm, explain ideas, and organize information.",
    "But AI can sound confident and still get facts wrong, even about bananas.",
    "If its training examples are unfair or incomplete, AI can give biased answers too.",
    "Check important answers with trusted sources, and keep private information out of your prompts.",
    "AI is a tool, so people still need to make the important decisions.",
]
COLORS = ['#F17862', '#1FA7A1', '#F2AF31', '#8C68BC', '#57AA78', '#E66E9D', '#5B86CA', '#DC8545', '#219C93']
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
pdfmetrics.registerFont(TTFont('StoryBold', FONT))

def wrap(text, font, size, width):
    lines, line = [], ''
    for word in text.split():
        trial = f'{line} {word}'.strip()
        if line and pdfmetrics.stringWidth(trial, font, size) > width:
            lines.append(line)
            line = word
        else:
            line = trial
    if line:
        lines.append(line)
    return lines

out = ROOT / 'A Little Book About AI.pdf'
c = canvas.Canvas(str(out), pagesize=(SIZE, SIZE), pageCompression=1)
c.setTitle("A Little Book About AI")
c.setAuthor('An illustrated introduction to artificial intelligence')
for i, (sentence, color) in enumerate(zip(SENTENCES, COLORS), 1):
    c.setFillColor(HexColor(color))
    c.rect(0, 0, SIZE, SIZE, fill=1, stroke=0)
    # Festive polka dots bring the bright border to life without adding text.
    for x in (21, 52, 668, 699):
        for y in range(180, 720, 62):
            c.setFillColor(HexColor('#FFE8A3') if (x + y) % 3 else HexColor('#FFFFFF'))
            c.circle(x, y, 3.5, fill=1, stroke=0)
    c.setFillColor(HexColor('#FFF6DA'))
    c.roundRect(80, 151, 560, 560, 12, fill=1, stroke=0)
    c.drawImage(ImageReader(str(ROOT / 'art' / f'page{i}.jpg')), 85, 156, 550, 550, preserveAspectRatio=True)
    c.setFillColor(HexColor('#FFF8E8'))
    c.roundRect(25, 20, 670, 119, 19, fill=1, stroke=0)
    c.setFillColor(HexColor('#342A41'))
    size = 22
    lines = wrap(sentence, 'StoryBold', size, 602)
    while len(lines) > 3:
        size -= 1
        lines = wrap(sentence, 'StoryBold', size, 602)
    leading = size * 1.30
    first_y = 80 + (len(lines) - 1) * leading / 2
    c.setFont('StoryBold', size)
    for n, line in enumerate(lines):
        c.drawCentredString(SIZE / 2, first_y - n * leading, line)
    c.setFillColor(HexColor(color))
    c.setFont('Helvetica-Bold', 10)
    c.drawCentredString(SIZE / 2, 29, str(i))
    c.showPage()
c.save()
print(out)
