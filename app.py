from tkinter import Tk,Label,Entry,Button,Text,Toplevel,Radiobutton,Frame,Listbox,ttk, PhotoImage
from tkinter import filedialog,messagebox,Grid,NSEW,END,LEFT,RIGHT,TOP,BOTTOM,CENTER
import processamento as pr
from processamento import path
from PIL import Image, ImageTk

class App:
    def __init__(self,root):
        pr.definir_working_directory_padrao()
        pr.gerar_qrcode()
        self.lista_relatorios = pr.mapa_arquivos("",pr.reports_path)
        self.contador_produtos = 0
        self.pix = pr.chave_pix()
        self.qrcode = pr.pix_qrcode()
        self.root = root
        self.w = self.root.winfo_screenwidth()
        self.h = self.root.winfo_screenheight()
        self.tamanho_janela = f"{self.w}x{self.h}"
        self.produtos_open = False
        self.clientes_open = False
        self.relatorios_open = False
        self.vender_open = False
        self.estoque_open = False
        self.obrigado_open = False
        self.creditos_open = False
        self.root.geometry("500x500")
        self.root.title("Gerencial Fácil - Menu Principal")
        self.icon = PhotoImage(file=pr.gerar_icones())
        self.root.iconphoto(True,self.icon)
        self.botao_produtos = Button(
            self.root,
            text="Gerenciar produtos",
            padx=5, pady=5,
            font="arial 25",
            command=self.abrir_produtos
            )

        self.botao_clientes = Button(
            self.root,
            text="Gerenciar Clientes",
            padx=5, pady=5,
            font="arial 25",
            command=self.abrir_clientes
            )

        self.botao_vendas = Button(
            self.root,
        text="Realizar Vendas",
        padx=5, pady=5,
        font="arial 25",
        command=self.abrir_vendas
        )
        
        self.botao_relatorios = Button(
            self.root,
            text="Relatórios de Venda",
            padx=5, pady=5,
            font="arial 25",
            command=self.abrir_relatorios
            )

        self.botao_checar_estoque = Button(
            self.root,
            text="Visualizar Estoque",
            padx=5,pady=5,
            font="arial 25",
            command=self.abrir_gerenciar_estoque
            )

        self.botao_obrigado = Button(
            self.root,
            text="Sobre o Programa",
            padx=5, pady=5,
            font="arial 25",
            command = self.abrir_janela_obrigado
        )

        for i in range(6):
            Grid.rowconfigure(self.root, i, weight=1)
        Grid.columnconfigure(self.root, 0, weight=1)

        self.botao_produtos.grid(row=0, column=0, sticky=NSEW)
        self.botao_clientes.grid(row=1, column=0, sticky=NSEW)
        self.botao_vendas.grid(row=2,column=0,sticky=NSEW)
        self.botao_relatorios.grid(row=3, column=0, sticky=NSEW)
        self.botao_checar_estoque.grid(row=4,column=0,sticky=NSEW)
        self.botao_obrigado.grid(row=5, column=0,sticky=NSEW)

    def abrir_janela_obrigado(self):
        try:
            pr.definir_working_directory_padrao()
            pr.gerar_qrcode()
            pr.gerar_icones()
            if not self.obrigado_open:
                self.obrigado_open = True
                self.root.withdraw()
                self.janela_obrigado = Toplevel(self.root)
                self.janela_obrigado.title("Sobre o Desenvolvedor")
                self.janela_obrigado.geometry("600x600")
                self.janela_obrigado.protocol("WM_DELETE_WINDOW",self.fechar_janela_obrigado)
                self.frame_obrigado = Frame(self.janela_obrigado)
                self.label_dev = Label(self.frame_obrigado,text="Desenvolvedor: Ytalo santos Aragão",padx=10,pady=10)
                self.label_dev2 = Label(self.frame_obrigado,text="Email: ytaloytalosantos@gmail.com",padx=10,pady=10)
                self.label_dev3 = Label(self.frame_obrigado,text="Espero que tenha gostado\n do programa e que lhe seja bem útil".upper(),padx=10,pady=10)
                self.label_dev4 = Label(self.frame_obrigado,text="Se quiser me apoiar a produzir\n mais software livre como esse e me incentivar\n a melhorar cada vez mais, você pode me apoiar\n através de doações que podem ser feitas via PIX\n QR Code abaixo:".upper(),padx=10,pady=10)
                imagem = ImageTk.PhotoImage(Image.open(pr.qrcode_path).resize((300,300)))
                self.label_qrcode = Label(self.frame_obrigado,image=imagem)
                self.label_qrcode.photo = imagem
                self.botao_copiar_chave = Button(
                    self.janela_obrigado,
                    text="Copiar chave PIX",
                    command=self.copiar_PIX
                )
                pr.mudar_diretorio(pr.root_path)
                Grid.columnconfigure(self.frame_obrigado,0,weight=1)
                for i in range(5):
                    Grid.rowconfigure(self.frame_obrigado,i,weight=1)
                self.label_dev.grid(row=0,column=0,sticky=NSEW)
                self.label_dev2.grid(row=1,column=0,sticky=NSEW)
                self.label_dev3.grid(row=2,column=0,sticky=NSEW)
                self.label_dev4.grid(row=3,column=0,sticky=NSEW)
                self.frame_obrigado.pack(fill="both",side=TOP)
                self.label_qrcode.grid(row=4,column=0)
                self.botao_copiar_chave.pack()
            else:
                pr.definir_working_directory_padrao()
                self.abrir_janela_obrigado.focus()
        except:
            pass

    def copiar_PIX(self):
        pr.to_clipboard(pr.chave_pix())
        messagebox.showinfo(
            title="Chave copiada com sucesso",
            message="Chave PIX copiada!"
            )
    
    def fechar_janela_obrigado(self):
        try:
            pr.definir_working_directory_padrao()
            pr.gerar_icones()
            pr.gerar_qrcode()
            self.obrigado_open = False
            self.janela_obrigado.destroy()
            self.root.deiconify()
        except:
            pass

    def salvar_produto(self):
        try:
            pr.definir_working_directory_padrao()
            dados = {}
            dados["nome"] = self.campo_produto_nome.get()
            dados["descricao"] = self.campo_descricao.get()
            dados["unidade"] = self.campo_unidade.get().lower()
            dados["preco"] = pr.numero_string(self.campo_preco.get().replace("R$","").replace("$",""))
            dados["estoque_minimo"] = pr.numero_string(self.campo_estoque_minimo.get())
            dados["estoque"] = pr.numero_string(self.campo_estoque.get().lower())
            if type(dados["estoque"]) == str :
                dados["estoque"] = "n/a"
                dados["estoque_minimo"] = "n/a"
            pr.mudar_diretorio(pr.products_path)
            nome_arquivo = pr.tratar_string_nome(dados["nome"])+"_produto.json"
            if not path.exists(nome_arquivo):
                pr.cadastrar_produto(dados)
                self.limpar_campos_produto()
                messagebox.showinfo(
                    title="Sucesso!",
                    message="Produto cadastrado com sucesso"
                    )
                
            else:
                self.confirmar = messagebox.askyesno(
                    title="Atenção!",
                    message="Produto já cadastrado!\nDeseja sobrescrever?"
                    )
                if self.confirmar:
                    pr.cadastrar_produto(dados)
                    self.limpar_campos_produto()
                    messagebox.showinfo(
                        title="Sucesso!",
                        message="Produto sobrescrito com sucesso"
                        )
                else:
                    self.limpar_campos_produto()
            pr.definir_working_directory_padrao()
        except:
            pass

    def limpar_campos_produto(self):
        try:
            self.campo_produto_nome.delete(0,END)
            self.campo_descricao.delete(0,END)
            self.campo_unidade.delete(0,END)
            self.campo_preco.delete(0,END)
            self.campo_estoque.delete(0,END)
            self.campo_estoque_minimo.delete(0,END)
        except:
            pass

    def carregar_produto(self):
        try:
            pr.definir_working_directory_padrao()
            pr.mudar_diretorio(pr.products_path)
            tipos = [("Produto","*_produto.json")]
            self.caminho = filedialog.askopenfilename(
                initialdir=pr.getcwd(),
                title="Selecione o arquivo de um Produto",
                filetypes=tipos
                )
            try:
                dados = pr.ler_arquivo_json_para_python(self.caminho)
                self.limpar_campos_produto()
                self.campo_produto_nome.insert(0,dados["nome"])
                self.campo_descricao.insert(0,dados["descricao"])
                self.campo_unidade.insert(0,dados["unidade"])
                self.campo_preco.insert(0,dados["preco"])
                self.campo_estoque.insert(0,dados["estoque"])
                self.campo_estoque_minimo.insert(0,dados["estoque_minimo"])
            except:
                pass

            pr.definir_working_directory_padrao()
        except:
            pass

    def abrir_produtos(self):
        pr.definir_working_directory_padrao()
        if not self.produtos_open:
            try:
                self.root.withdraw()
                pr.mudar_diretorio(pr.products_path)
                self.produtos_open = True
                self.janela_produtos = Toplevel(self.root)
                self.janela_produtos.geometry(self.tamanho_janela)
                self.janela_produtos.title("Gerenciar Produtos")
                self.janela_produtos.protocol(
                    "WM_DELETE_WINDOW",
                    self.fechar_janela_produtos
                    )
                
                self.label_nome_produto = Label(
                    self.janela_produtos,
                    text="Nome do Produto",
                    padx=5, pady=5,
                    font="arial 25"
                    )
                
                self.label_descricao_produto = Label(
                    self.janela_produtos,
                    text="Descrição do Produto",
                    padx=5, pady=5,
                    font="arial 25"
                    )
                
                self.label_unidade_produto = Label(
                    self.janela_produtos,
                    text="Unidade de Medida",
                    padx=5, pady=5,
                    font="arial 25"
                    )
                
                self.label_preco = Label(
                    self.janela_produtos,
                    text="Valor Unitário",
                    padx=5, pady=5,
                    font="arial 25"
                    )
                
                self.label_estoque = Label(
                    self.janela_produtos,
                    text="Estoque atual",padx=5, pady=5,
                    font="arial 25"
                    )
                
                self.label_estoque_minimo = Label(
                    self.janela_produtos,text="Estoque Mínimo",
                    padx=5, pady=5,
                    font="arial 25"
                    )

                self.botao_salvar_produto = Button(
                    self.janela_produtos,
                    text="Salvar Produto",
                    padx=5, pady=5,
                    font="arial 25",
                    command=self.salvar_produto
                    )
                self.botao_ler_produto = Button(
                    self.janela_produtos,
                    text="Abrir / Editar Produto",
                    padx=5, pady=5,
                    font="arial 25",
                    command=self.carregar_produto
                    )

                self.campo_produto_nome = Entry(
                    self.janela_produtos,
                    font="arial 25"
                    )
                
                self.campo_descricao = Entry(
                    self.janela_produtos,
                    font="arial 25"
                    )
                
                self.campo_unidade = Entry(
                    self.janela_produtos,
                    font="arial 25"
                    )
                
                self.campo_preco = Entry(
                    self.janela_produtos,
                    font="arial 25"
                    )
                
                self.campo_estoque = Entry(
                    self.janela_produtos,
                    font="arial 25"
                    )
                
                self.campo_estoque_minimo = Entry(
                    self.janela_produtos,
                    font="arial 25"
                    )

                for i in range(7):
                    Grid.rowconfigure(self.janela_produtos,i,weight=1)
                for i in range(2):
                    Grid.columnconfigure(self.janela_produtos,i,weight=1)

                self.label_nome_produto.grid(row=0,column=0,sticky=NSEW)
                self.campo_produto_nome.grid(row=0,column=1,sticky=NSEW)
                self.label_descricao_produto.grid(row=1,column=0,sticky=NSEW)
                self.campo_descricao.grid(row=1,column=1,sticky=NSEW)
                self.label_unidade_produto.grid(row=2,column=0,sticky=NSEW)
                self.campo_unidade.grid(row=2,column=1,sticky=NSEW)
                self.label_preco.grid(row=3,column=0,sticky=NSEW)
                self.campo_preco.grid(row=3,column=1,sticky=NSEW)
                self.label_estoque.grid(row=4,column=0,sticky=NSEW)
                self.campo_estoque.grid(row=4,column=1,sticky=NSEW)
                self.label_estoque_minimo.grid(row=5, column=0, sticky=NSEW)
                self.campo_estoque_minimo.grid(row=5, column=1, sticky=NSEW)
                self.botao_ler_produto.grid(row=6, column=0, sticky=NSEW)
                self.botao_salvar_produto.grid(row=6,column=1,sticky=NSEW)
            except:
                try:
                    self.janela_produtos.destroy()
                    self.root.deiconify()
                except:
                    self.root.deiconify()
        else:
            pr.definir_working_directory_padrao()
            pr.mudar_diretorio(pr.products_path)
            self.janela_produtos.focus()

    def fechar_janela_produtos(self):
        try:
            self.produtos_open = False
            pr.definir_working_directory_padrao()
            self.janela_produtos.destroy()
            self.root.deiconify()
        except:
            pass
    
    def limpar_campos_cliente(self):
        try:
            self.campo_nome_cliente.delete(0,END)
            self.campo_contato.delete(0,END)
            self.campo_endereco.delete(0,END)
            self.campo_observacoes.delete("1.0",END)
        except:
            pass

    def carregar_cliente(self):
        try:
            pr.definir_working_directory_padrao()
            pr.mudar_diretorio(pr.clients_path)
            tipos = [("Cliente","*_cliente.json")]
            self.caminho = filedialog.askopenfilename(
                initialdir=pr.getcwd(),
                title="Selecione o arquivo de um cliente",
                filetypes=tipos
                )
            try:
                dados = pr.ler_arquivo_json_para_python(self.caminho)
            
                self.limpar_campos_cliente()
            
                self.campo_nome_cliente.insert(0,dados["nome"])
                self.campo_contato.insert(0,dados["contato"])
                self.campo_endereco.insert(0,dados["endereco"])
                self.campo_observacoes.insert(1.0,dados["observacoes"])
                
                pr.mudar_diretorio(pr.root_path)
            except:
                pass
        except:
            pass

    def salvar_cliente(self):
        try:
            pr.definir_working_directory_padrao()
            pr.mudar_diretorio(pr.clients_path)
            dados = {}
            dados["nome"] = self.campo_nome_cliente.get()
            dados["contato"] = self.campo_contato.get()
            dados["endereco"] = self.campo_endereco.get()
            dados["observacoes"] = self.campo_observacoes.get("1.0","end-1c")
            nome_arquivo = pr.tratar_string_nome(dados["nome"])+"_cliente.json"
            if not path.exists(nome_arquivo):
                pr.cadastrar_cliente(dados)
                self.limpar_campos_cliente()
                messagebox.showinfo(
                    title="Salvo",
                    message="Cliente cadastrado com sucesso!"
                    )
            else:
                self.confirmar = messagebox.askyesno(
                    title="Atenção!",
                    message="Cliente já cadastrado!\nDeseja Sobrescrever?"
                )
                if self.confirmar:
                    pr.cadastrar_cliente(dados)
                    self.limpar_campos_cliente()
                    messagebox.showinfo(
                        title="Salvo",
                        message="Cliente sobrescrito com sucesso!"
                        )
                else:
                    self.limpar_campos_cliente()
        except:
            pass

    def abrir_clientes(self):
        pr.definir_working_directory_padrao()
        if not self.clientes_open:
            try:
                self.root.withdraw()
                pr.mudar_diretorio(pr.clients_path)
                self.clientes_open = True
                self.janela_clientes = Toplevel(self.root)
                self.janela_clientes.title("Gerenciar Clientes")
                self.janela_clientes.geometry(self.tamanho_janela)
                self.janela_clientes.protocol("WM_DELETE_WINDOW",self.fechar_janela_clientes)

                for i in range(5):
                    Grid.rowconfigure(self.janela_clientes,i,weight=1)
                for i in range(2):
                    Grid.columnconfigure(self.janela_clientes,0,weight=1)            
                self.label_nome_cliente = Label(
                    self.janela_clientes,
                    text="Nome",
                    padx=5, pady=5,
                    font="arial 24"
                    )
                
                self.campo_nome_cliente = Entry(
                    self.janela_clientes,
                    font="arial 14"
                    )
                
                self.label_contato = Label(
                    self.janela_clientes,
                    text="Contato / Número de telefone",
                    padx=5, pady=5,
                    font="arial 24"
                    )
                
                self.campo_contato = Entry(
                    self.janela_clientes,
                    font="arial 14"
                    )
                
                self.label_endereco = Label(
                    self.janela_clientes,
                    text="Endereço",
                    padx=5, pady=5,
                    font="arial 24"
                    )
                
                self.campo_endereco = Entry(
                    self.janela_clientes,
                    font="arial 14"
                    )
                
                self.label_observacoes = Label(
                    self.janela_clientes,
                    text="Observacoes:",
                    padx=5, pady=5, 
                    font="arial 24",
                    anchor="n",
                    justify="right"
                    )
                
                self.campo_observacoes = Text(
                    self.janela_clientes,
                    font="arial 14"
                    )
                
                self.botao_ler = Button(
                    self.janela_clientes,
                    text="Buscar Cliente",
                    command=self.carregar_cliente,
                    padx=4, pady=4,
                    font="arial 24"
                    )
                
                self.botao_salvar_cliente = Button(
                    self.janela_clientes,
                    text="Salvar",
                    padx=4, pady=4,
                    font="arial 24",
                    command=self.salvar_cliente
                    )

                self.label_nome_cliente.grid(row=0,column=0,sticky=NSEW)
                self.campo_nome_cliente.grid(row=0,column=1,sticky=NSEW)
                self.label_contato.grid(row=1,column=0,sticky=NSEW)
                self.campo_contato.grid(row=1,column=1,sticky=NSEW)
                self.label_endereco.grid(row=2,column=0,sticky=NSEW)
                self.campo_endereco.grid(row=2,column=1,sticky=NSEW)            
                self.label_observacoes.grid(row=3,column=0,sticky=NSEW)
                self.campo_observacoes.grid(row=3,column=1,sticky=NSEW)
                self.botao_ler.grid(row=4,column=0,sticky=NSEW)
                self.botao_salvar_cliente.grid(row=4,column=1,sticky=NSEW)
            
            except:
                try:
                    self.janela_clientes.destroy()
                    self.root.deiconify()
                except:
                    self.root.deiconify()
        else:
            pr.definir_working_directory_padrao()
            pr.mudar_diretorio(pr.clients_path)
            self.janela_clientes.focus()
    
    def fechar_janela_clientes(self):
        try:
            self.clientes_open = False
            pr.definir_working_directory_padrao()
            self.janela_clientes.destroy()
            self.root.deiconify()
        except:
            pass
    
    def limpar_campo_relatorio(self):
        try:
            self.campo_relatorio.config(state="normal")
            self.campo_relatorio.delete("1.0",END)
            self.campo_relatorio.config(state="disabled")
        except:
            pass
    
    def listar_relatorios(self):
        try:
            pr.mudar_diretorio(pr.reports_path)
            self.dicionario_relatorios = pr.mapa_arquivos("",pr.reports_path)
            self.lista_relatorios.delete(0,END)
            for key in self.dicionario_relatorios:
                self.lista_relatorios.insert(END,key)
        except:
            pass

    def listar_relatorios_dia(self):
        try:
            pr.mudar_diretorio(pr.reports_path)
            filtro = pr.data_hora().split("_")[0]
            self.dicionario_relatorios = pr.mapa_arquivos(filtro,pr.reports_path)
            self.lista_relatorios.delete(0,END)
            for key in self.dicionario_relatorios:
                self.lista_relatorios.insert(END,key)
        except:
            pass

    def exibir_relatorio(self):
        try:
            pr.mudar_diretorio(pr.reports_path)
            self.relatorio_selecionado = str(self.lista_relatorios.get(self.lista_relatorios.curselection()))
            caminho = self.dicionario_relatorios[self.relatorio_selecionado]
            dados = pr.ler_arquivo_json_para_python(caminho)
            cliente = ""
            for key in dados:
                cliente = key
            self.campo_relatorio.config(state="normal")
            self.campo_relatorio.delete("1.0",END)
            self.campo_relatorio.insert(END,f"Cliente: {cliente}\n\n")
            for key in dados[cliente]:
                if key.__contains__("Total"):
                    self.campo_relatorio.insert(END,f"Total da venda: R${dados[cliente][key]}")
                    break
                else:
                    self.campo_relatorio.insert(END,f"{key}\n")
                quantidade = dados[cliente][key]["quantidade"]
                self.campo_relatorio.insert(END,f"Quantidade: {quantidade}\n")
                unitario = dados[cliente][key]["valor_unitario"]
                self.campo_relatorio.insert(END,f"Valor unitário: R${unitario}\n")
                total_item = dados[cliente][key]["total"]
                self.campo_relatorio.insert(END,f"Total do item: R${total_item}\n\n")
            self.campo_relatorio.config(state="disabled")
        except:
            pass

    def fechar_relatorios(self):
        try:
            self.relatorios_open = False
            pr.definir_working_directory_padrao()
            self.janela_relatorios.destroy()
            self.root.deiconify()
        except:
            pass
    
    def abrir_relatorios(self):
        try:
            pr.definir_working_directory_padrao()
            if not self.relatorios_open:
                self.relatorios_open = True
                self.root.withdraw()
                pr.mudar_diretorio(pr.reports_path)
                self.janela_relatorios = Toplevel(self.root)
                self.janela_relatorios.protocol("WM_DELETE_WINDOW",self.fechar_relatorios)
                self.janela_relatorios.title("Relatórios de venda")
                self.janela_relatorios.geometry(self.tamanho_janela)
                self.frame_esquerdo = Frame(self.janela_relatorios)
                self.frame_direito = Frame(self.janela_relatorios)
                self.campo_relatorio = Text(self.frame_direito,font="arial 25")
                self.campo_relatorio.config(state="disabled")
                
                self.dias = Button(
                    self.frame_esquerdo,
                    text="Todos os relatórios",
                    font="arial 25",
                    command=self.listar_relatorios
                    )
                
                self.hoje = Button(
                    self.frame_esquerdo,
                    text="Relatórios de hoje",
                    font="arial 25",
                    command= self.listar_relatorios_dia
                    )
                
                self.exibir = Button(
                    self.frame_esquerdo,
                    text="Exibir relatório selecionado",
                    font="arial 25",
                    command=self.exibir_relatorio
                )
                
                self.lista_relatorios = Listbox(
                    self.frame_esquerdo,
                    font="arial 25"
                    )
                
                self.frame_esquerdo.pack(fill="both",side=LEFT)
                self.frame_direito.pack(fill="both",side=RIGHT)
                self.dias.grid(row=0,column=0,sticky=NSEW)
                self.hoje.grid(row=0,column=1,sticky=NSEW)
                self.exibir.grid(row=2,column=0,columnspan=2,sticky=NSEW)
                self.lista_relatorios.grid(row=1,column=0,columnspan=2,sticky=NSEW)
                self.campo_relatorio.grid(row=1,column=0,columnspan=2,sticky=NSEW)
                Grid.rowconfigure(self.frame_esquerdo,0,weight=1)
                Grid.rowconfigure(self.frame_esquerdo,1,weight=1)
                Grid.rowconfigure(self.frame_esquerdo,2,weight=1)
                Grid.columnconfigure(self.frame_esquerdo,0,weight=1)
                Grid.columnconfigure(self.frame_esquerdo,1,weight=1)
                Grid.rowconfigure(self.frame_direito,0,weight=1)
                Grid.columnconfigure(self.frame_direito,0,weight=1)
                Grid.rowconfigure(self.frame_direito,1,weight=1)
                Grid.columnconfigure(self.frame_direito,1,weight=1)

            else:
                pr.definir_working_directory_padrao()
                pr.mudar_diretorio(pr.reports_path)
                self.janela_relatorios.focus()
        except:
            pass

    def buscar_produtos(self):
        try:
            self.termo_busca = self.campo_busca.get().lower()
            self.resultado_busca = pr.mapa_arquivos(self.termo_busca,pr.products_path)
            self.lista_produtos.delete(0,END)
            for key in self.resultado_busca:
                self.lista_produtos.insert(END,key)
        except:
            pass

    def adicionar_produto(self):
        try:
            pr.mudar_diretorio(pr.products_path)
            self.selecionado = self.lista_produtos.get(self.lista_produtos.curselection())
            self.arquivo_src = self.resultado_busca[self.selecionado]
            self.detalhes_pedido.config(state="normal")
            self.dados_temp = pr.ler_arquivo_json_para_python(self.arquivo_src)
            nome = self.dados_temp["nome"]
            quantidade = pr.numero_string(self.campo_quantidade.get())
            unidade = self.dados_temp["unidade"]
            preco = pr.numero_string(self.dados_temp["preco"])
            estoque = pr.numero_string(self.dados_temp["estoque"])
            estoque_minimo = pr.numero_string(self.dados_temp["estoque_minimo"])
            
            if (type(quantidade) != str) and (type(preco) != str) and ((type(estoque)!=str) or estoque == "n/a"):
                if estoque <= estoque_minimo:
                    messagebox.showinfo(title="Estoque em baixa",message="Atenção!\nEste produto está\ncom estoque abaixo\ndo mínimo\nou abaixo de 0")
                self.total_produto = quantidade * preco
                self.lista_venda.append([self.arquivo_src,quantidade,preco])
                if type(estoque) != str:
                    if quantidade > estoque:
                        messagebox.showinfo(
                            title="Excesso na venda",
                            message="O número de itens desse produto excede o estoque!\nFinalizar essa venda resultará em estoque negativo!")
                self.detalhes_pedido.insert(END,f'{nome} | {quantidade} x {unidade} | R${preco} | Total: R${self.total_produto}\n')
                self.atualizar_valor_venda()
                self.label_valor_venda.config(text=f"Total: R${self.total_venda}")
                self.detalhes_pedido.see(END)
                self.detalhes_pedido.config(state="disabled")
            else:
                messagebox.showwarning(
                    title="Algo de errado aconteceu",
                    message="Atenção!\nO item elecionado possui\num preço inválido ou\nnão foi informado\numa quantidade válida\npara esse item")
        except:
            pass

    def atualizar_valor_venda(self):
        try:
            total = 0
            for linha in self.lista_venda:
                total += linha[1] * linha[2]
            self.total_venda = total
            if type(self.total_venda) == float:
                self.total_venda = round(self.total_venda,2)
        except:
            pass

    def limpar_venda(self):
        try:
            self.lista_venda = []
            self.detalhes_pedido.config(state="normal")
            self.detalhes_pedido.delete("1.0",END)
            self.detalhes_pedido.config(state="disabled")
            self.total_venda = 0
            self.label_valor_venda.config(text=f"Total: R${self.total_venda}")
        except:
            pass

    def remover_produto(self):
            try:
                self.lista_venda.pop()
                self.detalhes_pedido.config(state="normal")
                self.detalhes_pedido.delete("end-2l","end-1l")
                self.detalhes_pedido.config(state="disabled")
                self.atualizar_valor_venda()
                self.label_valor_venda.config(text=f"Total: R${self.total_venda}")
            except:
                pass
  
    def finalizar_venda(self):
        try:
            pr.mudar_diretorio(pr.products_path)
            cliente = "cliente_padrao"
            if len(self.lista_venda) > 0:
                algum_cliente = messagebox.askyesno(title="Cliente",message="Essa venda é para\nalgum cliente cadastrado?")
                if algum_cliente:
                    messagebox.showinfo(message="Por favor, selecione\num cliente a seguir")
                    cliente = filedialog.askopenfilename(initialdir=pr.clients_path)
                    if type(cliente) == tuple:
                        cliente = "cliente_padrao"
                for linha in range(len(self.lista_venda)):
                    nome_arquivo = self.lista_venda[linha][0]
                    arquivo = open(nome_arquivo,encoding="utf-8")
                    dicionario = pr.json.load(arquivo)
                    if dicionario["estoque"] != "n/a":
                        dicionario["estoque"] -= self.lista_venda[linha][1]
                    nome = dicionario["nome"]
                    dados = pr.json.dumps(dicionario,indent=4,ensure_ascii=False)
                    pr.string_para_arquivo(dados,nome_arquivo.replace(".json",""))
                messagebox.showinfo(title="Pronto",message="Venda efetuada\ncom sucesso!")
                pr.gerar_relatorio_venda(cliente,self.lista_venda)
                self.limpar_venda()
            else:
                messagebox.showwarning(title="Vazio",message="Não há nada na lista de venda!")
        except:
            pass
    
    def fechar_vendas(self):
        try:
            pr.definir_working_directory_padrao()
            self.vender_open = False
            self.janela_vendas.destroy()
            self.root.deiconify()
        except:
            pass

    def abrir_vendas(self):
        try:
            pr.definir_working_directory_padrao()
            pr.mudar_diretorio(pr.reports_path)
            self.lista_venda = []
            self.total_produto = 0
            self.total_venda = 0
            if not self.vender_open:
                try:
                    self.root.withdraw()
                    self.vender_open = True
                    self.janela_vendas = Toplevel(self.root)
                    self.janela_vendas.title("Realizar Vendas")
                    self.janela_vendas.geometry(self.tamanho_janela)
                    self.janela_vendas.protocol("WM_DELETE_WINDOW",self.fechar_vendas)
                    self.frame_esquerdo_vendas = Frame(self.janela_vendas)
                    self.frame_direito_vendas = Frame(self.janela_vendas)
                    self.detalhes_pedido = Text(self.frame_direito_vendas,font="arial 25")
                    self.label_valor_venda = Label(
                        self.frame_direito_vendas,
                        font="arial 25",
                        text="Total: R$0",
                        )
                    self.label_busca = Label(
                        self.frame_esquerdo_vendas,
                        text="Nome:",
                        font="arial 25",
                        anchor="w",
                        justify="left"
                        )
                    self.campo_busca = Entry(
                        self.frame_esquerdo_vendas,
                        font="arial 25")            
                    self.botao_buscar_produto = Button(
                        self.frame_esquerdo_vendas,
                        text="Buscar",
                        font="arial 25",
                        command=self.buscar_produtos
                        )           
                    self.lista_produtos = Listbox(
                        self.frame_esquerdo_vendas,
                        font="arial 25"
                        )
                    self.label_quantidade = Label(
                        self.frame_esquerdo_vendas,
                        text="Quantidade: ",
                        font="arial 25"
                        )
                    self.campo_quantidade = Entry(
                        self.frame_esquerdo_vendas,
                        font="arial 25"
                        )
                    self.botao_adicionar_produto = Button(
                        self.frame_esquerdo_vendas,
                        text="Adicionar",
                        font="arial 25",
                        anchor=CENTER,
                        command=self.adicionar_produto
                        )
                    self.botao_remover_produto = Button(
                        self.frame_esquerdo_vendas,
                        text="Remover último produto",
                        font="arial 25",
                        anchor=CENTER,
                        command=self.remover_produto
                        )
                    self.botao_finalizar_venda = Button(
                        self.frame_esquerdo_vendas,
                        text="Finalizar venda",
                        font="arial 25",
                        command=self.finalizar_venda
                        )

                    self.frame_esquerdo_vendas.pack(fill="both",side=LEFT)
                    self.frame_direito_vendas.pack(fill="both",side=RIGHT)
                    self.label_busca.grid(row=0,column=0,sticky=NSEW)
                    self.campo_busca.grid(row=0,column=1,sticky=NSEW)
                    self.botao_buscar_produto.grid(row=1,column=0,columnspan=2,sticky=NSEW)            
                    self.lista_produtos.grid(row=2,column=0,columnspan=2,sticky=NSEW)
                    self.label_quantidade.grid(row=3,column=0,sticky=NSEW)
                    self.campo_quantidade.grid(row=3,column=1,sticky=NSEW)
                    self.botao_adicionar_produto.grid(row=4,column=0,sticky=NSEW)
                    self.botao_remover_produto.grid(row=4,column=1,sticky=NSEW)
                    self.botao_finalizar_venda.grid(row=5,column=0,columnspan=2,sticky=NSEW)
                    for i in range(6):
                        Grid.rowconfigure(self.frame_esquerdo_vendas,i,weight=1)
                    for i in range(2):
                        Grid.columnconfigure(self.frame_esquerdo_vendas,i,weight=1)
                    self.label_valor_venda.pack()
                    self.detalhes_pedido.pack()
                    self.detalhes_pedido.config(state="disabled")
                except:
                    try:
                        self.janela_vendas.destroy()
                        self.root.deiconify()
                    except:
                        self.root.deiconify()
            else:
                self.janela_vendas.focus()
        except:
            pass

    def listar_estoque(self):
        try:
            busca = self.campo_filtro.get().lower()
            self.estoque = pr.mapa_arquivos(busca,pr.products_path)
            self.lista.delete(0,END)
            for key in self.estoque:
                self.lista.insert(END,key)
        except:
            pass

    def exibir_produto(self):
        try:
            pr.mudar_diretorio(pr.products_path)
            selecionado = self.lista.get(self.lista.curselection())
            dados = pr.ler_arquivo_json_para_python(self.estoque[selecionado])
            nome = dados["nome"]
            descricao = dados["descricao"]
            unidade = dados["unidade"]
            preco = dados["preco"]
            estoque = dados["estoque"]
            estoque_minimo = dados["estoque_minimo"]
            self.detalhes.config(state="normal")
            self.detalhes.delete("1.0",END)
            self.detalhes.insert(END,f"Nome:\n")
            self.detalhes.insert(END,f"{nome}\n")
            self.detalhes.insert(END,f"Descrição:\n")
            self.detalhes.insert(END,f"{descricao}\n")
            self.detalhes.insert(END,f"Unidade: {unidade}\n")
            self.detalhes.insert(END,f"Preço: R${preco}\n")
            self.detalhes.insert(END,f"Estoque: {estoque}\n")
            self.detalhes.insert(END,f"Estoque Mínimo: {estoque_minimo}\n")
            self.detalhes.config(state="disabled")
        except:
            pass
    
    def fechar_gerenciar_estoque(self):
        try:    
            self.janela_gerenciar_estoque.destroy()
            self.estoque_open = False
            self.root.deiconify()
        except:
            pass

    def abrir_gerenciar_estoque(self):
        try:
            if not self.estoque_open:
                self.root.withdraw()
                self.estoque_open = True
                self.janela_gerenciar_estoque = Toplevel(self.root)
                self.janela_gerenciar_estoque.protocol(
                    "WM_DELETE_WINDOW",
                    self.fechar_gerenciar_estoque)
                self.janela_gerenciar_estoque.title("Visualizar Estoque")
                self.janela_gerenciar_estoque.geometry(self.tamanho_janela)

                self.frame_l = Frame(self.janela_gerenciar_estoque)
                self.frame_r = Frame(self.janela_gerenciar_estoque)

                self.label_filtro = Label(
                    self.frame_l,
                    font="arial 25",
                    text="Filtrar por nome:"
                    )
                self.campo_filtro = Entry(self.frame_l,font="arial 25")
                self.botao_filtrar = Button(
                    self.frame_l,text="Buscar",
                    font="arial 25",
                    command=self.listar_estoque)
                self.lista = Listbox(
                    self.frame_l,
                    font="arial 25",
                    )
                self.botao_exibir = Button(
                    self.frame_l,
                    text="Visualizar",
                    font="arial 25",
                    command=self.exibir_produto)
                self.detalhes = Text(self.frame_r,font="arial 25")
                for i in range(5):
                    Grid.rowconfigure(self.frame_l,i,weight=1)
                Grid.rowconfigure(self.frame_r,0,weight=1)
                Grid.columnconfigure(self.frame_l,0,weight=1)
                Grid.columnconfigure(self.frame_r,0,weight=1)
                self.frame_l.pack(fill="both",side=LEFT)
                self.frame_r.pack(fill="both",side=RIGHT)
                self.label_filtro.grid(column=0,row=0,sticky=NSEW)
                self.campo_filtro.grid(row=1,column=0,sticky=NSEW)
                self.botao_filtrar.grid(row=2,column=0,sticky=NSEW)
                self.lista.grid(row=3,column=0,sticky=NSEW)
                self.botao_exibir.grid(row=4,column=0,sticky=NSEW)
                self.detalhes.pack(fill="both",side=RIGHT)
            else:
                self.janela_gerenciar_estoque.focus()
        except:
            pass

if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()