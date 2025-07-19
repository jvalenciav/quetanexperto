import streamlit as st
import json
import os
from datetime import datetime
from quiz_data import QUIZ_DATA

# Configuración de la página
st.set_page_config(
    page_title="¿Qué tan experto eres?",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizado para mejorar el diseño
st.markdown("""
<style>
    /* Ocultar elementos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Estilo del título principal */
    .main-title {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Estilo del subtítulo */
    .subtitle {
        text-align: center;
        font-size: 1.3rem;
        color: #666;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    /* Estilo para el saludo personalizado */
    .welcome-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    
    .welcome-message h2 {
        margin: 0;
        font-size: 1.8rem;
        font-weight: 600;
    }
    
    .welcome-message p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
        font-size: 1.1rem;
    }
    
    /* Cards de quiz mejoradas */
    .quiz-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        margin: 1rem 0;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .quiz-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb, #f5576c);
        background-size: 400% 400%;
        animation: gradient 3s ease infinite;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .quiz-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
    }
    
    .quiz-card.completed {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        border-left: 5px solid #00d4aa;
    }
    
    .quiz-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    
    .quiz-description {
        color: #555;
        font-size: 1rem;
        margin-bottom: 1rem;
        line-height: 1.5;
    }
    
    .quiz-meta {
        display: flex;
        gap: 1rem;
        margin-bottom: 1rem;
        flex-wrap: wrap;
    }
    
    .meta-item {
        background: rgba(255,255,255,0.7);
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        color: #444;
    }
    
    /* Estadísticas mejoradas */
    .stats-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .stats-title {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .stat-item {
        background: rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem;
    }
    
    /* Iconos de dificultad */
    .difficulty-easy { color: #27ae60; }
    .difficulty-medium { color: #f39c12; }
    .difficulty-hard { color: #e74c3c; }
    
    /* Botones mejorados */
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #764ba2, #667eea);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    
    /* Formulario de bienvenida */
    .welcome-form {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin: 2rem 0;
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
    }
    
    .welcome-form h1 {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        font-weight: 700;
    }
    
    .welcome-form p {
        font-size: 1.2rem;
        margin-bottom: 2rem;
        opacity: 0.9;
    }
    
    /* Sidebar de usuario */
    .user-sidebar {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    /* Animaciones */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.6s ease forwards;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main-title { font-size: 2.5rem !important; }
        .quiz-meta { flex-direction: column; }
        .stats-container { padding: 1rem; }
        .welcome-form { padding: 2rem 1rem; }
        .welcome-form h1 { font-size: 2rem; }
    }
</style>
""", unsafe_allow_html=True)

# Archivo para guardar resultados
RESULTS_FILE = "quiz_results.txt"
USERS_FILE = "users.json"

def load_users():
    """Carga la lista de usuarios registrados"""
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_user(username):
    """Guarda un nuevo usuario"""
    users = load_users()
    if username not in users:
        users[username] = {
            "first_login": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "last_login": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_sessions": 1
        }
    else:
        users[username]["last_login"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        users[username]["total_sessions"] = users[username].get("total_sessions", 0) + 1
    
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def load_completed_quizzes(username):
    """Carga los quizzes completados por un usuario específico"""
    completed = set()
    if os.path.exists(RESULTS_FILE):
        try:
            with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line.strip())
                        if data.get('username') == username:
                            completed.add(data['quiz'])
        except:
            pass
    return completed

def save_quiz_result(username, quiz_name, score, total_questions, answers):
    """Guarda el resultado del quiz con el nombre de usuario"""
    result = {
        "username": username,
        "quiz": quiz_name,
        "score": score,
        "total": total_questions,
        "percentage": round((score/total_questions)*100, 2),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "answers": answers
    }
    
    with open(RESULTS_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(result, ensure_ascii=False) + '\n')

def get_user_stats(username):
    """Obtiene estadísticas detalladas del usuario"""
    stats = {
        "total_attempts": 0,
        "total_score": 0,
        "total_questions": 0,
        "best_quiz": None,
        "worst_quiz": None,
        "average_score": 0,
        "quiz_history": []
    }
    
    if os.path.exists(RESULTS_FILE):
        try:
            with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
                user_results = []
                for line in f:
                    if line.strip():
                        data = json.loads(line.strip())
                        if data.get('username') == username:
                            user_results.append(data)
                
                if user_results:
                    stats["total_attempts"] = len(user_results)
                    stats["total_score"] = sum(r["score"] for r in user_results)
                    stats["total_questions"] = sum(r["total"] for r in user_results)
                    stats["average_score"] = round((stats["total_score"] / stats["total_questions"]) * 100, 2)
                    
                    # Mejor y peor quiz
                    best = max(user_results, key=lambda x: x["percentage"])
                    worst = min(user_results, key=lambda x: x["percentage"])
                    stats["best_quiz"] = f"{best['quiz']} ({best['percentage']:.1f}%)"
                    stats["worst_quiz"] = f"{worst['quiz']} ({worst['percentage']:.1f}%)"
                    
                    stats["quiz_history"] = sorted(user_results, key=lambda x: x["date"], reverse=True)
        except:
            pass
    
    return stats

def get_difficulty_icon(difficulty):
    """Retorna el icono apropiado según la dificultad"""
    if difficulty.lower() in ['básico', 'basico', 'fácil', 'facil']:
        return "🟢"
    elif difficulty.lower() in ['intermedio', 'medio']:
        return "🟡"
    else:
        return "🔴"

def get_quiz_icon(quiz_name):
    """Retorna un icono específico para cada quiz"""
    icons = {
        "Bases de Datos": "🗄️",
        "Mercadotecnia": "📈",
        "Diseño": "🎨",
        "Diseño Web": "💻",
        "Metodologías": "⚡",
        "Python": "🐍",
        "JavaScript": "⚡",
        "Inteligencia Artificial": "🤖",
        "Ciberseguridad": "🔐",
        "Cloud Computing": "☁️"
    }
    return icons.get(quiz_name, "📝")

def show_welcome_screen():
    """Muestra la pantalla de bienvenida para nuevos usuarios"""
    st.markdown("""
    <div class="welcome-form fade-in">
        <h1>🎉 ¡Bienvenido/a!</h1>
        <p>Para comenzar tu journey de aprendizaje, necesitamos conocerte un poco mejor.</p>
        <p>✨ Tu progreso se guardará automáticamente ✨</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("welcome_form"):
        st.markdown("### 👋 ¿Cómo te llamas?")
        username = st.text_input(
            "Ingresa tu nombre o apodo:",
            placeholder="Ej: Ana, Carlos, DevMaster...",
            help="Este nombre se usará para guardar tu progreso"
        )
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submitted = st.form_submit_button("🚀 ¡Comenzar Aventura!", use_container_width=True)
        
        if submitted:
            if username.strip():
                clean_username = username.strip().title()
                st.session_state.username = clean_username
                save_user(clean_username)
                st.success(f"¡Perfecto, {clean_username}! Tu cuenta ha sido creada. 🎊")
                st.balloons()
                st.rerun()
            else:
                st.error("Por favor, ingresa un nombre válido. 😊")

def display_user_sidebar():
    """Muestra información del usuario en la sidebar"""
    username = st.session_state.username
    users = load_users()
    user_info = users.get(username, {})
    
    st.sidebar.markdown(f"""
    <div class="user-sidebar">
        <h3>👋 ¡Hola, {username}!</h3>
        <p><strong>Primera visita:</strong><br>{user_info.get('first_login', 'Hoy')}</p>
        <p><strong>Sesiones totales:</strong> {user_info.get('total_sessions', 1)}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Botón para cambiar usuario
    if st.sidebar.button("🔄 Cambiar Usuario"):
        # Limpiar sesión
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    
    # Mostrar estadísticas detalladas
    stats = get_user_stats(username)
    if stats["total_attempts"] > 0:
        st.sidebar.markdown("### 📊 Tus Estadísticas")
        st.sidebar.metric("Quizzes Completados", stats["total_attempts"])
        st.sidebar.metric("Puntuación Promedio", f"{stats['average_score']:.1f}%")
        
        if stats["best_quiz"]:
            st.sidebar.success(f"🏆 Mejor: {stats['best_quiz']}")
        
        # Mostrar historial reciente
        if st.sidebar.expander("📈 Historial Reciente"):
            for result in stats["quiz_history"][:5]:
                st.sidebar.write(f"**{result['quiz']}**")
                st.sidebar.write(f"📅 {result['date'][:10]} - {result['percentage']:.1f}%")
                st.sidebar.write("---")

def display_quiz_card(quiz_name, quiz_info, is_completed, username):
    """Muestra una tarjeta mejorada para cada quiz"""
    icon = get_quiz_icon(quiz_name)
    difficulty_icon = get_difficulty_icon(quiz_info['difficulty'])
    
    # Determinar la clase CSS según el estado
    card_class = "completed" if is_completed else ""
    status_text = "¡Completado!" if is_completed else "¡Nuevo desafío te espera!"
    status_color = "#00d4aa" if is_completed else "#667eea"
    
    # Obtener mejor puntuación si existe
    best_score = ""
    if is_completed:
        user_results = []
        if os.path.exists(RESULTS_FILE):
            try:
                with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            data = json.loads(line.strip())
                            if data.get('username') == username and data['quiz'] == quiz_name:
                                user_results.append(data)
                
                if user_results:
                    best = max(user_results, key=lambda x: x["percentage"])
                    best_score = f"🏆 Mejor: {best['percentage']:.1f}%"
            except:
                pass
    
    st.markdown(f"""
    <div class="quiz-card {card_class} fade-in">
        <div class="quiz-title">
            {icon} {quiz_name} {'✅' if is_completed else ''}
        </div>
        <div class="quiz-description">
            {quiz_info['description']}
        </div>
        <div class="quiz-meta">
            <div class="meta-item">
                📊 {len(quiz_info['questions'])} preguntas
            </div>
            <div class="meta-item">
                {difficulty_icon} {quiz_info['difficulty']}
            </div>
            <div class="meta-item">
                ⏱️ ~{len(quiz_info['questions']) * 1} min
            </div>
        </div>
        <p style="color: {status_color}; font-weight: 600; font-size: 0.9rem; margin: 0;">
            {status_text}
        </p>
        {f'<p style="color: #ff6b6b; font-size: 0.85rem; margin: 0.5rem 0 0 0;">{best_score}</p>' if best_score else ''}
    </div>
    """, unsafe_allow_html=True)
    
    # Botón con mejor estilo
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        button_text = "🔄 Repetir" if is_completed else "🚀 Comenzar"
        if st.button(button_text, key=f"btn_{quiz_name}", use_container_width=True):
            st.session_state.current_quiz = quiz_name
            st.session_state.quiz_started = True
            st.session_state.current_question = 0
            st.session_state.user_answers = []
            st.session_state.show_result = False
            st.rerun()

def run_quiz(quiz_name, quiz_data):
    """Ejecuta el quiz seleccionado"""
    questions = quiz_data['questions']
    username = st.session_state.username
    
    # Inicializar estado del quiz si no existe
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = []
    if 'show_result' not in st.session_state:
        st.session_state.show_result = False
    
    # Mostrar progreso
    progress = st.session_state.current_question / len(questions)
    st.progress(progress)
    st.markdown(f"**Pregunta {st.session_state.current_question + 1} de {len(questions)}**")
    
    if not st.session_state.show_result:
        # Mostrar pregunta actual
        current_q = questions[st.session_state.current_question]
        st.markdown(f"### {current_q['question']}")
        
        # Mostrar opciones
        selected_answer = st.radio(
            "Selecciona tu respuesta:",
            current_q['options'],
            key=f"q_{st.session_state.current_question}"
        )
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("⬅️ Anterior", disabled=st.session_state.current_question == 0):
                if st.session_state.current_question > 0:
                    st.session_state.current_question -= 1
                    st.rerun()
        
        with col2:
            if st.button("Siguiente ➡️", disabled=st.session_state.current_question >= len(questions)-1):
                # Guardar respuesta
                if len(st.session_state.user_answers) <= st.session_state.current_question:
                    st.session_state.user_answers.append(selected_answer)
                else:
                    st.session_state.user_answers[st.session_state.current_question] = selected_answer
                
                if st.session_state.current_question < len(questions) - 1:
                    st.session_state.current_question += 1
                    st.rerun()
        
        with col3:
            if st.button("🏁 Terminar Quiz"):
                # Guardar respuesta actual
                if len(st.session_state.user_answers) <= st.session_state.current_question:
                    st.session_state.user_answers.append(selected_answer)
                else:
                    st.session_state.user_answers[st.session_state.current_question] = selected_answer
                
                # Calcular puntuación
                score = 0
                for i, answer in enumerate(st.session_state.user_answers):
                    if i < len(questions) and answer == questions[i]['correct']:
                        score += 1
                
                # Guardar resultado con username
                save_quiz_result(username, quiz_name, score, len(questions), st.session_state.user_answers)
                st.session_state.show_result = True
                st.session_state.final_score = score
                st.rerun()
    
    else:
        # Mostrar resultado final
        st.balloons()
        st.markdown(f"# 🎉 ¡Quiz Completado, {username}!")
        
        score = st.session_state.final_score
        total = len(questions)
        percentage = (score / total) * 100
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Respuestas Correctas", f"{score}/{total}")
        with col2:
            st.metric("Porcentaje", f"{percentage:.1f}%")
        with col3:
            if percentage >= 80:
                st.markdown("### 🏆 ¡Excelente!")
            elif percentage >= 60:
                st.markdown("### 👍 ¡Bien hecho!")
            else:
                st.markdown("### 📚 ¡Sigue practicando!")
        
        # Mostrar respuestas detalladas
        with st.expander("Ver respuestas detalladas"):
            for i, question in enumerate(questions):
                user_answer = st.session_state.user_answers[i] if i < len(st.session_state.user_answers) else "No respondida"
                is_correct = user_answer == question['correct']
                
                st.markdown(f"**Pregunta {i+1}:** {question['question']}")
                st.markdown(f"**Tu respuesta:** {user_answer} {'✅' if is_correct else '❌'}")
                st.markdown(f"**Respuesta correcta:** {question['correct']}")
                st.markdown("---")
        
        if st.button("🏠 Volver al Menu Principal"):
            # Limpiar estado del quiz
            for key in ['current_quiz', 'quiz_started', 'current_question', 'user_answers', 'show_result', 'final_score']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

def main():
    """Función principal de la aplicación"""
    
    # Verificar si el usuario está logueado
    if 'username' not in st.session_state:
        show_welcome_screen()
        return
    
    # Mostrar sidebar de usuario
    display_user_sidebar()
    
    # Título principal mejorado con saludo personalizado
    username = st.session_state.username
    st.markdown('<h1 class="main-title">🧠 ¿Qué tan experto eres?</h1>', unsafe_allow_html=True)
    
    # Mensaje de bienvenida personalizado
    users = load_users()
    user_info = users.get(username, {})
    is_returning = user_info.get('total_sessions', 1) > 1
    
    if is_returning:
        welcome_msg = f"¡Bienvenido de vuelta, {username}! 🎯"
        subtitle = "Continúa tu journey de aprendizaje donde lo dejaste"
    else:
        welcome_msg = f"¡Hola {username}! 🌟"
        subtitle = "¡Es genial tenerte aquí! Comienza tu aventura de aprendizaje"
    
    st.markdown(f"""
    <div class="welcome-message">
        <h2>{welcome_msg}</h2>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Inicializar estado de la sesión
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
    
    # Cargar quizzes completados para este usuario
    completed_quizzes = load_completed_quizzes(username)
    
    if not st.session_state.quiz_started:
        # Estadísticas mejoradas personalizadas
        total_quizzes = len(QUIZ_DATA)
        completed_count = len(completed_quizzes)
        progress_percentage = (completed_count/total_quizzes)*100 if total_quizzes > 0 else 0
        
        # Obtener estadísticas del usuario
        user_stats = get_user_stats(username)
        
        st.markdown(f"""
        <div class="stats-container">
            <div class="stats-title">📊 Tu Progreso Personal, {username}</div>
            <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
                <div class="stat-item">
                    <h2 style="margin: 0; color: #fff;">🎯 {total_quizzes}</h2>
                    <p style="margin: 0; opacity: 0.9;">Quizzes Disponibles</p>
                </div>
                <div class="stat-item">
                    <h2 style="margin: 0; color: #00ff88;">✅ {completed_count}</h2>
                    <p style="margin: 0; opacity: 0.9;">Completados</p>
                </div>
                <div class="stat-item">
                    <h2 style="margin: 0; color: #ffd700;">🏆 {progress_percentage:.0f}%</h2>
                    <p style="margin: 0; opacity: 0.9;">Progreso Global</p>
                </div>
                <div class="stat-item">
                    <h2 style="margin: 0; color: #ff9f43;">📈 {user_stats['average_score']:.1f}%</h2>
                    <p style="margin: 0; opacity: 0.9;">Puntuación Promedio</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Barra de progreso visual
        st.progress(progress_percentage / 100)
        
        # Mensaje motivacional personalizado
        if progress_percentage == 100:
            st.success(f"🎉 ¡Increíble, {username}! Has completado todos los quizzes disponibles. ¡Eres un verdadero experto!")
        elif progress_percentage >= 50:
            st.info(f"🔥 ¡Excelente trabajo, {username}! Ya completaste más de la mitad de los quizzes.")
        elif completed_count > 0:
            st.info(f"🚀 ¡Vas muy bien, {username}! Sigue así para convertirte en un experto.")
        else:
            st.info(f"🌟 ¡Perfecto, {username}! Selecciona tu primer quiz y comienza tu journey de aprendizaje.")
        
        # Separador visual
        st.markdown("---")
        
        # Título de la sección de quizzes
        st.markdown("## 🎮 Selecciona tu próximo desafío")
        
        # Mostrar quizzes en una cuadrícula mejorada
        cols = st.columns(2)  # 2 columnas para mejor organización
        for idx, (quiz_name, quiz_info) in enumerate(QUIZ_DATA.items()):
            with cols[idx % 2]:
                is_completed = quiz_name in completed_quizzes
                display_quiz_card(quiz_name, quiz_info, is_completed, username)
                st.markdown("<br>", unsafe_allow_html=True)
        
        # Botón para ver historial personalizado
        if completed_quizzes:
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("📈 Ver Mi Historial Completo", use_container_width=True):
                    st.session_state.show_history = True
                    st.rerun()
        
        # Mostrar historial si se solicita
        if st.session_state.get('show_history', False):
            st.markdown(f"## 📊 Historial Completo de {username}")
            user_stats = get_user_stats(username)
            
            if user_stats["quiz_history"]:
                # Métricas del historial
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Intentos", user_stats["total_attempts"])
                with col2:
                    st.metric("Promedio General", f"{user_stats['average_score']:.1f}%")
                with col3:
                    if user_stats["best_quiz"]:
                        st.success(f"🏆 Mejor: {user_stats['best_quiz']}")
                with col4:
                    if user_stats["worst_quiz"]:
                        st.info(f"📚 Mejorar: {user_stats['worst_quiz']}")
                
                st.markdown("### 📋 Detalles de tus resultados:")
                
                # Tabla de resultados
                for i, result in enumerate(user_stats["quiz_history"]):
                    with st.expander(f"{result['quiz']} - {result['percentage']:.1f}% ({result['date'][:10]})", 
                                   expanded=i < 3):  # Expandir los 3 más recientes
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.write(f"**Fecha:** {result['date']}")
                            st.write(f"**Puntuación:** {result['score']}/{result['total']}")
                        with col2:
                            st.write(f"**Porcentaje:** {result['percentage']:.1f}%")
                            if result['percentage'] >= 80:
                                st.write("**Estado:** 🏆 Excelente")
                            elif result['percentage'] >= 60:
                                st.write("**Estado:** 👍 Bien")
                            else:
                                st.write("**Estado:** 📚 Mejorable")
                        with col3:
                            quiz_icon = get_quiz_icon(result['quiz'])
                            st.write(f"**Quiz:** {quiz_icon} {result['quiz']}")
                            
                            # Opción para repetir desde el historial
                            if st.button(f"🔄 Repetir {result['quiz']}", key=f"repeat_{result['quiz']}_{i}"):
                                st.session_state.current_quiz = result['quiz']
                                st.session_state.quiz_started = True
                                st.session_state.current_question = 0
                                st.session_state.user_answers = []
                                st.session_state.show_result = False
                                st.session_state.show_history = False
                                st.rerun()
            else:
                st.info("Aún no has completado ningún quiz. ¡Comienza tu primer desafío arriba!")
            
            # Botón para cerrar historial
            if st.button("❌ Cerrar Historial"):
                st.session_state.show_history = False
                st.rerun()
        
        # Footer inspiracional personalizado
        st.markdown("---")
        motivational_quotes = [
            f"💡 'El conocimiento es poder, {username}!'",
            f"🌟 'Cada quiz completado te acerca más a la maestría, {username}!'",
            f"🚀 'Tu curiosidad es tu superpoder, {username}!'",
            f"📚 'El aprendizaje nunca termina, {username}!'",
            f"💪 'Cada pregunta respondida es un paso hacia el éxito, {username}!'"
        ]
        
        import random
        selected_quote = random.choice(motivational_quotes)
        
        st.markdown(f"""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(45deg, #f093fb, #f5576c); 
                    border-radius: 15px; color: white; margin-top: 2rem;">
            <h3>{selected_quote}</h3>
            <p>Cada quiz completado es un paso más hacia la maestría. ¡Sigue aprendiendo y creciendo!</p>
            <p style="opacity: 0.8; font-size: 0.9rem;">Progreso guardado automáticamente para {username} ✨</p>
        </div>
        """, unsafe_allow_html=True)
    
    else:
        # Ejecutar quiz seleccionado
        quiz_name = st.session_state.current_quiz
        st.markdown(f'<h1 class="main-title">📝 Quiz: {quiz_name}</h1>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 1rem; padding: 1rem; background: rgba(102, 126, 234, 0.1); border-radius: 10px;">
            <p style="margin: 0; color: #667eea; font-weight: 600;">👤 Usuario: {username} | 🎯 Quiz: {quiz_name}</p>
        </div>
        """, unsafe_allow_html=True)
        run_quiz(quiz_name, QUIZ_DATA[quiz_name])

if __name__ == "__main__":
    main()