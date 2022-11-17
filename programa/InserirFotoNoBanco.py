# Classe criada para inserir imagem fixas no banco para a codificação correta.
# Para inserir um novo registro no banco, inserir a imagem no projeto e referenciar na linha 22.

# Necessário alterar o ID pois é chave primária e as demais informações de acordo com a foto inserida.

import pymysql
import face_recognition as fr
import cv2

conexao = pymysql.connect(
    host='localhost',
    user='root',
    password='123456'
)


def ArrayToString(array):
    resultado = ''
    for elemento in array:
        resultado = resultado + str(elemento) + ";"
    return resultado[0:-1]


processarImagem = fr.load_image_file('Elon.jpg')
processarImagem = cv2.cvtColor(processarImagem, cv2.COLOR_BGR2RGB)

faceLoc = fr.face_locations(processarImagem)[0]
cv2.rectangle(processarImagem, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (0, 255, 0), 2)

encodeImagemProcessada = fr.face_encodings(processarImagem)[0]

cursor = conexao.cursor()
cursor.execute(
    "INSERT INTO db_acesso.tb_usuario(id_convidado, nome, foto, nivel_acesso) VALUES(03, 'Elon Musk', '" + ArrayToString(
        encodeImagemProcessada) + "', 02) ")
conexao.commit()

conexao.close()
