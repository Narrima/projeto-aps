import cv2
import face_recognition as fr
import pymysql

def StringToArray(linha):
    temp = linha.split(';')
    resultado = []
    for elemento in temp:
        resultado.append(float(elemento))
    return resultado

# Criando conexão com banco Mysql
conexao = pymysql.connect(
    host='localhost',
    user='root',
    password='123456'
)

cursor = conexao.cursor()

# Seleciona todos os registros da tabela
cursor.execute("SELECT id_convidado,nome, foto, nivel_acesso from db_acesso.tb_usuario")
registros = cursor.fetchall()

video_capture = cv2.VideoCapture(0)
processar_imagem = True
achou = False
nomes_rostos = []
while not achou:

    # Captura a imagem da câmera
    video, imagem = video_capture.read()

    # Pular pra processar a cada dois frames APENAS
    if processar_imagem:

        # Diminui a imagem para melhor performance - opcional
        imagem_pequena = cv2.resize(imagem, (0, 0), fx=0.25, fy=0.25)

        # Converte a imagem de BRG para RGB (necessário para a biblioteca face_recognition)
        imagem_rgb_pequena = imagem_pequena[:, :, ::-1]

        # Identifica os rostos na imagem e gera a codificação
        localizacoes_rostos = fr.face_locations(imagem_rgb_pequena)
        codificacoes_rostos = fr.face_encodings(imagem_rgb_pequena, localizacoes_rostos)

        nomes_rostos = []
        for rosto_encontrado in codificacoes_rostos:

            # Varre todos os registros do banco de dados
            for reg in registros:
                id_convidado = reg[0]
                nome = reg[1]
                foto = reg[2]
                nivel_acesso = reg[3]

                # Verifica se o rosto encontrado na imagem é igual a algum do banco de dados
                encontrados = fr.compare_faces([StringToArray(foto)], rosto_encontrado)

                # Se tem algum rosto encontrado, guarda os dados
                if True in encontrados:
                    achou = True
                    id = id_convidado
                    name = nome
                    level = nivel_acesso
                    nomes_rostos.append(name)

    # Controla Pular pra processar a cada dois frames APENAS
    processar_imagem = not processar_imagem

    # Marca os rostos encontrados com retangulo
    for (topo, direita, baixo, esquerda), name in zip(localizacoes_rostos, nomes_rostos):

        # Ajusta a escala
        topo *= 4
        direita *= 4
        baixo *= 4
        esquerda *= 4

        # Desenha um retangulo no rosto
        cv2.rectangle(imagem, (esquerda, topo), (direita, baixo), (0, 0, 255), 2)

        # Escreve o nome do rosto identificado
        cv2.rectangle(imagem, (esquerda, baixo - 35), (direita, baixo), (0, 0, 255), cv2.FILLED)
        fonte = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(imagem, name, (esquerda + 6, baixo - 6), fonte, 1.0, (255, 255, 255), 1)

    # Mostra a imagem resultante
    cv2.imshow('Achou', imagem)

    # Se digitar a tecla 'q', sai do programa
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Prints para validação, não é necessário manter
print("Id do usuário: " + str(id))
print("Nome do usuário: " + name)
print("Nível de acesso: " + str(level))

# Libera a camera
video_capture.release()
cv2.destroyAllWindows()
