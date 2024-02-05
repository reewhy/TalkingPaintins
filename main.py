import datetime
import os
os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')
import vlc

import cv2

# Crea un classificatore delle immagini (con dati per riconoscimento facciale)
face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# Nome del video
video_name = 'vid4.mp4'
# Istanza della webcam
cap = cv2.VideoCapture(0)

# Variabili semaforo per il controllo del video
video_playing = False
can_play = True

# Ultima volta che è stato avviato il video
last_played = datetime.datetime.now()

# Funzione per il riconoscimento facciale
def detect_face(img, draw=False):
    # Conversione dell'immagine in un'immagine grigia
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Ottieni la lista di facce
    faces = face_classifier.detectMultiScale(gray_img, 1.1, 5, minSize=(40, 40))
    # Se vuoi disegnare la scatola intorno la faccia
    if draw:
        # Prendi le informazioni di ogni faccia
        for(x, y, w, h) in faces:
            # Disegna un triangolo intorno la faccia
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 4)
    # Ritorna la lista di facce
    return faces

# Istanza del media player con il video che si vuole mostrare
video = vlc.MediaPlayer(video_name)
# Loop infinito
while True:
    # Prendi un frame dalla fotocamera
    res1, frame = cap.read()

    # Se il video sta riproducendo, mostra la scritta "playing"
    # Se no, ma il video è avviabile, mostra la scritta "not playing"
    # Altrimenti mostra la scritta "Cooldown"
    if video_playing:
        cv2.putText(frame, 'Playing...', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
    elif can_play:
        cv2.putText(frame, 'Not playing', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
    else:
        cv2.putText(frame, 'Cooldown', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    # Se il video sta riproducendo
    if video_playing:
        can_play = False
        # Avvia il video
        video.play()

    # Riconosci le facce nel frame preso dalla fotocamera (e disegnale)
    faces = detect_face(frame, draw=True)

    # Se c'è almeno una faccia e il video può essere riprodotto
    if len(faces) > 0 and can_play:
        video_playing = True

    # Se sono passati 3 secondi da quando è finito il video
    if datetime.datetime.now().second == last_played.second+3:
        # Rendi il video riproducibile
        can_play = True

    # Mostra il frame della fotocamera
    cv2.imshow('Video1', frame)

    # Se il video è finito
    if video.get_state() == 6:
        video_playing = False
        # Riporta il video all'inizio
        video.set_media(video.get_media())
        # Salva quando è finito
        last_played = datetime.datetime.now()

    if(cv2.waitKey(1) and 0xFF == ord("q")):
        break

# Rilascia la fotocamera e chiudi le finestre
cap.release()
cv2.destroyAllWindows()