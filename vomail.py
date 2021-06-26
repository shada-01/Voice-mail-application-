import sys 
import getpass
import time
from pydub import AudioSegment
import speech_recognition as sr 
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#from smtplib import SMTP
import ssl

r = sr.Recognizer()


def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


def convert_mp3_wav(aud):  
	# assign files
	input_file = aud
	output_file ="result.wav"
	  
	# convert mp3 file to wav file
	sound = AudioSegment.from_mp3(input_file)
	sound.export(output_file, format="wav")

def voicerec():
	r = sr.Recognizer()
	mic=sr.Microphone()
	time.sleep(2)
	for j in range(3):
		print('Speak!')
		guess = recognize_speech_from_mic(r, mic)
		if guess["transcription"]:
			break
		if not guess["success"]:
			break
		print("I didn't catch that. What did you say?\n")
	print("You said: {}".format(guess["transcription"]))
	res=int(input("Enter 1 for recording once more or 0 if the speech is correct : "))
	if(res==1):
		voicerec()
	else:
		return (guess["transcription"])
 



# a function that splits the audio file into chunks
# and applies speech recognition
def get_large_audio_transcription(filee):
    
    r = sr.Recognizer()
    # open the audio file using pydub
    sound = AudioSegment.from_wav(filee)  
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,silence_thresh = sound.dBFS-14,keep_silence=500)
    folder_name = "audio-chunks"
   
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    
    for i, audio_chunk in enumerate(chunks, start=1):
        
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
       
        with sr.AudioFile(chunk_filename) as source:
            #r.adjust_for_ambient_noise(source) #clears the ambient noise of the file
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                whole_text += text
           
    return whole_text

def main():
	
 
		print("\t\tVOMAIL APPLICATION\n")	
        
	
		usr=input   ("Enter your email      : ")
		pas=getpass.getpass(prompt='Enter your password   :')
		rec=input    ("Enter reciever email  : ")
		print("\nRecord your subject ")
		sub=str(voicerec())
		sub=f"{sub.capitalize()}"
		filee=input("Enter audio file name of body : ")
		body=convert_mp3_wav(filee)
		text=get_large_audio_transcription("result.wav")
		
		message = MIMEMultipart()
		message['From'] = usr
		message['To'] = rec
		message['Subject'] = sub
		message["Bcc"] = rec
                # Add body to email
		message.attach(MIMEText(text, "plain"))
		textt = message.as_string()

		try:
			server=smtplib.SMTP("smtp.gmail.com",587)
			server.starttls()
			server.login(usr,pas)
			server.sendmail(usr,rec,textt)
			server.quit()
			print("Mail sent!")
		except SMTPException:

			print ("Error:Unable to send mail.Try again later!")
			

main()
	



