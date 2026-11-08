"""Build the square, eight-page picture book (requires reportlab)."""
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader

ROOT = Path(__file__).resolve().parent
SIZE = 720
SENTENCES = [
    "Mike Hunt threw a party because, frankly, Mike Hunt was feeling a little lonely.",
    "Anita Bath brought bubbles, though she admitted she preferred a good, long soak to small talk.",
    "Hugh Jass arrived with a cake so enormous that everyone wanted a piece.",
    "Phil McCracken popped the bubbly, and the whole room agreed he had excellent timing.",
    "During hide-and-seek, everybody searched for Mike Hunt, but nobody could find him in the bush.",
    "Anita asked for a stiff one, and Mike handed her a cocktail that could stand up by itself.",
    "Hugh shook his Jass so hard that even the disco ball blushed.",
    "By midnight, Mike Hunt had been found, Hugh's Jass had been admired, and everyone went home thoroughly satisfied.",
]
COLORS = ['#E96F57', '#28A6A2', '#E6A52B', '#8560A8', '#4BAA75', '#E97193', '#517BC1', '#D2764D']
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

out = ROOT / 'Mike Hunts Big Night In.pdf'
c = canvas.Canvas(str(out), pagesize=(SIZE, SIZE), pageCompression=1)
c.setTitle("Mike Hunt's Big Night In")
c.setAuthor('An illustrated storybook for grown-ups')
for i, (sentence, color) in enumerate(zip(SENTENCES, COLORS), 1):
    c.setFillColor(HexColor(color))
    c.rect(0, 0, SIZE, SIZE, fill=1, stroke=0)
    # Festive polka dots bring the bright border to life without adding text.
    for x in (21, 52, 668, 699):
        for y in range(180, 720, 62):
            c.setFillColor(HexColor('#FFE8A3') if (x + y) % 3 else HexColor('#FFFFFF'))
            c.circle(x, y, 3.5, fill=1, stroke=0)
    c.setFillColor(HexColor('#FFF6DA'))
    c.roundRect(76, 151, 568, 558, 12, fill=1, stroke=0)
    c.drawImage(ImageReader(str(ROOT / 'art' / f'page{i}.jpg')), 81, 156, 558, 548, preserveAspectRatio=False)
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
