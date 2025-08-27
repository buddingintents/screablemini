import streamlit as st
import random
import time
import json
import streamlit.components.v1 as components
from datetime import datetime, timedelta
import hashlib
import math

# Configure page
st.set_page_config(
    page_title="Word Scramble Mini Pro",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Game configuration
GAME_CONFIG = {
    "base_rounds": 5,
    "base_time_per_round": 60,
    "base_points_per_correct": 10,
    "time_bonus_multiplier": 0.1,
    "xp_per_game": 50,
    "xp_per_correct": 25,
    "level_up_base_xp": 500,
    "daily_streak_bonus": 1.2,
    "achievement_xp_bonus": 100
}

# Enhanced word database with categories and difficulty levels
WORD_DATABASE = {
    "easy": {
        "animals": ["CAT", "DOG", "FISH", "BIRD", "BEAR", "LION", "FROG", "DUCK"],
        "colors": ["RED", "BLUE", "GREEN", "BLACK", "WHITE", "PINK", "GOLD"],
        "food": ["CAKE", "MILK", "BREAD", "RICE", "MEAT", "FISH", "SOUP"],
        "objects": ["BOOK", "CHAIR", "DOOR", "LAMP", "DESK", "PHONE", "CLOCK"]
    },
    "medium": {
        "animals": ["ELEPHANT", "GIRAFFE", "MONKEY", "RABBIT", "TURTLE", "CHICKEN", "DOLPHIN"],
        "countries": ["FRANCE", "BRAZIL", "CANADA", "EGYPT", "JAPAN", "RUSSIA", "MEXICO"],
        "technology": ["PYTHON", "STREAM", "CODING", "LAPTOP", "MOBILE", "TABLET", "CAMERA"],
        "nature": ["JUNGLE", "PLANET", "FOREST", "GARDEN", "FLOWER", "SUNSET", "WINTER"]
    },
    "hard": {
        "advanced": ["ALGORITHM", "PHILOSOPHY", "METAMORPHOSIS", "ENCYCLOPEDIA", "ARCHITECTURE"],
        "science": ["CHEMISTRY", "PSYCHOLOGY", "GEOGRAPHY", "ASTRONOMY", "MATHEMATICS"],
        "professional": ["ENGINEERING", "MANAGEMENT", "DEVELOPMENT", "ADMINISTRATION", "COORDINATION"],
        "complex": ["EXTRAORDINARY", "ENTREPRENEURSHIP", "RESPONSIBILITY", "CHARACTERISTICS", "TRANSFORMATION"]
    }
}

# Achievement definitions
ACHIEVEMENTS = {
    "first_game": {"name": "Getting Started", "desc": "Complete your first game", "xp": 100, "icon": "🎮"},
    "perfect_game": {"name": "Perfectionist", "desc": "Get all words correct in one game", "xp": 200, "icon": "🎯"},
    "speed_demon": {"name": "Speed Demon", "desc": "Solve a word in under 10 seconds", "xp": 150, "icon": "⚡"},
    "streak_3": {"name": "Hot Streak", "desc": "Get 3 words correct in a row", "xp": 100, "icon": "🔥"},
    "streak_7": {"name": "Daily Warrior", "desc": "Play for 7 consecutive days", "xp": 300, "icon": "🗡️"},
    "word_master": {"name": "Word Master", "desc": "Solve 100 words total", "xp": 500, "icon": "📚"},
    "hint_less": {"name": "No Help Needed", "desc": "Complete a game without using hints", "xp": 250, "icon": "🧠"},
    "power_user": {"name": "Power User", "desc": "Use 10 power-ups in total", "xp": 200, "icon": "⭐"},
    "social_butterfly": {"name": "Social Butterfly", "desc": "Share your score", "xp": 150, "icon": "📱"},
    "level_10": {"name": "Rising Star", "desc": "Reach level 10", "xp": 400, "icon": "🌟"},
    "category_master": {"name": "Category Expert", "desc": "Complete all categories", "xp": 600, "icon": "🏆"}
}

# Power-up definitions
POWER_UPS = {
    "time_freeze": {"name": "Time Freeze", "desc": "Pause timer for 10 seconds", "cost": 2, "icon": "⏰", "duration": 10},
    "double_points": {"name": "Double Points", "desc": "2x points for this round", "cost": 3, "icon": "💰", "multiplier": 2},
    "letter_reveal": {"name": "Letter Reveal", "desc": "Show 2 random letters", "cost": 2, "icon": "💡", "count": 2},
    "word_bank": {"name": "Word Bank", "desc": "Show 3 possible answers", "cost": 4, "icon": "📝", "options": 3},
    "shuffle_master": {"name": "Shuffle Master", "desc": "Re-scramble optimally", "cost": 1, "icon": "🔄", "uses": 1}
}

def add_adsense_meta_tag():
    """Add Google AdSense account verification meta tag"""
    meta_html = """
    <script>
    if (!document.querySelector('meta[name="google-adsense-account"]')) {
        var meta = document.createElement('meta');
        meta.name = 'google-adsense-account';
        meta.content = 'ca-pub-2020561089374332';
        document.head.appendChild(meta);
    }
    </script>
    """
    components.html(meta_html, height=0)

def show_banner_ad(ad_type="top"):
    """Display banner advertisement using Google AdSense"""
    try:
        adsense_client = st.secrets["google"]["adsense_client_id"]
        ad_slot = st.secrets["google"][f"{ad_type}_ad_slot"]
    except:
        adsense_client = "ca-pub-2020561089374332"
        ad_slot = "1234567890"

    ad_html = f"""
    <div style="text-align: center; margin: 20px 0;">
        <script>
        if (!document.querySelector('meta[name="google-adsense-account"]')) {{
            var meta = document.createElement('meta');
            meta.name = 'google-adsense-account';
            meta.content = 'ca-pub-2020561089374332';
            document.head.appendChild(meta);
        }}
        </script>

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

def show_rewarded_ad(reward_type="power_up"):
    """Display rewarded advertisement"""
    try:
        adsense_client = st.secrets["google"]["adsense_client_id"]
        rewarded_slot = st.secrets["google"]["rewarded_ad_slot"]
    except:
        adsense_client = "ca-pub-2020561089374332"
        rewarded_slot = "1234567890"

    reward_messages = {
        "power_up": "🎁 Watch ad to earn a free power-up!",
        "hint": "💡 Watch ad to unlock a premium hint!",
        "xp": "⭐ Watch ad to earn bonus XP!",
        "coins": "💰 Watch ad to earn coins!"
    }

    ad_html = f"""
    <div style="text-align: center; padding: 30px; background: #fff8dc; border: 2px solid #ffd700; border-radius: 10px;">
        <h4 style="color: #b8860b; margin-bottom: 15px;">{reward_messages.get(reward_type, "🎁 Free Reward!")}</h4>
        <p style="color: #666; margin-bottom: 20px;">Support the game and earn rewards!</p>

        <script>
        if (!document.querySelector('meta[name="google-adsense-account"]')) {{
            var meta = document.createElement('meta');
            meta.name = 'google-adsense-account';
            meta.content = 'ca-pub-2020561089374332';
            document.head.appendChild(meta);
        }}
        </script>

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

def init_player_profile():
    """Initialize comprehensive player profile"""
    if 'player_profile' not in st.session_state:
        st.session_state.player_profile = {
            'level': 1,
            'xp': 0,
            'total_games': 0,
            'total_words_solved': 0,
            'total_score': 0,
            'current_streak': 0,
            'best_streak': 0,
            'last_played': None,
            'daily_streak': 0,
            'coins': 5,  # In-game currency
            'power_ups': {'time_freeze': 1, 'double_points': 1, 'letter_reveal': 2},
            'achievements_unlocked': [],
            'statistics': {
                'games_played': 0,
                'words_correct': 0,
                'words_total': 0,
                'average_time': 0,
                'fastest_solve': float('inf'),
                'perfect_games': 0,
                'hints_used': 0,
                'power_ups_used': 0
            },
            'preferences': {
                'difficulty': 'medium',
                'preferred_categories': [],
                'auto_difficulty': True,
                'sound_enabled': True
            }
        }

def init_session_state():
    """Initialize all session state variables"""
    if 'initialized' not in st.session_state:
        # Game state
        st.session_state.screen = 'home'
        st.session_state.game_mode = 'classic'
        st.session_state.current_round = 1
        st.session_state.score = 0
        st.session_state.current_word = ''
        st.session_state.scrambled_word = ''
        st.session_state.current_category = ''
        st.session_state.current_difficulty = 'medium'
        st.session_state.round_start_time = None
        st.session_state.hint_used = False
        st.session_state.hints_available = {'category': True, 'definition': True, 'shuffle': True, 'reveal': True}
        st.session_state.feedback_message = ''
        st.session_state.feedback_type = 'info'
        st.session_state.awaiting_next_round = False
        st.session_state.last_update = time.time()
        st.session_state.game_complete = False
        st.session_state.round_results = []

        # Enhanced features
        st.session_state.active_power_ups = {}
        st.session_state.round_multiplier = 1
        st.session_state.time_freeze_remaining = 0
        st.session_state.letters_revealed = []
        st.session_state.word_bank_shown = False

        # Game modes
        st.session_state.total_rounds = GAME_CONFIG['base_rounds']
        st.session_state.time_per_round = GAME_CONFIG['base_time_per_round']

        # Social features
        st.session_state.show_leaderboard = False
        st.session_state.leaderboard_data = []

        st.session_state.initialized = True

    # Always ensure player profile is initialized
    init_player_profile()

def get_player_level_info():
    """Calculate level progression info"""
    profile = st.session_state.player_profile
    current_level = profile['level']
    current_xp = profile['xp']

    # Calculate XP needed for current level
    xp_for_current_level = GAME_CONFIG['level_up_base_xp'] * (current_level - 1) * 1.5
    xp_for_next_level = GAME_CONFIG['level_up_base_xp'] * current_level * 1.5

    xp_progress = current_xp - xp_for_current_level
    xp_needed = xp_for_next_level - xp_for_current_level

    progress_percentage = min(100, (xp_progress / xp_needed) * 100) if xp_needed > 0 else 100

    return {
        'current_level': current_level,
        'xp_progress': xp_progress,
        'xp_needed': xp_needed,
        'progress_percentage': progress_percentage,
        'next_level': current_level + 1
    }

def add_xp(amount, reason=""):
    """Add XP and handle level ups"""
    profile = st.session_state.player_profile
    profile['xp'] += amount

    # Check for level up
    level_info = get_player_level_info()
    if level_info['progress_percentage'] >= 100:
        profile['level'] += 1
        profile['coins'] += profile['level'] * 2  # Coins reward for leveling
        st.success(f"🎉 Level Up! You're now level {profile['level']}! Earned {profile['level'] * 2} coins!")

        # Check for level-based achievements
        if profile['level'] == 10:
            unlock_achievement('level_10')

def unlock_achievement(achievement_id):
    """Unlock an achievement and add rewards"""
    if achievement_id not in st.session_state.player_profile['achievements_unlocked']:
        achievement = ACHIEVEMENTS[achievement_id]
        st.session_state.player_profile['achievements_unlocked'].append(achievement_id)
        add_xp(achievement['xp'], f"Achievement: {achievement['name']}")
        st.success(f"🏆 Achievement Unlocked: {achievement['icon']} {achievement['name']}!")

def select_word_by_difficulty():
    """Intelligent word selection based on player performance and preferences"""
    profile = st.session_state.player_profile

    if profile['preferences']['auto_difficulty']:
        # AI-driven difficulty adjustment
        accuracy = profile['statistics']['words_correct'] / max(1, profile['statistics']['words_total'])

        if accuracy < 0.4:
            difficulty = 'easy'
        elif accuracy > 0.8:
            difficulty = 'hard'
        else:
            difficulty = 'medium'
    else:
        difficulty = profile['preferences']['difficulty']

    # Select category
    categories = list(WORD_DATABASE[difficulty].keys())
    if profile['preferences']['preferred_categories']:
        available_categories = [cat for cat in profile['preferences']['preferred_categories'] 
                              if cat in categories]
        if available_categories:
            categories = available_categories

    category = random.choice(categories)
    word = random.choice(WORD_DATABASE[difficulty][category])

    st.session_state.current_difficulty = difficulty
    st.session_state.current_category = category

    return word, category, difficulty

def scramble_word(word):
    """Advanced word scrambling with multiple algorithms"""
    letters = list(word)

    # Different scrambling strategies for variety
    strategies = ['random', 'vowel_separate', 'reverse_chunks']
    strategy = random.choice(strategies)

    if strategy == 'random':
        random.shuffle(letters)
    elif strategy == 'vowel_separate':
        vowels = [l for l in letters if l.lower() in 'aeiou']
        consonants = [l for l in letters if l.lower() not in 'aeiou']
        random.shuffle(vowels)
        random.shuffle(consonants)
        letters = vowels + consonants
    elif strategy == 'reverse_chunks':
        mid = len(letters) // 2
        letters = letters[mid:] + letters[:mid]
        random.shuffle(letters)

    scrambled = ''.join(letters)
    return scrambled if scrambled != word else scramble_word(word)

def get_hint(hint_type):
    """Enhanced hint system with multiple types"""
    word = st.session_state.current_word
    category = st.session_state.current_category

    hints = {
        'category': f"💡 Category: This is a {category.replace('_', ' ')}",
        'definition': get_word_definition(word),
        'shuffle': f"🔄 Try this arrangement: {scramble_word(word)}",
        'reveal': get_letter_reveal_hint(word)
    }

    return hints.get(hint_type, "No hint available")

def get_word_definition(word):
    """Generate contextual definitions for words"""
    definitions = {
        # Animals
        'CAT': '🐱 A small domesticated carnivorous mammal',
        'DOG': '🐕 A domesticated descendant of the wolf',
        'ELEPHANT': '🐘 The largest existing land animal',
        'GIRAFFE': '🦒 The tallest living terrestrial animal',

        # Technology
        'PYTHON': '🐍 A high-level programming language',
        'CODING': '💻 The process of creating computer software',
        'ALGORITHM': '⚙️ A step-by-step procedure for solving problems',

        # Nature
        'FOREST': '🌲 A large area covered chiefly with trees',
        'SUNSET': '🌅 The time when the sun disappears below the horizon',

        # Default
        'DEFAULT': f'💭 A word related to {st.session_state.current_category}'
    }

    return definitions.get(word, definitions['DEFAULT'])

def get_letter_reveal_hint(word):
    """Smart letter reveal based on difficulty"""
    if len(word) <= 4:
        return f"💡 First letter: {word[0]}"
    elif len(word) <= 7:
        return f"💡 Letters: {word[0]}_{'_' * (len(word)-2)}{word[-1]}"
    else:
        mid = len(word) // 2
        return f"💡 Letters: {word[0]}_{word[mid]}_{'_' * (len(word)-3)}{word[-1]}"

def use_power_up(power_up_type):
    """Activate power-up effects"""
    if power_up_type in st.session_state.player_profile['power_ups']:
        if st.session_state.player_profile['power_ups'][power_up_type] > 0:
            st.session_state.player_profile['power_ups'][power_up_type] -= 1
            st.session_state.player_profile['statistics']['power_ups_used'] += 1

            if power_up_type == 'time_freeze':
                st.session_state.time_freeze_remaining = POWER_UPS['time_freeze']['duration']
                st.success("⏰ Time frozen for 10 seconds!")
            elif power_up_type == 'double_points':
                st.session_state.round_multiplier = 2
                st.success("💰 Double points activated for this round!")
            elif power_up_type == 'letter_reveal':
                word = st.session_state.current_word
                available_positions = [i for i in range(len(word)) if i not in st.session_state.letters_revealed]
                if available_positions:
                    reveal_positions = random.sample(available_positions, min(2, len(available_positions)))
                    st.session_state.letters_revealed.extend(reveal_positions)
                    st.success(f"💡 Letters revealed at positions: {[p+1 for p in reveal_positions]}")
            elif power_up_type == 'word_bank':
                st.session_state.word_bank_shown = True
                st.success("📝 Word bank activated!")
            elif power_up_type == 'shuffle_master':
                st.session_state.scrambled_word = scramble_word(st.session_state.current_word)
                st.success("🔄 Word re-scrambled optimally!")

            # Check achievement
            if st.session_state.player_profile['statistics']['power_ups_used'] >= 10:
                unlock_achievement('power_user')

            return True
    return False

def calculate_score(time_taken, difficulty, hints_used):
    """Advanced scoring system with multiple factors"""
    base_points = GAME_CONFIG['base_points_per_correct']

    # Difficulty multiplier
    difficulty_multipliers = {'easy': 1.0, 'medium': 1.5, 'hard': 2.0}
    difficulty_bonus = base_points * difficulty_multipliers[difficulty]

    # Time bonus
    time_remaining = max(0, st.session_state.time_per_round - time_taken)
    time_bonus = int(time_remaining * GAME_CONFIG['time_bonus_multiplier'])

    # Hint penalty
    hint_penalty = hints_used * 2

    # Round multiplier (power-ups)
    multiplier = st.session_state.round_multiplier

    # Streak bonus
    streak_bonus = min(st.session_state.player_profile['current_streak'] * 2, 20)

    total_score = int((difficulty_bonus + time_bonus + streak_bonus - hint_penalty) * multiplier)

    return max(5, total_score)  # Minimum 5 points

def start_new_round():
    """Initialize a new game round with enhanced features"""
    word, category, difficulty = select_word_by_difficulty()

    st.session_state.current_word = word
    st.session_state.scrambled_word = scramble_word(word)
    st.session_state.current_category = category
    st.session_state.current_difficulty = difficulty
    st.session_state.round_start_time = time.time()
    st.session_state.hint_used = False
    st.session_state.hints_available = {'category': True, 'definition': True, 'shuffle': True, 'reveal': True}
    st.session_state.feedback_message = ''
    st.session_state.feedback_type = 'info'
    st.session_state.awaiting_next_round = False
    st.session_state.last_update = time.time()
    st.session_state.screen = 'playing'

    # Reset round-specific power-up effects
    st.session_state.round_multiplier = 1
    st.session_state.letters_revealed = []
    st.session_state.word_bank_shown = False

def process_guess(user_guess):
    """Process user guess with comprehensive feedback"""
    current_word = st.session_state.current_word
    start_time = st.session_state.round_start_time

    if user_guess == current_word:
        # Correct guess
        elapsed_time = time.time() - start_time
        hints_used = len([h for h in st.session_state.hints_available.values() if not h])

        round_score = calculate_score(elapsed_time, st.session_state.current_difficulty, hints_used)
        st.session_state.score += round_score

        # Update player statistics
        profile = st.session_state.player_profile
        profile['statistics']['words_correct'] += 1
        profile['statistics']['words_total'] += 1
        profile['current_streak'] += 1
        profile['best_streak'] = max(profile['best_streak'], profile['current_streak'])

        if elapsed_time < profile['statistics']['fastest_solve']:
            profile['statistics']['fastest_solve'] = elapsed_time

        # Store round result
        st.session_state.round_results.append({
            'word': current_word,
            'time': elapsed_time,
            'score': round_score,
            'difficulty': st.session_state.current_difficulty,
            'correct': True
        })

        st.session_state.feedback_message = f"🎉 Correct! '{current_word}' is right! +{round_score} points!"
        st.session_state.feedback_type = 'success'
        st.session_state.awaiting_next_round = True

        # Check achievements
        if elapsed_time < 10:
            unlock_achievement('speed_demon')
        if st.session_state.player_profile['current_streak'] >= 3:
            unlock_achievement('streak_3')
        if hints_used == 0 and st.session_state.current_round == st.session_state.total_rounds:
            unlock_achievement('hint_less')

        # XP reward
        difficulty_xp = {'easy': 15, 'medium': 25, 'hard': 40}
        add_xp(difficulty_xp[st.session_state.current_difficulty], "Correct answer")

    else:
        # Incorrect guess
        st.session_state.player_profile['statistics']['words_total'] += 1
        st.session_state.player_profile['current_streak'] = 0

        st.session_state.round_results.append({
            'word': current_word,
            'time': time.time() - start_time,
            'score': 0,
            'difficulty': st.session_state.current_difficulty,
            'correct': False
        })

        st.session_state.feedback_message = f"❌ '{user_guess}' is incorrect. The word was '{current_word}'"
        st.session_state.feedback_type = 'error'
        st.session_state.awaiting_next_round = True

def get_game_modes():
    """Define available game modes"""
    return {
        'classic': {
            'name': 'Classic Mode',
            'desc': 'Traditional 5-round word scramble',
            'rounds': 5,
            'time_per_round': 60,
            'icon': '🎯'
        },
        'speed': {
            'name': 'Speed Challenge',
            'desc': '10 rounds, 30 seconds each',
            'rounds': 10,
            'time_per_round': 30,
            'icon': '⚡'
        },
        'marathon': {
            'name': 'Marathon Mode',
            'desc': '20 rounds with increasing difficulty',
            'rounds': 20,
            'time_per_round': 45,
            'icon': '🏃'
        },
        'themed': {
            'name': 'Category Challenge',
            'desc': 'Focus on specific word categories',
            'rounds': 8,
            'time_per_round': 50,
            'icon': '📚'
        }
    }

def create_auto_refresh_timer():
    """Enhanced timer with power-up effects"""
    start_time = st.session_state.round_start_time
    round_duration = st.session_state.time_per_round
    time_freeze = st.session_state.time_freeze_remaining

    timer_html = f"""
    <div id="timer-container" style="text-align: center; margin: 10px 0;">
        <div id="countdown-timer" style="font-size: 1.8em; font-weight: bold; color: #27ae60; 
             background: #eafaf1; padding: 15px; border-radius: 12px; border: 3px solid #27ae60;">
            ⏰ <span id="timer-display">{round_duration}</span>s
            <div id="freeze-indicator" style="display: none; color: #3498db; font-size: 0.8em;">
                ❄️ FROZEN ❄️
            </div>
        </div>
        <div id="progress-container" style="margin-top: 10px;">
            <div style="background: #ecf0f1; height: 10px; border-radius: 5px; overflow: hidden; border: 1px solid #bdc3c7;">
                <div id="progress-bar" style="background: linear-gradient(90deg, #27ae60, #f1c40f, #e74c3c); 
                     height: 100%; width: 100%; transition: width 1s linear;"></div>
            </div>
        </div>
    </div>

    <script>
    let startTime = {start_time};
    let roundDuration = {round_duration};
    let timeFrozen = {time_freeze};
    let freezeStartTime = Date.now() / 1000;

    function updateTimer() {{
        let currentTime = Date.now() / 1000;
        let elapsed = currentTime - startTime;

        // Handle time freeze
        if (timeFrozen > 0) {{
            document.getElementById('freeze-indicator').style.display = 'block';
            let freezeRemaining = timeFrozen - (currentTime - freezeStartTime);
            if (freezeRemaining <= 0) {{
                timeFrozen = 0;
                startTime = currentTime - elapsed;
                document.getElementById('freeze-indicator').style.display = 'none';
            }}
            return; // Don't update timer while frozen
        }}

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
                timerElement.style.animation = 'pulse 0.5s infinite';
            }}
        }} else if (timeLeft <= 30) {{
            timerElement.style.color = '#f39c12';
            timerElement.style.background = '#fef9e7';
            timerElement.style.borderColor = '#f39c12';
        }}

        if (timeLeft <= 0) {{
            window.parent.postMessage({{type: 'time_up'}}, '*');
        }}
    }}

    let style = document.createElement('style');
    style.textContent = `
        @keyframes pulse {{
            0% {{ transform: scale(1); }}
            50% {{ transform: scale(1.1); }}
            100% {{ transform: scale(1); }}
        }}
    `;
    document.head.appendChild(style);

    updateTimer();
    let timerInterval = setInterval(updateTimer, 1000);

    window.addEventListener('message', function(event) {{
        if (event.data.type === 'freeze_time') {{
            timeFrozen = event.data.duration;
            freezeStartTime = Date.now() / 1000;
        }}
    }});
    </script>
    """
    return timer_html

def generate_leaderboard():
    """Generate mock leaderboard data"""
    # In a real app, this would connect to a database
    mock_data = [
        {"name": "WordMaster", "score": 2450, "level": 15, "games": 127},
        {"name": "SpeedDemon", "score": 2380, "level": 14, "games": 98},
        {"name": "BrainPower", "score": 2220, "level": 12, "games": 156},
        {"name": "QuickThink", "score": 2100, "level": 11, "games": 89},
        {"name": "PuzzlePro", "score": 1980, "level": 10, "games": 143},
        {"name": "You", "score": st.session_state.player_profile['total_score'], "level": st.session_state.player_profile['level'], "games": st.session_state.player_profile['total_games']}
    ]

    return sorted(mock_data, key=lambda x: x['score'], reverse=True)

def main():
    """Main application with all enhanced features"""
    init_session_state()
    add_adsense_meta_tag()

    # Enhanced CSS with new features
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 25px 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 25px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }
    .player-stats {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .power-up-card {
        background: linear-gradient(135deg, #ff9a56 0%, #ffad56 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        text-align: center;
        cursor: pointer;
        transition: transform 0.2s;
    }
    .power-up-card:hover {
        transform: scale(1.05);
    }
    .achievement-badge {
        background: linear-gradient(135deg, #ffd700 0%, #ffed4a 100%);
        color: #333;
        padding: 10px;
        border-radius: 20px;
        margin: 5px;
        display: inline-block;
        font-size: 0.9em;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .game-mode-card {
        background: white;
        border: 2px solid #e3f2fd;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .game-mode-card:hover {
        border-color: #2196f3;
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
    }
    .scrambled-word {
        font-size: 3.5em;
        font-weight: bold;
        text-align: center;
        color: #4CAF50;
        letter-spacing: 0.3em;
        margin: 25px 0;
        padding: 25px;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 15px;
        border: 3px dashed #4CAF50;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
    }
    .word-reveal {
        background: #fff3cd;
        border: 2px solid #ffc107;
        color: #856404;
        padding: 10px;
        border-radius: 8px;
        margin: 10px 0;
        text-align: center;
        font-weight: bold;
    }
    .leaderboard-item {
        background: white;
        border-left: 4px solid #4CAF50;
        padding: 15px;
        margin: 8px 0;
        border-radius: 0 8px 8px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .final-score-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        color: #2c3e50;
        border: 3px solid #4CAF50;
        padding: 40px;
        border-radius: 20px;
        margin: 25px 0;
        box-shadow: 0 12px 24px rgba(76, 175, 80, 0.2);
        text-align: center;
    }
    .xp-progress {
        background: #e9ecef;
        height: 20px;
        border-radius: 10px;
        overflow: hidden;
        margin: 10px 0;
    }
    .xp-fill {
        background: linear-gradient(90deg, #4CAF50, #45a049);
        height: 100%;
        transition: width 0.5s ease;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Auto-refresh mechanism
    if st.session_state.screen == 'playing' and st.session_state.round_start_time:
        current_time = time.time()
        elapsed = current_time - st.session_state.round_start_time

        if current_time - st.session_state.last_update >= 2.0:
            st.session_state.last_update = current_time

            # Handle time freeze
            if st.session_state.time_freeze_remaining > 0:
                st.session_state.time_freeze_remaining = max(0, st.session_state.time_freeze_remaining - 2)
            else:
                if elapsed >= st.session_state.time_per_round and not st.session_state.awaiting_next_round:
                    st.session_state.feedback_message = f"⏰ Time's up! The word was '{st.session_state.current_word}'"
                    st.session_state.feedback_type = 'error'
                    st.session_state.awaiting_next_round = True

                    # Record as incorrect
                    st.session_state.player_profile['statistics']['words_total'] += 1
                    st.session_state.player_profile['current_streak'] = 0

            st.rerun()

    # Top banner advertisement
    show_banner_ad("top")

    # Enhanced header with player info
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="main-header">
            <h1>🎯 Word Scramble Mini Pro</h1>
            <p>Ultimate word unscrambling experience!</p>
        </div>
        """, unsafe_allow_html=True)

    # Player stats header
    if st.session_state.screen != 'home':
        profile = st.session_state.player_profile
        level_info = get_player_level_info()

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="player-stats">
                <div style="font-size: 1.2em; font-weight: bold;">🏆 Level {profile['level']}</div>
                <div style="font-size: 0.9em; opacity: 0.9;">XP: {profile['xp']}</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="player-stats">
                <div style="font-size: 1.2em; font-weight: bold;">💰 {profile['coins']} Coins</div>
                <div style="font-size: 0.9em; opacity: 0.9;">Total Score: {profile['total_score']}</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="player-stats">
                <div style="font-size: 1.2em; font-weight: bold;">🔥 {profile['current_streak']} Streak</div>
                <div style="font-size: 0.9em; opacity: 0.9;">Best: {profile['best_streak']}</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="player-stats">
                <div style="font-size: 1.2em; font-weight: bold;">📊 {len(profile['achievements_unlocked'])} Badges</div>
                <div style="font-size: 0.9em; opacity: 0.9;">Games: {profile['total_games']}</div>
            </div>
            """, unsafe_allow_html=True)

        # XP Progress bar
        st.markdown(f"""
        <div class="xp-progress">
            <div class="xp-fill" style="width: {level_info['progress_percentage']}%"></div>
        </div>
        <div style="text-align: center; font-size: 0.9em; color: #666;">
            {int(level_info['xp_progress'])}/{int(level_info['xp_needed'])} XP to Level {level_info['next_level']}
        </div>
        """, unsafe_allow_html=True)

    # Screen routing
    if st.session_state.screen == 'home':
        show_home_screen()
    elif st.session_state.screen == 'mode_select':
        show_mode_selection_screen()
    elif st.session_state.screen == 'playing':
        show_enhanced_game_screen()
    elif st.session_state.screen == 'complete':
        show_enhanced_final_screen()
    elif st.session_state.screen == 'leaderboard':
        show_leaderboard_screen()
    elif st.session_state.screen == 'achievements':
        show_achievements_screen()
    elif st.session_state.screen == 'shop':
        show_shop_screen()

    # Footer advertisement
    st.markdown("---")
    show_banner_ad("footer")

def show_home_screen():
    """Enhanced home screen with all features"""
    st.markdown("### 🎮 Welcome to Word Scramble Mini Pro!")

    # Recent achievements
    profile = st.session_state.player_profile
    if profile['achievements_unlocked']:
        st.markdown("#### 🏆 Recent Achievements")
        recent_achievements = profile['achievements_unlocked'][-3:]
        cols = st.columns(len(recent_achievements))
        for i, achievement_id in enumerate(recent_achievements):
            achievement = ACHIEVEMENTS[achievement_id]
            with cols[i]:
                st.markdown(f"""
                <div class="achievement-badge">
                    {achievement['icon']} {achievement['name']}
                </div>
                """, unsafe_allow_html=True)

    # Main menu options
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🎯 Start Game", type="primary", use_container_width=True):
            st.session_state.screen = 'mode_select'
            st.rerun()

    with col2:
        if st.button("🏆 Leaderboard", use_container_width=True):
            st.session_state.screen = 'leaderboard'
            st.rerun()

    with col3:
        if st.button("🏅 Achievements", use_container_width=True):
            st.session_state.screen = 'achievements'
            st.rerun()

    # Secondary options
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🛒 Power-up Shop", use_container_width=True):
            st.session_state.screen = 'shop'
            st.rerun()

    with col2:
        if st.button("📊 Statistics", use_container_width=True):
            show_statistics_modal()

    with col3:
        if st.button("⚙️ Settings", use_container_width=True):
            show_settings_modal()

def show_mode_selection_screen():
    """Game mode selection with detailed info"""
    st.markdown("### 🎮 Select Game Mode")

    game_modes = get_game_modes()

    for mode_id, mode_info in game_modes.items():
        with st.container():
            st.markdown(f"""
            <div class="game-mode-card">
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <div>
                        <h4 style="margin: 0; color: #2c3e50;">{mode_info['icon']} {mode_info['name']}</h4>
                        <p style="margin: 5px 0; color: #7f8c8d;">{mode_info['desc']}</p>
                        <small style="color: #95a5a6;">
                            {mode_info['rounds']} rounds • {mode_info['time_per_round']}s per round
                        </small>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Play {mode_info['name']}", key=f"play_{mode_id}", use_container_width=True):
                st.session_state.game_mode = mode_id
                st.session_state.total_rounds = mode_info['rounds']
                st.session_state.time_per_round = mode_info['time_per_round']
                start_new_round()
                st.rerun()

    if st.button("🏠 Back to Home", use_container_width=True):
        st.session_state.screen = 'home'
        st.rerun()

def show_enhanced_game_screen():
    """Enhanced gameplay screen with all features"""
    # Game stats with power-up indicators
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Round", f"{st.session_state.current_round}/{st.session_state.total_rounds}")
    with col2:
        multiplier_text = f" (×{st.session_state.round_multiplier})" if st.session_state.round_multiplier > 1 else ""
        st.metric("Score", f"{st.session_state.score}{multiplier_text}")
    with col3:
        if st.session_state.round_start_time:
            elapsed = time.time() - st.session_state.round_start_time
            time_left = max(0, st.session_state.time_per_round - elapsed)

            if st.session_state.time_freeze_remaining > 0:
                st.metric("❄️ Time Frozen", f"{int(st.session_state.time_freeze_remaining)}s")
            elif time_left <= 10:
                st.metric("⚠️ Time Left", f"{int(time_left)}s", delta="Hurry!")
            else:
                st.metric("⏰ Time Left", f"{int(time_left)}s")
        else:
            st.metric("Time Left", f"{st.session_state.time_per_round}s")
    with col4:
        difficulty_colors = {'easy': '🟢', 'medium': '🟡', 'hard': '🔴'}
        st.metric("Difficulty", f"{difficulty_colors.get(st.session_state.current_difficulty, '⚪')} {st.session_state.current_difficulty.title()}")

    # Auto-updating visual timer
    if st.session_state.round_start_time and not st.session_state.awaiting_next_round:
        timer_html = create_auto_refresh_timer()
        components.html(timer_html, height=120)

    # Power-ups panel
    st.markdown("#### ⚡ Power-ups")
    power_up_cols = st.columns(5)

    for i, (power_id, power_info) in enumerate(POWER_UPS.items()):
        with power_up_cols[i]:
            available = st.session_state.player_profile['power_ups'].get(power_id, 0)
            if available > 0 and not st.session_state.awaiting_next_round:
                if st.button(f"{power_info['icon']} {power_info['name']} ({available})", 
                           key=f"power_{power_id}", use_container_width=True):
                    use_power_up(power_id)
                    st.rerun()
            else:
                st.markdown(f"""
                <div style="text-align: center; padding: 8px; background: #f8f9fa; border-radius: 5px; color: #6c757d;">
                    {power_info['icon']}<br>{available}
                </div>
                """, unsafe_allow_html=True)

    # Enhanced word display with letter reveals
    word_display = st.session_state.scrambled_word
    if st.session_state.letters_revealed:
        word_list = list(word_display)
        for pos in st.session_state.letters_revealed:
            if pos < len(word_list):
                word_list[pos] = f"<span style='color: #e74c3c; background: #ffebee; padding: 2px 4px; border-radius: 3px;'>{st.session_state.current_word[pos]}</span>"
        word_display = "".join(word_list)

    st.markdown(f"""
    <div class="scrambled-word">
        {word_display}
    </div>
    """, unsafe_allow_html=True)

    # Word bank (if power-up is active)
    if st.session_state.word_bank_shown:
        word = st.session_state.current_word
        fake_words = generate_fake_words(word, 2)
        options = [word] + fake_words
        random.shuffle(options)

        st.markdown("""
        <div class="word-reveal">
            💡 Word Bank: Choose from these options
        </div>
        """, unsafe_allow_html=True)

        bank_cols = st.columns(len(options))
        for i, option in enumerate(options):
            with bank_cols[i]:
                if st.button(option, key=f"bank_{i}", use_container_width=True):
                    process_guess(option)
                    st.rerun()

    # Hint system
    if not st.session_state.awaiting_next_round and not st.session_state.word_bank_shown:
        st.markdown("#### 💡 Hints Available")
        hint_cols = st.columns(4)

        hint_types = {
            'category': ('📂', 'Category'),
            'definition': ('📖', 'Definition'),  
            'shuffle': ('🔄', 'Re-scramble'),
            'reveal': ('💡', 'Letter Reveal')
        }

        for i, (hint_id, (icon, name)) in enumerate(hint_types.items()):
            with hint_cols[i]:
                if st.session_state.hints_available[hint_id]:
                    if st.button(f"{icon} {name}", key=f"hint_{hint_id}", use_container_width=True):
                        hint_text = get_hint(hint_id)
                        st.info(hint_text)
                        st.session_state.hints_available[hint_id] = False
                        st.session_state.player_profile['statistics']['hints_used'] += 1
                        st.rerun()
                else:
                    st.markdown(f"""
                    <div style="text-align: center; padding: 8px; background: #f8f9fa; border-radius: 5px; color: #6c757d;">
                        {icon} Used
                    </div>
                    """, unsafe_allow_html=True)

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

            col1, col2, col3 = st.columns(3)
            with col1:
                submit_guess = st.form_submit_button("Submit Guess", type="primary", use_container_width=True)
            with col2:
                skip_round = st.form_submit_button("Skip Round", use_container_width=True)
            with col3:
                watch_ad = st.form_submit_button("📺 Free Hint", use_container_width=True)

        if submit_guess:
            if user_guess.strip():
                process_guess(user_guess.strip().upper())
                st.rerun()
            else:
                st.warning("Please enter a word!")

        if skip_round:
            process_guess("__SKIP__")  # Process as incorrect
            st.rerun()

        if watch_ad:
            show_rewarded_ad("hint")
            # Grant a free hint
            available_hints = [k for k, v in st.session_state.hints_available.items() if v]
            if available_hints:
                hint_id = random.choice(available_hints)
                hint_text = get_hint(hint_id)
                st.success(f"🎁 Free hint earned! {hint_text}")
                st.session_state.hints_available[hint_id] = False
                st.rerun()
    else:
        # Show next round button
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎯 Next Round", type="primary", use_container_width=True):
                next_round()
                st.rerun()
        with col2:
            if st.button("📺 Earn Power-up", use_container_width=True):
                show_rewarded_ad("power_up")
                # Grant random power-up
                power_up = random.choice(list(POWER_UPS.keys()))
                st.session_state.player_profile['power_ups'][power_up] = st.session_state.player_profile['power_ups'].get(power_up, 0) + 1
                st.success(f"🎁 Earned {POWER_UPS[power_up]['name']}!")
                st.rerun()

def next_round():
    """Enhanced round progression"""
    st.session_state.current_round += 1
    st.session_state.feedback_message = ''
    st.session_state.awaiting_next_round = False

    if st.session_state.current_round <= st.session_state.total_rounds:
        start_new_round()
    else:
        # Game complete
        profile = st.session_state.player_profile
        profile['total_games'] += 1
        profile['total_score'] += st.session_state.score

        # Check for perfect game
        all_correct = all(r['correct'] for r in st.session_state.round_results)
        if all_correct:
            unlock_achievement('perfect_game')
            profile['statistics']['perfect_games'] += 1

        # Check first game
        if profile['total_games'] == 1:
            unlock_achievement('first_game')

        # Check word master (100 words)
        if profile['statistics']['words_correct'] >= 100:
            unlock_achievement('word_master')

        # Add game completion XP
        add_xp(GAME_CONFIG['xp_per_game'], "Game completed")

        st.session_state.screen = 'complete'

def show_enhanced_final_screen():
    """Enhanced final screen with detailed results"""
    profile = st.session_state.player_profile
    results = st.session_state.round_results

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div class="final-score-card">
            <h2>🎮 Game Complete!</h2>
            <div style="font-size: 4em; color: #4CAF50; margin: 20px 0; font-weight: bold;">
                {st.session_state.score}
            </div>
            <div style="font-size: 1.3em; margin-bottom: 30px;">Final Score</div>

            <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h4>📊 Round Summary</h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; text-align: left;">
                    <div><strong>Correct Answers:</strong> {sum(1 for r in results if r['correct'])}/{len(results)}</div>
                    <div><strong>Average Time:</strong> {sum(r['time'] for r in results)/len(results):.1f}s</div>
                    <div><strong>Best Time:</strong> {min(r['time'] for r in results):.1f}s</div>
                    <div><strong>Total XP Earned:</strong> +{GAME_CONFIG['xp_per_game'] + sum(25 for r in results if r['correct'])}</div>
                </div>
            </div>

            <div style="margin: 20px 0;">
                {get_performance_message_enhanced(st.session_state.score, results)}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Action buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄 Play Again", type="primary", use_container_width=True):
            reset_game()
            st.session_state.screen = 'mode_select'
            st.rerun()

    with col2:
        if st.button("📱 Share Score", use_container_width=True):
            share_score()

    with col3:
        if st.button("🏠 Home", use_container_width=True):
            reset_game()
            st.session_state.screen = 'home'
            st.rerun()

def show_leaderboard_screen():
    """Enhanced leaderboard with rankings"""
    st.markdown("### 🏆 Global Leaderboard")

    leaderboard = generate_leaderboard()

    for i, player in enumerate(leaderboard, 1):
        rank_icon = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        player_class = "background: linear-gradient(135deg, #ffd700, #ffed4a);" if player['name'] == 'You' else ""

        st.markdown(f"""
        <div class="leaderboard-item" style="{player_class}">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong>{rank_icon} {player['name']}</strong>
                    <div style="font-size: 0.9em; color: #666;">
                        Level {player['level']} • {player['games']} games played
                    </div>
                </div>
                <div style="font-size: 1.2em; font-weight: bold; color: #4CAF50;">
                    {player['score']}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    if st.button("🏠 Back to Home", use_container_width=True):
        st.session_state.screen = 'home'
        st.rerun()

def show_achievements_screen():
    """Comprehensive achievements display"""
    st.markdown("### 🏅 Achievements")

    profile = st.session_state.player_profile
    unlocked = profile['achievements_unlocked']

    # Progress summary
    st.markdown(f"**Progress: {len(unlocked)}/{len(ACHIEVEMENTS)} achievements unlocked**")

    # Display achievements
    for achievement_id, achievement in ACHIEVEMENTS.items():
        is_unlocked = achievement_id in unlocked
        opacity = "1.0" if is_unlocked else "0.6"
        background = "linear-gradient(135deg, #ffd700, #ffed4a)" if is_unlocked else "#f8f9fa"

        st.markdown(f"""
        <div style="background: {background}; opacity: {opacity}; padding: 15px; border-radius: 10px; margin: 10px 0; border: 2px solid {'#ffc107' if is_unlocked else '#e9ecef'};">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <div style="font-size: 1.2em; font-weight: bold;">
                        {achievement['icon']} {achievement['name']} {'✓' if is_unlocked else '🔒'}
                    </div>
                    <div style="font-size: 0.9em; color: #666;">
                        {achievement['desc']}
                    </div>
                </div>
                <div style="font-weight: bold; color: #4CAF50;">
                    +{achievement['xp']} XP
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    if st.button("🏠 Back to Home", use_container_width=True):
        st.session_state.screen = 'home'
        st.rerun()

def show_shop_screen():
    """Power-up shop with coin system"""
    st.markdown("### 🛒 Power-up Shop")

    profile = st.session_state.player_profile
    st.markdown(f"**Your Coins: 💰 {profile['coins']}**")

    # Power-up packages
    shop_items = {
        'power_pack_small': {
            'name': 'Starter Pack',
            'desc': '2 Time Freeze + 1 Double Points',
            'cost': 5,
            'items': {'time_freeze': 2, 'double_points': 1}
        },
        'power_pack_medium': {
            'name': 'Pro Pack', 
            'desc': '3 Letter Reveals + 2 Word Banks',
            'cost': 8,
            'items': {'letter_reveal': 3, 'word_bank': 2}
        },
        'power_pack_large': {
            'name': 'Ultimate Pack',
            'desc': 'All power-ups bundle',
            'cost': 12,
            'items': {'time_freeze': 2, 'double_points': 2, 'letter_reveal': 3, 'word_bank': 2, 'shuffle_master': 5}
        }
    }

    for item_id, item_info in shop_items.items():
        can_afford = profile['coins'] >= item_info['cost']

        st.markdown(f"""
        <div style="background: {'white' if can_afford else '#f8f9fa'}; border: 2px solid {'#4CAF50' if can_afford else '#e9ecef'}; border-radius: 10px; padding: 20px; margin: 15px 0;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="margin: 0; color: {'#2c3e50' if can_afford else '#6c757d'};">{item_info['name']}</h4>
                    <p style="margin: 5px 0; color: #666;">{item_info['desc']}</p>
                    <small>Contains: {', '.join([f"{v}x {POWER_UPS[k]['name']}" for k, v in item_info['items'].items()])}</small>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 1.3em; font-weight: bold; color: #4CAF50;">
                        💰 {item_info['cost']} coins
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if can_afford:
            if st.button(f"Buy {item_info['name']}", key=f"buy_{item_id}", type="primary", use_container_width=True):
                # Purchase item
                profile['coins'] -= item_info['cost']
                for power_id, amount in item_info['items'].items():
                    profile['power_ups'][power_id] = profile['power_ups'].get(power_id, 0) + amount
                st.success(f"✅ Purchased {item_info['name']}!")
                st.rerun()
        else:
            st.button(f"Need {item_info['cost'] - profile['coins']} more coins", disabled=True, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 💰 Earn More Coins")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("📺 Watch Ad (+3 coins)", use_container_width=True):
            show_rewarded_ad("coins")
            profile['coins'] += 3
            st.success("🎁 Earned 3 coins!")
            st.rerun()

    with col2:
        st.markdown("**Ways to earn coins:**
- Complete games
- Level up
- Watch ads
- Daily streaks")

    if st.button("🏠 Back to Home", use_container_width=True):
        st.session_state.screen = 'home'
        st.rerun()

def generate_fake_words(real_word, count):
    """Generate fake words for word bank power-up"""
    # Simple fake word generation
    letters = list(real_word)
    fakes = []

    for _ in range(count):
        fake_letters = letters.copy()
        # Add/remove/change letters slightly
        if len(fake_letters) > 4:
            fake_letters.pop(random.randint(0, len(fake_letters)-1))
        if len(fake_letters) < 8:
            fake_letters.insert(random.randint(0, len(fake_letters)), random.choice('AEIOU'))

        random.shuffle(fake_letters)
        fake_word = ''.join(fake_letters)
        if fake_word != real_word and fake_word not in fakes:
            fakes.append(fake_word)
        else:
            fakes.append(''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=len(real_word))))

    return fakes

def get_performance_message_enhanced(score, results):
    """Enhanced performance feedback"""
    accuracy = sum(1 for r in results if r['correct']) / len(results)
    avg_time = sum(r['time'] for r in results) / len(results)

    if accuracy == 1.0:
        return "🏆 Perfect Game! You're a true word master!"
    elif accuracy >= 0.8:
        return "🎯 Excellent performance! You're getting really good at this!"
    elif accuracy >= 0.6:
        return "👍 Good job! Keep practicing to improve further!"
    elif avg_time < 20:
        return "⚡ Great speed! Work on accuracy next!"
    else:
        return "💪 Nice effort! Every game makes you better!"

def share_score():
    """Social sharing functionality"""
    profile = st.session_state.player_profile
    score_text = f"I just scored {st.session_state.score} points in Word Scramble Mini Pro! 🎯 Level {profile['level']} with {len(profile['achievements_unlocked'])} achievements! Can you beat my score?"

    st.info(f"Share this: {score_text}")
    unlock_achievement('social_butterfly')

def show_statistics_modal():
    """Display detailed player statistics"""
    profile = st.session_state.player_profile
    stats = profile['statistics']

    with st.expander("📊 Detailed Statistics", expanded=True):
        col1, col2 = st.columns(2)

        with col1:
            st.metric("Games Played", stats['games_played'])
            st.metric("Words Solved", stats['words_correct'])
            st.metric("Accuracy", f"{(stats['words_correct']/max(1, stats['words_total'])*100):.1f}%")
            st.metric("Perfect Games", stats['perfect_games'])

        with col2:
            st.metric("Current Streak", profile['current_streak'])
            st.metric("Best Streak", profile['best_streak'])
            st.metric("Fastest Solve", f"{stats['fastest_solve']:.1f}s" if stats['fastest_solve'] != float('inf') else "N/A")
            st.metric("Hints Used", stats['hints_used'])

def show_settings_modal():
    """Game settings and preferences"""
    profile = st.session_state.player_profile
    prefs = profile['preferences']

    with st.expander("⚙️ Game Settings", expanded=True):
        # Difficulty preference
        difficulty = st.selectbox(
            "Preferred Difficulty",
            ['easy', 'medium', 'hard'],
            index=['easy', 'medium', 'hard'].index(prefs['difficulty'])
        )
        prefs['difficulty'] = difficulty

        # Auto-difficulty
        auto_diff = st.checkbox("Auto-adjust difficulty", value=prefs['auto_difficulty'])
        prefs['auto_difficulty'] = auto_diff

        # Sound (placeholder)
        sound = st.checkbox("Sound Effects", value=prefs['sound_enabled'])
        prefs['sound_enabled'] = sound

        if st.button("Save Settings"):
            st.success("Settings saved!")

def reset_game():
    """Reset game state for new game"""
    st.session_state.screen = 'home'
    st.session_state.current_round = 1
    st.session_state.score = 0
    st.session_state.current_word = ''
    st.session_state.scrambled_word = ''
    st.session_state.round_start_time = None
    st.session_state.hint_used = False
    st.session_state.hints_available = {'category': True, 'definition': True, 'shuffle': True, 'reveal': True}
    st.session_state.feedback_message = ''
    st.session_state.feedback_type = 'info'
    st.session_state.awaiting_next_round = False
    st.session_state.game_complete = False
    st.session_state.round_results = []
    st.session_state.active_power_ups = {}
    st.session_state.round_multiplier = 1
    st.session_state.time_freeze_remaining = 0
    st.session_state.letters_revealed = []
    st.session_state.word_bank_shown = False

if __name__ == "__main__":
    main()
