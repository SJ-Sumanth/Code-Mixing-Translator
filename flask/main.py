import os
import gtts
import pytesseract
import speech_recognition as s_r
from PIL import Image
from flask import Flask, render_template, request, redirect
from googletrans import Translator
from langdetect import detect
from playsound import playsound
from deep_translator import GoogleTranslator

app = Flask(__name__)


@app.route('/')
def homes():
    return render_template("home.html")


# image to translate
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


path = os.getcwd()
UPLOAD_FOLDER = os.path.join(path, 'G:/Projects/Code-Mixing Translator/flask/uploads/')
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def ocr_core(filename):
    pytesseract.pytesseract.tesseract_cmd = 'C:/Tesseract-OCR/tesseract.exe'
    text = pytesseract.image_to_string(Image.open(filename))
    return text


@app.route('/image', methods=['GET', 'POST'])
def upload_page():
    global translation
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('uploaded.html', msg='No file selected')
        file = request.files['file']
        if file.filename == '':
            return render_template('uploaded.html', msg='No file')
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            text3 = ocr_core(file)
            if detect(text3) == 'te':
                translation = GoogleTranslator(source='te', target='en').translate(text3)
                translation1 = GoogleTranslator(source='en', target='hi').translate(translation)
                # translator = Translator()
                # translation = translator.translate(text3, src='te', dest='en')
                # translator1 = Translator()
                # translation1 = translator1.translate(translation.text, src='en', dest='hi')
                tts = gtts.gTTS(translation, lang="te")
                tts.save("G:/Projects/Code-Mixing Translator/flask/my-translation.mp3")
                playsound("G:/Projects/Code-Mixing Translator/flask/my-translation.mp3")
                # os.remove("G:/Projects/Code-Mixing Translator/flask/my-translation.mp3")
            elif detect(text3) != 'te':
                translation = GoogleTranslator(source='en', target='te').translate(text3)
                translation1 = GoogleTranslator(source='te', target='hi').translate(translation)

                # translator = Translator()
                # translation = translator.translate(text3, src='en', dest='te')
                # translator1 = Translator()
                # translation1 = translator1.translate(translation.text, src='te', dest='hi')
                tts = gtts.gTTS(translation, lang="te")
                tts.save("G:/Projects/Code-Mixing Translator/flask/my-translation.mp3")
                playsound("G:/Code-Mixing Translator/flask/my-translation.mp3")
                os.remove("G:/Projects/Code-Mixing Translator/flask/my-translation.mp3")
            else:
                translation1 = "ERROR TRY AGAIN"
            return render_template('uploaded.html', msg='CODE-MIXING TRANSLATOR',
                                   extracted=translation1,
                                   extracted1=translation,
                                   img_src=file.filename)
    else:
        return render_template('upload.html')


@app.route('/uploads/<filename>')
def send_uploaded_file(filename=''):
    from flask import send_from_directory
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# wav file to translate
@app.route("/file", methods=["GET", "POST"])
def index():
    translation = ""
    translation1 = ""
    if request.method == "POST":
        print("FORM DATA RECEIVED")

        if "file" not in request.files:
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)

        if file:
            recognizer = s_r.Recognizer()
            audioFile = s_r.AudioFile(file)
            with audioFile as source:
                data = recognizer.record(source)
            text2 = str(recognizer.recognize_google(data, key=None))
            if detect(text2) == 'te':
                translation = GoogleTranslator(source='te', target='en').translate(text2)
                translation1 = GoogleTranslator(source='en', target='hi').translate(translation)
                # translator = Translator()
                # translation = translator.translate(text2, src='te', dest='en')
                # translator1 = Translator()
                # translation1 = translator1.translate(translation.text, src='en', dest='hi')
                # translation1 = translation1.text
                # translation = translation.text
                # tts = gtts.gTTS(translation1.text, lang="hi")
                # tts.save("my-translation.mp3")
                # playsound("my-translation.mp3")
                # os.remove("my-translation.mp3")
            elif detect(text2) != 'te':
                translation = GoogleTranslator(source='en', target='te').translate(text2)
                translation1 = GoogleTranslator(source='te', target='hi').translate(translation)
                # translator = Translator()
                # translation = translator.translate(text2, src='en', dest='te')
                # translator1 = Translator()
                # translation1 = translator1.translate(translation.text, src='te', dest='hi')
                # translation1 = translation1.text
                # translation = translation.text
                # tts = gtts.gTTS(translation1.text, lang="hi")
                # tts.save("my-translation.mp3")
                # playsound("my-translation.mp3")
                # os.remove("my-translation.mp3")
            else:
                translation1 = "ERROR TRY AGAIN"

    return render_template('audio.html', transcript=translation1, transcript1=translation)


# audio to translate

@app.route('/audio')
def index1():
    return render_template('file.html')


@app.route('/result', methods=['POST', 'GET'])
def result():
    global translation1, translation
    if request.method == 'POST':
        text1 = str(request.form.getlist('Name'))
        text1 = text1.replace('[', '')
        text1 = text1.replace(']', '')
        if detect(text1) == 'te':
            translation = GoogleTranslator(source='te', target='en').translate(text1)
            translation1 = GoogleTranslator(source='en', target='hi').translate(translation)
            # translator = Translator()
            # translation = translator.translate(text1, src='te', dest='en')
            # translator1 = Translator()
            # translation1 = translator1.translate(translation.text, src='en', dest='hi')
            # tts = gtts.gTTS(translation.text, lang="te")
            # tts.save("my-translation.mp3")
            # playsound("my-translation.mp3")
            # os.remove("my-translation.mp3")
        elif detect(text1) != 'te':
            translation = GoogleTranslator(source='en', target='te').translate(text1)
            translation1 = GoogleTranslator(source='te', target='hi').translate(translation)
            # translator = Translator()
            # translation = translator.translate(text1, src='en', dest='te')
            # translator1 = Translator()
            # translation1 = translator1.translate(translation.text, src='te', dest='hi')
            # tts = gtts.gTTS(translation.text, lang="en")
            # tts.save("my-translation.mp3")
            # playsound("my-translation.mp3")
            # os.remove("my-translation.mp3")
        else:
            translation1 = "ERROR TRY AGAIN"
    return render_template("result.html", result=translation1, result1=translation)

# text to translate

@app.route("/text")
def customer():
    return render_template('text.html')


@app.route('/success', methods=['POST', 'GET'])
def home():
    global translation1, translation
    translator = Translator()
    if request.method == 'POST':
        text = str(request.form.getlist("name"))
        text = text.replace('[', '')
        text = text.replace(']', '')
        if detect(str(text)) == 'te':
            translation = GoogleTranslator(source='te', target='en').translate(text)
            translation1 = GoogleTranslator(source='en', target='hi').translate(translation)
            # nltk_tokens = nltk.sent_tokenize(translation)
            # nltk_tokens = nltk.sent_tokenize(translation1)
            tts = gtts.gTTS(translation1, lang="en")
            tts.save("G:/Projects/Code-Mixing Translator/flask/my-translation.mp3")
            playsound("G:/Projects/Code-Mixing Translator/flask/my-translation.mp3")
            os.remove("G:/Projects/Code-Mixing Translator/flask/my-translation.mp3")
        elif detect(str(text)) != 'te':
            translation = GoogleTranslator(source='en', target='te').translate(text)
            translation1 = GoogleTranslator(source='te', target='hi').translate(translation)
            # translator = Translator()
            # translation = translator.translate(str(text), src='en', dest='te')
            # translator1 = Translator()
            # translation1 = translator1.translate(translation.text, src='te', dest='hi')
            tts = gtts.gTTS(translation1, lang="en")
            tts.save("G:/Projects/Code-Mixing Translator/flask/my-translation2.mp3")
            playsound("G:/Projects/Code-Mixing Translator/flask/my-translation2.mp3")
            os.remove("G:/Projects/Code-Mixing Translator/flask/my-translation2.mp3")
        else:
            translation1 = "ERROR TRY AGAIN"
    return render_template("result_data.html", result=translation1, result1=translation)


if __name__ == '__main__':
    app.run(debug=True)