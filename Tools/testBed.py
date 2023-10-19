from pocketsphinx import LiveSpeech

speech = LiveSpeech(keyphrase='simon', kws_threshold=1e-20)

for phrase in speech:
    print(phrase.segments(detailed=True))