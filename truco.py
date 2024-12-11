import random

class Carta:
    def __init__(self, forca):
        self.forca = forca

class Jogador:
    def __init__(self, nome, equipe):
        self.nome = nome
        self.equipe = equipe
        self.mao = []

class Equipe:
    def __init__(self, nome):
        self.nome = nome
        self.jogadores = []
        self.pontos = 0

class Jogo:
    def __init__(self):
        self.baralho = []
        self.equipe1 = Equipe("Equipe 1")
        self.equipe2 = Equipe("Equipe 2")
        self.valor_rodada = 1
        self.cartas_jogadas = []
        self.rodada_atual = 0
        self.vez_atual = 0
        self.truco_pedido = False
        self.quem_pediu_truco = None

    def criar_baralho(self):
        # Criar 4 cópias de cada carta de 1 a 6
        for forca in range(1, 7):
            for _ in range(4):
                self.baralho.append(Carta(forca))

        # Adicionar as manilhas (valores únicos)
        for forca in range(7, 11):
            self.baralho.append(Carta(forca))

        # Remover uma carta aleatória de 1 a 6
        cartas_removiveis = [carta for carta in self.baralho if 1 <= carta.forca <= 6]
        carta_removida = random.choice(cartas_removiveis)
        self.baralho.remove(carta_removida)

        # Embaralhar
        random.shuffle(self.baralho)

    def iniciar_jogo(self):
        # Criar jogadores e equipes
        self.equipe1.jogadores = [Jogador(f"Jogador 1", self.equipe1), Jogador(f"Jogador 3", self.equipe1)]
        self.equipe2.jogadores = [Jogador(f"Jogador 2", self.equipe2), Jogador(f"Jogador 4", self.equipe2)]

        # Ordem dos jogadores
        self.jogadores = [
            self.equipe1.jogadores[0],
            self.equipe2.jogadores[0],
            self.equipe1.jogadores[1],
            self.equipe2.jogadores[1]
        ]

        # Distribuir cartas
        for jogador in self.jogadores:
            for _ in range(3):
                jogador.mao.append(self.baralho.pop())

    def get_estado_jogo(self):
        """Retorna o estado do jogo como um dicionário para a IA."""
        return {
            "cartas_jogadas": [(jogador.nome, carta.forca) 
                              for jogador, carta in self.cartas_jogadas],
            "mao_jogadores": {
                jogador.nome: [carta.forca for carta in jogador.mao]
                for jogador in self.jogadores
            },
            "valor_rodada": self.valor_rodada,
            "pontos": {
                self.equipe1.nome: self.equipe1.pontos,
                self.equipe2.nome: self.equipe2.pontos
            },
            "rodada_atual": self.rodada_atual,
            "truco_pedido": self.truco_pedido,
            "quem_pediu_truco": self.quem_pediu_truco.nome if self.quem_pediu_truco else None
        }

    def jogar_rodada(self, decidir_acao):
        """Executa uma rodada completa utilizando a função de decisão da IA."""
        self.cartas_jogadas = []
        self.rodada_atual += 1
        
        for jogador in self.jogadores:
            if not jogador.mao:
                print(f"{jogador.nome} não tem mais cartas para jogar.")
                continue

            estado = self.get_estado_jogo()
            
            # Se houver truco pedido, precisa responder primeiro
            if self.truco_pedido and jogador.equipe != self.quem_pediu_truco.equipe:
                resposta = decidir_acao(jogador, estado, "resposta_truco")
                print(f"{jogador.nome} decidiu {resposta} para truco.")
                if resposta == "correr":
                    self.quem_pediu_truco.equipe.pontos += self.valor_rodada
                    return
                elif resposta == "aumentar":
                    self.valor_rodada = min(12, self.valor_rodada + 3)
                self.truco_pedido = False
                self.quem_pediu_truco = None

            acao = decidir_acao(jogador, estado, "normal")
            print(f"{jogador.nome} decidiu {acao['tipo']}.")

            if acao["tipo"] == "jogar":
                carta_jogada = jogador.mao.pop(acao["indice"])
                if acao.get("escondida", False) and self.rodada_atual > 1:
                    carta_jogada.forca = 0
                self.cartas_jogadas.append((jogador, carta_jogada))
            elif acao["tipo"] == "truco":
                self.truco_pedido = True
                self.quem_pediu_truco = jogador
                self.valor_rodada += 3
                continue

        # Determinar vencedor da rodada se houver cartas jogadas
        if self.cartas_jogadas:
            vencedor = max(self.cartas_jogadas, key=lambda x: x[1].forca)
            vencedor[0].equipe.pontos += self.valor_rodada
            print(f"{vencedor[0].nome} ganhou a rodada com carta de força {vencedor[1].forca}.")

    def verificar_vencedor(self):
        if self.equipe1.pontos >= 12:
            return self.equipe1
        elif self.equipe2.pontos >= 12:
            return self.equipe2
        return None

# Exemplo de função de decisão para a IA
def decidir_acao_ia(jogador, estado, tipo_decisao="normal"):
    """Decide ações de forma mais elaborada com base no estado do jogo."""
    if tipo_decisao == "resposta_truco":
        # Decidir entre correr, aceitar ou aumentar
        escolha = random.choice(["correr", "aceitar", "aumentar"])
        return escolha
    
    # Decisão normal
    if estado["rodada_atual"] > 1 and random.random() < 0.2:
        # 20% de chance de jogar carta escondida após primeira rodada
        escolha = {
            "tipo": "jogar",
            "indice": random.randint(0, len(jogador.mao) - 1),
            "escondida": True
        }
        print(f"{jogador.nome} jogou carta escondida: {escolha}.")
        return escolha
    elif not estado["truco_pedido"] and random.random() < 0.3:
        # 30% de chance de pedir truco se ainda não foi pedido
        escolha = {"tipo": "truco"}
        print(f"{jogador.nome} pediu truco.")
        return escolha
    else:
        # Jogar carta normalmente
        escolha = {
            "tipo": "jogar",
            "indice": random.randint(0, len(jogador.mao) - 1),
            "escondida": False
        }
        print(f"{jogador.nome} jogou uma carta: {escolha}.")
        return escolha

# Loop principal para simulação
def main():
    jogo = Jogo()
    jogo.criar_baralho()
    jogo.iniciar_jogo()

    vencedor = None
    while not vencedor:
        jogo.jogar_rodada(decidir_acao_ia)
        vencedor = jogo.verificar_vencedor()

    print(f"{vencedor.nome} venceu com {vencedor.pontos} pontos!")

if __name__ == "__main__":
    main()