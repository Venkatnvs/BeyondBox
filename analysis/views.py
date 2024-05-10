from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os
import subprocess
import speech_recognition as sr
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import pos_tag
from nltk.corpus import wordnet
import json
import cv2
import numpy as np

def index(request):
    return render(request, 'analysis/AV/index.html')

@csrf_exempt
def upload(request):
    if request.method == 'POST':
        video_file = request.FILES.get('video')
        # Ensure the uploads directory exists
        uploads_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        os.makedirs(uploads_dir, exist_ok=True)

        # Save the video file
        video_path = os.path.join(uploads_dir, video_file.name)
        with open(video_path, 'wb') as f:
            for chunk in video_file.chunks():
                f.write(chunk)
        
        confidence_level, expression_counts = analyze_video(video_path)
        # Transcribe audio from the video using ffmpeg
        # audio_path = os.path.join(uploads_dir, 'audio.wav')
        # subprocess.run(['ffmpeg', '-i', video_path, '-vn', audio_path])

        # # Perform text analysis on transcribed audio (replace this with your actual analysis logic)
        # transcription = recognize_speech(audio_path)

        return JsonResponse({'message': 'Video uploaded successfully.', 'confidence_level': confidence_level, 'expression_counts': expression_counts})

    return JsonResponse({'error': 'Invalid request'})

def recognize_speech(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source) 
    try:
        transcription = recognizer.recognize_google(audio_data)
        return transcription
    except sr.UnknownValueError:
        return "Speech could not be recognized"
    except sr.RequestError as e:
        return f"Error occurred during recognition: {e}"
    finally:
        # os.remove(audio_path)
        pass

@csrf_exempt
def AudioAnalysis(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'})
        transcription = str(data.get('transcript'))
        print(transcription)
        word_tokens = word_tokenize(transcription)
        sentence_tokens = sent_tokenize(transcription)
        pos_tags = pos_tag(word_tokens)

        # Calculate average sentence length
        avg_sentence_length = sum(len(sent.split()) for sent in sentence_tokens) / len(sentence_tokens)
        pause_count = transcription.count(' ')

        # Calculate average word length
        avg_word_length = sum(len(word) for word in word_tokens) / len(word_tokens)
        total_words = sum(len(sentence.split()) for sentence in sentence_tokens)
        avg_words_per_sentence = total_words / len(sentence_tokens)

        fluency_score = max(0, 1 - (pause_count / total_words) - (avg_words_per_sentence / 20))

        # Perform grammar analysis
        grammar_errors = []

        # Check for subject-verb agreement errors
        for (word, tag) in pos_tags:
            if 'VB' in tag:  # Verbs
                synsets = wordnet.synsets(word)
                if not any('VB' in synset.pos() for synset in synsets):
                    grammar_errors.append(f"Possible subject-verb agreement error: {word}")

        # Return the analysis result
        analysis_result = {
            'transcription': transcription,
            'avg_sentence_length': avg_sentence_length,
            'avg_word_length': avg_word_length,
            'grammar_errors': grammar_errors,
            'fluency_score': fluency_score
        }

        return JsonResponse(analysis_result)

def analyze_video(video_path):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    expression_counts = {'Neutral': 0, 'Happy': 0, 'Sad': 0, 'Angry': 0, 'Surprise': 0, 'Fear': 0, 'Disgust': 0}
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # Draw bounding boxes around detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Extract region of interest (ROI) for facial expression analysis
            roi_gray = gray[y:y+h, x:x+w]

            # Perform facial expression analysis on roi_gray (pixel intensity analysis)
            detected_expression = analyze_expression(roi_gray)

            # Update expression counts based on the detected expression
            if detected_expression:
                expression_counts[detected_expression] += 1

        # Increment frame count
        frame_count += 1

    cap.release()

    # Calculate confidence level based on facial expressions
    total_expressions = sum(expression_counts.values())
    confidence_level = total_expressions / total_frames

    return abs(confidence_level), expression_counts

def analyze_expression(roi_gray):
    # Calculate average pixel intensity within the ROI
    average_intensity = np.mean(roi_gray)

    # Define thresholds for different facial expressions based on pixel intensity
    thresholds = { 'Happy': 140, 'Surprise': 130, 'Neutral': 110, 'Angry': 100, 'Sad': 80, 'Fear': 75, 'Disgust': 60}

    # Determine the expression based on the average intensity compared to the thresholds
    detected_expression = None
    min_difference = float('inf')  # Initialize with a large value
    for expression, threshold in thresholds.items():
        difference = abs(average_intensity - threshold)
        if difference < min_difference:
            min_difference = difference
            detected_expression = expression

    if detected_expression is None:
        detected_expression = 'Neutral'

    return detected_expression


def FaceRecognition(request):
    return render(request, 'analysis/AV/FaceRecognition.html')