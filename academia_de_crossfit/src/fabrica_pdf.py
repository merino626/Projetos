from fpdf import FPDF
import datetime

tabela_teste = [(1, "Luis", 25, 21312331, 40028922, "dudu@gmail.com"),
 (2, "Carlos almeida junior", 29, 301932194, 49218321, "caca@gmail.com"),
 (1, "Luis", 25, 21312331, 40028922, "dudu@gmail.com"),
 (2, "Carlos almeida junior", 29, 301932194, 49218321, "caca@gmail.com"),
 (1, "Luis", 25, 21312331, 40028922, "dudu@gmail.com"),
 (2, "Carlos almeida junior", 29, 301932194, 49218321, "caca@gmail.com"),
 (1, "Luis", 25, 21312331, 40028922, "dudu@gmail.com"),
 (2, "Carlos almeida junior", 29, 301932194, 49218321, "caca@gmail.com"),(1, "Luis", 25, 21312331, 40028922, "dudu@gmail.com"),
 (2, "Carlos almeida junior", 29, 301932194, 49218321, "caca@gmail.com"),(1, "Luis", 25, 21312331, 40028922, "dudu@gmail.com"),
 (2, "Carlos almeida junior", 29, 301932194, 49218321, "caca@gmail.com")]

### FORMATOS DE PDF QUE É POSSIVEL USAR ###
# layout("P", "L")
# unit ("mm", "cm", "in")
# format ("A3", "A4", (default), "A5", "Letter", "Legal", (100, 150))



class PDF(FPDF):
    def __init__(self, orientation='P',unit='mm',format='A4', title="Sem titulo"):
        super().__init__(orientation, unit, format)
        self.title = title

    def header(self):
        self.image("src\Icons\logo_crosslife.png", 10, 8, 40)
        self.set_font("helvetica", "B", 20)
        self.cell(0, 5, ln=1)
        self.cell(0, 10, self.title, border=False, ln=1, align="C")
        self.ln()

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 10)
        self.set_text_color(169,169,169)
        self.cell(0, 10, f'Página {self.page_no()}/{{nb}}', align="C")
        self.set_font("helvetica", "B", 10)
        data = datetime.datetime.now().strftime("Relatório gerado: %d/%m/%Y %H:%M:%S")
        self.cell(0, 10, data, border=False, ln=1, align="R")

    def carrega_imagem(self, path_img):
        self.set_font("helvetica", "B", 15)
        self.cell(0, 10, "Gráficos", ln=1, align="C")
        print(self.get_x())
        print(self.get_y())
        self.cell(20, 5)
        self.image(path_img, self.get_x(), self.get_y(), 150, 100)
        for i in range(22):
            self.ln()
        #self.cell(0, 10, "Ola", border=1, align="C")


    def montador_de_tabela_alunos(self, data2, headers=(), title=""):
        data = data2.copy()
        data.insert(0,headers)
        epw = self.w - 2*self.l_margin
        col_width = epw/4
        th = self.font_size
        self.set_font('helvetica','B',14.0) 
        self.cell(epw, 0.0, title, align='C')
        self.set_font('Times','',10.0) 
        self.ln(4)
        for j, row in enumerate(data):
            for i, datum in enumerate(row):
                if i >= 1:
                    if j == 0:
                        self.set_font('helvetica','B',10.0) 
                    else:
                        self.set_font('Times','',10.0)
                    if i == 2:
                        self.cell(20, 2*th, str(datum), border=1)
                    elif i == 3 or i == 4: 
                        self.cell(40, 2*th, str(datum), border=1)
                    elif i == 5:
                        if len(str(datum)) > 30:
                            self.set_font('Times','',6.7)
                        else:
                            self.set_font('Times','',10.0)
                        if j == 0: 
                            self.set_font('helvetica','B',10.0) 
                        self.cell(col_width, 2*th, str(datum), border=1)
                    else:
                        self.cell(col_width, 2*th, str(datum), border=1)
        
            self.ln(2*th)
        self.cell(epw, 6, f'Total de alunos: {len(data)-1}', align='C')
        self.ln(25)

    def montador_de_tabela_estoque(self, data2, headers=(), title=""):
        data = data2.copy()
        data.insert(0,headers)
        epw = self.w - 2*self.l_margin
        col_width = epw/4
        th = self.font_size
        self.set_font('helvetica','B',14.0) 
        self.cell(epw, 0.0, title, align='C')
        self.set_font('Times','',10.0) 
        self.ln(4)
        for j, row in enumerate(data):
            for i, datum in enumerate(row):
                if i >= 1:
                    if j == 0:
                        self.set_font('helvetica','B',10.0) 
                    else:
                        self.set_font('Times','',10.0)
                    if i == 2:
                        self.cell(60, 2*th, str(datum), border=1, align='C')
                    elif i == 3 or i == 4: 
                        self.cell(70, 2*th, str(datum), border=1, align='C')
                    elif i == 5:
                        if len(str(datum)) > 30:
                            self.set_font('Times','',6.7)
                        else:
                            self.set_font('Times','',10.0)
                        if j == 0: 
                            self.set_font('helvetica','B',10.0) 
                        self.cell(col_width, 2*th, str(datum), border=1)
                    else:
                        self.cell(70, 2*th, str(datum), border=1, align='C')
        
            self.ln(2*th)
        self.cell(epw, 6, f'Total de produtos: {len(data)-1}', align='C')
        self.ln(25)

    def montador_de_tabela_despesas(self, data2, headers=(), title=""):
        data = data2.copy()
        data.insert(0,headers)
        epw = self.w - 2*self.l_margin
        col_width = epw/4
        th = self.font_size
        self.set_font('helvetica','B',14.0) 
        self.cell(epw, 0.0, title, align='C')
        self.set_font('Times','',10.0) 
        self.ln(4)
        for j, row in enumerate(data):
            for i, datum in enumerate(row):
                if i >= 1:
                    if j == 0:
                        self.set_font('helvetica','B',10.0) 
                    else:
                        self.set_font('Times','',10.0)
                    if i == 2:
                        self.cell(50, 2*th, str(datum), border=1, align='C')
                    elif i == 3 or i == 4: 
                        self.cell(50, 2*th, str(datum), border=1, align='C')
                    elif i == 5:
                        if len(str(datum)) > 30:
                            self.set_font('Times','',6.7)
                        else:
                            self.set_font('Times','',10.0)
                        if j == 0: 
                            self.set_font('helvetica','B',10.0) 
                        self.cell(col_width, 2*th, str(datum), border=1)
                    else:
                        self.cell(50, 2*th, str(datum), border=1, align='C')
        
            self.ln(2*th)
        self.cell(epw, 6, f'Total de despesas: {len(data)-1}', align='C')
        self.ln(25)

if __name__ == '__main__':
    ### CRIANDO O OBJETO PDF ###
    pdf = PDF("P", "mm", "Letter", "Relatório de alunos")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.alias_nb_pages()
    ### Adicionando uma página ###
    pdf.add_page()

    ### Especificando uma fonte ###
    #fontes ("times", "courier", "helvetica", "symbol", "zpfdingbats")
    # "B" para bold, "U" para underlined, "I" para italico, "" para regular, ou "BU" para bolded and underlined
    pdf.set_font("helvetica", "", 20)

    ### Adicionando texto ###
    # pdf.cell(100, 50, "Hello world", border=1)
    # pdf.cell(150, 100, "teste", border=1, ln=1)
    pdf.carrega_imagem("dados_alunos.png")
    headers =  (0, "Nome do aluno", "Idade", "Cpf", "Telefone", "E-mail")
    pdf.montador_de_tabela_alunos(tabela_teste, headers,'Alunos cadastrados')
    pdf.montador_de_tabela_alunos(tabela_teste, headers, title="Alunos que não realizaram avaliação física")
    pdf.montador_de_tabela_alunos(tabela_teste, headers,'Alunos com avaliação física realizada')
    pdf.montador_de_tabela_alunos(tabela_teste, headers,'Alunos com matricula ativa')
    pdf.montador_de_tabela_alunos(tabela_teste, headers,'Alunos com matricula inativa')


    pdf.output("teste.pdf")

