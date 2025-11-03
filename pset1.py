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


# Classe Imagem:
class Imagem:
    def __init__(self, largura, altura, pixels):
        self.largura = largura
        self.altura = altura
        self.pixels = pixels

    # ler o pixel por coordenada
    def get_pixel(self, x, y):
        return self.pixels[y * self.largura + x]
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
        indice_centro = tamanho_kernel // 2
        final_img = Imagem.nova(self.largura, self.altura)
        for x in range(final_img.largura):
            for y in range(final_img.altura):
                nova_cor = 0
                for w in range(tamanho_kernel):
                    for h in range(tamanho_kernel):
                        x1 = x - indice_centro + h
                        y1 = y - indice_centro + w
                        # Limitar índices aos limites da imagem (clamping)
                        x1 = max(0, min(x1, self.largura - 1))
                        y1 = max(0, min(y1, self.altura - 1))
                        nova_cor += self.get_pixel(x1, y1) * kernel[w][h]
                # Arredondar e limitar o valor ao intervalo [0, 255]
                nova_cor = round(nova_cor)
                nova_cor = max(0, min(255, nova_cor))
                final_img.set_pixel(x, y, nova_cor)
        return final_img

    def borrada(self, n):
        raise NotImplementedError

    def focada(self, n):
        raise NotImplementedError

    def bordas(self):
        raise NotImplementedError

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

    # QUESTÃO 02: faça a depuração e, quando terminar, seu código deve conseguir passar em todos os testes do grupo de teste
    # TestInvertida (incluindo especificamente o que você acabou de criar). Execute seu filtro de inversão na imagem
    # test_images/bluegill.png, salve o resultado como uma imagem PNG e salve a imagem.

    # CÓDIGO:
    #imagem_peixe = Imagem.carregar('test_images/bluegill.png')
    #imagem_peixe_invertida = imagem_peixe.invertida()
    #imagem_peixe_invertida.salvar('test_images/bluegill.png')
    #imagem_peixe_invertida.mostrar()

    # RESPOSTA:
    # Primeiro carrega a imagem original do peixe e adiciona variável
    # depois aplica o filtro de inversão e adiciona variável de resultado
    # depois salva a imagem invertida e mostra a imagem invertida

    # QUESTÃO 03: Qual será o valor do pixel na imagem de saída no local indicado pelo destaque vermelho? Observe que neste ponto ainda 
    # não arredondamos ou recortamos o valor, informe exatamente como você calculou. Observação: demonstre passo a passo os cálculos realizados.

    # CÓDIGO:
    # Imagem do kernel de entrada:
    kernel = [
        [0.00, -0.07, 0.00],
        [-0.45, 1.20, -0.25],
        [0.00, -0.12, 0.00]
    ]

    # Imagem de entrada dada pela questão: 
    imagem_entrada = Imagem(3, 3, [80, 53, 99, 129, 127, 148, 175, 174, 193])
    
    # Funcao de correlacao:
    imagem_gerada = imagem_entrada.correlacao(kernel)
    valor_pixel = imagem_gerada.get_pixel(1, 1)
    print("O valor do pixel na posicao (1, 1) é:", valor_pixel)

    # RESPOSTA:
    # O valor do pixel na imagem de saída no local indicado pelo destaque vermelho é: 33.
    # Passo a passo dos cálculos realizados:
    
    # 1. Multiplicar o pixel da imagem de entrada pelo valor do kernel:
    # 80 * 0.00 = 0
    # 53 * -0.07 = -3.71
    # 99 * 0.00 = 0
    # 129 * -0.45 = -58.05
    # 127 * 1.20 = 152.4
    # 148 * -0.25 = -37.0
    # 175 * 0.00 = 0
    # 174 * -0.12 = -20.88
    # 193 * 0.00 = 0
    
    # 2. Somar os resultados das multiplicações:
    # 0 + (-3.71) + 0 + (-58.05) + 152.4 + (-37.0) + 0 + (-20.88) + 0 = 32.76
    
    # 3. Arredondar o resultado para o inteiro mais próximo:
    # 32.76 arredondado para o inteiro mais próximo é 33.
    
    # 4. O valor do pixel na imagem de saída no local indicado pelo destaque vermelho é: 33.









    # O código a seguir fará com que as janelas de Imagem.mostrar
    # sejam exibidas corretamente, quer estejamos executando
    # interativamente ou não:
    
    if WINDOWS_OPENED and not sys.flags.interactive:
        tk_root.mainloop()
