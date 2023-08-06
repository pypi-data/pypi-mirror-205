import io
from pydub import AudioSegment
import speech_recognition as sr
import whisper
import queue
import tempfile
import os
import threading
import click
import torch
import numpy as np
from os import listdir
from os.path import isfile, join

@click.command()
@click.option("--model", default="base", help="Model to use", type=click.Choice(["tiny","base", "small","medium","large"]))
@click.option("--device", default=("cuda" if torch.cuda.is_available() else "cpu"), help="Device to use", type=click.Choice(["cpu","cuda"]))
@click.option("--script_path", default=(os.getcwd()), help="runs scripts in provided directory based on if the filename can be found in the model output ex: 'computer run whisper.bash' ", type=click.Path())
# for when i figure out how to make this search and execute from multiple directories
# @click.option("--script_path", help="runs scripts in script_path directories based on keywords", multiple=True, type=click.Path())
@click.option("--script_extensions", '-s', default=[], help="valid script extensions to execute ex: .bash, defaults to .bash .py if none are provided", multiple=True, type=str)
@click.option("--ambient", default=False, help="allows for ambient noise adjustment at startup",is_flag=True,type=bool)
@click.option("--english", default=False, help="Whether to use English model",is_flag=True, type=bool)
@click.option("--verbose", default=False, help="Whether to print verbose output", is_flag=True,type=bool)
@click.option("--energy", default=300, help="Energy level for mic to detect", type=int)
@click.option("--dynamic_energy", default=False,is_flag=True, help="Flag to enable dynamic energy", type=bool)
@click.option("--pause", default=0.1, help="Pause time before entry ends", type=float)
@click.option("--phrase_length", default=0.8, help="minimum sound length for transcription to start (set to 0.3 to transcribe basically everything default 0.8 )", type=float)
@click.option("--save_file",default=False, help="Flag to save file", is_flag=True,type=bool)
def main(model, english,verbose, energy, pause,dynamic_energy,save_file,device,script_path,script_extensions,ambient,phrase_length):
    temp_dir = tempfile.mkdtemp() if save_file else None
    #there are no english models for large
    if model != "large" and english:
        model = model + ".en"
    audio_model = whisper.load_model(model).to(device)
    audio_queue = queue.Queue()
    result_queue = queue.Queue()
    threading.Thread(target=record_audio,
                     args=(audio_queue, energy, pause, dynamic_energy, save_file, temp_dir, ambient, phrase_length)).start()
    threading.Thread(target=transcribe_forever,
                     args=(audio_queue, result_queue, audio_model, english, verbose, save_file)).start()
    
    # Honestly i really just caveman'ed this section together all the way to os.system(exec) and it should really be rewritten, reformatted, optimized and multithreaded but at least it works even if it has some edge cases 
    # todo Edgecases: it will execute all the scripts with the valid extensions with the same keywords. That's perhaps not good?

    if script_path != os.getcwd() and not script_extensions:
        acceptablescripttypes = ('.bash','.py')
    else:
        acceptablescripttypes = script_extensions
    
    keywordlist = getnewkeywordlist(script_path, acceptablescripttypes)
    if keywordlist:
        print("Keyword list :" + str(keywordlist))
    
    while True:
        model_output = result_queue.get()
        keywordlist = getnewkeywordlist(script_path, acceptablescripttypes)
        print(model_output)
        #parts of this should probably be moved into getnewkerwordlist  
        for keywords in keywordlist:
             for skrtypes in acceptablescripttypes:
                  if keywords.endswith(skrtypes) and keywords.removesuffix(skrtypes).upper() in (model_output.removeprefix('You said: ')).upper().translate(str.maketrans(dict.fromkeys(',!.;', ''))):
             	      print("keyword recognized: " + str(keywords.removesuffix(skrtypes)))
             	      os.system('exec ' + '"' + script_path + keywords + '" &')
def getnewkeywordlist(script_path, acceptablescripttypes):
    return [scriptfile for scriptfile in listdir(script_path) if isfile(join(script_path, scriptfile)) and scriptfile.endswith(acceptablescripttypes) ]          
    
def record_audio(audio_queue, energy, pause, dynamic_energy, save_file, temp_dir, ambient, phrase_length):
    #load the speech recognizer and set the initial energy threshold and pause threshold
    r = sr.Recognizer()
    r.energy_threshold = energy
    if pause < r.non_speaking_duration:
        r.non_speaking_duration = pause
    r.pause_threshold = pause
    r.dynamic_energy_threshold = dynamic_energy
    r.phrase_threshold = phrase_length
    # r.dynamic_energy_adjustment_ratio = 600
    # r.dynamic_energy_adjustment_damping = 0.1
    
    with sr.Microphone(sample_rate=16000) as source:
        if ambient == True:
            print("Calibrating microphone for ambient noise...")
            r.adjust_for_ambient_noise(source, duration = 1) #thanks AryanEmbered

        print("Say something!")
        i = 0
        while True:
            #get and save audio to wav file
            audio = r.listen(source)
            if save_file:
                data = io.BytesIO(audio.get_wav_data())
                audio_clip = AudioSegment.from_file(data)
                filename = os.path.join(temp_dir, f"temp{i}.wav")
                audio_clip.export(filename, format="wav")
                audio_data = filename
            else:
                torch_audio = torch.from_numpy(np.frombuffer(audio.get_raw_data(), np.int16).flatten().astype(np.float32) / 32768.0)
                audio_data = torch_audio

            audio_queue.put_nowait(audio_data)
            i += 1


def transcribe_forever(audio_queue, result_queue, audio_model, english, verbose, save_file):
    while True:
        audio_data = audio_queue.get()
        if english:
            result = audio_model.transcribe(audio_data,language='english')
        else:
            result = audio_model.transcribe(audio_data)

        if not verbose:
            predicted_text = result["text"]
            result_queue.put_nowait("You said: " + predicted_text)
        else:
            result_queue.put_nowait(result)

        if save_file:
            os.remove(audio_data)

if __name__ == "__main__":
    main()
