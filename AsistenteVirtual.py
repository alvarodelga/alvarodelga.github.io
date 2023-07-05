import speech_recognition as sr
import whisper
import openai
from pytube import YouTube
import os
from elevenlabs import voices
from elevenlabs import set_api_key
from elevenlabs import generate, play
from playsound import playsound



# Key openai para ChatGPT
openai.api_key = "YOURAPIKEY"

# Modelo GPT utilizado
model_engine = "gpt-3.5-turbo"  # or any other model you'd like to use

r = sr.Recognizer()
model = whisper.load_model("small")

# Api key ElevenLabs
set_api_key("YOURAPIKEY")
# Voces disponibles eleven labs
voices = voices()

def voicerec():
    with sr.Microphone() as source:
        print("Escuchando...")
        playsound('sonidos\\escuchando.mp3')
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        with open("audio.wav", "wb") as f:
            f.write(audio.get_wav_data())
        text_dict = model.transcribe("audio.wav", fp16=False, language='es')
        text_str = text_dict["text"].lower()  # Convertir el valor de la clave "text" a una cadena en minúsculas
        print("El texto transcrito es: " + text_str)
        return text_str


def transvideo():
    model = whisper.load_model("small")
    result = model.transcribe("VideoAudio.mp3", fp16=False)
    print(result["text"])
    nombre_archivo = "transcripcion.txt"
    with open(nombre_archivo, "w") as archivo:
        archivo.write(result["text"])

def comanddetection(text_str):

    conversacion = "ordenador"

    try:
        if conversacion in text_str:
            # Extraer el texto que sigue a "ordenador"
            command = text_str.split(conversacion)[1]
            command = "ordenador " + command
            print("Peticion:", command)
            return command

    except sr.UnknownValueError:
        print("Lo siento, no he entendido lo que has dicho")

def gptturbo(command):

    messages = [{"role": "system",
                 "content": "Eres un asistente virtual con un toque hirónico, tu nombre es ordenador "
                            "y cada vez que me dirija a ti te llamare ordenador, tus respuestas no deben ser demasiado largas "}]

    content = command

    messages.append({"role": "user",
                     "content": content})

    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=messages)

    response_content = response.choices[0].message.content

    print(response_content)
    return response_content


def speaker(consulta):
    audio = generate(
        text=consulta,
        voice="alvaro",
        model='eleven_multilingual_v1')

    play(audio)

def videoyoutube(URL):
    # Definimos el enlace del video de YouTube que queremos descargar
    video_link = URL

    # Creamos una instancia de la clase YouTube
    yt = YouTube(video_link, use_oauth=True, allow_oauth_cache=True)

    # Obtenemos la mejor pista de audio disponible
    audio = yt.streams.filter(only_audio=True).first()

    # Definimos el nombre del archivo a descargar
    filename = "VideoAudio.mp3"

    # Comprobamos si el archivo ya existe y lo eliminamos
    if os.path.exists(filename):
        os.remove(filename)

    # Descargamos el audio
    audio.download(output_path="./", filename="temp")

    # Renombramos el archivo de audio descargado con el nombre "VideoAudio.mp3"
    os.rename("temp", filename)


def main():
    while True:
        text_str = voicerec()
        command = comanddetection(text_str)
        if command:
            if command.split(" ")[0] == "ordenador":
                if "descargar" in command or "descargame" in command or "descarga" in command or "descargue" in command:
                    print("comando: descarga")
                    consulta = "¿Que vídeo quieres que descargue?"
                    speaker(consulta)
                    videonum = voicerec()
                    if "1" in videonum or "uno" in videonum:
                        playsound('sonidos\\descarga.mp3')
                        print("descargando video 1...")
                        URL = "https://www.youtube.com/watch?v=J0B_eS0JuNQ&ab_channel=LinkinParkSubtitulos"
                        videoyoutube(URL)
                        transvideo()
                        consulta = "Se ha descargado y transcrito el vídeo 1"
                        speaker(consulta)

                    elif "2" in videonum or "dos" in videonum:
                        playsound('sonidos\\descarga.mp3')
                        print("descargando video 2...")
                        URL = "https://www.youtube.com/shorts/woUGD_Y1Djs"
                        videoyoutube(URL)
                        transvideo()
                        consulta = "Se ha descargado y transcrito el vídeo 2"
                        speaker(consulta)
                    else:
                        consulta = "No se ha reconocido correctamente que vídeo quieres que descargue"
                        speaker(consulta)
                elif "consulta" in command:
                    print("comando: consulta")
                    consulta = gptturbo(command)
                    speaker(consulta)

if __name__ == "__main__":
    main()