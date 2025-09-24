# Mudar o backend para evitar conflitos com o PyGame
import matplotlib
matplotlib.use('Agg')  # Usar backend não-interativo
import matplotlib.pyplot as plt
import pygame
import numpy as np
import time

"""-----------DEFINIR FUNÇÕES E CLASSES-----------"""

# Função para velocidades após colisão elástica unidimensional
def velocidades_depois_colisao(massa_corpo1, massa_corpo2, velocidade_corpo1, velocidade_corpo2):
    """
    Essa função utiliza a equação de colisão elástica unidimensional entre dois corpos para calcular a velocidade de cada corpo após a colisão.

    Argumentos:
    massa_corpo1: massa do corpo 1
    massa_corpo2: massa do corpo 2 
    velcocidade_corpo1: velocidade do corpo 1 antes da colisão
    velocidade_corpo2: velocidade do corpo 2 antes da colisão

    Retornos:
    v1: velocidade do corpo 1 após a colisão 
    v2: velocidade do corpo 2 após a colisão
    """
    v1 = ((massa_corpo1 - massa_corpo2) * velocidade_corpo1 + 2 * massa_corpo2 * velocidade_corpo2) / (massa_corpo1 + massa_corpo2)
    v2 = ((massa_corpo2 - massa_corpo1) * velocidade_corpo2 + 2 * massa_corpo1 * velocidade_corpo1) / (massa_corpo1 + massa_corpo2)
    
    return v1, v2

# Função posição
def pos(x0, v0, t):
    """
    Essa função utiliza a equação horária da posição para calcular a posição de um corpo a velocidade constante

    Argumentos:
    x0: posição inicial
    v0: velocidade inicial
    t: tempo de movimento

    Retorno:
    Posição do corpo no tempo t 
    """
    return x0 + v0 * t

# Colisão elástica com a parede
def colisao_com_parede(v0):
    """Essa função retorna a velocidade de um corpo que colide com uma parede imóvel de forma elástica"""
    return -v0

# Tamnho dos blocos
def largura_pela_massa(m):
    """Essa função define a largura dos blocos conforme a sua massa"""
    # Talvez dê para procurar uma função que englobe esses pontos
    if 0 < m <= 10: 
        return 10
    elif 10 < m <= 100: 
        return 20
    elif 100 < m <= 10000: 
        return 25
    elif 10000 < m <= 1000000: 
        return 30
    elif 1000000 <= m: 
        return 35

# Caixas de texto (para o menu)    
class CaixaTexto:
    def __init__(self, x, y, largura, altura, texto_inicial):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.cor = CINZA
        self.texto = texto_inicial
        self.ativo = False
        self.cursor_visivel = True
        self.tempo_cursor = 0
        
    def manipular_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            # Verificar se clicou na caixa de texto
            if self.rect.collidepoint(evento.pos):
                self.ativo = True
                self.cor = AZUL
            else:
                self.ativo = False
                self.cor = CINZA
        
        if evento.type == pygame.KEYDOWN and self.ativo:
            if evento.key == pygame.K_BACKSPACE: # Apertou a tecla de apagar
                self.texto = self.texto[:-1] # Apagar último caractere
            elif evento.unicode in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "-"]: # Apertou um numero no teclado
                # Adicionar caractere (limitar a 18 caracteres)
                if len(self.texto) < 18:
                    self.texto += evento.unicode
        return False  # Retorna False por padrão
    
    def atualizar(self):
        # Piscar o cursor
        self.tempo_cursor += 1
        if self.tempo_cursor > 600:  # A cada 600 frames
            self.cursor_visivel = not self.cursor_visivel
            self.tempo_cursor = 0
    
    def desenhar(self, superficie):
        # Desenhar a caixa
        pygame.draw.rect(superficie, self.cor, self.rect, 2)
        
        # Desenhar o texto
        texto_surface = fonte.render(self.texto, True, BRANCO)
        superficie.blit(texto_surface, (self.rect.x + 5, self.rect.y + 5))
        
        # Desenhar cursor se estiver ativo
        if self.ativo and self.cursor_visivel:
            cursor_x = self.rect.x + 5 + texto_surface.get_width()
            pygame.draw.line(superficie, BRANCO, 
                           (cursor_x, self.rect.y + 5),
                           (cursor_x, self.rect.y + self.rect.height - 5), 
                           2)

# Abrir Menu
def abrir_menu(valores_iniciais):
    """
    Essa função abre e roda o menu de definição de parametros

    Argumento:
    valores_iniciais: uma lista com os valores iniciais dos 7 parâmetros da simulação
    -Ordem dos parâmtros: [Massa 1, Massa 2, Velocidade 1, Velocidade 2, Posição 1,
                           Posição 2, Posição da Parede, Tempo, fps]

    Retorno:
    parametros: o valor final dos parâmetros definidos pelo usuário
    -Retorna False se o programa for desligado
    """
    # Criar caixa de texto
    caixas_texto = []
    for i in range(9):
        caixas_texto.append(CaixaTexto(200, 100 + 70*i, 300, 50, str(valores_iniciais[i])))

    # Criar textos
    nomes_textos = ["Massa 1", "Massa 2", "Vel 1", "Vel 2", "Pos 1", "Pos 2", "Pos Parede", "Tempo", "fps"]
    textos = []
    for i in range(9):
        textos.append((nomes_textos[i], 180, 100 + 70*i))

    def desenhar_texto(nome, x, y):
        """Essa função desenha um texto a partir do texto (nome) e posição (x, y)"""
        texto = fonte.render(nome, True, BRANCO)
        tela.blit(texto, (x - texto.get_width(), y))

    # Botão de enviar
    texto_botao = fonte.render("Iniciar Simulação", True, BRANCO)
    botao_enviar = pygame.Rect(1240 - texto_botao.get_width(), 680 - texto_botao.get_height(), texto_botao.get_width() + 20, texto_botao.get_height() + 20)
    
    
    # Loop - Menu aberto

    menu_aberto = True # Determina se o menu está aberto ou não

    while menu_aberto:
        tela.fill(PRETO) 

        # Título do Menu
        texto_titulo = fonte.render("Definir parâmetros da simulação", True, BRANCO)
        tela.blit(texto_titulo, ((LARGURA-texto_titulo.get_width())/2, 30))

        # Eventos da Simulação
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: # Clicou no X
                # Fecha o menu e desliga o programa
                menu_aberto = False
                return False

            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE: # Clicou em Esc
                # Fecha o menu e desliga o programa
                menu_aberto = False
                return False
            
            for caixa_texto in caixas_texto: # Atualiza as caixa de texto conforme o evento
                caixa_texto.manipular_evento(evento)
            
            if evento.type == pygame.MOUSEBUTTONDOWN: # Clicou com o botão do mouse
                if botao_enviar.collidepoint(evento.pos): # Clicou no botão de enviar
                    # Fecha o menu e retorna os parâmetros
                    menu_aberto = False
                    return [int(caixa_texto.texto) for caixa_texto in caixas_texto]

        # Caixas de texto
        for i in range(9):
            # Atualizar caixas de texto
            caixas_texto[i].atualizar()
            
            # Desenhar caixa de texto
            caixas_texto[i].desenhar(tela)

            # Desenhar textos
            desenhar_texto(textos[i][0], textos[i][1], textos[i][2])
        
        # Desenhar botão
        pygame.draw.rect(tela, VERMELHO, botao_enviar, border_radius=10)
        tela.blit(texto_botao, (botao_enviar.x + 10, botao_enviar.y + 10))

        # Atualiza o display
        pygame.display.flip()

# Realizar simulação
def realizar_simulacao():
    """
    Essa função realiza a simulação frame a frame da colisão elástica

    Retorno:
    frames: lista com os parâmetro da simulação. Para cada frame, possui uma tupla com a posição dos blocos e os contadores.
    t: lista de tempos da simulação
    x1: lista das posições do bloco 1 ao longo da simulação
    x2: lista das posições do bloco 1 ao longo da simulação
    """

    #Variáveis para a simulação

    t = np.linspace(0, tempo_simulacao, fps * tempo_simulacao) # Lista de tempos para simulação
    x1, x2 = [], [] # Listas de posições ao longo da simulação
    x1_simulado, x2_simulado = x01, x02 # Posições temporárias durante a simulação
    v1_simulado, v2_simulado = v01, v02 # Velocidades temporárias durante a simulação
    passo_de_tempo = 1 / fps # Variação de tempo entre cada instante simulado
    contador = 0 # Conta o número total de colisões
    contador_esquerda = 0 # Conta o número de colisões com a parede
    contador_direita = 0 # Conta o número de colisões entre o blocos
    frames = [] # Carrega parâmetros para a simulação. Para cada frame, possuirá uma tupla com a posição dos blocos e os contadores.

    tempo_inicio = time.time() # Será usado para ver quanto tempo a simulação demorou

    # Fazendo os calculos da simulação

    for _ in t:
        #Atualiza a posição
        x1_simulado = pos(x1_simulado, v1_simulado, passo_de_tempo)
        x2_simulado = pos(x2_simulado, v2_simulado, passo_de_tempo)

        #Checa a colisão entre os blocos
        if x1_simulado + (l1/2) >= x2_simulado - (l2/2):
            v1_simulado, v2_simulado = velocidades_depois_colisao(m1, m2, v1_simulado, v2_simulado)
            x1_simulado = x2_simulado - (l1/2) - (l2/2) # Ajuste para considerar a largura dos blocos na colisão (x1 + l1 = x2 - l2 -> x1 = x2 - l2 - l1)
            contador += 1
            contador_direita += 1

        #Checa a colisão com a parede
        if x1_simulado - (l1/2) <= x_parede:
            v1_simulado = colisao_com_parede(v1_simulado)
            x1_simulado = x_parede + (l1/2) # Ajuste para considerar a largura dos blocos na colisão 
            contador +=1
            contador_esquerda += 1

        #Atualiza a lista de posições
        x1.append(x1_simulado)
        x2.append(x2_simulado)
        frames.append((x1_simulado, x2_simulado, contador, contador_esquerda, contador_direita))
        # Checa se já ocorreu o número máximo de colisões
        if v1_simulado >= 0 and v2_simulado >= 0 and v2_simulado > v1_simulado:
            # Adiciona frames extras para facilitar a visualização após o fim das colisões 
            segundos_extras = 3
            passos_extras = int(segundos_extras * fps)

            for _ in range(passos_extras):
                x1_simulado = pos(x1_simulado, v1_simulado, passo_de_tempo)
                x2_simulado = pos(x2_simulado, v2_simulado, passo_de_tempo)
                
                x1.append(x1_simulado) # Atualiza a lista de posições do bloco 1
                x2.append(x2_simulado) # Atualiza a lista de posições do bloco 2
                frames.append((x1_simulado, x2_simulado, contador, contador_esquerda, contador_direita)) # Atualiza a lista de parâmetros para animação
            break

    tempo_fim = time.time()
    tempo_gasto = tempo_fim - tempo_inicio

    print(f"Cálculos concluídos! O tempo gasto foi de {tempo_gasto:.4f} segundos")
    print(f"Ocorreram {contador} colisões durante a simulação")
    return frames, t, x1, x2

# Mostrar o Gráfico
def mostrar_grafico():
    """Essa função gera o gráfico e abre a tela para a sua vizualização"""

    # Plotando o gráfico de trajetórias 
    plt.figure(figsize=(10, 6), dpi=300) 
    plt.plot(t[:len(x1)], x1, label='Corpo 1 (vermelho)', color = 'crimson')
    plt.plot(t[:len(x2)], x2, label='Corpo 2 (azul)', color = 'dodgerblue')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Posição (m)')
    plt.title('Trajetórias dos corpos')
    plt.grid(True, linestyle="--")
    plt.legend()
    plt.savefig("grafico.png", dpi=100)

    # Carregar gráfico
    grafico_surface = pygame.image.load("grafico.png")

    # Redimensionar para ocupar toda a janela
    grafico_surface = pygame.transform.smoothscale(grafico_surface, (LARGURA, ALTURA))

    # Botão de voltar
    texto_botao = fonte.render("Voltar", True, BRANCO)
    botao_voltar = pygame.Rect(1240 - texto_botao.get_width(), 680 - texto_botao.get_height(), texto_botao.get_width() + 20, texto_botao.get_height() + 20)
    
    # Loop - menu aberto

    grafico_ativo = True
    while grafico_ativo:
        tela.fill(PRETO)

        # Desenhar gráfico
        tela.blit(grafico_surface, (0, 0))

        # Desenhar botão
        pygame.draw.rect(tela, VERMELHO, botao_voltar, border_radius=10)
        tela.blit(texto_botao, (botao_voltar.x + 10, botao_voltar.y + 10))

        # Eventos do sistema
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: # Apertou o X
                # Fecha a animação e desliga o programa
                grafico_ativo = False
                return False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE: # Apertou Esc
                # Fecha a animação e mantem o programa ligado
                grafico_ativo = False
                return True

            if evento.type == pygame.MOUSEBUTTONDOWN: # Clique com botão do mouse
                if botao_voltar.collidepoint(evento.pos): # Clicou no botão de voltar
                    # Fecha a animação e mantem o programa ligado
                    grafico_ativo = False
                    return True

        # Atualiza display
        pygame.display.flip()

# Rodar animação
def rodar_animacao():
    # Ajuste da escala para visualização

    espaco_necessario = x02 + 100
    ESCALA = LARGURA / espaco_necessario  # Escala baseada na quantidade de espaço necessária em metros 

    # Tamanho em pixels dos objetos

    LADO1, LADO2 = int(l1 * ESCALA), int(l2 * ESCALA ) # Converte para pixels

    # Posição do chão

    altura_do_chao = LARGURA // 2.5 

    # Definindo variáveis da animação

    relogio = pygame.time.Clock() 
    simulacao_ativa = True # Determina se a janela de simulação está aberta ou não
    animacao_ativa = True # Determina se animação de colisão está ocorrendo ou não
    tempo_inicio_animacao = time.time() # Define o tempo inicial da animção
    contador_esquerda_anterior = 0 
    contador_direita_anterior = 0
    duracao_da_particula = 0 # Duração do efeito de partícula de colisão, que inicialmente é 0

    # Inicialização da fonte
    fonte_2 = pygame.font.SysFont(None, 36)

    # Loop - animação aberta

    try:
        while simulacao_ativa:
            tela.fill(PRETO)
            
            # Eventos do sistema
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT: # Clicou no X
                    # Fecha a animação e desliga o programa
                    simulacao_ativa = False
                    return False
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE: # Clicou na tecla Esc
                    # Fecha a animação e mantem o programa ligado
                    simulacao_ativa = False
                    return True
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r: # Clicou na tecla R
                    # Reinicia a animação
                    animacao_ativa = True
                    duracao_da_particula = 0
                    tempo_inicio_animacao = time.time()
                    contador_direita_atual = contador_direita_anterior = 0
                    contador_esquerda_atual = contador_esquerda_anterior = 0
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_x: # Clicou na tecla X
                    # Fecha a animação e mantem o programa ligado
                    simulacao_ativa = False
                    return True

            # Nos diz o tempo atual de simulação, isso ajuda sicronizar a animação com o tempo real
            tempo_atual_animacao = time.time() - tempo_inicio_animacao

            # Caso a animação estiver ativa atualiza o frame atual
            if animacao_ativa == True:
                frame_atual = int(tempo_atual_animacao * fps)
                if frame_atual >= len(frames): # Se já chegou ao final mantém o último frame e indica que a animação foi concluida
                    frame_atual = len(frames) - 1
                    animacao_ativa = False
            
            x1_simulado, x2_simulado, contador_atual, contador_esquerda_atual, contador_direita_atual = frames[frame_atual]

            # Conversão de posições físicas para pixels 
            x1_s = int((x1_simulado - l1/2) * ESCALA)  # O -l1/2 serve para transformar os calculos que estavam no centro para o canto esquerdo (o pygame tem como origem o canto superior esquerdo)
            x2_s = int((x2_simulado - l2/2) * ESCALA)
            x_parede_s = int(x_parede * ESCALA) 

            # Desenha a parede
            pygame.draw.line(tela, BRANCO, (x_parede_s, 0), (x_parede_s, altura_do_chao), 4)
            
            # Desenho do bloco 1:
            pygame.draw.rect(tela, VERMELHO, (x1_s, altura_do_chao - LADO1, LADO1, LADO1)) # Desenha o bloco
            pygame.draw.rect(tela, BRANCO, (x1_s, altura_do_chao - LADO1, LADO1, LADO1), 2) # Borda do bloco

            # Texto em cima bloco 1:
            texto_m1 = fonte_2.render(f"{m1:,} Kg", True, BRANCO)
            tela.blit(texto_m1, (x1_s + LADO1 // 6, altura_do_chao - LADO1 - 27))
            
            # Desenho do bloco 2:
            pygame.draw.rect(tela, AZUL, (x2_s, altura_do_chao - LADO2, LADO2, LADO2)) # Desenha o bloco
            pygame.draw.rect(tela, BRANCO, (x2_s, altura_do_chao - LADO2, LADO2, LADO2), 2) # Borda do bloco

            # Texto em cima do bloco 2:
            texto_m2 = fonte_2.render(f"{m2:,} Kg", True, BRANCO)
            tela.blit(texto_m2, (x2_s + LADO2 // 6, altura_do_chao - LADO2 - 27))

            # Desenha a linha no nível da altura do chão
            pygame.draw.line(tela, BRANCO, (x_parede_s,altura_do_chao), (LARGURA, altura_do_chao), 4)
            
            # Adicionando os efeitos visuais de partículas e sonoros na colisão
            particula = pygame.image.load("particula.png")
            som_colisao = pygame.mixer.Sound("som da colisao.mp3")
            
            # Definindo o diâmetro da partícula
            tamanho = (25, 25) 
            particula_redimencionada = pygame.transform.scale(particula, tamanho)
            
            # Verifica se ocorreu uma colisão com a parede, se sim o tempo de duração da partícula é definido
            if contador_esquerda_atual != contador_esquerda_anterior:
                duracao_da_particula = tempo_atual_animacao + 0.065 
                posicao_particula = (x1_s - tamanho[0]/2, altura_do_chao - LADO1/2 - tamanho[0]/2)
                som_colisao.play()

            # Verifica se ocorreu uma colisão entre os blocos, se sim o tempo de duração da partícula é definido
            if contador_direita_atual != contador_direita_anterior:
                duracao_da_particula = tempo_atual_animacao + 0.065
                posicao_particula = (x1_s + LADO1 - tamanho[0]/2, altura_do_chao - LADO1/2 - tamanho[0]/2)
                som_colisao.play()

            # Verifica se a partícula ainda deve ser exibida
            if duracao_da_particula > tempo_atual_animacao:
                tela.blit(particula_redimencionada, posicao_particula)

            contador_esquerda_anterior = contador_esquerda_atual
            contador_direita_anterior = contador_direita_atual

            # Indica na tela o número de colisões
            texto_contador = fonte.render(f"Número de colisões: {contador_atual}", True, BRANCO)
            tela.blit(texto_contador, (x_parede_s + 30, 15))

            # Caso a animação tenha acabado aperece um texto na tela
            if animacao_ativa == False:
                texto = fonte.render("Simulação concluída - Clique no X para fechar", True, BRANCO)
                tela.blit(texto, (LARGURA//2 - 200, 100))

                # Botão de alterar parametros
                texto_botao_p = fonte.render("Alterar Paramêtros", True, BRANCO)
                botao_parametros = pygame.Rect(1240 - texto_botao_p.get_width(), 680 - texto_botao_p.get_height(), texto_botao_p.get_width() + 20, texto_botao_p.get_height() + 20)
                # Desenhar botão
                pygame.draw.rect(tela, VERMELHO, botao_parametros, border_radius=10)
                tela.blit(texto_botao_p, (botao_parametros.x + 10, botao_parametros.y + 10))

                # Botão de enviar
                texto_botao_g = fonte.render("Mostrar Gráfico", True, BRANCO)
                botao_grafico = pygame.Rect(1240 - texto_botao_g.get_width(), 580 - texto_botao_g.get_height(), texto_botao_g.get_width() + 20, texto_botao_g.get_height() + 20)
                # Desenhar botão
                pygame.draw.rect(tela, VERMELHO, botao_grafico, border_radius=10)
                tela.blit(texto_botao_g, (botao_grafico.x + 10, botao_grafico.y + 10))

                # Eventos da simulação
                for evento in pygame.event.get():
                    if evento.type == pygame.MOUSEBUTTONDOWN: # Clicou com o botão do mouse
                        if botao_parametros.collidepoint(evento.pos): # Clicou no botão de aletrar parametros
                            # Sai da simulação, mantendo o programa ligado
                            simulacao_ativa = False
                            return True
                        if botao_grafico.collidepoint(evento.pos): # Clicou no botão de mostrar gráfico
                            # Mostra o gráfico
                            simulacao_ativa = mostrar_grafico()
                            if not simulacao_ativa: # Confere se o programa continua ligado
                                return False


            pygame.display.flip()  # Atualiza a tela
            relogio.tick(120)  # Limite de fps da tela
            
    finally:
        pass

"""-----------INICIAR PYGAME-----------"""

pygame.init()
pygame.mixer.init()

# Inicialização da fonte
fonte = pygame.font.SysFont('Arial', 36)
                
# Configurações da janela

LARGURA, ALTURA = 1280, 740
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Simulação de Colisão")

# Cores

BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
PRETO = (0, 0, 0)
CINZA = (200, 200, 200)

# Valores iniciais dos parâmetros
parametros = [1, 1000000, 0, -15, 50, 100, 20, 40, 120000]

# Loop - Programa

reiniciar = True

while reiniciar:
    # Abre o menu e recebe os parâmetros definidos pelo usuário
    parametros = abrir_menu(parametros)

    if parametros != False: # Checa se o programa ainda está rodando
        # Define os parÃmetros conforme os valores conferidos pelo usuário
        m1, m2, v01, v02, x01, x02, x_parede, tempo_simulacao, fps = parametros
        l1, l2 = largura_pela_massa(m1), largura_pela_massa(m2)

        # Realiza a simulação
        frames, t, x1, x2 = realizar_simulacao()

        # Roda a animação e recebe True e deve reiniciar ou False se deve parar o programa
        reiniciar = rodar_animacao()
    else:
        reiniciar = False