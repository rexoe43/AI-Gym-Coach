# AI Gym Coach 🏋️‍♂️🤖

### Intelligent Exercise Analysis & Virtual Coaching System

**AI Gym Coach** is an intelligent desktop application designed to analyze
exercise technique using **Computer Vision, Machine Learning, and Large
Language Models (LLMs)**.

The system uses a camera to detect the user's body pose, extract movement
features, identify exercise patterns, count repetitions, detect predefined
technique errors, and provide understandable feedback through an AI-powered
assistant.

---

## ✨ Why AI Gym Coach? (Key Features)

### 🧠 AI-Powered Exercise Analysis

AI Gym Coach analyzes exercise movements using Computer Vision and a
Machine Learning model trained with data extracted from human movement.

The system is designed to identify patterns such as:

Correct execution
Incomplete range of motion
Incorrect posture
Other exercise-specific movement errors

## 🎥 Real-Time Pose Detection

The application uses the device camera to analyze the user's movement.

MediaPipe Pose extracts body landmarks that can be used to calculate:

Joint angles
Relative positions
Distances between joints
Movement trajectory
Velocity
Temporal characteristics

The detected pose can also be displayed directly over the camera feed.

## 🔢 Intelligent Rep Counter

Instead of relying on a simple timer, AI Gym Coach analyzes the different
phases of an exercise to determine when a repetition has actually been
completed.
The movement logic can be adapted to each supported exercise.

## 🏋️ Initial Exercise Program

The first version of the system will use a simple PPL structure:

PUSH

Push-ups

PULL

Bicep Curls

LEGS

Squats

The architecture is designed so additional exercises can be added without
rewriting the entire system.

## 📊 Machine Learning Model

The Machine Learning model will be trained using a custom dataset generated
from exercise movements.

The dataset will not initially use raw RGB images as the primary training
data.
Potential features include:

Joint angles
Normalized coordinates
Joint distances
Movement velocity
Displacement
Trajectory
Movement duration
Temporal features

The final features and model will be determined experimentally.

## 🧪 Model Evaluation

Different Machine Learning approaches can be evaluated, including:

Random Forest
Support Vector Machine (SVM)
XGBoost
Neural Networks

Models will be compared using real evaluation results.

Main metrics:

Accuracy
Precision
Recall
F1-Score
Confusion Matrix

No performance values will be reported until the models have actually been
trained and evaluated.

## 🤖 AI Feedback with Llama 3.2

The system integrates Llama 3.2 through Ollama as an additional AI
layer for explanation and feedback.

The Machine Learning model determines the technical result.

For example:

<img width="294" height="249" alt="image" src="https://github.com/user-attachments/assets/f6cfd07c-4d48-4dda-b19e-f3abf2426ad0" />


Llama 3.2 can then transform this information into understandable feedback.

The LLM does not replace the Machine Learning model and does not
directly determine whether an exercise was correctly performed.

## 🖥️ Desktop Application

AI Gym Coach will be distributed as a desktop application using Tauri.

The user interface is built with modern web technologies while remaining
responsive across:

Desktop
Laptop
Tablet
Mobile-sized screens

The primary target is desktop usage.

## 🎨 Modern & Responsive Design

The interface will use:

React
TypeScript
Tailwind CSS
Vite

The design will focus on:

Clear exercise visualization
Real-time training information
Technique feedback
Rep tracking
Simple navigation
Responsive layouts
Modern dashboard

## 🚀 Technical Stack

Built with a hybrid architecture combining modern web development,
Python-based AI processing, Computer Vision, and local LLM inference.

| **Component**        | **Technology**         | **Description**                             |
| -------------------- | ---------------------- | ------------------------------------------- |
| **Frontend**         | **React + TypeScript** | User interface and application logic        |
| **Styling**          | **Tailwind CSS**       | Responsive UI and component styling         |
| **Build Tool**       | **Vite**               | Frontend development and build system       |
| **Desktop**          | **Tauri**              | Desktop application packaging               |
| **Backend**          | **Python + FastAPI**   | API and AI processing layer                 |
| **Computer Vision**  | **OpenCV**             | Video and frame processing                  |
| **Pose Detection**   | **MediaPipe Pose**     | Human pose and landmark detection           |
| **Machine Learning** | **TensorFlow / Keras** | Model training and inference                |
| **Data Processing**  | **NumPy + Pandas**     | Dataset processing and numerical operations |
| **ML Evaluation**    | **scikit-learn**       | Evaluation and preprocessing                |
| **LLM**              | **Llama 3.2**          | AI-generated explanations and feedback      |
| **LLM Runtime**      | **Ollama**             | Local LLM execution                         |
| **Database**         | **SQLite (Optional)**  | Training history and statistics             |

## 🏗️ System Architecture

                                       AI GYM COACH
                                            │
                                            ▼
                               ┌────────────────────────┐
                               │ React + TypeScript     │
                               │ Tailwind CSS + Vite    │
                               └────────────┬───────────┘
                                            │
                                            ▼
                                     ┌────────────┐
                                     │   Tauri    │
                                     └─────┬──────┘
                                           │
                                           ▼
                                  ┌─────────────────┐
                                  │     FastAPI     │
                                  │     Python      │
                                  └────────┬────────┘
                                           │
                           ┌───────────────┼────────────────┐
                           │               │                │
                           ▼               ▼                ▼
                      ┌─────────┐    ┌───────────┐    ┌──────────┐
                      │  OpenCV │    │ MediaPipe │    │ TensorFlow│
                      └────┬────┘    └─────┬─────┘    └────┬─────┘
                           │               │               │
                           └───────────────┼───────────────┘
                                           ▼
                                  ┌─────────────────┐
                                  │ Feature         │
                                  │ Extraction      │
                                  └────────┬────────┘
                                           ▼
                                  ┌─────────────────┐
                                  │  ML Model       │
                                  └────────┬────────┘
                                           │
                                  ┌────────┴────────┐
                                  ▼                 ▼
                             Rep Counter       Technique
                                                    │
                                                    ▼
                                             Error Detection
                                                    │
                                                    ▼
                                            Structured Results
                                                    │
                                                    ▼
                                         ┌──────────────────┐
                                         │ Llama 3.2        │
                                         │ + Ollama         │
                                         └────────┬─────────┘
                                                  │
                                                  ▼
                                            AI Feedback
                                                  │
                                                  ▼
                                         React Interface
                                         
                           
## 🔄 AI Training Pipeline
The Machine Learning development process follows this pipeline: 

                                      ┌───────────────────┐
                                      │ Exercise Videos   │
                                      └─────────┬─────────┘
                                                ↓
                                      ┌───────────────────┐
                                      │ OpenCV Processing │
                                      └─────────┬─────────┘
                                                ↓
                                      ┌───────────────────┐
                                      │ MediaPipe Pose    │
                                      └─────────┬─────────┘
                                                ↓
                                      ┌───────────────────┐
                                      │ Body Landmarks    │
                                      └─────────┬─────────┘
                                                ↓
                                      ┌───────────────────┐
                                      │ Feature Extraction│
                                      └─────────┬─────────┘
                                                ↓
                                      ┌───────────────────┐
                                      │ Labeled Dataset   │
                                      └─────────┬─────────┘
                                                ↓
                                      ┌───────────────────┐
                                      │ Train / Validation│
                                      │ / Test            │
                                      └─────────┬─────────┘
                                                ↓
                                      ┌───────────────────┐
                                      │ Model Training    │
                                      └─────────┬─────────┘
                                                ↓
                                      ┌───────────────────┐
                                      │ Model Evaluation  │
                                      └─────────┬─────────┘
                                                ↓
                                      ┌───────────────────┐
                                      │ Selected Model    │
                                      └─────────┬─────────┘
                                                ↓
                                      ┌───────────────────┐
                                      │ Production Model  │
                                      └───────────────────┘

Data leakage must be avoided during dataset splitting. Data from the same
recording or person should not be distributed in a way that allows the
model to simply memorize the subject.

## 📂 Project Structure

                  AI-Gym-Coach/
                  │
                  ├── frontend/                  # React application
                  │   ├── src/
                  │   │   ├── components/        # Reusable UI components
                  │   │   ├── pages/             # Application pages
                  │   │   ├── services/          # API communication
                  │   │   ├── hooks/             # Custom React hooks
                  │   │   └── types/             # TypeScript types
                  │   ├── package.json
                  │   └── vite.config.ts
                  │
                  ├── backend/                   # Python backend
                  │   ├── app/
                  │   │   ├── api/               # API routes
                  │   │   ├── services/          # Business logic
                  │   │   ├── computer_vision/   # OpenCV / MediaPipe
                  │   │   ├── ml/                # ML inference
                  │   │   └── llm/               # Ollama integration
                  │   └── requirements.txt
                  │
                  ├── ai/                        # Machine Learning pipeline
                  │   ├── dataset/               # Dataset and metadata
                  │   ├── preprocessing/         # Data preprocessing
                  │   ├── features/              # Feature extraction
                  │   ├── training/              # Model training
                  │   ├── evaluation/            # Model evaluation
                  │   └── models/                # Trained models
                  │
                  ├── desktop/                   # Tauri configuration
                  │   └── tauri/
                  │
                  ├── docs/                      # Project documentation
                  │
                  ├── .gitignore
                  ├── README.md
                  └── LICENSE


## 🛠️ Installation & Setup
Prerequisites

Make sure the following tools are installed:

    Python 3.x
    Node.js
    npm
    Rust
    Tauri
    Ollama
    Git

1. Clone the repository

        git clone <repository_url>
        cd AI-Gym-Coach
2. Backend Setup

Create a Python virtual environment:

    python -m venv .venv

Activate it:

Windows:

    .venv\Scripts\activate

Linux / macOS:

    source .venv/bin/activate

Install dependencies:

    pip install -r backend/requirements.txt

Run the FastAPI server:

    uvicorn backend.app.main:app --reload

3. Frontend Setup
   
        cd frontend
        npm install
        npm run dev
   
5. Ollama Setup

Install Ollama and download the configured LLM:

    ollama pull llama3.2

Start Ollama:

    ollama serve

5. Desktop Application

Once the frontend and backend are configured:

    npm run tauri dev

The exact commands may change as the project structure evolves.

## ⚠️ Limitations

AI Gym Coach is an academic project and is not intended to replace a
professional personal trainer or provide medical advice.

The accuracy of the system may depend on:

Camera position
Lighting conditions
Visibility of the body
Clothing
Camera quality
Dataset size
Dataset diversity
Exercise complexity

These limitations will be evaluated during development.

## 🔒 Privacy

The project is designed with local processing in mind.

Whenever possible:

Video processing should occur locally.
LLM inference should occur locally through Ollama.
Personal videos should not be uploaded to external services.
Sensitive credentials must never be committed to Git.

Environment variables and secrets should be stored outside version
control.

## 📌 Project Status

🚧 Currently in development

The repository currently represents the planned architecture and development
roadmap. Model performance metrics and final implementation details will be
added after the corresponding components have been implemented and tested.
