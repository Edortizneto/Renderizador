#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# pylint: disable=invalid-name

"""
Biblioteca Gráfica / Graphics Library.

Desenvolvido por: Edgard Ortiz Neto
Disciplina: Computação Gráfica
Data: 24 de fevereiro de 2023
"""

import time         # Para operações com tempo
import gpu          # Simula os recursos de uma GPU
import math         # Funções matemáticas
import numpy as np  # Biblioteca do Numpy

class Stack:
    def __init__(self) -> None:
        self.stack = []
    
    def peek(self):
        if self.stack:
            return self.stack[-1]
    
    def push(self,value):
        self.stack.append(value)
    
    def pop(self):
        if self.stack:
            self.stack.pop()

class GL:
    """Classe que representa a biblioteca gráfica (Graphics Library)."""

    width = 800   # largura da tela
    height = 600  # altura da tela
    near = 0.01   # plano de corte próximo
    far = 1000    # plano de corte distante
    
    @staticmethod
    def setup(DEPTH, DRAW, width, height, near=0.01, far=1000):
        """Definr parametros para câmera de razão de aspecto, plano próximo e distante."""
        GL.DEPTH = DEPTH
        GL.DRAW = DRAW
        GL.width = width
        GL.height = height
        GL.near = near
        GL.far = far
        GL.transformed = Stack()
        GL.transformed.push(GL.identityMatrix())
        

    @staticmethod
    def polypoint2D(point, colors):
        """Função usada para renderizar Polypoint2D."""
        # Nessa função você receberá pontos no parâmetro point, esses pontos são uma lista
        # de pontos x, y sempre na ordem. Assim point[0] é o valor da coordenada x do
        # primeiro ponto, point[1] o valor y do primeiro ponto. Já point[2] é a
        # coordenada x do segundo ponto e assim por diante. Assuma a quantidade de pontos
        # pelo tamanho da lista e assuma que sempre vira uma quantidade par de valores.
        # O parâmetro colors é um dicionário com os tipos cores possíveis, para o Polypoint2D
        # você pode assumir inicialmente o desenho dos pontos com a cor emissiva (emissiveColor).

        # O print abaixo é só para vocês verificarem o funcionamento, DEVE SER REMOVIDO.
        # print("Polypoint2D : pontos = {0}".format(point)) # imprime no terminal pontos
        # print("Polypoint2D : colors = {0}".format(colors)) # imprime no terminal as cores

        R = colors['emissiveColor'][0]*255
        G = colors['emissiveColor'][1]*255
        B = colors['emissiveColor'][2]*255

        # Exemplo:
        # pos_x = GL.width//2
        # pos_y = GL.height//2
        for i in range(0,len(point),2):
            if (point[i] > 0 and point[i] < GL.width) and (point[i+1] > 0 and point[i+1] < GL.height):
                gpu.GPU.draw_pixel([int(point[i]), int(point[i+1])], gpu.GPU.RGB8, [R, G, B])  # altera pixel (u, v, tipo, r, g, b)
            #gpu.GPU.draw_pixel([GL.height//2, GL.width//2], gpu.GPU.RGB8, [R, G, B])
        # cuidado com as cores, o X3D especifica de (0,1) e o Framebuffer de (0,255)
        
    @staticmethod
    def polyline2D(lineSegments, colors):
        """Função usada para renderizar Polyline2D."""
        # Nessa função você receberá os pontos de uma linha no parâmetro lineSegments, esses
        # pontos são uma lista de pontos x, y sempre na ordem. Assim point[0] é o valor da
        # coordenada x do primeiro ponto, point[1] o valor y do primeiro ponto. Já point[2] é
        # a coordenada x do segundo ponto e assim por diante. Assuma a quantidade de pontos
        # pelo tamanho da lista. A quantidade mínima de pontos são 2 (4 valores), porém a
        # função pode receber mais pontos para desenhar vários segmentos. Assuma que sempre
        # vira uma quantidade par de valores.
        # O parâmetro colors é um dicionário com os tipos cores possíveis, para o Polyline2D
        # você pode assumir o desenho das linhas com a cor emissiva (emissiveColor).

        # print("Polyline2D : lineSegments = {0}".format(lineSegments)) # imprime no terminal
        # print("Polyline2D : colors = {0}".format(colors)) # imprime no terminal as cores


        for i in range(0,len(lineSegments)-2,2):
            x0 = (int(lineSegments[i]))
            y0 = (int(lineSegments[i+1]))
            x1 = (int(lineSegments[i+2]))
            y1 = (int(lineSegments[i+3]))

            dx = (abs(x1-x0))
            dy = (-abs(y1-y0))
            error = (dx+dy)
            sx = (1 if x0 < x1 else -1)
            sy = (1 if y0 < y1 else -1)
            

            # Algoritmo de Bresenham
            while True:
                #print("x0,y0 = ",x0,y0)
                GL.polypoint2D([x0, y0], colors) 
                if 2*error >= dy:
                    if x0 == x1:
                        break
                    x0  += sx
                    error += dy
                    
                if 2*error <= dx:
                    if y0 == y1:
                        break
                    y0  += sy
                    error += dx
                     
        
        # Exemplo:
        # pos_x = GL.width//2
        # pos_y = GL.height//2
        #gpu.GPU.draw_pixel([pos_x, pos_y], gpu.GPU.RGB8, [R, G, B])  # altera pixel (u, v, tipo, r, g, b)
        # cuidado com as cores, o X3D especifica de (0,1) e o Framebuffer de (0,255)

    @staticmethod
    def L(x, y, x0, y0, x1, y1):
        return (y1-y0)*x - (x1-x0)*y + y0*(x1-x0) - x0*(y1-y0)
    
    @staticmethod
    def triangleSet2D(vertices, colors):
        """Função usada para renderizar TriangleSet2D."""
        # Nessa função você receberá os vertices de um triângulo no parâmetro vertices,
        # esses pontos são uma lista de pontos x, y sempre na ordem. Assim point[0] é o
        # valor da coordenada x do primeiro ponto, point[1] o valor y do primeiro ponto.
        # Já point[2] é a coordenada x do segundo ponto e assim por diante. Assuma que a
        # quantidade de pontos é sempre multiplo de 3, ou seja, 6 valores ou 12 valores, etc.
        # O parâmetro colors é um dicionário com os tipos cores possíveis, para o TriangleSet2D
        # você pode assumir o desenho das linhas com a cor emissiva (emissiveColor).
        # print("TriangleSet2D : vertices = {0}".format(vertices)) # imprime no terminal
        # print("TriangleSet2D : colors = {0}".format(colors)) # imprime no terminal as cores

        for i in range(0,len(vertices),6):
            
            # Otimização: Definindo limites do bounding box dos triângulos

            x_max = int(max([vertices[i+0], vertices[i+2], vertices[i+4]]))
            x_min = int(min([vertices[i+0], vertices[i+2], vertices[i+4]]))
            y_max = int(max([vertices[i+1], vertices[i+3], vertices[i+5]]))
            y_min = int(min([vertices[i+1], vertices[i+3], vertices[i+5]]))
            
            for x in range(x_min, x_max + 1):
                for y in range(y_min, y_max + 1):
                    L1 = GL.L(vertices[i+0], vertices[i+1], vertices[i+2], vertices[i+3], x, y)
                    L2 = GL.L(vertices[i+2], vertices[i+3], vertices[i+4], vertices[i+5], x, y)
                    L3 = GL.L(vertices[i+4], vertices[i+5], vertices[i+0], vertices[i+1], x, y)
                    if L1 >= 0 and L2 >= 0 and L3 >= 0:
                        GL.polypoint2D([x, y], colors)

    @staticmethod
    def triangleSet(point, colors):
        """Função usada para renderizar TriangleSet."""
        # Nessa função você receberá pontos no parâmetro point, esses pontos são uma lista
        # de pontos x, y, e z sempre na ordem. Assim point[0] é o valor da coordenada x do
        # primeiro ponto, point[1] o valor y do primeiro ponto, point[2] o valor z da
        # coordenada z do primeiro ponto. Já point[3] é a coordenada x do segundo ponto e
        # assim por diante.
        # No TriangleSet os triângulos são informados individualmente, assim os três
        # primeiros pontos definem um triângulo, os três próximos pontos definem um novo
        # triângulo, e assim por diante.
        # O parâmetro colors é um dicionário com os tipos cores possíveis, você pode assumir
        # inicialmente, para o TriangleSet, o desenho das linhas com a cor emissiva
        # (emissiveColor), conforme implementar novos materias você deverá suportar outros
        # tipos de cores.

        # O print abaixo é só para vocês verificarem o funcionamento, DEVE SER REMOVIDO.
        #print("TriangleSet : pontos = {0}".format(point)) # imprime no terminal pontos
        #print("TriangleSet : colors = {0}".format(colors)) # imprime no terminal as cores

        # Exemplo de desenho de um pixel branco na coordenada 10, 10
        #gpu.GPU.draw_pixel([10, 10], gpu.GPU.RGB8, [255, 255, 255])  # altera pixel
        
        triangle_vertices = []

        for i in range(0, len(point), 3):
            triangle_vertices.append([ point[i], point[i+1], point[i+2], 1 ])
        
        triangle_vertices = np.transpose(np.array(triangle_vertices))

        transformed_matrix = np.matmul(GL.transformed.peek(), triangle_vertices)

        viewpoint_matrix = np.transpose(np.matmul(GL.projected, transformed_matrix)) 
        
        points_matrix = np.copy(viewpoint_matrix)

        # Divisão Homogênea (Homogeneous Divide) 
        for i in range(len(points_matrix)):
            points_matrix[i] /= points_matrix[i][-1]

        for i in range(0,len(points_matrix),3):
            #GL.triangleSet2D(np.concatenate((points_matrix[i+0][:2], points_matrix[i+1][:2],points_matrix[i+2][:2])), colors)
            Zs = [points_matrix[i][2],points_matrix[i+1][2],points_matrix[i+2][2]]
            point1,point2,point3 = points_matrix[i+0][:2], points_matrix[i+1][:2],points_matrix[i+2][:2]
                # Otimização: Definindo limites do bounding box dos triângulos
            x_max = int(max([point1[0], point2[0], point3[0]]))
            x_min = int(min([point1[0], point2[0], point3[0]]))
            y_max = int(max([point1[1], point2[1], point3[1]]))
            y_min = int(min([point1[1], point2[1], point3[1]]))
            if type(colors) is list:
                C1,C2,C3 = colors[:3],colors[3:6],colors[6:]
            for x in range(x_min, x_max + 1):
                for y in range(y_min, y_max + 1):
                    L1 = GL.L(point1[0], point1[1], point2[0], point2[1], x, y)
                    L2 = GL.L(point2[0], point2[1], point3[0], point3[1], x, y)
                    L3 = GL.L(point3[0], point3[1], point1[0], point1[1], x, y)
                    if L1 >= 0 and L2 >= 0 and L3 >= 0:
                        #GL.polypoint2D([x, y], colors)
                        
                        # Interpolação
                        xA,yA = point1
                        xB,yB = point2
                        xC,yC = point3
                        # Definindo as coordenadas baricêntricas alpha, beta e gama
                        alpha = (-(x-xB) * (yC-yB) + (y-yB) * (xC-xB)) / (-(xA-xB) * (yC-yB) + (yA-yB) * (xC-xB))
                        beta = (-(x-xC) * (yA-yC) + (y-yC) * (xA-xC)) / (-(xB-xC) * (yA-yC) + (yB-yC) * (xA-xC))
                        gama = 1 - alpha - beta
                        Z1, Z2, Z3 = Zs
                        # Retorna a Média harmônica ponderada
                        Z = 1 / (alpha / Z1 + beta / Z2 + gama / Z3)

                        gpu.GPU.bind_framebuffer(gpu.GPU.FRAMEBUFFER, GL.DEPTH) 
                        if (x > 0 and x < GL.width) and (y > 0 and y < GL.height):
                            if (Z < gpu.GPU.read_pixel([x,y], gpu.GPU.DEPTH_COMPONENT32F)):
                                if type(colors) is list:
                                    Cs = [[alpha*color for color in C1], [beta *color for color in C2], [gama *color for color in C3]]
                                    _color = [sum(c * 255) for c in zip(*Cs)]
                                gpu.GPU.draw_pixel([x,y], gpu.GPU.DEPTH_COMPONENT32F, [Z])
                                gpu.GPU.draw_pixel([x,y], gpu.GPU.RGB8, 3*[Z*255])
                                gpu.GPU.bind_framebuffer(gpu.GPU.FRAMEBUFFER, GL.DRAW)
                                if type(colors) is list:
                                    gpu.GPU.draw_pixel([x,y], gpu.GPU.RGB8, _color)
                                else:
                                    pixel_color = gpu.GPU.read_pixel([x,y], gpu.GPU.RGB8)
                                    pixel_color = [c * colors["transparency"] for c in pixel_color]
                                    emissive_color = [c * (1-colors["transparency"]) for c in colors["emissiveColor"]]
                                    gpu.GPU.draw_pixel([x,y], gpu.GPU.RGB8, np.clip([int(sum(c * 255)) for c in zip(emissive_color, pixel_color)], 0, 255))
                            gpu.GPU.bind_framebuffer(gpu.GPU.FRAMEBUFFER, GL.DRAW)

    @staticmethod
    def translateMatrix(ex,ey,ez):
        return np.array([[1, 0, 0,  ex],
                         [0, 1, 0,  ey],
                         [0, 0, 1,  ez],
                         [0, 0, 0,   1]])
    
    @staticmethod
    def scaleMatrix(x,y,z):
        return np.array([[x,   0,  0,   0],
                         [0,   y,  0,   0],
                         [0,   0,  z,   0],
                         [0,   0,  0,   1]])
    
    @staticmethod
    def mirrorMatrix():
        return np.array([[1,   0,  0,   0],
                         [0,  -1,  0,   0],
                         [0,   0,  1,   0],
                         [0,   0,  0,   1]])
    
    @staticmethod
    def identityMatrix():
        return np.array([[1,   0,  0,   0],
                         [0,   1,  0,   0],
                         [0,   0,  1,   0],
                         [0,   0,  0,   1]])

    @staticmethod
    def rotationMatrix(qr,qi,qj,qk):
        termo11 = 1 - 2*(qj**2+qk**2) # termo da linha 1 coluna 1
        termo12 = 2*(qi*qj - qk*qr) # termo da linha 1 coluna 2
        termo13 = 2*(qi*qk + qj*qr)
        termo21 = 2*(qi*qj + qk*qr)
        termo22 = 1 - 2*(qi**2+qk**2)
        termo23 = 2*(qj*qk + qi*qr)
        termo31 = 2*(qi*qk - qj*qr)
        termo32 = 2*(qj*qk + qi*qr)
        termo33 = 1 - 2*(qi**2+qj**2)
        return np.array([[termo11, termo12, termo13, 0],
                         [termo21, termo22, termo23, 0],
                         [termo31, termo32, termo33, 0],
                         [      0,       0,       0, 1]])
    
    @staticmethod
    def perspectiveMatrix(near,right,top,far):
        return np.array([[near/right, 0,                           0,                          0],
                         [0,   near/top,                           0,                          0],
                         [0,           0, -((far+near) / (far-near)), -2*(far*near) / (far-near)],
                         [0,           0,                         -1,                         0]])
    
    @staticmethod
    def FOVy(FOVd,height,width):
        return 2*np.arctan(np.tan(FOVd/2) * (height / (height**2+width**2)**0.5))

    @staticmethod
    def viewpoint(position, orientation, fieldOfView):
        """Função usada para renderizar (na verdade coletar os dados) de Viewpoint."""
        # Na função de viewpoint você receberá a posição, orientação e campo de visão da
        # câmera virtual. Use esses dados para poder calcular e criar a matriz de projeção
        # perspectiva para poder aplicar nos pontos dos objetos geométricos.

        # O print abaixo é só para vocês verificarem o funcionamento, DEVE SER REMOVIDO.
        # print("Viewpoint : ", end='')
        # print("position = {0} ".format(position), end='')
        # print("orientation = {0} ".format(orientation), end='')
        # print("fieldOfView = {0} ".format(fieldOfView))

        axis = np.array([orientation[0], orientation[1], orientation[2]])
        axis = axis/np.linalg.norm(axis)

        Qi = axis[0] * np.sin(orientation[3] / 2)
        Qj = axis[1] * np.sin(orientation[3] / 2)
        Qk = axis[2] * np.sin(orientation[3] / 2)
        Qr = np.cos(orientation[3] / 2)
        
        lookAt_translation_matrix = np.linalg.inv(GL.translateMatrix(position[0],position[1],position[2]))
        rotation_matrix = GL.rotationMatrix(Qr,Qi,Qj,Qk)
        lookAt_matrix = np.matmul(np.transpose(rotation_matrix), lookAt_translation_matrix)
        
        FOVy = GL.FOVy(fieldOfView,GL.height,GL.width)
        top = GL.near*np.tan(FOVy)
        aspect = GL.width/GL.height
        right = top*aspect

        perspective_matrix = GL.perspectiveMatrix(GL.near,right,top,GL.far)
        display_matrix = np.matmul(GL.translateMatrix(GL.width/2,GL.height/2,0),GL.scaleMatrix(GL.width/2,GL.height/2,1))
        display_matrix = np.matmul(display_matrix,GL.mirrorMatrix())
        
        GL.projected = np.matmul(display_matrix, perspective_matrix)
        GL.projected = np.matmul(GL.projected, lookAt_matrix)


    @staticmethod
    def transform_in(translation, scale, rotation):
        """Função usada para renderizar (na verdade coletar os dados) de Transform."""
        # A função transform_in será chamada quando se entrar em um nó X3D do tipo Transform
        # do grafo de cena. Os valores passados são a escala em um vetor [x, y, z]
        # indicando a escala em cada direção, a translação [x, y, z] nas respectivas
        # coordenadas e finalmente a rotação por [x, y, z, t] sendo definida pela rotação
        # do objeto ao redor do eixo x, y, z por t radianos, seguindo a regra da mão direita.
        # Quando se entrar em um nó transform se deverá salvar a matriz de transformação dos
        # modelos do mundo em alguma estrutura de pilha.

        # O print abaixo é só para vocês verificarem o funcionamento, DEVE SER REMOVIDO.
        # print("Transform : ", end='')
        # if translation:
        #     print("translation = {0} ".format(translation), end='') # imprime no terminal
        # if scale:
        #     print("scale = {0} ".format(scale), end='') # imprime no terminal
        # if rotation:
        #     print("rotation = {0} ".format(rotation), end='') # imprime no terminal
        # print("")
        
        
        axis = np.array([rotation[0], rotation[1], rotation[2]])
        axis = axis / np.linalg.norm(axis)

        Qi = axis[0] * np.sin(rotation[3] / 2)
        Qj = axis[1] * np.sin(rotation[3] / 2)
        Qk = axis[2] * np.sin(rotation[3] / 2)
        Qr = np.cos(rotation[3] / 2)
        
        transformation_matrix = np.matmul(GL.translateMatrix(translation[0], translation[1], translation[2]), GL.rotationMatrix(Qr,Qi,Qj,Qk))
        transformation_matrix = np.matmul(transformation_matrix, GL.scaleMatrix(scale[0],scale[1],scale[2]))
        GL.transformed.push(np.matmul(GL.transformed.peek(),transformation_matrix))
        #print(GL.transformed.stack)

    @staticmethod
    def transform_out():
        """Função usada para renderizar (na verdade coletar os dados) de Transform."""
        # A função transform_out será chamada quando se sair em um nó X3D do tipo Transform do
        # grafo de cena. Não são passados valores, porém quando se sai de um nó transform se
        # deverá recuperar a matriz de transformação dos modelos do mundo da estrutura de
        # pilha implementada.

        # O print abaixo é só para vocês verificarem o funcionamento, DEVE SER REMOVIDO.
        #print("Saindo de Transform")
        
        GL.transformed.pop()

    @staticmethod
    def triangleStripSet(point, stripCount, colors):
        """Função usada para renderizar TriangleStripSet."""
        # A função triangleStripSet é usada para desenhar tiras de triângulos interconectados,
        # você receberá as coordenadas dos pontos no parâmetro point, esses pontos são uma
        # lista de pontos x, y, e z sempre na ordem. Assim point[0] é o valor da coordenada x
        # do primeiro ponto, point[1] o valor y do primeiro ponto, point[2] o valor z da
        # coordenada z do primeiro ponto. Já point[3] é a coordenada x do segundo ponto e assim
        # por diante. No TriangleStripSet a quantidade de vértices a serem usados é informado
        # em uma lista chamada stripCount (perceba que é uma lista). Ligue os vértices na ordem,
        # primeiro triângulo será com os vértices 0, 1 e 2, depois serão os vértices 1, 2 e 3,
        # depois 2, 3 e 4, e assim por diante. Cuidado com a orientação dos vértices, ou seja,
        # todos no sentido horário ou todos no sentido anti-horário, conforme especificado.

        # O print abaixo é só para vocês verificarem o funcionamento, DEVE SER REMOVIDO.
        # print("TriangleStripSet : pontos = {0} ".format(point), end='')
        # for i, strip in enumerate(stripCount):
        #     print("strip[{0}] = {1} ".format(i, strip), end='')
        # print("")
        # print("TriangleStripSet : colors = {0}".format(colors)) # imprime no terminal as cores

        # Exemplo de desenho de um pixel branco na coordenada 10, 10
        # gpu.GPU.draw_pixel([10, 10], gpu.GPU.RGB8, [255, 255, 255])  # altera pixel
        
        for i in range(stripCount[0]-2):
            first = i*3
            second = (i+1)*3
            third = (i+2)*3
            
            if i % 2 == 0:
                order = [*point[first:first+3], *point[second:second+3], *point[third:third+3]]
                
            else:
                order = [*point[second:second+3], *point[first:first+3], *point[third:third+3]]

            GL.triangleSet(order,colors)


    @staticmethod
    def indexedTriangleStripSet(point, index, colors):
        """Função usada para renderizar IndexedTriangleStripSet."""
        # A função indexedTriangleStripSet é usada para desenhar tiras de triângulos
        # interconectados, você receberá as coordenadas dos pontos no parâmetro point, esses
        # pontos são uma lista de pontos x, y, e z sempre na ordem. Assim point[0] é o valor
        # da coordenada x do primeiro ponto, point[1] o valor y do primeiro ponto, point[2]
        # o valor z da coordenada z do primeiro ponto. Já point[3] é a coordenada x do
        # segundo ponto e assim por diante. No IndexedTriangleStripSet uma lista informando
        # como conectar os vértices é informada em index, o valor -1 indica que a lista
        # acabou. A ordem de conexão será de 3 em 3 pulando um índice. Por exemplo: o
        # primeiro triângulo será com os vértices 0, 1 e 2, depois serão os vértices 1, 2 e 3,
        # depois 2, 3 e 4, e assim por diante. Cuidado com a orientação dos vértices, ou seja,
        # todos no sentido horário ou todos no sentido anti-horário, conforme especificado.

        # O print abaixo é só para vocês verificarem o funcionamento, DEVE SER REMOVIDO.
        # print("IndexedTriangleStripSet : pontos = {0}, index = {1}".format(point, index))
        # print("IndexedTriangleStripSet : colors = {0}".format(colors)) # imprime as cores

        # Exemplo de desenho de um pixel branco na coordenada 10, 10
        # gpu.GPU.draw_pixel([10, 10], gpu.GPU.RGB8, [255, 255, 255])  # altera pixel

        for i in range(len(index)-3):
            first = i*3
            second = (i+1)*3
            third = (i+2)*3

            if i % 2 == 0:
                order = [*point[first:first+3], *point[second:second+3], *point[third:third+3]]
                
            else:
                order = [*point[second:second+3], *point[first:first+3], *point[third:third+3]]

            GL.triangleSet(order,colors)


    @staticmethod
    def box(size, colors):
        """Função usada para renderizar Boxes."""
        # A função box é usada para desenhar paralelepípedos na cena. O Box é centrada no
        # (0, 0, 0) no sistema de coordenadas local e alinhado com os eixos de coordenadas
        # locais. O argumento size especifica as extensões da caixa ao longo dos eixos X, Y
        # e Z, respectivamente, e cada valor do tamanho deve ser maior que zero. Para desenha
        # essa caixa você vai provavelmente querer tesselar ela em triângulos, para isso
        # encontre os vértices e defina os triângulos.

        # O print abaixo é só para vocês verificarem o funcionamento, DEVE SER REMOVIDO.
        #print("Box : size = {0}".format(size)) # imprime no terminal pontos
        #print("Box : colors = {0}".format(colors)) # imprime no terminal as cores

        # Exemplo de desenho de um pixel branco na coordenada 10, 10
        #gpu.GPU.draw_pixel([10, 10], gpu.GPU.RGB8, [255, 255, 255])  # altera pixel

        x,y,z = size[0],size[1],size[2]
        vertices = [0.5*x, 0.5*y, 0.5*z, 
                    -0.5*x, 0.5*y, 0.5*z,
                    0.5*x, -0.5*y, 0.5*z,
                    -0.5*x, -0.5*y, 0.5*z,
                    0.5*x, 0.5*y, -0.5*z, 
                    -0.5*x, 0.5*y, -0.5*z, 
                    -0.5*x, -0.5*y, -0.5*z, 
                    0.5*x, -0.5*y, -0.5*z]

        
        indexes = [[0, 1, 2, -1, 1, 3, 2, -1],
                   [0, 4, 1, -1, 4, 5, 1, -1],
                   [1, 5, 3, -1, 5, 6, 3, -1],
                   [3, 6, 2, -1, 6, 7, 2, -1],
                   [2, 7, 0, -1, 7, 4, 0, -1],
                   [4, 7, 5, -1, 7, 6, 5, -1]]
        
        for i in range(len(indexes)):
            GL.indexedFaceSet(coord=vertices, coordIndex=indexes[i], colors=colors, colorPerVertex=False, color=None, colorIndex=[], texCoord=None, texCoordIndex=None, current_texture=None)

    @staticmethod
    def indexedFaceSet(coord, coordIndex, colorPerVertex, color, colorIndex,
                       texCoord, texCoordIndex, colors, current_texture):
        """Função usada para renderizar IndexedFaceSet."""
        # A função indexedFaceSet é usada para desenhar malhas de triângulos. Ela funciona de
        # forma muito simular a IndexedTriangleStripSet porém com mais recursos.
        # Você receberá as coordenadas dos pontos no parâmetro cord, esses
        # pontos são uma lista de pontos x, y, e z sempre na ordem. Assim coord[0] é o valor
        # da coordenada x do primeiro ponto, coord[1] o valor y do primeiro ponto, coord[2]
        # o valor z da coordenada z do primeiro ponto. Já coord[3] é a coordenada x do
        # segundo ponto e assim por diante. No IndexedFaceSet uma lista de vértices é informada
        # em coordIndex, o valor -1 indica que a lista acabou.
        # A ordem de conexão será de 3 em 3 pulando um índice. Por exemplo: o
        # primeiro triângulo será com os vértices 0, 1 e 2, depois serão os vértices 1, 2 e 3,
        # depois 2, 3 e 4, e assim por diante.
        # Adicionalmente essa implementação do IndexedFace aceita cores por vértices, assim
        # se a flag colorPerVertex estiver habilitada, os vértices também possuirão cores
        # que servem para definir a cor interna dos poligonos, para isso faça um cálculo
        # baricêntrico de que cor deverá ter aquela posição. Da mesma forma se pode definir uma
        # textura para o poligono, para isso, use as coordenadas de textura e depois aplique a
        # cor da textura conforme a posição do mapeamento. Dentro da classe GPU já está
        # implementadado um método para a leitura de imagens.

        # Os prints abaixo são só para vocês verificarem o funcionamento, DEVE SER REMOVIDO.
        # print("IndexedFaceSet : ")
        # if coord:
        #     print("\tpontos(x, y, z) = {0}, coordIndex = {1}".format(coord, coordIndex))
        # print("colorPerVertex = {0}".format(colorPerVertex))
        # if colorPerVertex and color and colorIndex:
        #     print("\tcores(r, g, b) = {0}, colorIndex = {1}".format(color, colorIndex))
        # if texCoord and texCoordIndex:
        #     print("\tpontos(u, v) = {0}, texCoordIndex = {1}".format(texCoord, texCoordIndex))
        # if current_texture:
        #     image = gpu.GPU.load_texture(current_texture[0])
        #     print("\t Matriz com image = {0}".format(image))
        #     print("\t Dimensões da image = {0}".format(image.shape))
        # print("IndexedFaceSet : colors = {0}".format(colors))  # imprime no terminal as cores

        # Exemplo de desenho de um pixel branco na coordenada 10, 10
        # gpu.GPU.draw_pixel([10, 10], gpu.GPU.RGB8, [255, 255, 255])  # altera pixel
        for i in range(0,len(coordIndex)-3,4):
            first = coordIndex[i]*3
            second = coordIndex[i+1]*3
            third = coordIndex[i+2]*3
            
            if len(colorIndex) > 0:
                color1 = colorIndex[i]*3
                color2 = colorIndex[i+1]*3
                color3 = colorIndex[i+2]*3
            
            if i % 2 == 0:
                order = [*coord[first:first+3], *coord[second:second+3], *coord[third:third+3]]
                if len(colorIndex) > 0:
                    order_colors = [*color[color1:color1+3], *color[color2:color2+3], *color[color3:color3+3]]
                
            else:
                order = [*coord[second:second+3], *coord[first:first+3], *coord[third:third+3]]
                if len(colorIndex) > 0:
                    order_colors = [*color[color2:color2+3], *color[color1:color1+3], *color[color3:color3+3]]

            if len(colorIndex) > 0: GL.triangleSet(order,order_colors)
            else: GL.triangleSet(order,colors)

    @staticmethod
    def sphere(radius, colors):
        """Função usada para renderizar Esferas."""
        # A função sphere é usada para desenhar esferas na cena. O esfera é centrada no
        # (0, 0, 0) no sistema de coordenadas local. O argumento radius especifica o
        # raio da esfera que está sendo criada. Para desenha essa esfera você vai
        # precisar tesselar ela em triângulos, para isso encontre os vértices e defina
        # os triângulos.

        # O print abaixo é só para vocês verificarem o funcionamento, DEVE SER REMOVIDO.
        #print("Sphere : radius = {0}".format(radius)) # imprime no terminal o raio da esfera
        # print("Sphere : colors = {0}".format(colors)) # imprime no terminal as cores
        coords = []
        u, v = np.mgrid[0:2*np.pi:32j, 0:np.pi:32j]
        x = radius*np.cos(u)*np.sin(v)
        y = radius*np.sin(u)*np.sin(v)
        z = radius*np.cos(v)
        for i in range(len(x)):
            circ = []
            for j in range(len(x[i])):
                circ.append([x[i,j],y[i,j],z[i,j]])
            coords.append(circ)
        for i in range(len(coords)-1):
            strip_seq = []
            strip_seq += coords[i][0]
            strip_seq += coords[i+1][0]
            strip_seq += coords[i][-1]
            strip_seq += coords[i+1][-1]
            for k in range(len(coords[i])):
                strip_seq += coords[i][k]
                strip_seq += coords[i+1][k]   
            
            index_seq = [i for i in range(len(strip_seq)//3)]
            GL.indexedTriangleStripSet(strip_seq, index_seq, colors)

    @staticmethod
    def navigationInfo(headlight):
        """Características físicas do avatar do visualizador e do modelo de visualização."""
        # O campo do headlight especifica se um navegador deve acender um luz direcional que
        # sempre aponta na direção que o usuário está olhando. Definir este campo como TRUE
        # faz com que o visualizador forneça sempre uma luz do ponto de vista do usuário.
        # A luz headlight deve ser direcional, ter intensidade = 1, cor = (1 1 1),
        # ambientIntensity = 0,0 e direção = (0 0 −1).

        # O print abaixo é só para vocês verificarem o funcionamento, DEVE SER REMOVIDO.
        print("NavigationInfo : headlight = {0}".format(headlight)) # imprime no terminal

    @staticmethod
    def directionalLight(ambientIntensity, color, intensity, direction):
        """Luz direcional ou paralela."""
        # Define uma fonte de luz direcional que ilumina ao longo de raios paralelos
        # em um determinado vetor tridimensional. Possui os campos básicos ambientIntensity,
        # cor, intensidade. O campo de direção especifica o vetor de direção da iluminação
        # que emana da fonte de luz no sistema de coordenadas local. A luz é emitida ao
        # longo de raios paralelos de uma distância infinita.

        # O print abaixo é só para vocês verificarem o funcionamento, DEVE SER REMOVIDO.
        print("DirectionalLight : ambientIntensity = {0}".format(ambientIntensity))
        print("DirectionalLight : color = {0}".format(color)) # imprime no terminal
        print("DirectionalLight : intensity = {0}".format(intensity)) # imprime no terminal
        print("DirectionalLight : direction = {0}".format(direction)) # imprime no terminal

    @staticmethod
    def pointLight(ambientIntensity, color, intensity, location):
        """Luz pontual."""
        # Fonte de luz pontual em um local 3D no sistema de coordenadas local. Uma fonte
        # de luz pontual emite luz igualmente em todas as direções; ou seja, é omnidirecional.
        # Possui os campos básicos ambientIntensity, cor, intensidade. Um nó PointLight ilumina
        # a geometria em um raio de sua localização. O campo do raio deve ser maior ou igual a
        # zero. A iluminação do nó PointLight diminui com a distância especificada.

        # O print abaixo é só para vocês verificarem o funcionamento, DEVE SER REMOVIDO.
        print("PointLight : ambientIntensity = {0}".format(ambientIntensity))
        print("PointLight : color = {0}".format(color)) # imprime no terminal
        print("PointLight : intensity = {0}".format(intensity)) # imprime no terminal
        print("PointLight : location = {0}".format(location)) # imprime no terminal

    @staticmethod
    def fog(visibilityRange, color):
        """Névoa."""
        # O nó Fog fornece uma maneira de simular efeitos atmosféricos combinando objetos
        # com a cor especificada pelo campo de cores com base nas distâncias dos
        # vários objetos ao visualizador. A visibilidadeRange especifica a distância no
        # sistema de coordenadas local na qual os objetos são totalmente obscurecidos
        # pela névoa. Os objetos localizados fora de visibilityRange do visualizador são
        # desenhados com uma cor de cor constante. Objetos muito próximos do visualizador
        # são muito pouco misturados com a cor do nevoeiro.

        # O print abaixo é só para vocês verificarem o funcionamento, DEVE SER REMOVIDO.
        print("Fog : color = {0}".format(color)) # imprime no terminal
        print("Fog : visibilityRange = {0}".format(visibilityRange))

    @staticmethod
    def timeSensor(cycleInterval, loop):
        """Gera eventos conforme o tempo passa."""
        # Os nós TimeSensor podem ser usados para muitas finalidades, incluindo:
        # Condução de simulações e animações contínuas; Controlar atividades periódicas;
        # iniciar eventos de ocorrência única, como um despertador;
        # Se, no final de um ciclo, o valor do loop for FALSE, a execução é encerrada.
        # Por outro lado, se o loop for TRUE no final de um ciclo, um nó dependente do
        # tempo continua a execução no próximo ciclo. O ciclo de um nó TimeSensor dura
        # cycleInterval segundos. O valor de cycleInterval deve ser maior que zero.

        # Deve retornar a fração de tempo passada em fraction_changed

        # O print abaixo é só para vocês verificarem o funcionamento, DEVE SER REMOVIDO.
        print("TimeSensor : cycleInterval = {0}".format(cycleInterval)) # imprime no terminal
        print("TimeSensor : loop = {0}".format(loop))

        # Esse método já está implementado para os alunos como exemplo
        epoch = time.time()  # time in seconds since the epoch as a floating point number.
        fraction_changed = (epoch % cycleInterval) / cycleInterval

        return fraction_changed

    @staticmethod
    def splinePositionInterpolator(set_fraction, key, keyValue, closed):
        """Interpola não linearmente entre uma lista de vetores 3D."""
        # Interpola não linearmente entre uma lista de vetores 3D. O campo keyValue possui
        # uma lista com os valores a serem interpolados, key possui uma lista respectiva de chaves
        # dos valores em keyValue, a fração a ser interpolada vem de set_fraction que varia de
        # zeroa a um. O campo keyValue deve conter exatamente tantos vetores 3D quanto os
        # quadros-chave no key. O campo closed especifica se o interpolador deve tratar a malha
        # como fechada, com uma transições da última chave para a primeira chave. Se os keyValues
        # na primeira e na última chave não forem idênticos, o campo closed será ignorado.

        # O print abaixo é só para vocês verificarem o funcionamento, DEVE SER REMOVIDO.
        print("SplinePositionInterpolator : set_fraction = {0}".format(set_fraction))
        print("SplinePositionInterpolator : key = {0}".format(key)) # imprime no terminal
        print("SplinePositionInterpolator : keyValue = {0}".format(keyValue))
        print("SplinePositionInterpolator : closed = {0}".format(closed))

        # Abaixo está só um exemplo de como os dados podem ser calculados e transferidos
        value_changed = [0.0, 0.0, 0.0]
        
        return value_changed

    @staticmethod
    def orientationInterpolator(set_fraction, key, keyValue):
        """Interpola entre uma lista de valores de rotação especificos."""
        # Interpola rotações são absolutas no espaço do objeto e, portanto, não são cumulativas.
        # Uma orientação representa a posição final de um objeto após a aplicação de uma rotação.
        # Um OrientationInterpolator interpola entre duas orientações calculando o caminho mais
        # curto na esfera unitária entre as duas orientações. A interpolação é linear em
        # comprimento de arco ao longo deste caminho. Os resultados são indefinidos se as duas
        # orientações forem diagonalmente opostas. O campo keyValue possui uma lista com os
        # valores a serem interpolados, key possui uma lista respectiva de chaves
        # dos valores em keyValue, a fração a ser interpolada vem de set_fraction que varia de
        # zeroa a um. O campo keyValue deve conter exatamente tantas rotações 3D quanto os
        # quadros-chave no key.

        # O print abaixo é só para vocês verificarem o funcionamento, DEVE SER REMOVIDO.
        print("OrientationInterpolator : set_fraction = {0}".format(set_fraction))
        print("OrientationInterpolator : key = {0}".format(key)) # imprime no terminal
        print("OrientationInterpolator : keyValue = {0}".format(keyValue))

        # Abaixo está só um exemplo de como os dados podem ser calculados e transferidos
        value_changed = [0, 0, 1, 0]

        return value_changed

    # Para o futuro (Não para versão atual do projeto.)
    def vertex_shader(self, shader):
        """Para no futuro implementar um vertex shader."""

    def fragment_shader(self, shader):
        """Para no futuro implementar um fragment shader."""
