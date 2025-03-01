import streamlit as st
import streamlit.components.v1 as components

def main():
    st.set_page_config(
        page_title="Pizza Toss Game",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    st.title("Pizza Toss Game")
    
    # HTML/JS code for the game - properly formatted as a string for Streamlit
    game_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Pizza Toss Game</title>
        <style>
            body {
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                font-family: 'Arial', sans-serif;
                overflow: hidden;
            }
            
            #game-container {
                position: relative;
                width: 100%;
                max-width: 800px;
                aspect-ratio: 4 / 3;
                margin: 0 auto;
                background: linear-gradient(135deg, #67B8DE, #0396FF);
                border: none;
                border-radius: 12px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4), 
                            0 0 100px rgba(255, 255, 255, 0.2);
                overflow: hidden;
                touch-action: none;
            }
            
            #game-info {
                position: absolute;
                top: 15px;
                left: 15px;
                color: white;
                background: rgba(0, 0, 0, 0.6);
                padding: 10px 15px;
                border-radius: 30px;
                font-size: 18px;
                font-weight: bold;
                z-index: 100;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                backdrop-filter: blur(5px);
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            #oven {
                position: absolute;
                bottom: 150px;
                left: 50px;
                width: 120px;
                height: 100px;
                background: linear-gradient(135deg, #555, #333, #222);
                border: none;
                border-radius: 12px;
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.4),
                            inset 0 -5px 15px rgba(0, 0, 0, 0.6),
                            inset 0 5px 10px rgba(255, 255, 255, 0.1);
                filter: drop-shadow(0 5px 10px rgba(0,0,0,0.4));
                transition: all 0.2s ease;
            }
            
            #oven-top-controls {
                position: absolute;
                width: 100%;
                height: 20px;
                background: linear-gradient(to right, #333, #444, #333);
                top: -10px;
                left: 0;
                border-radius: 10px 10px 0 0;
                box-shadow: inset 0 2px 3px rgba(255, 255, 255, 0.1);
            }
            
            .oven-knob {
                position: absolute;
                width: 12px;
                height: 12px;
                background: linear-gradient(135deg, #DDD, #999);
                border-radius: 50%;
                top: 4px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3),
                            inset 0 -2px 3px rgba(0, 0, 0, 0.2),
                            inset 0 2px 3px rgba(255, 255, 255, 0.7);
            }
            
            #oven-door {
                position: absolute;
                width: 85px;
                height: 70px;
                background: linear-gradient(135deg, #444, #222);
                top: 15px;
                left: 17px;
                border-radius: 8px;
                border: 1px solid #111;
                box-shadow: inset 0 0 15px rgba(0, 0, 0, 0.7),
                            0 0 5px rgba(0, 0, 0, 0.5);
                overflow: hidden;
            }
            
            #oven-handle {
                position: absolute;
                width: 50px;
                height: 8px;
                background: linear-gradient(to bottom, #EEE, #999);
                left: 17px;
                top: 35px;
                border-radius: 4px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.4),
                            inset 0 1px 2px rgba(255, 255, 255, 0.8);
            }
            
            #oven-window {
                position: absolute;
                width: 65px;
                height: 35px;
                background: linear-gradient(rgba(255, 170, 50, 0.3), rgba(255, 100, 0, 0.3));
                border: 2px solid #111;
                border-radius: 8px;
                left: 10px;
                top: 5px;
                box-shadow: inset 0 0 20px rgba(255, 100, 0, 0.7),
                            0 0 10px rgba(255, 120, 0, 0.5);
                overflow: hidden;
            }
            
            #oven-window::after {
                content: '';
                position: absolute;
                bottom: 5px;
                left: 5px;
                right: 5px;
                height: 3px;
                background: #FF3700;
                border-radius: 2px;
                box-shadow: 0 0 10px #FF5500, 0 0 20px #FF7700;
                animation: heating 1s ease-in-out infinite alternate;
            }
            
            @keyframes heating {
                from { opacity: 0.7; }
                to { opacity: 1; }
            }
            
            #pizza {
                position: absolute;
                width: 60px;
                height: 60px;
                background: radial-gradient(#FFDD99, #E8A33C, #C77B30);
                border-radius: 50%;
                border: 2px solid #B56D1C;
                display: flex;
                justify-content: center;
                align-items: center;
                font-size: 24px;
                transform: rotate(0deg);
                transition: transform 0.2s linear;
                z-index: 10;
                box-shadow: 0 3px 10px rgba(0, 0, 0, 0.3);
                filter: drop-shadow(0 2px 5px rgba(0, 0, 0, 0.3));
            }
            
            #pizza::before {
                content: '';
                position: absolute;
                width: 90%;
                height: 90%;
                border-radius: 50%;
                border: 2px dashed rgba(180, 120, 40, 0.5);
                top: 3%;
                left: 3%;
            }
            
            .pepperoni {
                position: absolute;
                width: 12px;
                height: 12px;
                background: radial-gradient(#FF6347, #D92800);
                border-radius: 50%;
                box-shadow: inset 0 0 3px rgba(0, 0, 0, 0.5),
                            0 1px 2px rgba(0, 0, 0, 0.2);
                z-index: 2;
            }
            
            .cheese {
                position: absolute;
                width: 10px;
                height: 7px;
                background: linear-gradient(#FFED97, #F7D358);
                border-radius: 40% 40% 40% 40%;
                transform: rotate(30deg);
                z-index: 1;
                box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
            }
            
            .sauce {
                position: absolute;
                width: 7px;
                height: 7px;
                background: rgba(200, 30, 0, 0.7);
                border-radius: 50%;
                z-index: 0;
            }
            
            #power-bar-container {
                position: absolute;
                bottom: 50px;
                left: 50%;
                transform: translateX(-50%);
                width: 300px;
                height: 30px;
                background: rgba(255, 255, 255, 0.2);
                border: none;
                border-radius: 15px;
                box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.3),
                            0 5px 15px rgba(0, 0, 0, 0.2);
                backdrop-filter: blur(5px);
                overflow: hidden;
            }
            
            #power-bar {
                position: absolute;
                height: 100%;
                width: 0;
                background: linear-gradient(90deg, #32CD32, #FFC107, #FF5252);
                border-radius: 15px;
                box-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
                transition: width 0.05s linear;
            }
            
            #power-bar::after {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 15px;
                background: linear-gradient(rgba(255, 255, 255, 0.4), rgba(255, 255, 255, 0));
                border-radius: 15px 15px 0 0;
            }
            
            .target {
                position: absolute;
                width: 80px;
                height: 80px;
                background: radial-gradient(circle, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0.5) 70%, rgba(255,255,255,0) 100%);
                border: 3px solid #FF5858;
                border-radius: 50%;
                display: flex;
                justify-content: center;
                align-items: center;
                font-weight: bold;
                font-size: 20px;
                color: #FF0000;
                text-shadow: 0 0 5px rgba(255, 255, 255, 0.7);
                box-shadow: 0 0 15px rgba(255, 0, 0, 0.4),
                            inset 0 0 15px rgba(255, 0, 0, 0.3);
                animation: targetPulse 2s infinite alternate ease-in-out;
            }
            
            @keyframes targetPulse {
                0% { transform: scale(1); box-shadow: 0 0 15px rgba(255, 0, 0, 0.4), inset 0 0 15px rgba(255, 0, 0, 0.3); }
                100% { transform: scale(1.05); box-shadow: 0 0 20px rgba(255, 0, 0, 0.6), inset 0 0 20px rgba(255, 0, 0, 0.5); }
            }
            
            .target::before {
                content: '';
                position: absolute;
                width: 60px;
                height: 60px;
                border: 2px dashed rgba(255, 0, 0, 0.7);
                border-radius: 50%;
            }
            
            .target::after {
                content: '';
                position: absolute;
                width: 30px;
                height: 30px;
                border: 2px solid rgba(255, 0, 0, 0.7);
                border-radius: 50%;
            }
            
            .powerup {
                position: absolute;
                width: 35px;
                height: 35px;
                border-radius: 50%;
                display: flex;
                justify-content: center;
                align-items: center;
                font-weight: bold;
                font-size: 16px;
                box-shadow: 0 0 20px rgba(255, 255, 255, 0.7);
                animation: powerupFloat 2s infinite alternate ease-in-out;
                filter: drop-shadow(0 5px 10px rgba(0,0,0,0.3));
                z-index: 20;
            }
            
            @keyframes powerupFloat {
                0% { transform: translateY(0) rotate(0deg); }
                100% { transform: translateY(-10px) rotate(10deg); }
            }
            
            .powerup::before {
                content: '';
                position: absolute;
                width: 100%;
                height: 100%;
                border-radius: 50%;
                background: inherit;
                filter: blur(10px);
                opacity: 0.5;
                z-index: -1;
            }
            
            .powerup-slow {
                background: radial-gradient(#FFD700, #FFA500);
                color: white;
                text-shadow: 0 1px 3px rgba(0,0,0,0.5);
            }
            
            .powerup-distance {
                background: radial-gradient(#1E90FF, #0000CD);
                color: white;
                text-shadow: 0 1px 3px rgba(0,0,0,0.5);
            }
            
            .powerup-pizza {
                background: radial-gradient(#FF6347, #DC143C);
                color: white;
                text-shadow: 0 1px 3px rgba(0,0,0,0.5);
            }
            
            #instructions, #game-over {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: rgba(0, 0, 0, 0.8);
                color: white;
                padding: 30px;
                border-radius: 20px;
                text-align: center;
                z-index: 1000;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5),
                            0 0 100px rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                max-width: 500px;
            }
            
            #game-over {
                display: none;
            }
            
            #instructions h2, #game-over h2 {
                margin-top: 0;
                color: #FF6347;
                font-size: 28px;
                text-shadow: 0 0 10px rgba(255, 99, 71, 0.5);
            }
            
            #instructions p, #game-over p {
                font-size: 16px;
                line-height: 1.6;
                margin-bottom: 20px;
            }
            
            #instructions button, #game-over button {
                margin-top: 20px;
                padding: 12px 30px;
                background: linear-gradient(135deg, #FF416C, #FF4B2B);
                color: white;
                border: none;
                border-radius: 30px;
                cursor: pointer;
                font-size: 18px;
                font-weight: bold;
                transition: all 0.3s ease;
                box-shadow: 0 5px 15px rgba(255, 75, 43, 0.4);
            }
            
            #instructions button:hover, #game-over button:hover {
                transform: translateY(-3px);
                box-shadow: 0 8px 20px rgba(255, 75, 43, 0.6);
            }
            
            #instructions button:active, #game-over button:active {
                transform: translateY(1px);
                box-shadow: 0 2px 10px rgba(255, 75, 43, 0.4);
            }
            
            @keyframes fadeInOut {
                0% { opacity: 0; transform: scale(0.5); }
                10% { opacity: 1; transform: scale(1.2); }
                20% { transform: scale(1); }
                80% { opacity: 1; }
                100% { opacity: 0; }
            }
            
            @keyframes pizzaFall {
                0% { transform: translateY(-50px) rotate(0deg); opacity: 0; }
                20% { transform: translateY(0) rotate(180deg); opacity: 1; }
                60% { transform: translateY(100px) rotate(360deg); opacity: 1; }
                100% { transform: translateY(250px) rotate(720deg); opacity: 0; }
            }
            
            @keyframes targetHit {
                0% { transform: scale(1); }
                50% { transform: scale(1.3); filter: brightness(1.5); }
                100% { transform: scale(1); }
            }
            
            @keyframes confettiFall {
                0% { transform: translateY(0) rotate(0); opacity: 1; }
                100% { transform: translateY(600px) rotate(360deg); opacity: 0; }
            }
            
            #streamlit-app-warning {
                position: absolute;
                bottom: 10px;
                left: 10px;
                color: white;
                background: rgba(0, 0, 0, 0.7);
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                z-index: 1000;
            }

            /* Mobile on-screen controls */
            #mobile-controls {
                position: absolute;
                bottom: 10px;
                left: 0;
                right: 0;
                display: flex;
                justify-content: space-between;
                padding: 10px;
                z-index: 200;
                pointer-events: none;
            }

            .control-button {
                width: 60px;
                height: 60px;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.3);
                backdrop-filter: blur(5px);
                border: 2px solid rgba(255, 255, 255, 0.5);
                display: flex;
                justify-content: center;
                align-items: center;
                font-size: 24px;
                color: white;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
                margin: 0 5px;
                pointer-events: auto;
                user-select: none;
                -webkit-tap-highlight-color: transparent;
            }

            .throw-button {
                width: 80px;
                height: 80px;
                background: rgba(255, 99, 71, 0.6);
                font-weight: bold;
            }

            .throw-button:active, .throw-button.active {
                background: rgba(255, 99, 71, 0.9);
                transform: scale(0.95);
            }

            .control-button:active {
                transform: scale(0.95);
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
            }

            .direction-controls {
                display: flex;
                flex-direction: column;
                align-items: center;
                pointer-events: none;
            }

            .up-button, .down-button {
                pointer-events: auto;
            }

            /* Hide on-screen controls on large screens */
            @media (min-width: 1024px) {
                #mobile-controls {
                    display: none;
                }
            }

            /* Make the game instructions responsive */
            @media (max-width: 600px) {
                #instructions, #game-over {
                    padding: 20px;
                    width: 90%;
                    max-width: none;
                }

                #instructions h2, #game-over h2 {
                    font-size: 24px;
                }

                #instructions p, #game-over p {
                    font-size: 14px;
                }

                #instructions button, #game-over button {
                    font-size: 16px;
                    padding: 10px 20px;
                }

                /* Make controls bigger for small screens */
                .control-button {
                    width: 70px;
                    height: 70px;
                }

                .throw-button {
                    width: 90px;
                    height: 90px;
                }
            }

            /* Adjust game layout for very small screens */
            @media (max-width: 400px) {
                #game-info {
                    font-size: 14px;
                    padding: 5px 10px;
                }

                #power-bar-container {
                    width: 80%;
                    height: 25px;
                }

                .target {
                    width: 70px;
                    height: 70px;
                }
            }
        </style>
    </head>
    <body>
        <div id="game-container">
            <div id="game-info">
                Score: <span id="score">0</span> | Pizzas: <span id="pizzas-left">5</span>
            </div>
            
            <div id="streamlit-app-warning">
                Click inside the game area to start!
            </div>
            
            <div id="oven">
                <div id="oven-top-controls">
                    <div class="oven-knob" style="left: 20px;"></div>
                    <div class="oven-knob" style="left: 40px;"></div>
                    <div class="oven-knob" style="left: 60px;"></div>
                    <div class="oven-knob" style="left: 80px;"></div>
                </div>
                <div id="oven-door">
                    <div id="oven-window"></div>
                    <div id="oven-handle"></div>
                </div>
            </div>
            
            <div id="pizza" style="display: none;"></div>
            
            <div id="power-bar-container">
                <div id="power-bar"></div>
            </div>
            
            <!-- Mobile on-screen controls -->
            <div id="mobile-controls">
                <div class="direction-controls">
                    <div class="control-button up-button">▲</div>
                    <div class="control-button down-button">▼</div>
                </div>
                <div class="control-button throw-button">TOSS</div>
            </div>
            
            <div id="instructions">
                <h2>Pizza Toss Game</h2>
                <p>Press SPACE or use the TOSS button to get a pizza from the oven.<br>
                Hold to charge the power bar, release to throw.<br>
                The longer you hold, the further the pizza will go!<br>
                Use UP/DOWN keys or buttons to move the oven.<br>
                <br>
                <span style="color: gold;">S</span>: Slows down power bar<br>
                <span style="color: #00BFFF;">D</span>: Increases throwing distance<br>
                <span style="color: #FF6347;">P</span>: Gives you 4 extra pizzas<br>
                <br>
                Hit targets to earn points! Collect powerups for bonuses!</p>
                <button id="start-game">Start Game</button>
            </div>
            
            <div id="game-over">
                <h2>Game Over!</h2>
                <p>Your final score: <span id="final-score">0</span></p>
                <button id="restart-game">Play Again</button>
            </div>
        </div>
        
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                // Game variables
                let score = 0;
                let pizzasLeft = 5;
                let gameActive = false;
                let pizzaInHand = false;
                let powerBarDirection = 1;
                let powerBarSpeed = 3;
                let powerBarPos = 0;
                let pizzaThrown = false;
                let ovenY = 150; // Initial oven vertical position
                let ovenMoveSpeed = 5; // Speed at which the oven moves
                let powerCharging = false;
                let powerLevel = 0;
                let chargeInterval;
                let activePowerups = {
                    slowBar: false,
                    extraDistance: false,
                    extraPizzas: false
                };
                let targets = [];
                let powerups = [];
                let lastFrameTime = 0;
                let isMobile = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
                
                // DOM elements
                const gameContainer = document.getElementById('game-container');
                const pizza = document.getElementById('pizza');
                const powerBar = document.getElementById('power-bar');
                const scoreDisplay = document.getElementById('score');
                const pizzasLeftDisplay = document.getElementById('pizzas-left');
                const instructionsPanel = document.getElementById('instructions');
                const gameOverPanel = document.getElementById('game-over');
                const finalScoreDisplay = document.getElementById('final-score');
                const throwButton = document.querySelector('.throw-button');
                const upButton = document.querySelector('.up-button');
                const downButton = document.querySelector('.down-button');
                
                // Start the game
                document.getElementById('start-game').addEventListener('click', function() {
                    instructionsPanel.style.display = 'none';
                    startGame();
                });
                
                // Restart the game
                document.getElementById('restart-game').addEventListener('click', function() {
                    gameOverPanel.style.display = 'none';
                    startGame();
                });
                
                // Start the game
                function startGame() {
                    score = 0;
                    pizzasLeft = 5;
                    gameActive = true;
                    pizzaInHand = false;
                    pizzaThrown = false;
                    ovenY = 150; // Reset oven position
                    document.getElementById('oven').style.bottom = ovenY + 'px';
                    
                    // Clear old targets and powerups
                    targets.forEach(target => {
                        if (target.element.parentNode) {
                            gameContainer.removeChild(target.element);
                        }
                    });
                    targets = [];
                    
                    powerups.forEach(powerup => {
                        if (powerup.element.parentNode) {
                            gameContainer.removeChild(powerup.element);
                        }
                    });
                    powerups = [];
                    
                    // Create new targets
                    createTargets();
                    
                    // Update displays
                    updateScore();
                    updatePizzasLeft();
                    
                    // Hide warning message
                    document.getElementById('streamlit-app-warning').textContent = 'Use the TOSS button or SPACE bar to play!';
                    setTimeout(() => {
                        document.getElementById('streamlit-app-warning').style.display = 'none';
                    }, 3000);
                    
                    // Start animation loop
                    lastFrameTime = performance.now();
                    requestAnimationFrame(gameLoop);
                }
                
                // Create targets
                function createTargets() {
                    // Clear existing targets first
                    targets.forEach(target => {
                        if (target.element.parentNode) {
                            gameContainer.removeChild(target.element);
                        }
                    });
                    targets = [];
                    
                    // Create new targets at different distances
                    for (let i = 0; i < 3; i++) {
                        const targetElement = document.createElement('div');
                        targetElement.className = 'target';
                        
                        // Distribute targets at different distances
                        const x = 350 + (i * 130);
                        const y = 100 + Math.random() * 350;
                        
                        targetElement.style.left = x + 'px';
                        targetElement.style.top = y + 'px';
                        
                        // Points increase with distance
                        const points = 10 + (i * 15);
                        targetElement.textContent = points;
                        
                        gameContainer.appendChild(targetElement);
                        
                        targets.push({
                            element: targetElement,
                            x: x,
                            y: y,
                            points: points,
                            hit: false
                        });
                    }
                }
                
                // Create a powerup
                function createPowerup() {
                    if (Math.random() < 0.5 && powerups.length < 3) {
                        const powerupElement = document.createElement('div');
                        powerupElement.className = 'powerup';
                        
                        const x = 300 + Math.random() * 400;
                        const y = 100 + Math.random() * 350;
                        
                        powerupElement.style.left = x + 'px';
                        powerupElement.style.top = y + 'px';
                        
                        // Randomly choose powerup type with weights
                        const rand = Math.random();
                        let type;
                        
                        if (rand < 0.4) {
                            type = 'S';  // Slow bar
                            powerupElement.classList.add('powerup-slow');
                        } else if (rand < 0.8) {
                            type = 'D';  // Distance booster
                            powerupElement.classList.add('powerup-distance');
                        } else {
                            type = 'P';  // Extra pizzas
                            powerupElement.classList.add('powerup-pizza');
                        }
                        
                        powerupElement.textContent = type;
                        
                        gameContainer.appendChild(powerupElement);
                        
                        powerups.push({
                            element: powerupElement,
                            x: x,
                            y: y,
                            type: type,
                            collected: false
                        });
                    }
                }
                
                // Update the score display with animation
                function updateScore() {
                    const oldScore = parseInt(scoreDisplay.textContent);
                    const newScore = score;
                    
                    if (newScore > oldScore) {
                        let displayScore = oldScore;
                        const interval = setInterval(() => {
                            displayScore += 1;
                            scoreDisplay.textContent = displayScore;
                            
                            if (displayScore >= newScore) {
                                clearInterval(interval);
                                // Flash effect
                                scoreDisplay.style.color = '#FFD700';
                                scoreDisplay.style.textShadow = '0 0 10px rgba(255, 215, 0, 0.7)';
                                setTimeout(() => {
                                    scoreDisplay.style.color = 'white';
                                    scoreDisplay.style.textShadow = 'none';
                                }, 300);
                            }
                        }, 50);
                    } else {
                        scoreDisplay.textContent = score;
                    }
                }
                
                // Update the pizzas left display with animation
                function updatePizzasLeft() {
                    pizzasLeftDisplay.textContent = pizzasLeft;
                    // Flash effect
                    pizzasLeftDisplay.style.color = '#FFD700';
                    pizzasLeftDisplay.style.textShadow = '0 0 10px rgba(255, 215, 0, 0.7)';
                    setTimeout(() => {
                        pizzasLeftDisplay.style.color = 'white';
                        pizzasLeftDisplay.style.textShadow = 'none';
                    }, 300);
                }
                
                // Create a fresh pizza with toppings
                function createPizza() {
                    pizza.style.display = 'block';
                    pizza.style.left = '70px';
                    pizza.style.bottom = (ovenY + 30) + 'px';
                    pizza.style.transform = 'rotate(0deg)';
                    
                    // Clear old toppings
                    while (pizza.firstChild) {
                        pizza.removeChild(pizza.firstChild);
                    }
                    
                    // Add sauce
                    for (let i = 0; i < 10; i++) {
                        const sauce = document.createElement('div');
                        sauce.className = 'sauce';
                        sauce.style.left = 5 + Math.random() * 50 + 'px';
                        sauce.style.top = 5 + Math.random() * 50 + 'px';
                        pizza.appendChild(sauce);
                    }
                    
                    // Add cheese
                    for (let i = 0; i < 12; i++) {
                        const cheese = document.createElement('div');
                        cheese.className = 'cheese';
                        cheese.style.left = 5 + Math.random() * 50 + 'px';
                        cheese.style.top = 5 + Math.random() * 50 + 'px';
                        cheese.style.transform = `rotate(${Math.random() * 360}deg)`;
                        pizza.appendChild(cheese);
                    }
                    
                    // Add pepperonis
                    for (let i = 0; i < 5; i++) {
                        const pepperoni = document.createElement('div');
                        pepperoni.className = 'pepperoni';
                        pepperoni.style.left = 10 + Math.random() * 40 + 'px';
                        pepperoni.style.top = 10 + Math.random() * 40 + 'px';
                        pizza.appendChild(pepperoni);
                    }
                    
                    // Add glow effect
                    pizza.style.filter = "drop-shadow(0 0 15px rgba(255, 120, 50, 0.8))";
                    setTimeout(() => {
                        pizza.style.filter = "drop-shadow(0 2px 5px rgba(0, 0, 0, 0.3))";
                    }, 1000);
                }
                
                // Reset for next pizza
                function resetForNextPizza() {
                    pizza.style.display = 'none';
                    powerLevel = 0;
                    powerBar.style.width = '0px';
                    
                    // Check if all targets are hit
                    const allTargetsHit = targets.every(target => target.hit);
                    if (allTargetsHit) {
                        createTargets();
                    }
                }
                
                // End the game
                function endGame() {
                    gameActive = false;
                    pizza.style.display = 'none';
                    
                    // Confetti
                    for (let i = 0; i < 100; i++) {
                        createConfetti();
                    }
                    
                    // Show final score
                    finalScoreDisplay.textContent = '0';
                    let displayScore = 0;
                    const scoreInterval = setInterval(() => {
                        displayScore += Math.max(1, Math.floor(score / 50));
                        if (displayScore >= score) {
                            displayScore = score;
                            clearInterval(scoreInterval);
                        }
                        finalScoreDisplay.textContent = displayScore;
                    }, 30);
                    
                    gameOverPanel.style.display = 'block';
                }
