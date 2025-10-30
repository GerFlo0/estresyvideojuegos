------------------------------------------------------INSTALACION------------------------------------------------------

REQUIERE PYTHON 3.9

//crear y activar entorno virtual

python3.9 -m venv env

.\env\Scripts\activate

//actualizar pip

python -m pip install --upgrade pip

//instalar requerimientos

pip install -r requirements.txt


//Configurar area de la webcam en frames.py

------------------------------------------------------EXPLICACION------------------------------------------------------

desviacionestandar.py calcula la desviacion estandar promedio de los datos por juego asi como la desviacion entre los jugadores.

emotions.py realza el analisis de las emociones utilizando mini-xception en deepface

frames.py raliza la doble funcion de recortar la seccion de los videos presentes en videos\por_analizar correspondientes a la webcam de los participantes y posteriormente captura una imagen del video resultante cada 3 regundos

graphics1.py y graphics2.py generan cada uno una serie de graficas con los datos recopilados al momento de la ejecucion

joincsvs.py unifica todos los csv individuales de cada video en un solo csv

requirements.txt contiene todos nombres de los paquetes que requiere el proyecto para funcionar correctamente 
