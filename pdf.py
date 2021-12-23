from reportlab.platypus import Spacer, SimpleDocTemplate, Table, TableStyle, Image, PageBreak
from reportlab.platypus.paragraph import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors

from PyQt5.QtWidgets import QFileDialog

def create(data,IMG_FOLDER_LOCALE,self):
    
    #path = QFileDialog.getSaveFileName(self,'Open a file', '','All Files (*.*)')
    path = QFileDialog.getSaveFileName(self, "Save recipes", "YourRecipes.pdf", "Pdf-File (*.pdf)")
    if path != ('', ''):
        print("File path : "+ path[0])
        path=path[0]
    else:
        path="yourRecipes.pdf"
        
    
    styleSheet = getSampleStyleSheet()
    results = data[0]
    indices = data[1]
    name = results[0][indices]
    img = results[1][indices]
    links = results[3][indices]
    instructions = results[5][indices]        
    doc = SimpleDocTemplate(path, pagesize=(8.5*inch, 11*inch), showBoundary=1)
    Story=[]
    
    for j in range(len(indices)):
        title_style = styleSheet['Heading1']
        title_style.alignment = 1
        title = Paragraph(name[j], title_style)
        Story.append(title)
        
        im = Image(IMG_FOLDER_LOCALE + str(img[j]) + ".jpg", 4.5*inch, 3*inch)
        Story.append(im)
           
        Story.append(Spacer(1, 12))
        
        address = '>> Open recipe in browser <<'
        address = '<link href="' + links[j] + '">' + address + '</link>'
        Story.append(Paragraph(address, styleSheet["Heading5"]))
          
        Story.append(Spacer(1, 12))        
        
        for i in range(len(instructions[j])):
            Story.append(Paragraph("Step "+str(i+1), styleSheet["Heading2"]))
            Story.append(Paragraph(instructions[j][i], styleSheet["Normal"])) 
            
        Story.append(Spacer(1, 12))    

        ts1 = TableStyle([
                    ('ALIGN', (0,0), (-1,0), 'RIGHT'),
                    ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
                    ('VALIGN', (0,0), (-1,-1), 'TOP'),
                    ('GRID', (0,0), (-1,-1), 0.25, colors.black),
                        ])
        
        ret = []
        ret.append(["Amount","Unit","Ingredient"])
        for i in range(len(results[2][indices][j])):
            ret.append([results[2][indices][j][i][0],results[2][indices][j][i][1],results[2][indices][j][i][2]])           
        
        
        t1 = Table(ret)
        t1.setStyle(ts1)
        Story.append(t1)
        Story.append(PageBreak())
    
    title = Paragraph("Overall ingredient list", title_style)
    Story.append(title)
    
    ovrAllList = [["Amount","Unit","Ingredient"]]
    for i in range(len(data[2])):
        ovrAllList.append([data[2][i][0],data[2][i][1],data[2][i][2]])  
    t1 = Table(ovrAllList)
    t1.setStyle(ts1)
    Story.append(t1)
    doc.build(Story)
    
    