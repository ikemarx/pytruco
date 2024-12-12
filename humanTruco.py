import random

class Carta:
    def __init__(self, forca):
        self.forca = forca

class Jogador:
    def __init__(self, nome, equipe):
        self.nome = nome
        self.equipe = equipe
        self.mao = []
        self.cartas_jogadas = []

    def mostrar_mao(self):
        print(f"\nCartas de {self.nome}:")
        for i, carta in enumerate(self.mao, 1):
            print(f"{i}. Carta com força {carta.forca}")

    def jogar_carta(self, i):
        carta = self.mao.pop(i - 1)
        self.cartas_jogadas.append(carta)
        return carta

class Equipe:
    def __init__(self, nome):
        self.nome = nome
        self.jogadores = []
        self.pontos = 0
        self.vitorias_rodada = 0

class Jogo:
    def __init__(self):
        self.baralho = []
        self.equipe1 = Equipe("Nós")
        self.equipe2 = Equipe("Eles")
        self.valor_rodada = 1
        self.cartas_jogadas = []
        self.rodada_atual = 0
        self.vez_atual = 0
        self.primeiro_jogador = 0
        self.truco_pedido = False
        self.quem_pediu_truco = None
        self.primeiro_jogador = 0

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
        # Get team names
        print("\n=== Configuração das Equipes ===")
        nome_equipe1 = input("Nome da primeira equipe: ").strip()
        nome_equipe2 = input("Nome da segunda equipe: ").strip()
    
        # Use default names if empty input
        self.equipe1.nome = nome_equipe1 if nome_equipe1 else "Nós"
        self.equipe2.nome = nome_equipe2 if nome_equipe2 else "Eles"
    
        print(f"\n=== Jogadores da equipe {self.equipe1.nome} ===")
        nome_jogador1 = input("Nome do primeiro jogador: ").strip()
        nome_jogador2 = input("Nome do segundo jogador: ").strip()
    
        print(f"\n=== Jogadores da equipe {self.equipe2.nome} ===")
        nome_jogador3 = input("Nome do primeiro jogador: ").strip()
        nome_jogador4 = input("Nome do segundo jogador: ").strip()
    
        # Use default names if empty input
        self.equipe1.jogadores = [
            Jogador(nome_jogador1 if nome_jogador1 else "João", self.equipe1),
            Jogador(nome_jogador2 if nome_jogador2 else "Sérgio", self.equipe1)
        ]
    
        self.equipe2.jogadores = [
            Jogador(nome_jogador3 if nome_jogador3 else "Paulo", self.equipe2),
            Jogador(nome_jogador4 if nome_jogador4 else "Carlos", self.equipe2)
        ]
    
        self.jogadores = [
            self.equipe1.jogadores[0],
            self.equipe2.jogadores[0],
            self.equipe1.jogadores[1],
            self.equipe2.jogadores[1]
        ]
    
        # Randomly select first player
        self.primeiro_jogador = random.randint(0, 3)
        primeiro_nome = self.jogadores[self.primeiro_jogador].nome
    
        print("\n=== Times configurados ===")
        print(f"Equipe {self.equipe1.nome}: {self.equipe1.jogadores[0].nome} e {self.equipe1.jogadores[1].nome}")
        print(f"Equipe {self.equipe2.nome}: {self.equipe2.jogadores[0].nome} e {self.equipe2.jogadores[1].nome}")
        print(f"\n{primeiro_nome} vai começar jogando!")
        print("\nIniciando o jogo...")
    
        self.criar_baralho()

    def distribuir_cartas(self):
        # Recolher todas as cartas jogadas e da mão dos jogadores
        for jogador in self.jogadores:
            self.baralho.extend(jogador.mao)
            self.baralho.extend(jogador.cartas_jogadas)
            jogador.mao = []
            jogador.cartas_jogadas = []
    
        # Embaralhar
        random.shuffle(self.baralho)
    
        # Distribuir novas cartas
        for jogador in self.jogadores:
            for _ in range(3):
                jogador.mao.append(self.baralho.pop())

    def jogar_rodada(self):
            self.equipe1.vitorias_rodada = 0
            self.equipe2.vitorias_rodada = 0
            self.valor_rodada = 1
            
            for turno in range(3):  # Melhor de 3
                if self.equipe1.vitorias_rodada == 2 or self.equipe2.vitorias_rodada == 2:
                    break
                    
                print(f"\n=== Turno {turno + 1} ===")
                cartas_turno = []
                jogador_atual = self.primeiro_jogador
                
                # Cada jogador joga uma carta
                for _ in range(4):
                    jogador = self.jogadores[jogador_atual]
                    if jogador.mao:  # Verifica se o jogador ainda tem cartas
                        print(f"\nVez de {jogador.nome} jogar")
                        
                        # Clear screen for privacy
                        input("Pressione Enter para ver suas cartas...")
                        print("\n" * 50)  # Simple screen clearing
                        
                        jogador.mostrar_mao()
                        
                        # Get valid card choice
                        while True:
                            try:
                                escolha = int(input(f"Escolha uma carta (1-{len(jogador.mao)}): "))
                                if 1 <= escolha <= len(jogador.mao):
                                    break
                                print("Escolha inválida!")
                            except ValueError:
                                print("Por favor, digite um número válido!")
                        
                        carta_jogada = jogador.jogar_carta(escolha)
                        cartas_turno.append((carta_jogada, jogador))
                        
                        print(f"{jogador.nome} jogou carta com força {carta_jogada.forca}")
                        input("Pressione Enter para continuar...")
                        print("\n" * 50)  # Clear screen again
                    
                    jogador_atual = (jogador_atual + 1) % 4

                if cartas_turno:
                    # Mostrar todas as cartas jogadas no turno
                    print("\nCartas jogadas neste turno:")
                    for carta, jogador in cartas_turno:
                        print(f"{jogador.nome}: carta com força {carta.forca}")
                    
                    # Determinar vencedor do turno
                    carta_vencedora = max(cartas_turno, key=lambda x: x[0].forca)
                    jogador_vencedor = carta_vencedora[1]
                    print(f"\n{jogador_vencedor.nome} venceu o turno com carta {carta_vencedora[0].forca}")
                    
                    if jogador_vencedor.equipe == self.equipe1:
                        self.equipe1.vitorias_rodada += 1
                    else:
                        self.equipe2.vitorias_rodada += 1

                    print(f"\nPlacar do round: {self.equipe1.nome} {self.equipe1.vitorias_rodada} x {self.equipe2.vitorias_rodada} {self.equipe2.nome}")
                    input("\nPressione Enter para continuar...")

            # Após a rodada terminar, próximo jogador será o próximo na ordem anti-horária
            self.primeiro_jogador = (self.primeiro_jogador + 1) % 4

            # Determinar vencedor da rodada
            if self.equipe1.vitorias_rodada > self.equipe2.vitorias_rodada:
                self.equipe1.pontos += self.valor_rodada
                return self.equipe1
            else:
                self.equipe2.pontos += self.valor_rodada
                return self.equipe2

    def pedir_truco(self, equipe_pedinte):
        if self.valor_rodada == 1:
            self.valor_rodada = 3
        elif self.valor_rodada == 3:
            self.valor_rodada = 6
        elif self.valor_rodada == 6:
            self.valor_rodada = 9
        elif self.valor_rodada == 9:
            self.valor_rodada = 12
        
        self.truco_pedido = True
        self.quem_pediu_truco = equipe_pedinte

    def correr_truco(self, equipe_desistente):
        equipe_vencedora = self.equipe1 if equipe_desistente == self.equipe2 else self.equipe2
        equipe_vencedora.pontos += self.valor_rodada

    def verificar_vencedor(self):
        if self.equipe1.pontos >= 12:
            return self.equipe1
        elif self.equipe2.pontos >= 12:
            return self.equipe2
        return None


def main():
    print("=== Bem-vindo ao Truco! ===")
    jogo = Jogo()
    jogo.iniciar_jogo()

    vencedor = None
    rodada = 1
    while not vencedor:
        print(f"\n=== Rodada {rodada} ===")
        print(f"Placar: {jogo.equipe1.nome} {jogo.equipe1.pontos} x {jogo.equipe2.pontos} {jogo.equipe2.nome}")
        jogo.distribuir_cartas()
        
        vencedor_rodada = jogo.jogar_rodada()
        print(f"\nVencedor da rodada: {vencedor_rodada.nome}")
        
        vencedor = jogo.verificar_vencedor()
        rodada += 1

    print(f"\n{vencedor.nome} venceu o jogo com {vencedor.pontos} pontos!")
    
if __name__ == "__main__":
    main()

