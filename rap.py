import magenta.music as mm
import fluidsynth
from tortoise.api import TextToSpeech
from pydub import AudioSegment
import time

# Step 1: Read User Lyrics
with open("lyrics.txt", "r") as file:
    lyrics = file.read()
print("Loaded lyrics:\n", lyrics)

# Step 2: Generate Melody & Chords
def generate_melody():
    return mm.Melody([60, 62, 64, 65, 67, 69, 71, 72])  # C Major scale
melody = generate_melody()
print("Generated melody:", melody)

# Step 3: Convert Melody to Audio using FluidSynth
def generate_instrumental():
    fs = fluidsynth.Synth()
    fs.start()
    sfid = fs.sfload("soundfont.sf2")  # Ensure you have a valid soundfont file
    fs.program_select(0, sfid, 0, 0)
    
    instrumental = "instrumental.wav"
    for note in melody._events:
        fs.noteon(0, note, 100)
        time.sleep(0.5)
        fs.noteoff(0, note)
    
    fs.delete()
    return instrumental

instrumental = generate_instrumental()
print("Instrumental generated.")

# Step 4: Generate AI Vocals
tts = TextToSpeech()
audio = tts.synthesize(lyrics, voice="random")

with open("vocals.wav", "wb") as f:
    f.write(audio)
print("Vocals generated.")

# Step 5: Mix Vocals & Instrumental
def mix_tracks(inst, voc):
    inst_audio = AudioSegment.from_wav(inst)
    voc_audio = AudioSegment.from_wav(voc)
    final_mix = inst_audio.overlay(voc_audio, position=0)
    final_mix.export("final_song.wav", format="wav")
    print("Final song saved as final_song.wav")

mix_tracks("instrumental.wav", "vocals.wav")
