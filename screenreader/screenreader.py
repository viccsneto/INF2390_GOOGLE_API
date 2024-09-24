import pyautogui
import google.generativeai as genai
import os
import time
import uuid
from gtts import gTTS
import playsound
import keyboard
# Configure your API key (replace with your actual key)
#genai.configure(api_key="AIzaSy************************XlsElsLOs")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to capture the screen
def capture_screen():
    screenshot = pyautogui.screenshot()
    # Generate a random temp file using uuid    
    image_path = f'./temp/screenshot_{uuid.uuid4()}.png'
    
    screenshot.save(image_path)
    return image_path

# Function to send the image to Gemini and get the description
def get_description(image_path):
    model = genai.GenerativeModel(model_name="gemini-1.5-pro")  # Specify vision-description model

    sample_file = genai.upload_file(path=image_path,
                            display_name="Screenshot")

    try:
        # Send request to generate description
        response = model.generate_content([sample_file, "Descreva a imagem para um deficiente visual com uma resposta curta e objetiva."])
        return response.text
    except Exception as e:
        return f"Error: {e}"  # Handle potential errors

# Function to convert text to speech using gTTS
def text_to_speech(text):
    print(text)
    # Generate speech
    tts = gTTS(text=text, lang='pt-br')
    audio_file = f'./temp/audio_{uuid.uuid4()}.mp3'
    
    # Save the generated speech to a file
    tts.save(audio_file)
    
    # Play the audio file
    playsound.playsound(audio_file)
    
    # Remove the audio file after playback
    os.remove(audio_file)

# Main loop
if __name__ == '__main__':
    # Create temp directory if not exists
    if not os.path.exists('./temp'):
        os.makedirs('./temp')

    print("--------------------------------------------------------------------")
    text_to_speech("O leitor de tela está rodando. Pressione Ctrl+Shift para capturar a tela.")
    print("--------------------------------------------------------------------")
    while True:
        #check if ctrl+shift is pressed
        if keyboard.is_pressed('ctrl') and keyboard.is_pressed('shift'):            
            text_to_speech("Lendo a tela, por favor aguarde...")
            image_path = capture_screen()
            description = get_description(image_path)
            
            text_to_speech(description)
            
            # Clean up the captured image
            os.remove(image_path)
            print("--------------------------------------------------------------------")
            text_to_speech("O leitor de tela está rodando. Pressione Ctrl+Shift para capturar a tela.")
            print("--------------------------------------------------------------------")