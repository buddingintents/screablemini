Word Scramble Mini - Streamlit Game with Google AdSense
A fun and engaging word scramble game built with Streamlit, featuring Google AdSense integration for revenue generation.

🎮 Game Features
Word Scrambling: Unscramble letters to form meaningful words

Timer System: 60 seconds per round with time-based bonus scoring

5 Round Gameplay: Complete progression through multiple rounds

Hint System: Rewarded ads unlock hints (first letter reveal)

Score Tracking: Points system with time bonuses

Responsive Design: Clean, modern UI optimized for all devices

💰 Monetization Features
Banner Ads: Top and bottom page placement for consistent visibility

Interstitial Ads: Between-round advertisements for maximum engagement

Rewarded Ads: Optional hint system encourages user interaction

Strategic Placement: Ads positioned to avoid gameplay disruption

Mobile Optimized: AdSense units configured for mobile responsiveness

🚀 Quick Start
1. Installation
bash
# Clone or download the game files
# Install dependencies
pip install streamlit
2. Google AdSense Setup
Get AdSense Account: Apply at Google AdSense

Create Ad Units: Generate ad units for each placement type

Configure Secrets: Set up your AdSense credentials

3. Configuration
Create .streamlit/secrets.toml in your project directory:

text
[google]
adsense_client_id = "ca-pub-YOUR-ACTUAL-ID"
top_ad_slot = "YOUR-TOP-AD-SLOT"
footer_ad_slot = "YOUR-FOOTER-AD-SLOT"
interstitial_ad_slot = "YOUR-INTERSTITIAL-SLOT"
rewarded_ad_slot = "YOUR-REWARDED-SLOT"
4. Run the Game
bash
streamlit run word_scramble_streamlit.py
📋 AdSense Configuration Guide
Required Ad Units
Top Banner (728x90 Leaderboard)

Placement: Page header

Purpose: Consistent brand visibility

Footer Banner (728x90 Leaderboard)

Placement: Page footer

Purpose: Additional inventory without gameplay interruption

Interstitial Ad (970x250 Large Banner)

Placement: Between game rounds

Purpose: High-engagement moments for better CTR

Rewarded Ad (300x250 Medium Rectangle)

Placement: Hint system activation

Purpose: User-initiated engagement for hints

Ad Placement Strategy
Non-Intrusive: Ads placed outside active gameplay areas

User-Initiated: Rewarded ads only shown when users request hints

Natural Breaks: Interstitials during logical game pauses

Mobile-First: All ad units optimized for mobile gameplay

🎯 Game Configuration
Default Settings
Rounds per Game: 5

Time per Round: 60 seconds

Base Points: 10 per correct answer

Time Bonus: 0.1 points per second remaining

Word List: 50 carefully selected words (4-8 letters)

Customization
Modify GAME_CONFIG in the Python file:

python
GAME_CONFIG = {
    "rounds_per_game": 5,
    "time_per_round": 60,
    "points_per_correct": 10,
    "time_bonus_multiplier": 0.1
}
🔧 Deployment Options
Streamlit Cloud (Recommended)
Push code to GitHub repository

Connect to Streamlit Cloud

Add secrets through Streamlit Cloud dashboard

Deploy automatically

Heroku Deployment
bash
# Create Procfile
echo "web: sh setup.sh && streamlit run word_scramble_streamlit.py" > Procfile

# Create setup.sh
echo "mkdir -p ~/.streamlit/" > setup.sh
echo "echo '[server]'" >> setup.sh
echo "port = $PORT" >> setup.sh
echo "enableCORS = false" >> setup.sh
echo "headless = true" >> setup.sh
Local Development
bash
# Run locally for testing
streamlit run word_scramble_streamlit.py --server.port 8501
📊 Revenue Optimization Tips
Ad Performance
Banner Placement: Above the fold for maximum visibility

Interstitial Timing: Show after round completion for natural breaks

Rewarded Engagement: Clear value proposition for hint system

Mobile Optimization: Ensure all ad units render properly on mobile

User Experience
Fast Loading: Streamlit's caching ensures quick game responses

Progressive Enhancement: Ads don't block core gameplay

Clear UI: Obvious separation between game content and advertisements

Accessibility: All interactive elements keyboard accessible

Analytics Integration
Track key metrics:

Game completion rates

Ad click-through rates

Hint usage patterns

User session duration

🛠️ Technical Architecture
Core Technologies
Streamlit: Web app framework and UI

Python: Game logic and state management

HTML/JavaScript: AdSense integration via components

CSS: Custom styling and responsive design

State Management
Session State: Maintains game progress across interactions

Component Communication: Seamless integration between Python and JavaScript

Error Handling: Graceful fallbacks for missing configurations

Performance Optimizations
Caching: Word list and game assets cached for speed

Minimal Redraws: Strategic use of st.rerun() for efficiency

Lazy Loading: Ads loaded asynchronously to avoid blocking gameplay

📱 Mobile Responsiveness
Touch-Friendly: Large buttons and input fields

Adaptive Layout: Responsive design for all screen sizes

Fast Performance: Optimized for mobile connections

Ad Compatibility: Mobile-optimized AdSense units

🔒 Security Considerations
Secrets Management: AdSense credentials stored securely

Input Validation: User input sanitized and validated

XSS Protection: Streamlit's built-in security features

HTTPS Enforcement: Required for AdSense compliance

📈 Scaling Considerations
Performance
Add Redis caching for high-traffic deployments

Implement load balancing for multiple instances

Consider CDN for static assets

Features
User accounts and persistent high scores

Multiplayer functionality

Custom word lists and categories

Social sharing integration

📞 Support & Troubleshooting
Common Issues
Ads Not Displaying:

Verify AdSense account status

Check ad unit IDs in secrets.toml

Ensure domain is approved by AdSense

Game Not Loading:

Verify Streamlit installation

Check Python version compatibility

Review browser console for JavaScript errors

Performance Issues:

Clear browser cache

Check network connection

Verify deployment resources

Getting Help
Streamlit Documentation: https://docs.streamlit.io/

Google AdSense Help: https://support.google.com/adsense/

GitHub Issues: Report bugs and feature requests

📝 License
This project is open source and available under the MIT License.

🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

🏆 Credits
Created with ❤️ using Streamlit and Google AdSense for revenue generation.
