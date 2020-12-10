import os
from pocketsphinx import LiveSpeech, get_model_path

model_path = get_model_path()

speech = LiveSpeech(
    verbose=False,
    sampling_rate=16000,
    buffer_size=2048,
    no_search=False,
    full_utt=False,
    hmm=os.path.join(model_path, 'es-es'),
    lm=os.path.join(model_path, 'es_robot.lm'),
    dic=os.path.join(model_path, 'es_robot.dict')
)

for phrase in speech:
    print(phrase)