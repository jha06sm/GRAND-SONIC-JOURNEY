import io, numpy as np, wave, random

def _tone(freq, dur, sr=22050, amp=0.12):
    t = np.linspace(0, dur, int(sr*dur), endpoint=False)
    return (amp * np.sin(2*np.pi*freq*t)).astype(np.float32)

def _env(y, sr=22050, a=0.01, r=0.05):
    n = y.size; env = np.ones(n, dtype=np.float32)
    na = int(sr*a); nr = int(sr*r)
    if na>0: env[:na] = np.linspace(0,1,na,endpoint=False)
    if nr>0: env[-nr:] = np.linspace(1,0,nr,endpoint=False)
    return y * env

def _render(y, sr=22050):
    y = np.clip(y, -1.0, 1.0)
    pcm = (y * 32767.0).astype(np.int16)
    bio = io.BytesIO()
    with wave.open(bio, 'wb') as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr); wf.writeframes(pcm.tobytes())
    bio.seek(0); return bio.read()

def _scale(root, intervals):
    return [root * 2**(i/12) for i in intervals]

# Root note frequencies
ROOTS = {
    "C": 261.63, "C#": 277.18, "D": 293.66, "D#": 311.13,
    "E": 329.63, "F": 349.23, "F#": 369.99, "G": 392.00,
    "G#": 415.30, "A": 440.00, "A#": 466.16, "B": 493.88
}

# Intervals
MAJOR = [0,2,4,5,7,9,11]
NAT_MINOR = [0,2,3,5,7,8,10]
HARM_MINOR = [0,2,3,5,7,8,11]
MEL_MINOR = [0,2,3,5,7,9,11]

# All 72 scales
SCALES = {}
for root in ROOTS:
    SCALES[f"{root}"] = _scale(ROOTS[root], MAJOR)
    SCALES[f"{root} major"] = _scale(ROOTS[root], MAJOR)
    SCALES[f"{root} minor"] = _scale(ROOTS[root], NAT_MINOR)
    SCALES[f"{root} natural minor"] = _scale(ROOTS[root], NAT_MINOR)
    SCALES[f"{root} harmonic minor"] = _scale(ROOTS[root], HARM_MINOR)
    SCALES[f"{root} melodic minor"] = _scale(ROOTS[root], MEL_MINOR)

def compose_song_wav(key='C', bpm=100, bars=8, sr=22050):
    scale = SCALES.get(key, SCALES['C'])
    beat_period = 60.0 / bpm
    total = int(sr * bars * 4 * beat_period)
    y = np.zeros(total, dtype=np.float32)
    
    chord_prog = [0, 4, 5, 3]
    for i in range(int((bars*4)/2)):
        root = scale[chord_prog[i % len(chord_prog)]]
        chord = [root, root * 2*(4/12), root * 2*(7/12)]
        start = int(sr * i * 2 * beat_period)
        c = sum(_tone(f, 2*beat_period, sr, 0.06) for f in chord)
        c = _env(c, sr, 0.01, 0.02)
        y[start:start+len(c)] += c[:max(0, min(len(c), len(y)-start))]
    
    for q in range(bars*4):
        f = random.choice(scale)
        start = int(sr * q * beat_period)
        m = _env(_tone(f*2, beat_period*0.85, sr, 0.10), sr, 0.005, 0.03)
        y[start:start+len(m)] += m[:max(0, min(len(m), len(y)-start))]
    
    click = lambda d=0.03: (np.random.uniform(-1,1,int(sr*d)) * np.exp(-np.linspace(0, d, int(sr*d))*80.0)).astype(np.float32) * 0.6
    for b in range(bars*2):
        t0 = int(sr * (b * (beat_period/2.0)))
        y[t0:t0+len(click())] += click()
    
    y = np.tanh(1.8 * y)
    return _render(y, sr)

def generate_final_track(lyrics, genre, instruments):
    """
    Wrapper function for Streamlit.
    Currently ignores lyrics & instruments (for testing),
    uses compose_song_wav to generate audio based on scale.
    Returns path to generated wav file.
    """
    import os

    # Map genre or key to musical scale (example)
    key = 'C'  # default
    if genre.lower() == 'g':
        key = 'G'
    elif genre.lower() == 'a minor':
        key = 'A minor'
    elif genre.lower() == 'f':
        key = 'F'

    # Generate raw audio bytes
    audio_bytes = compose_song_wav(key=key)

    # Save to a temp wav file
    output_file = os.path.join(os.path.dirname(__file__), "generated_output.wav")
    with open(output_file, "wb") as f:
        f.write(audio_bytes)
    
    return output_file