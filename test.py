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
#


# Imports
import os
import pset1
import unittest

# Diretório
TEST_DIRECTORY = os.path.dirname(__file__)


# Classe para os testes de imagem:
class TestImagem(unittest.TestCase):
    def test_carregar(self):
        resultado = pset1.Imagem.carregar('test_images/centered_pixel.png')
        esperado = pset1.Imagem(11, 11,
                                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 255, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(resultado, esperado)


# Classe para os testes de inversão:
class TestInvertida(unittest.TestCase):
    def test_invertida_1(self):
        im = pset1.Imagem.carregar('test_images/centered_pixel.png')
        resultado = im.invertida()
        esperado = pset1.Imagem(11, 11,
                                [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                                 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                                 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                                 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                                 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                                 255, 255, 255, 255, 255, 0, 255, 255, 255, 255, 255,
                                 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                                 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                                 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                                 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                                 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255])
        self.assertEqual(resultado,  esperado)

    # Teste utilizado para fazer a questão 1, executando da forma correta para o unittest avaliar
    # "Modifique este método para que ele implemente o teste de cima (invertendo a pequena imagem 4×1)"
    def test_invertida_2(self):
        imagem_teste = pset1.Imagem(4, 1, [29, 89, 136, 200])
        imagem_invertida = imagem_teste.invertida()
        output_esperado = pset1.Imagem(4, 1, [226, 166, 119, 55])
        self.assertEqual(imagem_invertida, output_esperado)

    # Teste utilizado para fazer a questão 2, executando da forma correta para o unittest avaliar
    def test_invertida_3(self):
        imagem_peixe = pset1.Imagem.carregar('test_images/bluegill.png')
        imagem_peixe_invertida = imagem_peixe.invertida()
        output_esperado = pset1.Imagem(imagem_peixe.largura, imagem_peixe.altura, [255 - pixel for pixel in imagem_peixe.pixels])
        self.assertEqual(imagem_peixe_invertida, output_esperado)

    def test_imagens_invertidas(self):
        for nome_arquivo in ('mushroom', 'twocats', 'chess'):
            with self.subTest(f=nome_arquivo):
                arquivo_entrada = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % nome_arquivo)
                arquivo_saida = os.path.join(TEST_DIRECTORY, 'test_results', '%s_invert.png' % nome_arquivo)
                resultado = pset1.Imagem.carregar(arquivo_entrada).invertida()
                esperado = pset1.Imagem.carregar(arquivo_saida)
                self.assertEqual(resultado,  esperado)

# Classe para os testes dos filtros:
class TestFiltros(unittest.TestCase):
    def test_borrada(self):
        for tamanho_kernel in (1, 3, 7):
            for nome_arquivo in ('mushroom', 'twocats', 'chess'):
                with self.subTest(k=tamanho_kernel, f=nome_arquivo):
                    arquivo_entrada = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % nome_arquivo)
                    arquivo_saida = os.path.join(TEST_DIRECTORY, 'test_results',
                                                 '%s_blur_%02d.png' % (nome_arquivo, tamanho_kernel))
                    imagem_entrada = pset1.Imagem.carregar(arquivo_entrada)
                    imagem_entrada_copia = pset1.Imagem(imagem_entrada.largura, imagem_entrada.altura,
                                                        imagem_entrada.pixels)
                    resultado = imagem_entrada.borrada(tamanho_kernel)
                    esperado = pset1.Imagem.carregar(arquivo_saida)
                    self.assertEqual(imagem_entrada, imagem_entrada_copia,
                                     "Cuidado para não modificar a imagem original!")
                    self.assertEqual(resultado,  esperado)

    def test_focada(self):
        for tamanho_kernel in (1, 3, 9):
            for nome_arquivo in ('mushroom', 'twocats', 'chess'):
                with self.subTest(k=tamanho_kernel, f=nome_arquivo):
                    arquivo_entrada = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % nome_arquivo)
                    arquivo_saida = os.path.join(TEST_DIRECTORY, 'test_results',
                                                 '%s_sharp_%02d.png' % (nome_arquivo, tamanho_kernel))
                    imagem_entrada = pset1.Imagem.carregar(arquivo_entrada)
                    imagem_entrada_copia = pset1.Imagem(imagem_entrada.largura, imagem_entrada.altura,
                                                        imagem_entrada.pixels)
                    resultado = imagem_entrada.focada(tamanho_kernel)
                    esperado = pset1.Imagem.carregar(arquivo_saida)
                    self.assertEqual(imagem_entrada, imagem_entrada_copia,
                                     "Cuidado para não modificar a imagem original!")
                    self.assertEqual(resultado,  esperado)

    def test_bordas(self):
        for nome_arquivo in ('mushroom', 'twocats', 'chess'):
            with self.subTest(f=nome_arquivo):
                arquivo_entrada = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % nome_arquivo)
                arquivo_saida = os.path.join(TEST_DIRECTORY, 'test_results', '%s_edges.png' % nome_arquivo)
                imagem_entrada = pset1.Imagem.carregar(arquivo_entrada)
                imagem_entrada_copia = pset1.Imagem(imagem_entrada.largura, imagem_entrada.altura,
                                                    imagem_entrada.pixels)
                resultado = imagem_entrada.bordas()
                esperado = pset1.Imagem.carregar(arquivo_saida)
                self.assertEqual(imagem_entrada, imagem_entrada_copia,
                                 "Cuidado para não modificar a imagem original!")
                self.assertEqual(resultado,  esperado)


if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)

