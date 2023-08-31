from tkinter import Tk,Label,Entry,Button,Text,Toplevel,Radiobutton,Frame,Listbox,ttk
from tkinter import filedialog,messagebox,Grid,NSEW,END,LEFT,RIGHT,TOP,BOTTOM,CENTER
import processamento as pr
from processamento import path
from PIL import Image, ImageTk

class App:
    def __init__(self,root):
        pr.definir_working_directory_padrao()
        pr.gerar_qrcode(pr.pix_qrcode())
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
        self.root.title("Gerencial Fácil")

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

        self.botao_relatorios = Button(
            self.root,
            text="Exibir Relatórios de Venda",
            padx=5, pady=5,
            font="arial 25",
            command=self.abrir_relatorios
            )

        self.botao_vendas = Button(
            self.root,
        text="Executar Vendas",
        padx=5, pady=5,
        font="arial 25",
        command=self.abrir_vendas
        )

        self.botao_checar_estoque = Button(
            self.root,
            text="Checar Estoque",
            padx=5,pady=5,
            font="arial 25"
            )

        self.botao_obrigado = Button(
            self.root,
            text="Créditos e Agradecimentos",
            padx=5, pady=5,
            font="arial 25",
            command = self.abrir_janela_obrigado
        )

        for i in range(6):
            Grid.rowconfigure(self.root, i, weight=1)
        Grid.columnconfigure(self.root, 0, weight=1)

        self.botao_produtos.grid(row=0, column=0, sticky=NSEW)
        self.botao_clientes.grid(row=1, column=0, sticky=NSEW)
        self.botao_relatorios.grid(row=2, column=0, sticky=NSEW)
        self.botao_vendas.grid(row=3,column=0,sticky=NSEW)
        self.botao_checar_estoque.grid(row=4,column=0,sticky=NSEW)
        self.botao_obrigado.grid(row=5, column=0,sticky=NSEW)

    def abrir_janela_obrigado(self):
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
            recurso = Image.open(pr.qrcode_path)
            recurso2 = recurso.resize((300,300))
            imagem = ImageTk.PhotoImage(recurso2)
            self.label_qrcode = Label(self.frame_obrigado,image=imagem)
            self.label_qrcode.photo = imagem
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
        else:
            self.abrir_janela_obrigado.focus()
    
    def fechar_janela_obrigado(self):
        self.obrigado_open = False
        self.janela_obrigado.destroy()
        self.root.deiconify()

    def salvar_produto(self):
        dados = {}
        dados["nome"] = self.campo_produto_nome.get()
        dados["descricao"] = self.campo_descricao.get()
        dados["unidade"] = self.campo_unidade.get().lower()
        dados["preco"] = pr.numero_string(self.campo_preco.get())
        dados["estoque"] = pr.numero_string(self.campo_estoque.get().lower())
        dados["estoque_minimo"] = pr.numero_string(self.campo_estoque_minimo.get())
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
                    message="Produto cadastrado com sucesso"
                    )
            else:
                self.limpar_campos_produto()

    def limpar_campos_produto(self):
        self.campo_produto_nome.delete(0,END)
        self.campo_descricao.delete(0,END)
        self.campo_unidade.delete(0,END)
        self.campo_preco.delete(0,END)
        self.campo_estoque.delete(0,END)
        self.campo_estoque_minimo.delete(0,END)

    def carregar_produto(self):
        pr.mudar_diretorio(pr.products_path)
        print(pr.getcwd())
        tipos = [("Produto","*_produto.json")]
        self.caminho = filedialog.askopenfilename(
            initialdir=pr.getcwd(),
            title="Selecione o arquivo de um Produto",
            filetypes=tipos
            )
        try:
            dados = pr.ler_arquivo_json_para_python(caminho)
            self.limpar_campos_produto()
            self.campo_produto_nome.insert(0,dados["nome"])
            self.campo_descricao.insert(0,dados["descricao"])
            self.campo_unidade.insert(0,dados["unidade"])
            self.campo_preco.insert(0,dados["preco"])
            self.campo_estoque.insert(0,dados["estoque"])
            self.campo_estoque_minimo.insert(0,dados["estoque_minimo"])
        except:
            pass

        pr.mudar_diretorio(pr.root_path)

    def abrir_produtos(self):
        if not self.produtos_open:
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

        else:
            self.janela_produtos.focus()

    def fechar_janela_produtos(self):
        self.produtos_open = False
        pr.mudar_diretorio(pr.root_path)
        self.janela_produtos.destroy()
        self.root.deiconify()
    
    def limpar_campos_cliente(self):
        self.campo_nome_cliente.delete(0,END)
        self.campo_contato.delete(0,END)
        self.campo_endereco.delete(0,END)
        self.campo_observacoes.delete("1.0",END)

    def carregar_cliente(self):
        pr.mudar_diretorio(pr.clients_path)
        print(pr.getcwd())
        tipos = [("Cliente","*_cliente.json")]
        self.caminho = filedialog.askopenfilename(
            initialdir=pr.getcwd(),
            title="Selecione o arquivo de um cliente",
            filetypes=tipos
            )
        
        try:
            dados = pr.ler_arquivo_json_para_python(caminho)
        
            self.limpar_campos_cliente()
        
            self.campo_nome_cliente.insert(0,dados["nome"])
            self.campo_contato.insert(0,dados["contato"])
            self.campo_endereco.insert(0,dados["endereco"])
            self.campo_observacoes.insert(1.0,dados["observacoes"])
        except:
            pass
        
        pr.mudar_diretorio(pr.root_path)

    def salvar_cliente(self):
        dados = {}
        dados["nome"] = self.campo_nome_cliente.get()
        dados["contato"] = self.campo_contato.get()
        dados["endereco"] = self.campo_endereco.get()
        dados["observacoes"] = self.campo_observacoes.get("1.0","end-1c")
        pr.cadastrar_cliente(dados)
        self.limpar_campos_cliente()

        messagebox.showinfo(
            title="Salvo",
            message="Cliente cadastrado com sucesso!"
            )
    
    def abrir_clientes(self):
        if not self.clientes_open:
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
                text="Observacoes\n sobre o \nCliente",
                padx=5, pady=5, 
                font="arial 24"
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
        
        else:
            self.janela_clientes.focus()
    
    def fechar_janela_clientes(self):
        self.clientes_open = False
        pr.mudar_diretorio(pr.root_path)
        self.janela_clientes.destroy()
        self.root.deiconify()
    
    def fechar_relatorios(self):
        self.relatorios_open = False
        self.janela_relatorios.destroy()
        self.root.deiconify()
    
    def abrir_relatorios(self):
        if not self.relatorios_open:
            self.relatorios_open = True
            self.root.withdraw()
            self.janela_relatorios = Toplevel(self.root)
            self.janela_relatorios.protocol("WM_DELETE_WINDOW",self.fechar_relatorios)
            self.janela_relatorios.title("Relatórios de venda")
            self.janela_relatorios.geometry(self.tamanho_janela)
            self.frame_esquerdo = Frame(self.janela_relatorios)
            self.frame_direito = Frame(self.janela_relatorios)
            self.campo_relatorio = Text(self.frame_direito,font="arial 25")
            
            self.dias = Radiobutton(
                self.frame_esquerdo,
                text="Relatórios diários",
                font="arial 25"
                )
            
            self.hoje = Radiobutton(
                self.frame_esquerdo,
                text="Relatórios de hoje",
                font="arial 25"
                )
            
            self.lista_relatorios = Listbox(
                self.frame_esquerdo,
                font="arial 25"
                )
            
            self.frame_esquerdo.pack(fill="both",side=LEFT)
            self.frame_direito.pack(fill="both",side=RIGHT)
            self.dias.grid(row=0,column=0,sticky=NSEW)
            self.hoje.grid(row=0,column=1,sticky=NSEW)
            self.lista_relatorios.grid(row=1,column=0,columnspan=2,sticky=NSEW)
            self.campo_relatorio.grid(row=1,column=0,columnspan=2,sticky=NSEW)
            Grid.rowconfigure(self.frame_esquerdo,0,weight=1)
            Grid.rowconfigure(self.frame_esquerdo,1,weight=1)
            Grid.columnconfigure(self.frame_esquerdo,0,weight=1)
            Grid.columnconfigure(self.frame_esquerdo,1,weight=1)
            Grid.rowconfigure(self.frame_direito,0,weight=1)
            Grid.columnconfigure(self.frame_direito,0,weight=1)
            Grid.rowconfigure(self.frame_direito,1,weight=1)
            Grid.columnconfigure(self.frame_direito,1,weight=1)

        else:
            self.janela_relatorios.focus()

    def fechar_vendas(self):
        pr.mudar_diretorio(pr.root_path)
        self.vender_open = False
        self.janela_vendas.destroy()
        self.root.deiconify()

    def abrir_vendas(self):
        if not self.vender_open:
            self.root.withdraw()
            self.vender_open = True
            self.janela_vendas = Toplevel(self.root)
            self.janela_vendas.title("Realizar Vendas")
            self.janela_vendas.geometry(self.tamanho_janela)
            self.janela_vendas.protocol("WM_DELETE_WINDOW",self.fechar_vendas)
            self.frame_esquerdo_vendas = Frame(self.janela_vendas)
            self.frame_direito_vendas = Frame(self.janela_vendas)
            self.detalhes_pedido = Text(self.frame_direito_vendas,font="arial 25")
            self.label_qantidade = Label(
                self.frame_esquerdo_vendas,
                text="Quantidade: ",
                font="arial 25"
                )
            self.campo_quantidade = Entry(
                self.frame_esquerdo_vendas,
                font="arial 25"
                )
            self.label_busca = Label(
                self.frame_esquerdo_vendas,
                text=" Nome do Produto: ",
                font="arial 25"
                )
            self.campo_busca = Entry(self.frame_esquerdo_vendas,font="arial 25")
            self.lista_produtos = Listbox(self.frame_esquerdo_vendas,font="arial 25")
            
            self.botao_adicionar_produto = Button(
                self.frame_esquerdo_vendas,
                text="Adicionar",
                font="arial 25"
                )

            self.botao_remover_produto = Button(
                self.frame_esquerdo_vendas,
                text="Remover",
                font="arial 25"
                )

            self.botao_finalizar_venda = Button(
                self.frame_esquerdo_vendas,
                text="Finalizar venda",
                font="arial 25"
                )
            self.botao_buscar_produto = Button(
                self.frame_esquerdo_vendas,
                text="Buscar",
                font="arial 25"
                )
            self.frame_esquerdo_vendas.pack(fill="both",side=LEFT)
            self.frame_direito_vendas.pack(fill="both",side=RIGHT)
            self.label_busca.grid(row=0,column=0,columnspan=2,sticky=NSEW)
            self.campo_busca.grid(row=1,column=0,columnspan=2,sticky=NSEW)
            self.botao_buscar_produto.grid(row=2,column=0,columnspan=2,sticky=NSEW)
            self.lista_produtos.grid(row=3,column=0,columnspan=2,sticky=NSEW)
            self.botao_adicionar_produto.grid(row=4,column=0,sticky=NSEW)
            self.botao_remover_produto.grid(row=4,column=1,sticky=NSEW)
            self.botao_finalizar_venda.grid(row=5,column=0,columnspan=2,sticky=NSEW)
            for i in range(6):
                Grid.rowconfigure(self.frame_esquerdo_vendas,i,weight=1)
            for i in range(2):
                Grid.columnconfigure(self.frame_esquerdo_vendas,i,weight=1)
            self.detalhes_pedido.grid(row=0,column=0,sticky=NSEW)
            Grid.rowconfigure(self.frame_direito_vendas,0,weight=1)
            Grid.columnconfigure(self.frame_direito_vendas,0,weight=1)
     
        else:
            self.janela_vendas.focus()


if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()