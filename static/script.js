class GameUI {
    constructor() {
        this.chatContainer = document.getElementById('chatContainer');
        this.roundDisplay = document.getElementById('round');
        this.scoreDisplay = document.getElementById('score');
        this.bombDisplay = document.getElementById('bomb');
        this.resetBtn = document.getElementById('resetBtn');
        this.moveButtons = document.querySelectorAll('.move-btn');
        
        this.init();
    }

    init() {
        // Setup event listeners
        this.moveButtons.forEach(btn => {
            btn.addEventListener('click', () => this.handleMove(btn.dataset.move));
        });
        
        this.resetBtn.addEventListener('click', () => this.resetGame());
        
        // Add help button listener
        const helpBtn = document.getElementById('helpBtn');
        if (helpBtn) {
            helpBtn.addEventListener('click', () => this.showHelp());
        }
        
        // Start game
        this.startGame();
    }

    showHelp() {
        const helpMessage = `📖 GAME RULES

🎯 Objective: Win 2 out of 3 rounds

🎮 How to Play:
• Click a button to make your move
• Rock beats Scissors
• Scissors beats Paper  
• Paper beats Rock
• Same move = Draw

💣 Special Move - BOMB:
• Can be used ONCE per game
• Beats ALL moves (rock, paper, scissors)
• Bomb vs Bomb = Draw
• Use it wisely!

⚠️ Important:
• Invalid moves waste your round
• Game ends after 3 rounds
• Highest score wins!

Good luck! 🍀`;
        
        this.addMessage(helpMessage, 'ai');
    }

    async startGame() {
        try {
            // Add loading message
            this.addMessage('🎮 Initializing game...', 'ai');
            
            const response = await fetch('/api/start', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            
            const data = await response.json();
            
            // Clear loading and add welcome
            this.chatContainer.innerHTML = '';
            await this.addMessageWithTyping(data.message, 'ai');
            this.updateGameState(data.game_state);
        } catch (error) {
            console.error('Error starting game:', error);
            this.addMessage('Failed to start game. Please refresh.', 'ai');
        }
    }

    async handleMove(move) {
        // Disable buttons during processing
        this.setButtonsEnabled(false);
        
        // Add loading state
        const clickedBtn = document.querySelector(`[data-move="${move}"]`);
        clickedBtn.classList.add('loading');
        
        try {
            // Show user move with animation
            this.addMessage(move.toUpperCase(), 'user');
            
            // Small delay for better UX
            await new Promise(resolve => setTimeout(resolve, 300));
            
            const response = await fetch('/api/move', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ move })
            });
            
            const data = await response.json();
            
            // Add AI response with typing effect
            await this.addMessageWithTyping(data.message, 'ai');
            this.updateGameState(data.game_state);
            
            // Re-enable buttons if game not over
            if (!data.game_state.game_over) {
                this.setButtonsEnabled(true);
            }
        } catch (error) {
            console.error('Error processing move:', error);
            this.addMessage('Error processing move. Try again.', 'ai');
            this.setButtonsEnabled(true);
        } finally {
            clickedBtn.classList.remove('loading');
        }
    }

    async resetGame() {
        try {
            // Add confirmation
            this.addMessage('🔄 Starting new game...', 'user');
            
            const response = await fetch('/api/reset', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            
            const data = await response.json();
            
            // Clear chat with animation
            setTimeout(() => {
                this.chatContainer.innerHTML = '';
                this.addMessageWithTyping(data.message, 'ai');
                this.updateGameState(data.game_state);
                this.setButtonsEnabled(true);
            }, 300);
        } catch (error) {
            console.error('Error resetting game:', error);
        }
    }

    addMessage(text, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        // Format text with line breaks
        contentDiv.innerHTML = `<p>${this.escapeHtml(text).replace(/\n/g, '<br>')}</p>`;
        
        messageDiv.appendChild(contentDiv);
        this.chatContainer.appendChild(messageDiv);
        
        // Scroll to bottom smoothly
        this.chatContainer.scrollTo({
            top: this.chatContainer.scrollHeight,
            behavior: 'smooth'
        });
    }

    async addMessageWithTyping(text, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.innerHTML = '<p></p>';
        
        messageDiv.appendChild(contentDiv);
        this.chatContainer.appendChild(messageDiv);
        
        // Typing effect
        const p = contentDiv.querySelector('p');
        const formattedText = this.escapeHtml(text).replace(/\n/g, '<br>');
        
        // Instant display for better UX (typing effect can be slow)
        p.innerHTML = formattedText;
        
        // Scroll to bottom
        this.chatContainer.scrollTo({
            top: this.chatContainer.scrollHeight,
            behavior: 'smooth'
        });
    }

    updateGameState(state) {
        // Update round with animation
        this.roundDisplay.textContent = `${state.round_number}/3`;
        this.roundDisplay.style.transform = 'scale(1.2)';
        setTimeout(() => {
            this.roundDisplay.style.transform = 'scale(1)';
        }, 200);
        
        // Update score with animation
        this.scoreDisplay.textContent = `${state.user_score} - ${state.bot_score}`;
        this.scoreDisplay.style.transform = 'scale(1.2)';
        setTimeout(() => {
            this.scoreDisplay.style.transform = 'scale(1)';
        }, 200);
        
        // Update bomb status
        const bombBtn = document.querySelector('[data-move="bomb"]');
        if (state.user_bomb_used) {
            this.bombDisplay.textContent = '💣 Used';
            this.bombDisplay.style.color = '#a0a0a0';
            bombBtn.disabled = true;
        } else {
            this.bombDisplay.textContent = '💣 Ready';
            this.bombDisplay.style.color = '#00ff88';
            bombBtn.disabled = false;
        }
        
        // Disable all buttons if game over
        if (state.game_over) {
            this.setButtonsEnabled(false);
        }
    }

    setButtonsEnabled(enabled) {
        this.moveButtons.forEach(btn => {
            if (btn.dataset.move !== 'bomb') {
                btn.disabled = !enabled;
            }
        });
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize game when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new GameUI();
});
