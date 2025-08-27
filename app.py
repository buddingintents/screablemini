import streamlit as st
import random
import time
import streamlit.components.v1 as components
import threading
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="Word Scramble Mini",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Game configuration
GAME_CONFIG = {
    "rounds_per_game": 5,
    "time_per_round": 60,
    "points_per_correct": 10,
    "time_bonus_multiplier": 0.1
}

# Word list for the game
WORD_LIST = [
    "PYTHON", "STREAM", "CODING", "JUNGLE", "PLANET", "WIZARD", "CASTLE", 
    "DRAGON", "FLOWER", "GUITAR", "HOCKEY", "ISLAND", "KIWI", "LEMON", 
    "MONKEY", "NATURE", "ORANGE", "PIRATE", "QUEEN", "RABBIT", "SUNSET", 
    "TIGER", "UMBRELLA", "VIOLET", "WINTER", "YELLOW", "ZEBRA", "ANCHOR", 
    "BRIDGE", "CAMERA", "DOCTOR", "EAGLE", "FOREST", "GARDEN", "HAMMER", 
    "INSECT", "JACKET", "KNIGHT", "LADDER", "MOUNTAIN", "NEEDLE", "OCEAN", 
    "PUZZLE", "QUARTZ", "ROCKET", "SILVER", "TEMPLE", "VIKING", "WHISTLE"
]

def show_banner_ad(ad_type="top"):
    """Display banner advertisement using Google AdSense"""
    try:
        adsense_client = st.secrets["google"]["adsense_client_id"]
        ad_slot = st.secrets["google"][f"{ad_type}_ad_slot"]
    except:
        adsense_client = "ca-pub-1234567890123456"
        ad_slot = "1234567890"

    ad_html = f"""
    <div style="text-align: center; margin: 20px 0;">
        <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={adsense_client}"
                crossorigin="anonymous"></script>
        <ins class="adsbygoogle"
             style="display:inline-block;width:728px;height:90px"
             data-ad-client="{adsense_client}"
             data-ad-slot="{ad_slot}"></ins>
        <script>
             (adsbygoogle = window.adsbygoogle || []).push({{}});
        </script>
    </div>
    """
    components.html(ad_html, height=120)

def show_interstitial_ad():
    """Display interstitial advertisement between rounds"""
    try:
        adsense_client = st.secrets["google"]["adsense_client_id"]
        interstitial_slot = st.secrets["google"]["interstitial_ad_slot"]
    except:
        adsense_client = "ca-pub-1234567890123456"
        interstitial_slot = "1234567890"

    ad_html = f"""
    <div style="text-align: center; padding: 40px; background: #f0f8ff; border: 2px dashed #4CAF50; border-radius: 10px; margin: 20px 0;">
        <h3 style="color: #2E8B57; margin-bottom: 20px;">🎯 Round Complete!</h3>
        <p style="color: #666; margin-bottom: 20px;">Great job! Here's a quick break before the next round.</p>

        <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={adsense_client}"
                crossorigin="anonymous"></script>
        <ins class="adsbygoogle"
             style="display:inline-block;width:970px;height:250px"
             data-ad-client="{adsense_client}"
             data-ad-slot="{interstitial_slot}"></ins>
        <script>
             (adsbygoogle = window.adsbygoogle || []).push({{}});
        </script>
    </div>
    """
    components.html(ad_html, height=350)

def show_rewarded_ad():
    """Display rewarded advertisement for hints"""
    try:
        adsense_client = st.secrets["google"]["adsense_client_id"]
        rewarded_slot = st.secrets["google"]["rewarded_ad_slot"]
    except:
        adsense_client = "ca-pub-1234567890123456"
        rewarded_slot = "1234567890"

    ad_html = f"""
    <div style="text-align: center; padding: 30px; background: #fff8dc; border: 2px solid #ffd700; border-radius: 10px;">
        <h4 style="color: #b8860b; margin-bottom: 15px;">💡 Get a Hint!</h4>
        <p style="color: #666; margin-bottom: 20px;">Watch this ad to reveal the first letter of the word!</p>

        <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={adsense_client}"
                crossorigin="anonymous"></script>
        <ins class="adsbygoogle"
             style="display:inline-block;width:300px;height:250px"
             data-ad-client="{adsense_client}"
             data-ad-slot="{rewarded_slot}"></ins>
        <script>
             (adsbygoogle = window.adsbygoogle || []).push({{}});
        </script>
    </div>
    """
    components.html(ad_html, height=320)

def scramble_word(word):
    """Scramble the letters of a word"""
    letters = list(word)
    random.shuffle(letters)
    scrambled = ''.join(letters)
    return scrambled if scrambled != word else scramble_word(word)

def init_session_state():
    """Initialize all session state variables"""
    if 'initialized' not in st.session_state:
        st.session_state.screen = 'welcome'
        st.session_state.current_round = 1
        st.session_state.score = 0
        st.session_state.current_word = ''
        st.session_state.scrambled_word = ''
        st.session_state.round_start_time = None
        st.session_state.hint_used = False
        st.session_state.feedback_message = ''
        st.session_state.feedback_type = 'info'
        st.session_state.awaiting_next_round = False
        st.session_state.last_update = time.time()
        st.session_state.initialized = True

def start_new_round():
    """Start a new game round"""
    word = random.choice(WORD_LIST)
    st.session_state.current_word = word
    st.session_state.scrambled_word = scramble_word(word)
    st.session_state.round_start_time = time.time()
    st.session_state.hint_used = False
    st.session_state.feedback_message = ''
    st.session_state.feedback_type = 'info'
    st.session_state.awaiting_next_round = False
    st.session_state.screen = 'playing'
    st.session_state.last_update = time.time()

def calculate_score(time_taken):
    """Calculate score based on correctness and time"""
    base_points = GAME_CONFIG['points_per_correct']
    time_remaining = max(0, GAME_CONFIG['time_per_round'] - time_taken)
    time_bonus = int(time_remaining * GAME_CONFIG['time_bonus_multiplier'])
    return base_points + time_bonus

def process_guess(user_guess):
    """Process user's guess"""
    current_word = st.session_state.current_word

    if user_guess == current_word:
        elapsed_time = time.time() - st.session_state.round_start_time
        round_score = calculate_score(elapsed_time)

        st.session_state.score += round_score
        st.session_state.feedback_message = f"🎉 Correct! '{current_word}' is right! You earned {round_score} points!"
        st.session_state.feedback_type = 'success'
        st.session_state.awaiting_next_round = True
    else:
        st.session_state.feedback_message = f"❌ '{user_guess}' is not correct. Try again!"
        st.session_state.feedback_type = 'error'
        st.session_state.awaiting_next_round = False

def next_round():
    """Move to next round or end game"""
    st.session_state.current_round += 1
    st.session_state.feedback_message = ''
    st.session_state.awaiting_next_round = False

    if st.session_state.current_round <= GAME_CONFIG['rounds_per_game']:
        st.session_state.screen = 'interstitial'
    else:
        st.session_state.screen = 'complete'

def reset_game():
    """Reset game to initial state"""
    st.session_state.screen = 'welcome'
    st.session_state.current_round = 1
    st.session_state.score = 0
    st.session_state.current_word = ''
    st.session_state.scrambled_word = ''
    st.session_state.round_start_time = None
    st.session_state.hint_used = False
    st.session_state.feedback_message = ''
    st.session_state.feedback_type = 'info'
    st.session_state.awaiting_next_round = False

def get_performance_message(score):
    """Get performance message based on score"""
    max_possible = GAME_CONFIG['rounds_per_game'] * (GAME_CONFIG['points_per_correct'] + GAME_CONFIG['time_per_round'] * GAME_CONFIG['time_bonus_multiplier'])

    if score >= max_possible * 0.8:
        return "🏆 Outstanding! You're a word master!"
    elif score >= max_possible * 0.6:
        return "🎯 Great job! You did really well!"
    elif score >= max_possible * 0.4:
        return "👍 Good work! Keep practicing!"
    else:
        return "💪 Nice try! You'll do better next time!"

def create_auto_refresh_timer():
    """Create JavaScript-based auto-refreshing timer"""
    timer_html = f"""
    <div id="timer-container" style="text-align: center; margin: 10px 0;">
        <div id="countdown-timer" style="font-size: 1.5em; font-weight: bold; color: #e74c3c; 
             background: #fff5f5; padding: 10px; border-radius: 8px; border: 2px solid #e74c3c;">
            ⏰ <span id="timer-display">60</span>s
        </div>
        <div id="progress-container" style="margin-top: 10px;">
            <div style="background: #ecf0f1; height: 8px; border-radius: 4px; overflow: hidden;">
                <div id="progress-bar" style="background: linear-gradient(90deg, #27ae60, #f1c40f, #e74c3c); 
                     height: 100%; width: 100%; transition: width 1s linear;"></div>
            </div>
        </div>
    </div>

    <script>
    let startTime = {st.session_state.round_start_time if st.session_state.round_start_time else time.time()};
    let roundDuration = {GAME_CONFIG['time_per_round']};

    function updateTimer() {{
        let currentTime = Date.now() / 1000;
        let elapsed = currentTime - startTime;
        let timeLeft = Math.max(0, roundDuration - elapsed);

        document.getElementById('timer-display').textContent = Math.ceil(timeLeft);

        let progress = (timeLeft / roundDuration) * 100;
        document.getElementById('progress-bar').style.width = progress + '%';

        let timerElement = document.getElementById('countdown-timer');
        if (timeLeft <= 10) {{
            timerElement.style.color = '#e74c3c';
            timerElement.style.background = '#ffebee';
            timerElement.style.borderColor = '#e74c3c';
            if (timeLeft <= 5) {{
                timerElement.style.animation = 'pulse 1s infinite';
            }}
        }} else if (timeLeft <= 30) {{
            timerElement.style.color = '#f39c12';
            timerElement.style.background = '#fef9e7';
            timerElement.style.borderColor = '#f39c12';
        }} else {{
            timerElement.style.color = '#27ae60';
            timerElement.style.background = '#eafaf1';
            timerElement.style.borderColor = '#27ae60';
        }}

        if (timeLeft <= 0) {{
            window.parent.postMessage({{type: 'time_up'}}, '*');
        }}
    }}

    let style = document.createElement('style');
    style.textContent = `
        @keyframes pulse {{
            0% {{ transform: scale(1); }}
            50% {{ transform: scale(1.05); }}
            100% {{ transform: scale(1); }}
        }}
    `;
    document.head.appendChild(style);

    updateTimer();
    setInterval(updateTimer, 1000);

    window.addEventListener('message', function(event) {{
        if (event.data.type === 'reset_timer') {{
            startTime = Date.now() / 1000;
        }}
    }});
    </script>
    """
    return timer_html

def main():
    """Main application with auto-updating timer"""
    init_session_state()

    # Custom CSS - FIXED: Enhanced contrast for final screen
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 20px 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .game-card {
        background: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 20px 0;
    }
    .scrambled-word {
        font-size: 3em;
        font-weight: bold;
        text-align: center;
        color: #4CAF50;
        letter-spacing: 0.2em;
        margin: 20px 0;
        padding: 20px;
        background: #f8f9fa;
        border-radius: 10px;
        border: 2px dashed #4CAF50;
    }
    .game-instructions {
        background: #ffffff;
        color: #2c3e50;
        border: 2px solid #3498db;
        padding: 25px;
        border-radius: 12px;
        margin: 20px 0;
        box-shadow: 0 2px 8px rgba(52, 152, 219, 0.1);
    }
    .game-instructions h3 {
        color: #2980b9;
        margin-bottom: 15px;
        font-weight: 600;
    }
    .game-instructions ul {
        color: #34495e;
        font-size: 1.1em;
        line-height: 1.6;
    }
    .game-instructions li {
        margin-bottom: 8px;
        color: #2c3e50;
    }
    /* FIXED: Enhanced contrast for final score screen */
    .final-score-card {
        background: #ffffff;
        color: #2c3e50;
        border: 3px solid #4CAF50;
        padding: 40px;
        border-radius: 20px;
        margin: 20px 0;
        box-shadow: 0 8px 16px rgba(76, 175, 80, 0.2);
        text-align: center;
    }
    .final-score-title {
        color: #2c3e50;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 20px;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
    }
    .final-score-value {
        font-size: 4em;
        color: #4CAF50;
        font-weight: bold;
        margin: 30px 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        padding: 20px;
        background: #f8f9fa;
        border-radius: 15px;
        border: 2px solid #4CAF50;
    }
    .final-score-label {
        color: #2c3e50;
        font-size: 1.3em;
        font-weight: 600;
        margin-bottom: 30px;
    }
    .performance-message {
        color: #2c3e50;
        font-size: 1.4em;
        font-weight: 600;
        margin: 30px 0;
        padding: 20px;
        background: #e8f5e8;
        border-radius: 12px;
        border-left: 5px solid #4CAF50;
        text-align: left;
    }
    .auto-refresh {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

    # Auto-refresh mechanism for timer updates
    if st.session_state.screen == 'playing' and st.session_state.round_start_time:
        current_time = time.time()
        elapsed = current_time - st.session_state.round_start_time

        if current_time - st.session_state.last_update >= 2.0:
            st.session_state.last_update = current_time

            if elapsed >= GAME_CONFIG['time_per_round'] and not st.session_state.awaiting_next_round:
                st.session_state.feedback_message = f"⏰ Time's up! The word was '{st.session_state.current_word}'"
                st.session_state.feedback_type = 'error'
                st.session_state.awaiting_next_round = True

            st.rerun()

    # Top banner advertisement
    show_banner_ad("top")

    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>🎯 Word Scramble Mini</h1>
        <p>Unscramble words before time runs out!</p>
    </div>
    """, unsafe_allow_html=True)

    # Route to appropriate screen
    if st.session_state.screen == 'welcome':
        show_welcome_screen()
    elif st.session_state.screen == 'playing':
        show_game_screen()
    elif st.session_state.screen == 'interstitial':
        show_interstitial_screen()
    elif st.session_state.screen == 'complete':
        show_final_screen()

    # Footer advertisement
    st.markdown("---")
    show_banner_ad("footer")

def show_welcome_screen():
    """Display welcome screen"""
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("""
        <div class="game-instructions">
            <h3>🎮 How to Play:</h3>
            <ul>
                <li>🔀 Unscramble the letters to form a word</li>
                <li>⏰ You have 60 seconds per round</li>
                <li>🎯 Complete 5 rounds to finish the game</li>
                <li>💰 Earn 10 points per correct answer + time bonus</li>
                <li>💡 Use hints by watching ads for the first letter</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚀 Start Game", type="primary", use_container_width=True):
            start_new_round()
            st.rerun()

def show_game_screen():
    """Display main game screen with auto-updating timer"""
    # Game stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Round", f"{st.session_state.current_round}/{GAME_CONFIG['rounds_per_game']}")
    with col2:
        st.metric("Score", st.session_state.score)
    with col3:
        if st.session_state.round_start_time:
            elapsed = time.time() - st.session_state.round_start_time
            time_left = max(0, GAME_CONFIG['time_per_round'] - elapsed)

            if time_left <= 10:
                st.metric("⚠️ Time Left", f"{int(time_left)}s", delta="Hurry!")
            elif time_left <= 30:
                st.metric("⚡ Time Left", f"{int(time_left)}s", delta="Getting close")
            else:
                st.metric("⏰ Time Left", f"{int(time_left)}s")
        else:
            st.metric("Time Left", "60s")
    with col4:
        if st.button("💡 Get Hint", help="Watch an ad to get the first letter") and not st.session_state.hint_used:
            show_rewarded_ad()
            st.session_state.hint_used = True
            st.rerun()

    # Auto-updating visual timer
    if st.session_state.round_start_time and not st.session_state.awaiting_next_round:
        timer_html = create_auto_refresh_timer()
        components.html(timer_html, height=100)

    # Display scrambled word
    st.markdown(f"""
    <div class="scrambled-word">
        {st.session_state.scrambled_word}
    </div>
    """, unsafe_allow_html=True)

    # Show hint if used
    if st.session_state.hint_used:
        st.info(f"💡 Hint: The word starts with '{st.session_state.current_word[0]}'")

    # Show feedback
    if st.session_state.feedback_message:
        if st.session_state.feedback_type == 'success':
            st.success(st.session_state.feedback_message)
        elif st.session_state.feedback_type == 'error':
            st.error(st.session_state.feedback_message)

    # User input form
    if not st.session_state.awaiting_next_round:
        with st.form(key="guess_form", clear_on_submit=True):
            user_guess = st.text_input(
                "Your guess:", 
                placeholder="Enter the unscrambled word...",
                help="Type your answer and click Submit Guess"
            )

            col1, col2 = st.columns(2)
            with col1:
                submit_guess = st.form_submit_button("Submit Guess", type="primary", use_container_width=True)
            with col2:
                skip_round = st.form_submit_button("Skip Round", use_container_width=True)

        if submit_guess:
            if user_guess.strip():
                process_guess(user_guess.strip().upper())
                st.rerun()
            else:
                st.warning("Please enter a word!")

        if skip_round:
            next_round()
            st.rerun()
    else:
        if st.button("🎯 Next Round", type="primary", use_container_width=True):
            next_round()
            st.rerun()

def show_interstitial_screen():
    """Display interstitial advertisement screen"""
    st.markdown(f"""
    <div class="game-card">
        <h2 style="text-align: center; color: #4CAF50;">🎉 Round {st.session_state.current_round - 1} Complete!</h2>
        <p style="text-align: center; font-size: 1.2em;">
            Great job! Ready for the next challenge?
        </p>
    </div>
    """, unsafe_allow_html=True)

    show_interstitial_ad()

    if st.button("Continue to Next Round", type="primary", use_container_width=True):
        start_new_round()
        st.rerun()

def show_final_screen():
    """Display final score screen - FIXED: Enhanced contrast"""
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # FIXED: Using enhanced CSS classes for better contrast
        st.markdown(f"""
        <div class="final-score-card">
            <div class="final-score-title">🎮 Game Complete!</div>
            <div class="final-score-value">{st.session_state.score}</div>
            <div class="final-score-label">Final Score</div>
            <div class="performance-message">
                {get_performance_message(st.session_state.score)}
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔄 Play Again", type="primary", use_container_width=True):
                reset_game()
                st.rerun()

        with col_b:
            if st.button("🏠 Main Menu", use_container_width=True):
                reset_game()
                st.rerun()

if __name__ == "__main__":
    main()
