![Local Image](Imagens/Cabecalho.png)

<div align="center">
  <h1>Simulador de colisões elásticas</h1>
  <h4>Prática em Ciência de Dados</h4>
  <h4>Ilum Escola de Ciência</h4>
</div>

<br>

<div align='justify'>
  <h3> :bookmark_tabs: Introdução </h4>
  <p> Repositório para o trabalho final da disciplina Prática em Ciência de Dados. </p>
  <p> O trabalho consiste em uma simulação de um sistema unidimensional de colisões elásticas envolvendo dois blocos e uma parede, incluindo apresentações em gráficos e animações. O sistema possui um bloco de massa inferior inicialmente parado e um bloco de massa superior se movendo em direção ao primeiro, de modo que os blocos colidam e oprimeiro bloco seja lançado sobre a parede e colida com a mesma, sendo lançado novamente contra o outro bloco, repetindo esse processo durante o tempo de simulação. </p>
  <p> O simulador calcula a trajetória através do tempo dos corpos do sistema e conta o número de colisões que ocorreram, apresentando essa trajetória em um gráfico e na forma de uma animação didática. O projeto tem o objetivo de auxiliar no entendimento de colisões elásticas e apresentar relações entre a massa dos corpos e o número de colisões. </p>
  <p> O trabalho se aprofundará especialmente no estudo e apresentação da razão de massas dos corpos que resulta em um número de colisões que seguem os dígitos de pi. </p>
</div>

<br>

<div align='justify'>
  <h3> :open_file_folder: Conteúdos do Repositório </h3>
  <p> Este repositório possui todos os códigos - em notebooks jupyter - necessários para realizar a simulação bem como tabelas que relacionam a razão entre as massas dos corpos e vídeos para visualizar a simulação. </p>
  <ul>
    <li> :page_facing_up: [Nome do Arquivo principal]: Arquivo principal contendo o código para simulação, criação de gráficos e animações; </li>
    <li> :page_facing_up: Comparacao_de_massas.ipynb: Arquivo contendo o código para comparar as colisões simuladas em diferentes valores de massa e criar uma tabela com os dados; </li>
    <li> :page_facing_up: particula.png: Imagem utilizada para os efeitos da animação (manter no diretório do arquivo principal para utilizar a simulação sem atualizar o código); </li>
    <li> :sound: som da colisao.mp3: Contém o som utilizado para a marcação das colisões (manter no diretório do arquivo principal para utilizar a simulação sem atualizar o código); </li>
    <li> :file_folder: Imagens: Contém as imagens utilizadas para o Readme e outras partes não necessárias para a simulação; </li>
    <li> :file_folder:Resultados: Contém tabelas geradas com o arquivo Comparacao_de_massas para duas razões, assim como um vídeo exemplo da animação gerada pelo código. </li>
  </ul>
</div>

<br>

<div align="justify">
  <h3> :book: Base Teórica </h3>
  <p> Neste, elaboraremos os fundamentos teóricos por trás das colisões elásticas assim como explicar a razão por trás do número de colisões: </p>
  <p> O número de colisões para quaisquer valores de n em $m_2=m_1 *100^n$ possui dígitos de π. É possível construir um gráfico no qual as colisões são representadas por retas em uma circuferência. As retas representam o momento linear e a circuferência, a energia do sistema. O número de retas encontradas entrega o número de colisões. Quando ele é múltiplicado pelo ângulo entre as retas, tem-se uma aproximação para π ($N*θ≈π$). Abaixo está o link para um documento com uma explicação mais detalhada, no qual está também a referência para esta explicação. </p>
  <p>
  <a href="https://ilumcnpem-my.sharepoint.com/personal/giulio25036_ilum_cnpem_br/Documents/Explicacao_aproximacao_pi.pdf" target="_blank">
    Veja a explicação completa
  </a>
</p>
</div>

<br>

<div align="justify">
  <h3> :computer: Explicação do Código Principal </h3>
  <p> Nessa seção, explicaremos parte a parte o código principal da simulação. </p>
</div>

<div align="justify">
  <h4> :heavy_exclamation_mark: Recursos necessários </h3>
  <ul>
    <li> Bibliotecas necessárias: matplotlib, pygame, numpy, time; </li>
    <li> Plataforma capaz de executar notebooks python; </li>
    <li> Arquivos complementares ao código salvos no mesmo diretório do notebook: particula.png e som da colisao.mp3 </li>
  </ul>
</div>
  
  <h4> :pushpin: Constantes físicas </h4> 
  <p> Aqui são definidas constantes importantes para os cálculos da simulação, como a posição e velocidade inicial dos corpos, suas massas e o tempo de simulação. </p>  
</div>

```python
# Definindo constantes
m1, m2 = 1, 1000000000000  # massas em kg
v01, v02 = 0, -30  # velocidades iniciais em m/s
x01, x02 = 50, 100  # posições iniciais em metros
x_parede = 20  # posição da parede em metros
tempo_simulacao = 40  # segundos
```

<div align="justify">
  <p> A função largura_pela_massa define a largura - de forma arbritária - dos blocos de acordo com suas massas </p>
</div>

```python
# Tamnho dos blocos
def largura_pela_massa(m):
    """Essa função define a largura dos blocos conforme a sua massa"""
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
```

<div align="justify">
  <h4> :pushpin: Cálculo das colisões </h4>
  <p> A função velocidades_depois_colisao calcula e retorna a velocidade de ambos os corpos após uma colisão entre os blocos, segue a equação apresentada na seção anterior. </p>
</div>

```python
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
```

<div align="justify">
  <p> Já a função colisao_com_parede retorna a velocidade de um corpo após sua colisão com a parede considerando uma colisão com um reservatório de momento, como apresentado na seção anterior. </p>
</div>

```python
# Colisão elástica com a parede
def colisao_com_parede(v0):
    """Essa função retorna a velocidade de um corpo que colide com uma parede imóvel de forma elástica"""
    return -v0
```

<div align="justify">
  <h4> :pushpin: Cálculo da posição </h4>
  <p> A função pos calcula e retorna - seguindo a função horária da posição - a posição de um corpo com velocidade constante partindo de um ponto inicial após um certo tempo. </p>
</div>

```python
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
```

<div align="justify">
  <h4> :pushpin: Simulação </h4>
  <p> O coração da simulação, calculando o movimento, velocidade e colisões durante o tempo de simulação definido. </p>
  <p> Adiciona as variáveis necessárias à simulação: </p>
</div>
  
```python
# Variáveis para a simulação
fps = 12000  # A quantidade de frames por segundo (quanto maior esse número, maior o tempo de simulação)
t = np.linspace(0, tempo_simulacao, fps * tempo_simulacao)  # Lista de tempos para simulação
x1, x2 = [], []  # Listas de posições ao longo da simulação
l1, l2 = largura_pela_massa(m1), largura_pela_massa(m2)
x1_simulado, x2_simulado = x01, x02  # Posições temporárias durante a simulação
v1_simulado, v2_simulado = v01, v02  # Velocidades temporárias durante a simulação
passo_de_tempo = 1 / fps  # Variação de tempo entre cada instante simulado
contador = 0
contador_esquerda = 0
contador_direita = 0
frames = []
```

<div align="justify">
  <p> Realiza os cálculos da simulação: </p>
</div>

```python
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
        contador_esquerda += 1

    #Checa a colisão com a parede
    if x1_simulado - (l1/2) <= x_parede:
        v1_simulado = colisao_com_parede(v1_simulado)
        x1_simulado = x_parede + (l1/2) # Ajuste para considerar a largura dos blocos na colisão 
        contador +=1
        contador_direita += 1

    #Atualiza a lista de posições
    x1.append(x1_simulado)
    x2.append(x2_simulado)
    frames.append((x1_simulado, x2_simulado, contador, contador_esquerda, contador_direita))
    # Checa se já ocorreu o número máximo de colisões
    if v1_simulado >= 0 and v2_simulado >= 0 and v2_simulado > v1_simulado:
        # Adiciona frames extras para facilitar a visualização após o fim das colisões 
        segundos_extras = 8
        passos_extras = int(segundos_extras * fps)

        for _ in range(passos_extras):
            x1_simulado = pos(x1_simulado, v1_simulado, passo_de_tempo)
            x2_simulado = pos(x2_simulado, v2_simulado, passo_de_tempo)
            x1.append(x1_simulado)
            x2.append(x2_simulado)
            frames.append((x1_simulado, x2_simulado, contador, contador_esquerda, contador_direita))
        break
```

<div align="justify">
  <h4> :pushpin: Plotagem de gráficos </h4>
  <p> Cria o gráfico da posição no tempo considerando a posição do centro de massa dos corpos: </p>
</div>

```python
# Gráfico de trajetórias 
print("O gráfico está diferente porque os blocos não são mais considerados como pontos. Agora ele está plotando considerando o centro dos blocos. Na célula abaixo observa-se a visualização anterior")
plt.figure(figsize=(10, 6), dpi=300) 
plt.plot(t[:len(x1)], x1, label='Corpo 1 (vermelho)', color = 'crimson')
plt.plot(t[:len(x2)], x2, label='Corpo 2 (azul)', color = 'dodgerblue')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.title('Trajetórias dos corpos')
plt.grid(True, linestyle="--")
plt.legend()
plt.show()
```

<div align="justify">
  <p> Cria o gráfico da posição no tempo considerando os corpos como pontuais: </p>
</div>

```python
# Gráfico de trajetórias 
plt.figure(figsize=(10, 6), dpi=300) 
plt.plot(t[:len(x1)], x1, label='Corpo 1 (vermelho)', color = 'crimson')
plt.plot(t[:len(x2)], x2, label='Corpo 2 (azul)', color = 'dodgerblue')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.title('Trajetórias dos corpos')
plt.grid(True, linestyle="--")
plt.legend()
plt.show()
```

<div align="justify">
  <h4> :pushpin: Criação da animação </h4>
  <p> "Breve introdução para o código da animação" </p>
</div>

```python
# Corte do código
```

<div align="justify">
  <h3> :memo: Licensa </h3>
  <p> GPL 3.0 </p>
</div>

<div align="justify">
  <h3> :busts_in_silhouette: Autores </h3>
  <p> Alunos: </p>
  <ul>
    <li> <a href="https://github.com/AnielNeto" target="_blank"> Aniel de Souza Ribeiro Neto </li>
    <p> Contribuições Principais: Adicionou a parede - e colisões com ela - ao sistema e desenvolveu o loop principal da simulação. </p>
    <li> <a href="https://github.com/arthu0404" target="_blank"> Arthur Brandão do Nascimento </li>
    <p> Contribuições Principais: Adicionou a largura dos blocos ao loop principal da simulação e adicionou a animação do sistema. </p>
    <li> <a href="https://github.com/Giulio-Roux" target="_blank"> Giulio Oertel Spinelli Roux César </li>
    <p> Contribuições Principais: Desenvolveu a base do código, simulando uma colisão entre dois blocos e criando um gráfico de suas posições, e criou a base da animação para um bloco. </p>
    <li> <a href="https://github.com/otmaia" target="_blank"> Luís Otávio Alves Maia </li>
    <p> Contribuições Principais: Corrigiu um problema de atravessamento de corpos na simulação principal, adicionou partes para checar a eficiência do código. </p>
  </ul>
  <p> Professores: </p>
    <ul>
      <li> Daniel Roberto Cassar </li>
      <li> James Moraes de Almeida </li>
      <li> Leandro Nascimento Lemos </li>
    </ul>
</div>

