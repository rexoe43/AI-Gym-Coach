# AI Gym Coach 🏋️‍♂️🤖

### Intelligent Exercise Analysis & Virtual Coaching System

**AI Gym Coach** is an intelligent application designed to analyze exercise technique using **Computer Vision, Machine Learning, and Large Language Models (LLMs)**.

The system uses a camera to detect the user's body pose, extract movement features, identify exercise patterns, count repetitions, detect predefined technique errors, and provide understandable feedback through an AI-powered assistant.

---

## ✨ Why AI Gym Coach? (Key Features)

### 🧠 AI-Powered Exercise Analysis

AI Gym Coach analyzes exercise movements using Computer Vision and a Machine Learning model trained with data extracted from human movement.

The system is designed to identify patterns such as:

- Correct execution
- Incomplete range of motion
- Incorrect posture
- Other exercise-specific movement errors

## 🎥 Real-Time Pose Detection

The application uses the device camera to analyze the user's movement via MediaPipe Pose, which extracts body landmarks that can be used to calculate:

- Joint angles
- Relative positions
- Distances between joints
- Movement trajectory
- Velocity
- Temporal characteristics

The detected pose can also be displayed directly over the camera feed.

## 🔢 Intelligent Rep Counter

Instead of relying on a simple timer, AI Gym Coach analyzes the different phases of an exercise to determine when a repetition has actually been completed.
The movement logic can be adapted to each supported exercise.

## 🏋️ Initial Exercise Program

The first version of the system will use a simple PL structure:

- **PUSH** - Push-ups
- **LEGS** - Squats

The architecture is designed so additional exercises can be added without rewriting the entire system.

## 📊 Machine Learning Model

The Machine Learning model will be trained using a custom dataset generated from exercise movements.

The dataset will not initially use raw RGB images as the primary training data.
Potential features include:

- Joint angles
- Normalized coordinates
- Joint distances
- Movement velocity
- Displacement
- Trajectory
- Movement duration
- Temporal features

The final features and model will be determined experimentally.

## 🧪 Model Evaluation

Different Machine Learning approaches can be evaluated, including:

- Random Forest
- Support Vector Machine (SVM)
- XGBoost
- Neural Networks

Models will be compared using real evaluation results.

Main metrics:

- Accuracy
- Precision
- Recall
- F1-Score
- Confusion Matrix

No performance values will be reported until the models have actually been trained and evaluated.

## 🤖 AI Feedback with LLM Integration

The system integrates an LLM as an additional AI layer for explanation and feedback.

The Machine Learning model determines the technical result. The LLM can then transform this information into understandable, personalized feedback.

The LLM does not replace the Machine Learning model and does not directly determine whether an exercise was correctly performed.

## 🖥️ Web Application

AI Gym Coach is built as a modern web application with a responsive interface that works across:

- Desktop
- Laptop
- Tablet
- Mobile-sized screens

## 🎨 Modern & Responsive Design

The interface uses:

- **React 18** with TypeScript
- **Tailwind CSS** for styling
- **Vite** for build tooling
- **Axios** for HTTP requests
- **React Webcam** for camera access

The design focuses on:

- Clear exercise visualization
- Real-time training information
- Technique feedback
- Rep tracking
- Simple navigation
- Responsive layouts
- Modern dashboard

## 🚀 Technical Stack

Built with a hybrid architecture combining modern web development, Python-based AI processing, and Computer Vision.

| **Component**        | **Technology**         | **Description**                             |
| -------------------- | ---------------------- | ------------------------------------------- |
| **Frontend**         | **React 18 + TypeScript** | User interface and application logic        |
| **Styling**          | **Tailwind CSS**       | Responsive UI and component styling         |
| **Build Tool**       | **Vite**               | Frontend development and build system       |
| **HTTP Client**      | **Axios**              | API communication                           |
| **Camera Access**    | **React Webcam**       | Real-time video streaming from device camera |
| **Backend**          | **Python + FastAPI**   | API and AI processing layer                 |
| **Real-time Communication** | **WebSockets**   | Live data streaming between frontend and backend |
| **Computer Vision**  | **OpenCV**             | Video and frame processing                  |
| **Pose Detection**   | **MediaPipe Pose**     | Human pose and landmark detection           |
| **Machine Learning** | **TensorFlow / Keras** | Model training and inference                |
| **Data Processing**  | **NumPy + Pandas**     | Dataset processing and numerical operations |
| **ML Evaluation**    | **scikit-learn**       | Evaluation and preprocessing                |
| **Optimization**     | **XGBoost**            | Advanced model training                     |
| **LLM Integration**  | **Python requests**    | API-based LLM communication                 |

## 🏗️ System Architecture

```
                                   AI GYM COACH
                                        │
                                        ▼
                          ┌─────────────────────────┐
                          │  React + TypeScript UI  │
                          │  Tailwind CSS + Vite    │
                          └────────────┬────────────┘
                                       │
                                       ▼
                               ┌──────────────────┐
                               │   WebSockets     │
                               └────────┬─────────┘
                                        │
                                        ▼
                               ┌──────────────────┐
                               │   FastAPI        │
                               │   Python         │
                               └────────┬─────────┘
                                        │
                        ┌───────────────┼────────────────┐
                        │               │                │
                        ▼               ▼                ▼
                   ┌─────────┐    ┌───────────┐    ┌──────────┐
                   │ OpenCV  │    │ MediaPipe │    │TensorFlow│
                   └────┬────┘    └─────┬─────┘    └────┬─────┘
                        │               │               │
                        └───────────────┼───────────────┘
                                        ▼
                               ┌──────────────────┐
                               │ Feature          │
                               │ Extraction       │
                               └────────┬─────────┘
                                        ▼
                               ┌──────────────────┐
                               │  ML Model        │
                               └────────┬─────────┘
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
                                        │ LLM Processing   │
                                        └────────┬─────────┘
                                                 │
                                                 ▼
                                           AI Feedback
                                                 │
                                                 ▼
                                        React Interface
```

## 🔄 AI Training Pipeline

The Machine Learning development process follows this pipeline:

```
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
                                   │ / Test Split      │
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
```

Data leakage must be avoided during dataset splitting. Data from the same recording or person should not be distributed in a way that allows the model to simply memorize the subject.

## 📂 Project Structure

```
AI-Gym-Coach/
│
├── Frontend/                      # React web application
│   ├── src/
│   │   ├── components/            # Reusable UI components
│   │   ├── pages/                 # Application pages
│   │   ├── hooks/                 # Custom React hooks
│   │   ├── App.jsx                # Main application component
│   │   ├── main.jsx               # Entry point
│   │   └── index.css              # Global styles
│   ├── index.html                 # HTML entry point
│   ├── package.json               # Frontend dependencies
│   ├── vite.config.js             # Vite configuration
│   ├── tailwind.config.js         # Tailwind CSS configuration
│   └── postcss.config.js          # PostCSS configuration
│
├── Backend/                       # Python FastAPI backend
│   ├── app/
│   │   ├── main.py                # FastAPI application entry point
│   │   ├── websocket_manager.py   # WebSocket connection management
│   │   ├── pose_detector.py       # MediaPipe pose detection
│   │   ├── feature_extractor.py   # Feature extraction from pose data
│   │   ├── model_loader.py        # ML model loading and management
│   │   ├── predictor.py           # Model prediction logic
│   │   ├── repetition_counter.py  # Exercise rep counting
│   │   └── services/              # Business logic services
│   ├── models/                    # Pre-trained model storage
│   ├── .env                       # Environment variables
│   └── requirements.txt           # Backend dependencies
│
├── ai/                            # Machine Learning pipeline & utilities
│   ├── dataset/                   # Training datasets and metadata
│   ├── preprocessing/             # Data preprocessing scripts
│   ├── features/                  # Feature extraction utilities
│   ├── training/                  # Model training scripts
│   ├── models/                    # Trained model files
│   └── requirements.txt           # ML pipeline dependencies
│
├── docs/                          # Project documentation
│
├── .gitignore
├── README.md
└── LICENSE
```

### Directory Descriptions

**Frontend/**
- Contains the React web application
- Handles user interface and real-time camera feed visualization
- Communicates with backend via REST API and WebSockets
- Styling with Tailwind CSS, built with Vite

**Backend/app/**
- `main.py` - FastAPI server setup and route definitions
- `websocket_manager.py` - Manages WebSocket connections for real-time data streaming
- `pose_detector.py` - Integrates MediaPipe to detect body landmarks
- `feature_extractor.py` - Calculates joint angles and features from pose data
- `model_loader.py` - Loads and manages TensorFlow/Keras models
- `predictor.py` - Makes predictions using loaded models
- `repetition_counter.py` - Tracks and counts exercise repetitions based on movement phases
- `services/` - Modular business logic for specific features

**Backend/models/**
- Stores pre-trained ML models for inference during application runtime

**ai/**
- `dataset/` - Raw and processed training data
- `preprocessing/` - Scripts for data cleaning and normalization
- `features/` - Feature engineering and extraction utilities
- `training/` - Model training pipelines and experiment tracking
- `models/` - Generated trained models after training pipeline completion

## 🛠️ Installation & Setup

### Prerequisites

Make sure the following tools are installed:

- Python 3.8+
- Node.js 16+
- npm or yarn
- Git

### 1. Clone the repository

```bash
git clone https://github.com/rexoe43/AI-Gym-Coach.git
cd AI-Gym-Coach
```

### 2. Backend Setup

Create and activate a Python virtual environment:

```bash
python -m venv .venv

# On Windows:
.venv\Scripts\activate

# On Linux/macOS:
source .venv/bin/activate
```

Install Python dependencies:

```bash
pip install -r Backend/requirements.txt
```

Start the FastAPI server:

```bash
uvicorn Backend.app.main:app --reload
```

The backend will be available at `http://localhost:8000`

### 3. Frontend Setup

Install Node.js dependencies:

```bash
cd Frontend
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will typically be available at `http://localhost:5173`

### 4. ML Pipeline Setup (Optional for training)

If you want to work with model training:

```bash
pip install -r ai/requirements.txt
```

## ⚠️ Limitations

AI Gym Coach is an academic project and is not intended to replace a professional personal trainer or provide medical advice.

The accuracy of the system may depend on:

- Camera position and angle
- Lighting conditions
- Visibility of the body
- Clothing and obstructions
- Camera quality and resolution
- Dataset size and diversity
- Exercise complexity
- User body type variations

These limitations will be evaluated during development.

## 🔒 Privacy

The project is designed with local processing in mind.

Whenever possible:

- Video processing occurs locally on the user's device
- LLM inference is handled through external API calls
- Personal videos are not uploaded to external services
- Sensitive credentials must never be committed to Git

Environment variables and secrets should be stored in `.env` files outside version control.

## 📌 Project Status

✅ **Project Complete & Deployed**

The AI Gym Coach application is fully functional and has been successfully tested and deployed. 
All core features are implemented and working as intended.
### Development Roadmap

- [x] Initial project structure setup
- [x] Frontend React application scaffold
- [x] FastAPI backend with WebSocket support
- [x] MediaPipe pose detection integration
- [x] Feature extraction pipeline
- [x] ML model training and evaluation
- [x] Exercise rep counter refinement
- [x] Technique error detection
- [x] LLM feedback integration
- [x] Production deployment

---

**Last Updated:** September 2026  
**License:** MIT
