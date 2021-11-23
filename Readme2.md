#Trocar o Python padrão da maquina
 alias python=python3


#Install ambiente virtual

 apt install python3.8-venv

#montando ambiente virtual (onde .venv pode ser qualquer nome de ambiente virutal)
python -m venv .venv

#Activando o ambiente (onde .venv deve bater com o ambiente criado)
python -m venv .venv
ou no windows =>> ./.venv/Scripts/activate.bat
para desativar usar >> deactivate

#Para Utilizasr os requerimentos existentes
pip install -r requirements.txt 

#install Bibliotecas no ambiente virtual)
pip install Flask
pip install Flask-Restful

#Fixar Requiriments
pip freeze >requirements.txt

#Caso o IDE VScode não esteja vendo os pacotes utilize
Cmd/Ctrl + Shift + P → Python: Select Interpreter → choose the one with the packages you look for:

# To Run app
python app.py





