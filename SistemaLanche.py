import datetime

class McFastBurguer:
    def __init__(self):
        self.cardapio = {
            "Sanduíches especiais": {
                "Big Fast": 33.00,
                "X-Nervoso": 25.00,
                "X-Double Bacon Cheddar": 20.00,
                "X-Tudo": 22.00,
                "X-Salada Especial": 15.00,
                "X-Calabresa": 15.00,
                "X-Bacon": 17.00,
                "X-Salsicha": 15.00,
                "X-Salada": 12.00,
                "X-Egg": 10.00,
                "X-Burguer": 7.00,
            },
            "Lanches tradicionais": {
                "Americano": 14.00,
                "Bauru": 10.00,
                "Mistão": 7.00,
                "Misto Simples": 6.00,
            },
            "Refrigerantes | Lata 350ml": {
                "Coca-cola (350ml)": 6.00,
                "Guaraná Antártica (350ml)": 6.00,
                "Sprite (350ml)": 6.00,
                "Fanta Uva (350ml)": 6.00,
                "Fanta Laranja (350ml)": 6.00,
            },
            "Refrigerantes | 1 litro": {
                "Coca-cola (1 litro)": 10.00,
                "Guaraná Antártica (1 litro)": 10.00,
                "Baré (1 litro)": 7.00,
            },
            "Refrigerantes | 2 litros": {
                "Coca-cola (2 litros)": 14.00,
                "Guaraná Antártica (2 litros)": 12.00,
                "Baré (2 litros)": 10.00,
            },
            "Porções": {
                "Batata Frita": 17.00,
            },
        }
        self.itens_numerados = []
        self.pedidos = []
        self._numerar_itens()

    def _numerar_itens(self):
        """Associa números aos itens do cardápio para facilitar a seleção."""
        num = 1
        for categoria, itens in self.cardapio.items():
            for item, preco in itens.items():
                self.itens_numerados.append((num, item, preco, categoria))
                num += 1

    def exibir_pedido(self, pedido):
        """Exibe o resumo do pedido e calcula o total."""
        total = 0
        for item, preco, quantidade in pedido:
            total += preco * quantidade
        return total
    def gerar_relatorio(self):
        """Gera o relatório de vendas baseado nos pedidos registrados."""
        total_vendas = 0
        relatorio = "----- Relatório de Vendas -----\n"
        for i, pedido in enumerate(self.pedidos, start=1):
            relatorio += f"\nPedido #{i} - {pedido['data_hora'].strftime('%d/%m/%Y %H:%M:%S')}\n"  # Adiciona data e hora
            total_pedido = 0
            for item, preco, quantidade in pedido["itens"]:
                subtotal = preco * quantidade
                relatorio += f"  {quantidade}x {item:<30} R${subtotal:.2f}\n"
                total_pedido += subtotal
            relatorio += f"  Total do pedido: R$ {total_pedido:.2f}\n"
            relatorio += f"  Status: {pedido['status']}\n"
            total_vendas += total_pedido
        relatorio += f"\nTotal Final do Dia: R${total_vendas:.2f}\n"
        relatorio += "-------------------------------"
        return relatorio
    
 

