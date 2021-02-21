 #!/usr/bin/env python 
 
import boto3

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

polly = boto3.client('polly')

def play_sound(text):
    response = polly.synthesize_speech(Text=text, VoiceId='Lucia', OutputFormat='ogg_vorbis')
    body = response['AudioStream'].read()
    file_name = 'voice.ogg'
    
    with open(file_name, 'wb') as file:
        file.write(body)
        file.close()

if __name__ == '__main__':
    play_sound("Hola mundo")
    