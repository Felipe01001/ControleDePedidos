import datetime
from SistemaLanche import McFastBurguer
import tkinter as tk
from tkinter import Toplevel, ttk, messagebox, simpledialog, PhotoImage


class McFastBurguerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("McFast Burguer - Sistema de Pedidos")
        self.mc_fast_burguer = McFastBurguer()
        self.pedido_atual = []  # Lista para manter todos os itens do pedido atual

        # Tema escuro
        self.root.configure(bg="#333333")
        estilo = ttk.Style()
        estilo.theme_use('clam')
        estilo.configure("Treeview", 
            background="#999999", 
            foreground="white", 
            fieldbackground="#333333"
        )
        estilo.map('Treeview', background=[('selected', '#555555')])
        self.icone_aumentar = PhotoImage(file="img/botao-de-upload.png")
        self.icone_apagar = PhotoImage(file="img/excluir.png")

        # Configuração de frames
        self.frame_cardapio = tk.Frame(root, bg="#222222")  # Cor de fundo do frame
        self.frame_cardapio.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.frame_pedido = tk.Frame(root, bg="#222222")  # Cor de fundo do frame
        self.frame_pedido.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Inicialização das interfaces
        self._criar_cardapio()
        self._criar_pedido()

    def aumentar_quantidade(self):
        """Aumenta a quantidade do item selecionado no pedido."""
        selecionado = self.lista_pedido.focus()
        if selecionado:
            try:
                indice = self.lista_pedido.index(selecionado)
                item, preco, quantidade = self.pedido_atual[indice]
                quantidade += 1
                self.pedido_atual[indice] = (item, preco, quantidade)
                self._atualizar_pedido()
            except IndexError:
                messagebox.showwarning("Aviso", "Selecione um item válido no pedido.")

    def remover_item(self):
        """Remove o item selecionado do pedido."""
        selecionado = self.lista_pedido.focus()
        if selecionado:
            try:
                indice = self.lista_pedido.index(selecionado)
                del self.pedido_atual[indice]
                self._atualizar_pedido()
            except IndexError:
                messagebox.showwarning("Aviso", "Selecione um item válido no pedido.")

    def abrir_janela_controle(self):
        """Abre uma nova janela para controle dos pedidos."""
        if hasattr(self, "janela_controle") and self.janela_controle.winfo_exists():
            self.janela_controle.lift()
            return

        self.janela_controle = Toplevel(self.root)
        self.janela_controle.title("Controle de Pedidos")

        # Tabela de pedidos (adicionando coluna Data/Hora)
        self.lista_controle = ttk.Treeview(
                self.janela_controle,
                columns=("Pedido","Item", "Quantidade", "Preço", "Status", "Data/Hora"),
                show="headings",
                height=20
            )              
        self.lista_controle.pack(fill=tk.BOTH, expand=True)  # Exibe a tabela
        self.lista_controle.heading("Pedido", text="Pedido")  # Cabeçalho da coluna
        self.lista_controle.column("Pedido", width=80, anchor=tk.CENTER)  # Largura e alinhamento
        self.lista_controle.heading("#0", text="Pedido")
        self.lista_controle.heading("Item", text="Item")
        self.lista_controle.heading("Quantidade", text="Quantidade")
        self.lista_controle.heading("Preço", text="Preço (R$)")
        self.lista_controle.heading("Status", text="Status")
        self.lista_controle.heading("Data/Hora", text="Data/Hora")  # Adicionando cabeçalho
        self.lista_controle.column("#0", width=100, anchor=tk.W)
        self.lista_controle.column("Item", width=200, anchor=tk.W)
        self.lista_controle.column("Quantidade", width=100, anchor=tk.CENTER)
        self.lista_controle.column("Preço", width=100, anchor=tk.CENTER)
        self.lista_controle.column("Status", width=100, anchor=tk.CENTER)
        self.lista_controle.column("Data/Hora", width=150, anchor=tk.CENTER)  # Adicionando coluna

        # Botão para marcar como concluído
        btn_concluir = tk.Button(
            self.janela_controle,
            text="Marcar como Concluído",
            command=self.marcar_como_concluido
        )
        btn_concluir.pack(pady=5)

        self._atualizar_janela_controle()


    def _atualizar_janela_controle(self):
        """Atualiza os dados na janela de controle."""
        self.lista_controle.delete(*self.lista_controle.get_children())

        for idx, pedido in enumerate(self.mc_fast_burguer.pedidos, start=1):
            # Adiciona o título do pedido como nó principal (incluindo data/hora)
            data_hora_formatada = pedido["data_hora"].strftime('%d/%m/%Y %H:%M:%S')
            
            # Criando uma lista de valores para a linha do pedido
            valores_pedido = [idx, "", "", "", pedido["status"], data_hora_formatada]  
            
            pedido_id = self.lista_controle.insert(
                "", tk.END, text=f"Pedido #{idx}", values=valores_pedido
            )

            total_pedido = 0
            for item, preco, quantidade in pedido["itens"]:
                subtotal = preco * quantidade
                total_pedido += subtotal
                
                # Criando uma lista de valores para a linha do item
                valores_item = [idx, item, quantidade, f"{subtotal:.2f}", "", ""]  
                
                self.lista_controle.insert(
                    pedido_id, tk.END, values=valores_item
                )

            # Inserir o total do pedido na Treeview
            valores_total = [idx, "", "", f"Total: R$ {total_pedido:.2f}", "", ""]
            self.lista_controle.insert(
                pedido_id, tk.END, values=valores_total
            )

            if pedido["status"] == "concluído":
                self.lista_controle.item(pedido_id, tags=("concluido",))

            self.lista_controle.tag_configure("concluido", background="lightgreen")

    def marcar_como_concluido(self):
        """Marca o pedido selecionado como concluído."""
        item_selecionado = self.lista_controle.focus()
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um pedido.")
            return

        # Verifica se o item selecionado é um título de pedido
        valores = self.lista_controle.item(item_selecionado)["values"]
        if not valores or valores[4] == "":  # Alterar índice para 4
            messagebox.showwarning("Aviso", "Selecione o título de um pedido para concluir.")
            return

        # Atualiza o status do pedido
        pedido_idx = int(self.lista_controle.item(item_selecionado)["text"].split("#")[1]) - 1
        self.mc_fast_burguer.pedidos[pedido_idx]["status"] = "concluído"

        self._atualizar_janela_controle()

    def aumentar_quantidade(self):
        """Aumenta a quantidade do item selecionado no pedido."""
        item_selecionado = self.lista_pedido.focus()
        if item_selecionado:
            try:
                item_index = self.lista_pedido.index(item_selecionado)
                item, preco, quantidade = self.pedido_atual[item_index]
                quantidade += 1
                self.pedido_atual[item_index] = (item, preco, quantidade)
                self._atualizar_pedido()
            except IndexError:
                messagebox.showwarning("Aviso", "Selecione um item válido no pedido.")


    def mostrar_botao_aumentar_quantidade(self, event=None):
        """Mostra o botão 'Aumentar Quantidade' se um item estiver selecionado."""
        if self.lista_pedido.focus():  # Verifica se há item selecionado
            self.btn_aumentar_quantidade.pack(pady=5)
        else:
            self.btn_aumentar_quantidade.pack_forget()

    def mostrar_botoes_item(self, event=None):
        """Mostra/oculta os botões de apagar e aumentar quantidade quando um item estiver selecionado."""
        if self.lista_pedido.focus():  # Verifica se há item selecionado
            self.btn_apagar_item.pack(side="right", padx=7)  # Mostra o botão de apagar à esquerda
            self.btn_aumentar_quantidade.pack(side="left", padx=5)  # Mostra o botão de aumentar à esquerda
        else:
            self.btn_apagar_item.pack_forget()  # Oculta o botão de apagar
            self.btn_aumentar_quantidade.pack_forget()  # Oculta o botão de aumentar

    def _criar_cardapio(self):
        """Cria a interface do cardápio."""
        label_cardapio = tk.Label(self.frame_cardapio, text="Cardápio", font=("Helvetica", 20, "bold"), bg="#222222", fg="white")
        label_cardapio.pack(pady=10)

        # Corrigindo a fonte do Treeview
        estilo_treeview = ttk.Style()
        estilo_treeview.configure("meu_estilo.Treeview", font=("Helvetica", 12))

        def adicionar_item_direto(event=None):
            """Adiciona o item selecionado ao pedido com quantidade 1."""
            item_selecionado = self.lista_cardapio.focus()
            if item_selecionado:
                dados_item = self.lista_cardapio.item(item_selecionado)
                item_nome = dados_item.get("text", "")
                if item_nome:  # Verifica se o item tem um nome válido
                    preco = None
                    for _, nome, preco_item, _ in self.mc_fast_burguer.itens_numerados:
                        if nome == item_nome:
                            preco = preco_item
                            break

            if preco is not None:
                self.pedido_atual.append((item_nome, preco, 1))  # Quantidade 1
                self._atualizar_pedido()
                messagebox.showinfo("Item Adicionado", f"'{item_nome}' adicionado ao pedido.")

        self.lista_cardapio = ttk.Treeview(self.frame_cardapio, columns=("Preço"), show="tree headings", height=20, style="meu_estilo.Treeview")
        self.lista_cardapio.bind("<Return>", self.adicionar_ao_pedido)  # Vincula o evento <Return>
        self.lista_cardapio.heading("#0", text="Categoria / Item")
        self.lista_cardapio.heading("Preço", text="Preço (R$)")
        self.lista_cardapio.column("#0", width=200, anchor=tk.W)
        self.lista_cardapio.column("Preço", width=100, anchor=tk.CENTER)
        self.lista_cardapio.pack(fill=tk.BOTH, expand=True)
        self.lista_cardapio.bind("<Double-Button-1>", adicionar_item_direto)  # Clique duplo
        self.lista_cardapio.bind("<Return>", adicionar_item_direto)  # Tecla Enter

        for categoria, itens in self.mc_fast_burguer.cardapio.items():
            cat_id = self.lista_cardapio.insert("", tk.END, text=categoria, open=True)
            for item, preco in itens.items():
                self.lista_cardapio.insert(cat_id, tk.END, text=item, values=(f"{preco:.2f}"))

         # Botão adicionar com hover
        btn_adicionar = tk.Button(self.frame_cardapio, text="Adicionar ao Pedido", command=self.adicionar_ao_pedido)
        btn_adicionar.pack(pady=10)
        btn_adicionar.bind("<Enter>", lambda e: btn_adicionar.config(bg="#555555"))
        btn_adicionar.bind("<Leave>", lambda e: btn_adicionar.config(bg="SystemButtonFace"))
       

        # Botão controle com hover
        btn_controle = tk.Button(self.frame_cardapio, text="Abrir Controle de Pedidos", command=self.abrir_janela_controle)
        btn_controle.pack(pady=5)
        btn_controle.bind("<Enter>", lambda e: btn_controle.config(bg="#555555"))
        btn_controle.bind("<Leave>", lambda e: btn_controle.config(bg="SystemButtonFace"))


        

    def _criar_pedido(self):
        """Cria a interface do pedido."""
        label_pedido = tk.Label(self.frame_pedido, text="Pedido Atual", font=("Helvetica", 20, "bold"), bg="#222222", fg="white")  # Cor de fundo e texto
        label_pedido.pack(pady=10)

        # Corrigindo a fonte do Treeview
        estilo_treeview = ttk.Style()
        estilo_treeview.configure("meu_estilo.Treeview", font=("Helvetica", 12))

        self.lista_pedido = ttk.Treeview(
            self.frame_pedido, 
            columns=("Item", "Quantidade", "Preço"), 
            show="headings", 
            height=20, 
            style="meu_estilo.Treeview"  # Aplicando o estilo
        )
        
        self.lista_pedido.heading("Item", text="Item")
        self.lista_pedido.heading("Quantidade", text="Quantidade")
        self.lista_pedido.heading("Preço", text="Preço (R$)")
        self.lista_pedido.column("Item", width=200, anchor=tk.W)
        self.lista_pedido.column("Quantidade", width=100, anchor=tk.CENTER)
        self.lista_pedido.column("Preço", width=100, anchor=tk.CENTER)
        self.lista_pedido.pack(fill=tk.BOTH, expand=True)
        self.lista_pedido.bind("<<TreeviewSelect>>", self.mostrar_botoes_item)

        # Botão finalizar com hover
        btn_finalizar = tk.Button(self.frame_pedido, text="Finalizar Pedido", command=self.finalizar_pedido)
        btn_finalizar.pack(pady=5)
        btn_finalizar.bind("<Enter>", lambda e: btn_finalizar.config(bg="#555555"))
        btn_finalizar.bind("<Leave>", lambda e: btn_finalizar.config(bg="SystemButtonFace"))

        # Botão relatório com hover
        btn_relatorio = tk.Button(self.frame_pedido, text="Gerar Relatório", command=self.gerar_relatorio)
        btn_relatorio.pack(pady=5)
        btn_relatorio.bind("<Enter>", lambda e: btn_relatorio.config(bg="#555555"))
        btn_relatorio.bind("<Leave>", lambda e: btn_relatorio.config(bg="SystemButtonFace"))

         # Botão para apagar o item
        self.btn_apagar_item = tk.Button(self.frame_pedido, image=self.icone_apagar, command=self.remover_item)
        self.btn_apagar_item.pack_forget()  # Inicialmente oculto

        # Botão para aumentar a quantidade
        self.btn_aumentar_quantidade = tk.Button(self.frame_pedido, image=self.icone_aumentar, command=self.aumentar_quantidade)
        self.btn_aumentar_quantidade.pack_forget()  # Inicialmente oculto
        

    def adicionar_ao_pedido(self):
        """Adiciona um item ao pedido e atualiza a janela de controle."""
        item_selecionado = self.lista_cardapio.focus()
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um item do cardápio.")
            return
            

        # Obtém informações do item selecionado
        dados_item = self.lista_cardapio.item(item_selecionado)
        item_nome = dados_item.get("text", "")  # Nome do item está no campo "text"
        item_valores = dados_item.get("values", [])
        

        # Verifica se o item tem um nome válido
        if not item_nome:
            messagebox.showwarning("Aviso", "Por favor, selecione um item válido.")
            return

        # Pergunta a quantidade ao usuário
        quantidade = simpledialog.askinteger("Quantidade", f"Digite a quantidade para {item_nome}:")
        if not quantidade or quantidade <= 0:
            messagebox.showwarning("Aviso", "Quantidade inválida.")
            return

        # Busca o preço do item
        preco = None
        for _, nome, preco_item, _ in self.mc_fast_burguer.itens_numerados:
            if nome == item_nome:
                preco = preco_item
                break

        # Valida se encontrou o item
        if preco is None:
            messagebox.showerror("Erro", "Item não encontrado no sistema.")
            return

        # Adiciona o item ao pedido atual
        self.pedido_atual.append((item_nome, preco, quantidade))
        self._atualizar_pedido()  # Atualiza a interface do pedido
        messagebox.showinfo("Item Adicionado", f"{quantidade}x '{item_nome}' adicionado(s) ao pedido.")



    def _atualizar_pedido(self):
        """Atualiza a visualização do pedido atual."""
        self.lista_pedido.delete(*self.lista_pedido.get_children())
        for item, preco, quantidade in self.pedido_atual:
            subtotal = preco * quantidade
            self.lista_pedido.insert("", tk.END, values=(item, quantidade, f"{subtotal:.2f}"))
    def finalizar_pedido(self):
        """Finaliza o pedido atual."""
        if not self.pedido_atual:
            messagebox.showwarning("Aviso", "Nenhum pedido registrado.")
            return

        # Obtém a data e hora atuais
        data_hora = datetime.datetime.now()

        # Salva o pedido com status inicial "pendente" e data/hora
        self.mc_fast_burguer.pedidos.append({"itens": self.pedido_atual[:], "status": "pendente", "data_hora": data_hora})

        total = sum(preco * quantidade for _, preco, quantidade in self.pedido_atual)
        self.pedido_atual.clear()
        self._atualizar_pedido()
        messagebox.showinfo("Pedido Finalizado", f"Total do pedido: R$ {total:.2f}")


    def gerar_relatorio(self):
        """Exibe o relatório de vendas e permite copiar o texto."""
        if not self.mc_fast_burguer.pedidos:
            messagebox.showinfo("Relatório", "Nenhum pedido foi registrado.")
            return

        # Gera o relatório com base nos pedidos
        relatorio = self.mc_fast_burguer.gerar_relatorio()

        # Cria uma nova janela para exibir o relatório
        relatorio_window = Toplevel(self.root)
        relatorio_window.title("Relatório de Vendas")

        # Campo de texto para exibir o relatório
        text_area = tk.Text(relatorio_window, wrap=tk.WORD, width=80, height=25)
        text_area.insert("1.0", relatorio)
        text_area.config(state=tk.DISABLED)  # Apenas leitura
        text_area.pack(padx=10, pady=10)

        # Função para copiar o texto do relatório
        def copiar_para_area_transferencia():
            self.root.clipboard_clear()
            self.root.clipboard_append(relatorio)
            self.root.update()  # Atualiza a área de transferência
            messagebox.showinfo("Copiado", "Relatório copiado para a área de transferência!")

        # Botão para copiar o relatório
        btn_copiar = tk.Button(relatorio_window, text="Copiar Relatório", command=copiar_para_area_transferencia)
        btn_copiar.pack(pady=5)

        # Botão para fechar a janela
        btn_fechar = tk.Button(relatorio_window, text="Fechar", command=relatorio_window.destroy)
        btn_fechar.pack(pady=5)



root = tk.Tk()
app = McFastBurguerApp(root)
root.mainloop()
