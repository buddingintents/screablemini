import streamlit as st
import random
import time
import streamlit.components.v1 as components

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

# Google AdSense integration functions
def show_banner_ad(ad_type="top"):
    """Display banner advertisement using Google AdSense"""
    # Get AdSense configuration from Streamlit secrets
    try:
        adsense_client = st.secrets["google"]["adsense_client_id"]
        ad_slot = st.secrets["google"][f"{ad_type}_ad_slot"]
    except:
        # Fallback to demo mode if secrets not configured
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

        <div style="margin-top: 20px;">
            <button onclick="window.parent.postMessage('continue_game', '*')" 
                    style="background: #4CAF50; color: white; border: none; padding: 12px 24px; border-radius: 5px; cursor: pointer; font-size: 16px;">
                Continue to Next Round →
            </button>
        </div>
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

# Game utility functions
def scramble_word(word):
    """Scramble the letters of a word"""
    letters = list(word)
    random.shuffle(letters)
    scrambled = ''.join(letters)
    # Ensure scrambled word is different from original
    return scrambled if scrambled != word else scramble_word(word)

def initialize_game():
    """Initialize game state"""
    if 'game_state' not in st.session_state:
        st.session_state.game_state = {
            'current_round': 1,
            'score': 0,
            'total_rounds': GAME_CONFIG['rounds_per_game'],
            'round_start_time': None,
            'current_word': '',
            'scrambled_word': '',
            'hint_used': False,
            'game_active': False,
            'game_complete': False,
            'show_interstitial': False,
            'feedback_message': '',
            'feedback_type': 'info',
            'round_completed': False
        }

def start_new_round():
    """Start a new game round"""
    if st.session_state.game_state['current_round'] <= GAME_CONFIG['rounds_per_game']:
        word = random.choice(WORD_LIST)
        st.session_state.game_state.update({
            'current_word': word,
            'scrambled_word': scramble_word(word),
            'round_start_time': time.time(),
            'hint_used': False,
            'game_active': True,
            'show_interstitial': False,
            'feedback_message': '',
            'feedback_type': 'info',
            'round_completed': False
        })

def calculate_score(time_taken):
    """Calculate score based on correctness and time"""
    base_points = GAME_CONFIG['points_per_correct']
    time_remaining = max(0, GAME_CONFIG['time_per_round'] - time_taken)
    time_bonus = int(time_remaining * GAME_CONFIG['time_bonus_multiplier'])
    return base_points + time_bonus

def end_game():
    """End the current game"""
    st.session_state.game_state.update({
        'game_active': False,
        'game_complete': True
    })

# Main application
def main():
    # Custom CSS for better styling - FIXED COLOR CONTRAST
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
    .stats-container {
        display: flex;
        justify-content: space-around;
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
    }
    .stat-item {
        text-align: center;
    }
    .stat-value {
        font-size: 2em;
        font-weight: bold;
        color: #2E8B57;
    }
    .stat-label {
        color: #666;
        font-size: 0.9em;
    }
    .feedback-success {
        background: #d4edda;
        color: #155724;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #28a745;
    }
    .feedback-error {
        background: #f8d7da;
        color: #721c24;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #dc3545;
    }
    /* FIXED: Better color contrast for instructions */
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
    </style>
    """, unsafe_allow_html=True)

    # Initialize game
    initialize_game()

    # Top banner advertisement
    show_banner_ad("top")

    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>🎯 Word Scramble Mini</h1>
        <p>Unscramble words before time runs out!</p>
    </div>
    """, unsafe_allow_html=True)

    # Check if game is not started yet
    if not st.session_state.game_state['game_active'] and not st.session_state.game_state['game_complete']:
        show_welcome_screen()

    # Show interstitial ad between rounds
    elif st.session_state.game_state['show_interstitial']:
        show_interstitial_screen()

    # Main game screen
    elif st.session_state.game_state['game_active']:
        show_game_screen()

    # Final score screen
    elif st.session_state.game_state['game_complete']:
        show_final_screen()

    # Footer advertisement
    st.markdown("---")
    show_banner_ad("footer")

def show_welcome_screen():
    """Display welcome screen with game instructions"""
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

def show_interstitial_screen():
    """Display interstitial advertisement screen"""
    st.markdown("""
    <div class="game-card">
        <h2 style="text-align: center; color: #4CAF50;">🎉 Round Complete!</h2>
        <p style="text-align: center; font-size: 1.2em;">
            Great job! You completed round {current_round}.
        </p>
    </div>
    """.format(current_round=st.session_state.game_state['current_round'] - 1), unsafe_allow_html=True)

    # Show interstitial ad
    show_interstitial_ad()

    if st.button("Continue to Next Round", type="primary", use_container_width=True):
        if st.session_state.game_state['current_round'] <= GAME_CONFIG['rounds_per_game']:
            start_new_round()
        else:
            end_game()
        st.rerun()

def show_game_screen():
    """Display main game screen"""
    game_state = st.session_state.game_state

    # Game stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Round", f"{game_state['current_round']}/{game_state['total_rounds']}")
    with col2:
        st.metric("Score", game_state['score'])
    with col3:
        # Calculate time remaining
        if game_state['round_start_time']:
            elapsed = time.time() - game_state['round_start_time']
            time_left = max(0, GAME_CONFIG['time_per_round'] - elapsed)
            st.metric("Time Left", f"{int(time_left)}s")
        else:
            st.metric("Time Left", "60s")
    with col4:
        if st.button("💡 Get Hint", help="Watch an ad to get the first letter"):
            show_hint()

    # Display scrambled word
    st.markdown(f"""
    <div class="scrambled-word">
        {game_state['scrambled_word']}
    </div>
    """, unsafe_allow_html=True)

    # Show hint if used
    if game_state['hint_used']:
        st.info(f"💡 Hint: The word starts with '{game_state['current_word'][0]}'")

    # User input form
    with st.form("guess_form", clear_on_submit=True):
        user_guess = st.text_input(
            "Your guess:", 
            placeholder="Enter the unscrambled word...",
            key=f"user_input_{game_state['current_round']}_{time.time()}"  # Unique key to prevent caching
        ).upper().strip()

        col1, col2 = st.columns(2)
        with col1:
            submit_guess = st.form_submit_button("Submit Guess", type="primary", use_container_width=True)
        with col2:
            skip_round = st.form_submit_button("Skip Round", use_container_width=True)

    # Process guess - FIXED: Proper round progression
    if submit_guess and user_guess:
        process_guess(user_guess)
    elif skip_round:
        next_round()

    # Show feedback
    if game_state['feedback_message'] and not game_state['round_completed']:
        if game_state['feedback_type'] == 'success':
            st.success(game_state['feedback_message'])
        elif game_state['feedback_type'] == 'error':
            st.error(game_state['feedback_message'])
        else:
            st.info(game_state['feedback_message'])

    # FIXED: Auto-advance after correct answer
    if game_state['round_completed']:
        st.success(game_state['feedback_message'])
        if st.button("🎯 Next Round", type="primary", use_container_width=True):
            next_round()

def show_hint():
    """Display hint by showing rewarded ad"""
    if not st.session_state.game_state['hint_used']:
        # Show rewarded ad
        show_rewarded_ad()

        # Mark hint as used
        st.session_state.game_state['hint_used'] = True
        st.success("💡 Hint unlocked! The first letter is revealed above.")
        st.rerun()
    else:
        st.info("💡 Hint already used for this round!")

def process_guess(user_guess):
    """Process user's guess - FIXED: Proper round progression"""
    game_state = st.session_state.game_state
    current_word = game_state['current_word']

    if user_guess == current_word:
        # Correct guess
        elapsed_time = time.time() - game_state['round_start_time']
        round_score = calculate_score(elapsed_time)

        st.session_state.game_state['score'] += round_score
        st.session_state.game_state['feedback_message'] = f"🎉 Correct! '{current_word}' is right! You earned {round_score} points!"
        st.session_state.game_state['feedback_type'] = 'success'
        st.session_state.game_state['round_completed'] = True

        st.rerun()
    else:
        # Incorrect guess
        st.session_state.game_state['feedback_message'] = f"❌ '{user_guess}' is not correct. Try again!"
        st.session_state.game_state['feedback_type'] = 'error'
        st.session_state.game_state['round_completed'] = False
        st.rerun()

def next_round():
    """Move to next round or end game - FIXED: Proper state management"""
    st.session_state.game_state['current_round'] += 1

    if st.session_state.game_state['current_round'] <= GAME_CONFIG['rounds_per_game']:
        # Show interstitial ad between rounds
        st.session_state.game_state['show_interstitial'] = True
        st.session_state.game_state['game_active'] = False
    else:
        # End game
        end_game()

    st.rerun()

def show_final_screen():
    """Display final score and game over screen"""
    game_state = st.session_state.game_state

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown(f"""
        <div class="game-card" style="text-align: center;">
            <h2>🎮 Game Complete!</h2>
            <div class="stat-item">
                <div class="stat-value">{game_state['score']}</div>
                <div class="stat-label">Final Score</div>
            </div>
            <div style="margin: 30px 0;">
                {get_performance_message(game_state['score'])}
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔄 Play Again", type="primary", use_container_width=True):
                # Reset game state
                st.session_state.game_state = {
                    'current_round': 1,
                    'score': 0,
                    'total_rounds': GAME_CONFIG['rounds_per_game'],
                    'round_start_time': None,
                    'current_word': '',
                    'scrambled_word': '',
                    'hint_used': False,
                    'game_active': False,
                    'game_complete': False,
                    'show_interstitial': False,
                    'feedback_message': '',
                    'feedback_type': 'info',
                    'round_completed': False
                }
                st.rerun()

        with col_b:
            if st.button("🏠 Main Menu", use_container_width=True):
                # Reset to welcome screen
                st.session_state.game_state['game_complete'] = False
                st.rerun()

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

if __name__ == "__main__":
    main()
