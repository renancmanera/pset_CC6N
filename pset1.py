# IDENTIFICAÇÃO DO ESTUDANTE:
# Preencha seus dados e leia a declaração de honestidade abaixo. NÃO APAGUE
# nenhuma linha deste comentário de seu código!
#
#    Nome completo: Arthur Oliveira Rueda e Renan Carvalho Manera
#    Matrícula: 202308630 e 202308516
#    Turma: CC6N
#    Email: arthurolivrueda@gmail.com e rcarvalhomanera@gmail.com
#
# DECLARAÇÃO DE HONESTIDADE ACADÊMICA:
# Eu afirmo que o código abaixo foi de minha autoria. Também afirmo que não
# pratiquei nenhuma forma de "cola" ou "plágio" na elaboração do programa,
# e que não violei nenhuma das normas de integridade acadêmica da disciplina.
# Estou ciente de que todo código enviado será verificado automaticamente
# contra plágio e que caso eu tenha praticado qualquer atividade proibida
# conforme as normas da disciplina, estou sujeito à penalidades conforme
# definidas pelo professor da disciplina e/ou instituição.


# Imports permitidos (não utilize nenhum outro import!):
import sys
import math
import base64
import tkinter
from io import BytesIO
from PIL import Image as PILImage

def criar_kernel(n):
    if n <= 0:
        raise ValueError("O tamanho do kernel 'n' deve ser positivo.")
        
    valor = 1.0 / (n * n) # n2 é o numero total de elementos que tem na matriz
    kernel = [[valor] * n for _ in range(n)]
    
    return kernel

# Classe Imagem:
class Imagem:
    def __init__(self, largura, altura, pixels):
        self.largura = largura
        self.altura = altura
        self.pixels = pixels

    # ler o pixel por coordenada
    # se o pixel for fora da imagem, retorna o pixel mais proximo
    def get_pixel(self, x, y):
        x_valido = max(0, x)
        x_valido = min(x_valido, self.largura - 1)
        y_valido = max(0, y)
        y_valido = min(y_valido, self.altura - 1)
        return self.pixels[y_valido * self.largura + x_valido]
    
    # logica: y largura da linha + x que é ate onde voce quer chegar = indice do pixel
    def set_pixel(self, x, y, c):
        self.pixels[y * self.largura + x] = c

    # cria uma nova imagem em branco, percorre cada pixel na imagem original, aplica a funcao e salva na imagem nova
    def aplicar_por_pixel(self, func):
        resultado = Imagem.nova(self.largura, self.altura) # largura e altura ordem correta
        for x in range(resultado.largura):
            for y in range(resultado.altura):
                cor = self.get_pixel(x, y)
                nova_cor = func(cor)
                resultado.set_pixel(x, y, nova_cor) # dentro do loop interno, é chamado para cada pixel da imagem original
        return resultado

    def invertida(self):
        return self.aplicar_por_pixel(lambda c: 255 - c) # 255 - c pois o pixel é um numero de 0 a 255

    def correlacao(self, kernel):
        tamanho_kernel = len(kernel)
        indice_central = tamanho_kernel // 2
        imagem_nova = Imagem.nova(self.largura, self.altura)
        # loop de cada pixel
        for x in range(imagem_nova.largura):
            
            for y in range(imagem_nova.altura):
                nova_cor = 0
                # loop em cada elemento do kernel
                for w in range(tamanho_kernel):
                    for h in range(tamanho_kernel):
                        x1 = x - indice_central + h
                        y1 = y - indice_central + w
                        nova_cor += self.get_pixel(x1, y1) * kernel[w][h]
                        # define o valor do pixel final
                imagem_nova.set_pixel(x, y, nova_cor)
        return imagem_nova


    def borrada(self, n):
        kernel = criar_kernel(n) # cria kernel de media de tamanho n x n
        imagem_borrada = self.correlacao(kernel) # usa o kernel para fazer com que cada nova pixel seja media dos seus vizinhos
        imagem_borrada.limpar()
        return imagem_borrada
    
    # Arredonda e limita o valor ao intervalo [0, 255]
    # Criado separado devido a instrucao da focada (nitidez) de nao arredondar ate o final
    def limpar(self):
        for i in range(len(self.pixels)):
            valor_atual = self.pixels[i]
            valor_arredondado = round(valor_atual)
            valor_limitado = max(0, min(255, valor_arredondado))
            self.pixels[i] = valor_limitado

    def focada(self, n):
        kernel_blur = criar_kernel(n)
        # Gera Imagem borrada B
        imagem_borrada_B = self.correlacao(kernel_blur)
        # Gera imagem nitida S
        imagem_nitida_S = Imagem.nova(self.largura, self.altura)
        # fórmula: S = 2*I - B
        for x in range(self.largura):
            for y in range(self.altura):
                # pega o pixel da imagem original
                pixel_I = self.get_pixel(x, y)
                # pega o pixel da imagem borrada
                pixel_B = imagem_borrada_B.get_pixel(x, y)
                # calcula o novo pixel usando a formula
                pixel_S = (2 * pixel_I) - pixel_B
                imagem_nitida_S.set_pixel(x, y, pixel_S)
        imagem_nitida_S.limpar()
        return imagem_nitida_S

    def bordas(self):
        # bordas verticais
        Kx = [
            [-1, 0, 1],
            [-2, 0, 2],
            [-1, 0, 1]
        ]
        
        # bordas horizontais
        Ky = [
            [-1, -2, -1],
            [ 0,  0,  0],
            [ 1,  2,  1]
        ]
        
        # nova imagem com a "forca" das bordas
        Ox = self.correlacao(Kx)
        Oy = self.correlacao(Ky)
        # gera imagem nova
        imagem_final = Imagem.nova(self.largura, self.altura)
        
        # itera em cada pixel das imagens Ox e Oy
        for x in range(self.largura):
            for y in range(self.altura):
                pixel_ox = Ox.get_pixel(x, y)
                pixel_oy = Oy.get_pixel(x, y)
                novo_valor = math.sqrt(pixel_ox**2 + pixel_oy**2)
                imagem_final.set_pixel(x, y, novo_valor)
        imagem_final.limpar()
        
        return imagem_final

    # Abaixo deste ponto estão utilitários para carregar, salvar e mostrar
    # as imagens, bem como para a realização de testes. Você deve ler as funções
    # abaixo para entendê-las e verificar como funcionam, mas você não deve
    # alterar nada abaixo deste comentário.
    #
    # ATENÇÃO: NÃO ALTERE NADA A PARTIR DESTE PONTO!!! Você pode, no final
    # deste arquivo, acrescentar códigos dentro da condicional
    #
    #                 if __name__ == '__main__'
    #
    # para executar testes e experiências enquanto você estiver executando o
    # arquivo diretamente, mas que não serão executados quando este arquivo
    # for importado pela suíte de teste e avaliação.
    def __eq__(self, other):
        return all(getattr(self, i) == getattr(other, i)
                   for i in ('altura', 'largura', 'pixels'))

    def __repr__(self):
        return "Imagem(%s, %s, %s)" % (self.largura, self.altura, self.pixels)

    @classmethod
    def carregar(cls, nome_arquivo):
        """
        Carrega uma imagem do arquivo fornecido e retorna uma instância dessa
        classe representando essa imagem. Também realiza a conversão para tons
        de cinza.

        Invocado como, por exemplo:
           i = Imagem.carregar('test_images/cat.png')
        """
        with open(nome_arquivo, 'rb') as guia_para_imagem:
            img = PILImage.open(guia_para_imagem)
            img_data = img.getdata()
            if img.mode.startswith('RGB'):
                pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2]) for p in img_data]
            elif img.mode == 'LA':
                pixels = [p[0] for p in img_data]
            elif img.mode == 'L':
                pixels = list(img_data)
            else:
                raise ValueError('Modo de imagem não suportado: %r' % img.mode)
            l, a = img.size
            return cls(l, a, pixels)

    @classmethod
    def nova(cls, largura, altura):
        """
        Cria imagens em branco (tudo 0) com a altura e largura fornecidas.

        Invocado como, por exemplo:
            i = Imagem.nova(640, 480)
        """
        return cls(largura, altura, [0 for i in range(largura * altura)])

    def salvar(self, nome_arquivo, modo='PNG'):
        """
        Salva a imagem fornecida no disco ou em um objeto semelhante a um arquivo.
        Se o nome_arquivo for fornecido como uma string, o tipo de arquivo será
        inferido a partir do nome fornecido. Se nome_arquivo for fornecido como
        um objeto semelhante a um arquivo, o tipo de arquivo será determinado
        pelo parâmetro 'modo'.
        """
        saida = PILImage.new(mode='L', size=(self.largura, self.altura))
        saida.putdata(self.pixels)
        if isinstance(nome_arquivo, str):
            saida.save(nome_arquivo)
        else:
            saida.save(nome_arquivo, modo)
        saida.close()

    def gif_data(self):
        """
        Retorna uma string codificada em base 64, contendo a imagem
        fornecida, como uma imagem GIF.

        Função utilitária para tornar show_image um pouco mais limpo.
        """
        buffer = BytesIO()
        self.salvar(buffer, modo='GIF')
        return base64.b64encode(buffer.getvalue())

    def mostrar(self):
        """
        Mostra uma imagem em uma nova janela Tk.
        """
        global WINDOWS_OPENED
        if tk_root is None:
            # Se Tk não foi inicializado corretamente, não faz mais nada.
            return
        WINDOWS_OPENED = True
        toplevel = tkinter.Toplevel()
        # O highlightthickness=0 é um hack para evitar que o redimensionamento da janela
        # dispare outro evento de redimensionamento (causando um loop infinito de
        # redimensionamento). Para maiores informações, ver:
        # https://stackoverflow.com/questions/22838255/tkinter-canvas-resizing-automatically
        tela = tkinter.Canvas(toplevel, height=self.altura,
                              width=self.largura, highlightthickness=0)
        tela.pack()
        tela.img = tkinter.PhotoImage(data=self.gif_data())
        tela.create_image(0, 0, image=tela.img, anchor=tkinter.NW)

        def ao_redimensionar(event):
            # Lida com o redimensionamento da imagem quando a tela é redimensionada.
            # O procedimento é:
            #  * converter para uma imagem PIL
            #  * redimensionar aquela imagem
            #  * obter os dados GIF codificados em base 64 (base64-encoded GIF data)
            #    a partir da imagem redimensionada
            #  * colocar isso em um label tkinter
            #  * mostrar a imagem na tela
            nova_imagem = PILImage.new(mode='L', size=(self.largura, self.altura))
            nova_imagem.putdata(self.pixels)
            nova_imagem = nova_imagem.resize((event.width, event.height), PILImage.NEAREST)
            buffer = BytesIO()
            nova_imagem.save(buffer, 'GIF')
            tela.img = tkinter.PhotoImage(data=base64.b64encode(buffer.getvalue()))
            tela.configure(height=event.height, width=event.width)
            tela.create_image(0, 0, image=tela.img, anchor=tkinter.NW)

        # Por fim, faz o bind da função para que ela seja chamada quando a tela
        # for redimensionada:
        tela.bind('<Configure>', ao_redimensionar)
        toplevel.bind('<Configure>', lambda e: tela.configure(height=e.height, width=e.width))

        # Quando a tela é fechada, o programa deve parar
        toplevel.protocol('WM_DELETE_WINDOW', tk_root.destroy)


# Não altere o comentário abaixo:
# noinspection PyBroadException
try:
    tk_root = tkinter.Tk()
    tk_root.withdraw()
    tcl = tkinter.Tcl()


    def refaz_apos():
        tcl.after(500, refaz_apos)


    tcl.after(500, refaz_apos)
except:
    tk_root = None

WINDOWS_OPENED = False

if __name__ == '__main__':
    # O código neste bloco só será executado quando você executar
    # explicitamente seu script e não quando os testes estiverem
    # sendo executados. Este é um bom lugar para gerar imagens, etc.
    pass

# ---------------------------------------------------------------------------------------------------------------------------

    # QUESTÃO 01: se você passar essa imagem pelo filtro de inversão, qual seria o
    # output esperado? Justifique sua resposta.

    # CÓDIGO:
    #imagem_teste = Imagem(4, 1, [29, 89, 136, 200])
    #imagem_invertida = imagem_teste.invertida()
    #print("Os pixels da imagem invertida gerada são:", imagem_invertida.pixels)
    #output_esperado = Imagem(4, 1, [226, 166, 119, 55])
    #if imagem_invertida.pixels == output_esperado.pixels:
    #   print("Os pixels da imagem invertida gerada correspondem exatamente aos pixels que eram esperados.")
    #else:
    #    print("Os valores de pixel na imagem invertida são diferentes do que era esperado.")

    # RESPOSTA:
    # Output esperado dos pixels é [226, 166, 119, 55].
    # A fórmula para inverter um pixel é: novo_pixel = 255 - pixel_original
    # Para obtê-lo, basta subtrair os valores de cada um dos pixels originais ([29, 89, 136, 200]) de 255.
    # Cálculo:
    # 255 - 29 = 226
    # 255 - 89 = 166
    # 255 - 136 = 119
    # 255 - 200 = 55

# ---------------------------------------------------------------------------------------------------------------------------

    # QUESTÃO 02: faça a depuração e, quando terminar, seu código deve conseguir passar em todos os testes do grupo de teste
    # TestInvertida (incluindo especificamente o que você acabou de criar). Execute seu filtro de inversão na imagem
    # test_images/bluegill.png, salve o resultado como uma imagem PNG e salve a imagem.

    # CÓDIGO:
    imagem_peixe = Imagem.carregar('test_images/bluegill.png')
    imagem_peixe_invertida = imagem_peixe.invertida()
    imagem_peixe_invertida.mostrar()
    imagem_peixe_invertida.salvar('test_images/bluegill.png')

    # RESPOSTA:
    # Primeiro carrega a imagem original do peixe e adiciona variável
    # depois aplica o filtro de inversão e adiciona variável de resultado
    # depois salva a imagem invertida e mostra a imagem invertida

# ---------------------------------------------------------------------------------------------------------------------------

    # QUESTÃO 03: Qual será o valor do pixel na imagem de saída no local indicado pelo destaque vermelho? Observe que neste ponto ainda 
    # não arredondamos ou recortamos o valor, informe exatamente como você calculou. Observação: demonstre passo a passo os cálculos realizados.

    # CÓDIGO:
    # Imagem do kernel de entrada:
    #kernel = [
    #	 [0.00, -0.07, 0.00],
    #    [-0.45, 1.20, -0.25],
    #    [0.00, -0.12, 0.00]
    #]

    # Imagem de entrada dada pela questão: 
    #imagem_entrada = Imagem(3, 3, [80, 53, 99, 129, 127, 148, 175, 174, 193])
    
    # Funcao de correlacao:
    #imagem_gerada = imagem_entrada.correlacao(kernel)
    #valor_pixel = imagem_gerada.get_pixel(1, 1)
    #print("O valor do pixel na posicao (1, 1) é:", valor_pixel)

    # RESPOSTA:
    # O valor do pixel na imagem de saída no local indicado pelo destaque vermelho é: 32.76.
    # Passo a passo dos cálculos realizados:
    
    # Multiplicar o pixel da imagem de entrada pelo valor do kernel:
    # 80 * 0.00 = 0
    # 53 * -0.07 = -3.71
    # 99 * 0.00 = 0
    # 129 * -0.45 = -58.05
    # 127 * 1.20 = 152.4
    # 148 * -0.25 = -37.0
    # 175 * 0.00 = 0
    # 174 * -0.12 = -20.88
    # 193 * 0.00 = 0
    
    # Somar os resultados das multiplicações:
    # 0 + (-3.71) + 0 + (-58.05) + 152.4 + (-37.0) + 0 + (-20.88) + 0 = 32.76
    # O valor do pixel na imagem de saída no local indicado pelo destaque vermelho é: 32.76.

    # OBS: o valor 32.76 que deveria ser gerado pelo código pode ter um valor diferente, como: 32.760000000000005
    # devido ao fato do float sofrer de erros de precisão inerentes à sua representação em binário.

# ---------------------------------------------------------------------------------------------------------------------------

    # QUESTÃO 04: quando você tiver implementado seu código, tente executá-lo em
    # test_images/pigbird.png com o seguinte kernel 9 × 9:
    
    # CÓDIGO:
    # Imagem de entrada:
    #imagem_porco_entrada = Imagem.carregar('test_images/pigbird.png')
    #kernel = [
    #    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #    [1, 0, 0, 0, 0, 0, 0, 0, 0],
    #    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #    [0, 0, 0, 0, 0, 0, 0, 0, 0]
    #]

    # Funcao de correlacao:
    #imagem_porco_correlacao = imagem_porco_entrada.correlacao(kernel)

    # Salvar e mostrar imagem gerada
    #imagem_porco_correlacao.salvar('test_images/pigbird.png')
    #imagem_porco_correlacao.mostrar()

# ---------------------------------------------------------------------------------------------------------------------------
    
    # QUESTÃO DA IMAGEM DO GATO COM FILTRO BORRADO

    # CÓDIGO
    #imagem_gato = Imagem.carregar('test_images/cat.png')
    #imagem_gato_borrado = imagem_gato.borrada(5)
    #imagem_gato_borrado.salvar('test_images/cat.png')
    #imagem_gato_borrado.mostrar()

# ---------------------------------------------------------------------------------------------------------------------------

    # QUESTÃO 05: se quisermos usar uma versão desfocada B que foi feita com um
    # kernel de desfoque de caixa de 3 × 3, que kernel k poderíamos usar para calcular
    # toda a imagem nítida com uma única correlação? Justifique sua resposta mostrando os cálculos.
    # Implemente uma máscara de não nitidez como o método focada da classe
    # Imagem, onde n denota o tamanho do kernel de desfoque que deve ser usado para
    # gerar a cópia desfocada da imagem. Este método deve retornar uma nova imagem
    # mais nítida. Você pode implementar isso como uma correlação única ou usando`
    # uma subtração explícita, mas se você usar uma subtração explícita, certifique-se de
    # não fazer nenhum arredondamento até o final (a versão desfocada intermediária não
    # deve ser arredondada ou cortada de forma alguma.
    # Quando terminar e seu código passar nos testes relacionados à nitidez, execute
    # seu filtro de nitidez na imagem test_images/python.png usando um kernel
    # de tamanho 11, salve o resultado como uma imagem PNG.`

    # RESPOSTA: 
    # A fórmula da nitidez é: S = 2*I - B (Nítida = 2*Original - Borrada).
    # Como a correlação é linear, podemos aplicar nos kernels:
    # k_Nitidez = 2 * k_Identidade - k_Desfoque
    # Para 3x3:
    # k_Identidade = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    # k_Desfoque = [[1/9, 1/9, 1/9], [1/9, 1/9, 1/9], [1/9, 1/9, 1/9]] média dos 9 pixels, por isso 1/9 em toda posição  
    # Cálculo:
    # k_Nitidez = [[0, 0, 0], [0, 2, 0], [0, 0, 0]] - [[1/9, 1/9, 1/9], [1/9, 1/9, 1/9], [1/9, 1/9, 1/9]]
    # k_Nitidez = [[-1/9, -1/9, -1/9], [-1/9, 17/9, -1/9], [-1/9, -1/9, -1/9]]

    # CÓDIGO:
    #imagem_python = Imagem.carregar('test_images/python.png')
    #imagem_python_focada = imagem_python.focada(11)
    #imagem_python_focada.salvar('python_nitida.png')
    #imagem_python_focada.mostrar()

# ---------------------------------------------------------------------------------------------------------------------------

    # QUESTÃO 06: explique e o que cada um dos kernels acima, por si só, está fazendo.
    # Tente executar mostrar nos resultados dessas correlações intermediárias para ter
    # uma noção do que está acontecendo aqui.
    # Implemente o detector de bordas como o método bordas dentro da classe
    # Imagem. O método deve retornar uma nova instância de Imagem resultante das operações acima.
    # Quando terminar e seu código passar nos testes de detecção de borda, execute
    # seu detector de borda na imagem test_images/construct.png, salve o resultado como uma imagem PNG.

    # RESPOSTA: 
    # Kernel Kx (Detecta Bordas Verticais):
    # Kx = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    # Este kernel subtrai os pixels da coluna da esquerda dos pixels da direita. 
    # Ele gera um valor alto se houver uma mudança radical de cores na vertical.

    # Kernel Ky (Detecta Bordas Horizontais):
    # Ky = [[-1, -2, -1], [ 0, 0, 0], [ 1, 2, 1]]
    # Este kernel subtrai os pixels da linha de cima dos pixels da linha de baixo, 
    # detectando mudanças abruptas na horizontal (bordas horizontais).

    # A fórmula final (sqrt(Ox^2 + Oy^2)) usa o Teorema de Pitágoras
    # para calcular a força total da borda, não importando sua direção.

    # CÓDIGO:
    #imagem_construct = Imagem.carregar('test_images/construct.png')
    #imagem_bordas = imagem_construct.bordas()
    #imagem_bordas.salvar('construct_bordas.png')
    #imagem_bordas.mostrar()

# ---------------------------------------------------------------------------------------------------------------------------

    # O código a seguir fará com que as janelas de Imagem.mostrar
    # sejam exibidas corretamente, quer estejamos executando
    # interativamente ou não:
    
    if WINDOWS_OPENED and not sys.flags.interactive:
        tk_root.mainloop()
