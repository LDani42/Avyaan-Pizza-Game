import streamlit as st
import streamlit.components.v1 as components

def main():
    st.set_page_config(
        page_title="Pizza Toss Game",
        layout="wide"
    )

    st.title("Pizza Toss Game")

    # HTML/JS code for the game
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
                font-family: 'Arial', sans-serif;
                background: #111;
            }
            #game-container {
                position: relative;
                width: 100%;
                max-width: 800px;
                aspect-ratio: 4 / 3;
                margin: 0 auto;
                background: linear-gradient(124deg, #ff2400, #e81d1d, #e8b71d, #e3e81d, #1de840, #1ddde8, #2b1de8, #dd00f3, #dd00f3);
                background-size: 1800% 1800%;
                animation: rainbow 18s ease infinite;
                border-radius: 12px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4), 
                            0 0 100px rgba(255, 255, 255, 0.2);
                overflow: hidden;
            }
            @keyframes rainbow { 
                0% { background-position: 0% 82% }
                50% { background-position: 100% 19% }
                100% { background-position: 0% 82% }
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

            /* NEW MOBILE CONTROLS */
            #mobile-controls {
                position: absolute;
                bottom: 10px;
                width: 100%;
                display: flex;
                justify-content: center;
                gap: 20px;
            }
            .arrow-button,
            .space-button {
                background: rgba(0, 0, 0, 0.7);
                color: white;
                border-radius: 10px;
                padding: 20px;
                font-size: 18px;
                text-align: center;
                cursor: pointer;
                pointer-events: auto;
                user-select: none;
            }
            .space-button {
                font-size: 16px;
                width: 100px;
            }
        </style>
    </head>
    <body>
        <div id="game-container">
            <div id="game-info">
                Score: <span id="score">0</span> | Pizzas: <span id="pizzas-left">5</span>
            </div>

            <div id="streamlit-app-warning">
                Click inside the game area and press SPACE to start!
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

            <div id="instructions">
                <h2>Pizza Toss Game</h2>
                <p>Press SPACE to get a pizza from the oven.<br>
                Hold SPACE to charge, release to throw.<br>
                The longer you hold, the further it will go!<br>
                Use UP and DOWN keys to move the oven.<br>
                <br>
                <span style="color: gold;">S</span>: Slows down power bar<br>
                <span style="color: #00BFFF;">D</span>: Increases throwing distance<br>
                <span style="color: #FF6347;">P</span>: Gives you 4 extra pizzas<br>
                <br>
                Hit targets to earn points! Get powerups for bonuses!</p>
                <button id="start-game">Start Game</button>
            </div>

            <div id="game-over">
                <h2>Game Over!</h2>
                <p>Your final score: <span id="final-score">0</span></p>
                <button id="restart-game">Play Again</button>
            </div>

            <!-- MOBILE CONTROLS OVERLAY -->
            <div id="mobile-controls">
                <div class="arrow-button" id="btn-up">▲</div>
                <div class="arrow-button" id="btn-down">▼</div>
                <div class="space-button" id="btn-space">THROW</div>
            </div>
        </div>

        <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Game variables
            let score = 0;
            let pizzasLeft = 5;
            let gameActive = false;
            let pizzaInHand = false;
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

            const gameContainer = document.getElementById('game-container');
            const pizza = document.getElementById('pizza');
            const powerBar = document.getElementById('power-bar');
            const scoreDisplay = document.getElementById('score');
            const pizzasLeftDisplay = document.getElementById('pizzas-left');
            const instructionsPanel = document.getElementById('instructions');
            const gameOverPanel = document.getElementById('game-over');
            const finalScoreDisplay = document.getElementById('final-score');

            // Object to track which keys are held down
            const keysPressed = {
                ArrowUp: false,
                ArrowDown: false
            };

            // Refactored Key Handlers
            function handleKeyDown(code) {
                if (!gameActive) return;

                if (code === 'ArrowUp' || code === 'ArrowDown') {
                    keysPressed[code] = true;
                }

                if (code === 'Space') {
                    if (!pizzaInHand && !pizzaThrown) {
                        createPizza();
                        pizzaInHand = true;
                    } else if (pizzaInHand && !pizzaThrown && !powerCharging) {
                        // Start charging
                        powerCharging = true;
                        powerLevel = 0;
                        chargeInterval = setInterval(() => {
                            powerLevel += 2;
                            if (powerLevel > 300) powerLevel = 300;
                            powerBar.style.width = powerLevel + 'px';
                        }, 16);
                    }
                }
            }

            function handleKeyUp(code) {
                if (!gameActive) return;

                if (code === 'ArrowUp' || code === 'ArrowDown') {
                    keysPressed[code] = false;
                }

                if (code === 'Space') {
                    if (powerCharging) {
                        clearInterval(chargeInterval);
                        powerCharging = false;
                        pizzaThrown = true;

                        // Calculate throw power
                        let throwPower = 0.5 + (powerLevel / 300) * 2.0;
                        if (activePowerups.extraDistance) {
                            throwPower *= 1.5;
                        }

                        // Animate throw
                        let pizzaX = 70;
                        let pizzaY = ovenY + 30;
                        let pizzaRotation = 0;
                        let pizzaXSpeed = 7 * throwPower;
                        let pizzaYSpeed = 2 * throwPower;
                        let pizzaGravity = 0.15;

                        const throwInterval = setInterval(() => {
                            pizzaX += pizzaXSpeed;
                            pizzaY += pizzaYSpeed;
                            pizzaYSpeed -= pizzaGravity;
                            pizzaRotation += 5;

                            pizza.style.left = pizzaX + 'px';
                            pizza.style.bottom = pizzaY + 'px';
                            pizza.style.transform = `rotate(${pizzaRotation}deg)`;

                            // Out of bounds?
                            if (pizzaX > 850 || pizzaY < -50) {
                                clearInterval(throwInterval);
                                pizzasLeft--;
                                updatePizzasLeft();
                                pizzaThrown = false;
                                pizzaInHand = false;

                                if (pizzasLeft > 0) {
                                    resetForNextPizza();
                                } else {
                                    endGame();
                                }
                            }
                        }, 16);

                        // Reset bar
                        setTimeout(() => {
                            powerBar.style.width = '0px';
                        }, 500);
                    }
                }
            }

            // Existing keyboard events now just call handleKeyDown/handleKeyUp
            document.addEventListener('keydown', function(event) {
                if (event.repeat) return;
                event.preventDefault();
                handleKeyDown(event.code);
            });

            document.addEventListener('keyup', function(event) {
                event.preventDefault();
                handleKeyUp(event.code);
            });

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

            function startGame() {
                score = 0;
                pizzasLeft = 5;
                gameActive = true;
                pizzaInHand = false;
                pizzaThrown = false;
                ovenY = 150; // Reset oven position
                document.getElementById('oven').style.bottom = ovenY + 'px';

                // Clear old targets
                targets.forEach(target => {
                    if (target.element.parentNode) {
                        gameContainer.removeChild(target.element);
                    }
                });
                targets = [];

                // Clear old powerups
                powerups.forEach(powerup => {
                    if (powerup.element.parentNode) {
                        gameContainer.removeChild(powerup.element);
                    }
                });
                powerups = [];

                createTargets();
                updateScore();
                updatePizzasLeft();

                lastFrameTime = performance.now();
                requestAnimationFrame(gameLoop);
            }

            function createTargets() {
                // Remove existing
                targets.forEach(target => {
                    if (target.element.parentNode) {
                        gameContainer.removeChild(target.element);
                    }
                });
                targets = [];

                // Make 3 targets
                for (let i = 0; i < 3; i++) {
                    const targetElement = document.createElement('div');
                    targetElement.className = 'target';

                    const x = 350 + (i * 130);
                    const y = 100 + Math.random() * 350;

                    targetElement.style.left = x + 'px';
                    targetElement.style.top = y + 'px';

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

            function createPowerup() {
                if (Math.random() < 0.5 && powerups.length < 3) {
                    const powerupElement = document.createElement('div');
                    powerupElement.className = 'powerup';

                    const x = 300 + Math.random() * 400;
                    const y = 100 + Math.random() * 350;
                    powerupElement.style.left = x + 'px';
                    powerupElement.style.top = y + 'px';

                    const rand = Math.random();
                    let type;
                    if (rand < 0.4) {
                        type = 'S';
                        powerupElement.classList.add('powerup-slow');
                    } else if (rand < 0.8) {
                        type = 'D';
                        powerupElement.classList.add('powerup-distance');
                    } else {
                        type = 'P';
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

            function updatePizzasLeft() {
                pizzasLeftDisplay.textContent = pizzasLeft;
                pizzasLeftDisplay.style.color = '#FFD700';
                pizzasLeftDisplay.style.textShadow = '0 0 10px rgba(255, 215, 0, 0.7)';
                setTimeout(() => {
                    pizzasLeftDisplay.style.color = 'white';
                    pizzasLeftDisplay.style.textShadow = 'none';
                }, 300);
            }

            function createPizza() {
                pizza.style.display = 'block';
                pizza.style.left = '70px';
                pizza.style.bottom = (ovenY + 30) + 'px';
                pizza.style.transform = 'rotate(0deg)';

                while (pizza.firstChild) {
                    pizza.removeChild(pizza.firstChild);
                }

                // sauce
                for (let i = 0; i < 10; i++) {
                    const sauce = document.createElement('div');
                    sauce.className = 'sauce';
                    sauce.style.left = 5 + Math.random() * 50 + 'px';
                    sauce.style.top = 5 + Math.random() * 50 + 'px';
                    pizza.appendChild(sauce);
                }

                // cheese
                for (let i = 0; i < 12; i++) {
                    const cheese = document.createElement('div');
                    cheese.className = 'cheese';
                    cheese.style.left = 5 + Math.random() * 50 + 'px';
                    cheese.style.top = 5 + Math.random() * 50 + 'px';
                    cheese.style.transform = `rotate(${Math.random() * 360}deg)`;
                    pizza.appendChild(cheese);
                }

                // pepperoni
                for (let i = 0; i < 5; i++) {
                    const pepperoni = document.createElement('div');
                    pepperoni.className = 'pepperoni';
                    pepperoni.style.left = 10 + Math.random() * 40 + 'px';
                    pepperoni.style.top = 10 + Math.random() * 40 + 'px';
                    pizza.appendChild(pepperoni);
                }

                pizza.style.filter = "drop-shadow(0 0 15px rgba(255, 120, 50, 0.8))";
                setTimeout(() => {
                    pizza.style.filter = "drop-shadow(0 2px 5px rgba(0, 0, 0, 0.3))";
                }, 1000);
            }

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

            function endGame() {
                gameActive = false;
                pizza.style.display = 'none';

                // confetti
                for (let i = 0; i < 100; i++) {
                    createConfetti();
                }

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

            function createConfetti() {
                const colors = ['#FF5252', '#FFEB3B', '#2196F3', '#4CAF50', '#E040FB', '#FF9800'];
                const confetti = document.createElement('div');
                const color = colors[Math.floor(Math.random() * colors.length)];

                confetti.style.position = 'absolute';
                confetti.style.width = Math.random() * 10 + 5 + 'px';
                confetti.style.height = Math.random() * 5 + 5 + 'px';
                confetti.style.backgroundColor = color;
                confetti.style.borderRadius = Math.random() > 0.5 ? '50%' : '0';
                confetti.style.top = '-10px';
                confetti.style.left = Math.random() * gameContainer.offsetWidth + 'px';
                confetti.style.transform = `rotate(${Math.random() * 360}deg)`;
                confetti.style.zIndex = '1000';
                confetti.style.opacity = Math.random() + 0.5;
                confetti.style.animation = `confettiFall ${Math.random() * 3 + 2}s forwards ease-in`;

                gameContainer.appendChild(confetti);

                setTimeout(() => {
                    if (confetti.parentNode) {
                        gameContainer.removeChild(confetti);
                    }
                }, 5000);
            }

            // MOBILE TOUCH CONTROLS
            const btnUp = document.getElementById('btn-up');
            const btnDown = document.getElementById('btn-down');
            const btnSpace = document.getElementById('btn-space');

            function preventScroll(e) { e.preventDefault(); }

            btnUp.addEventListener('touchstart', (e) => {
                preventScroll(e);
                handleKeyDown('ArrowUp');
            });
            btnUp.addEventListener('touchend', (e) => {
                preventScroll(e);
                handleKeyUp('ArrowUp');
            });

            btnDown.addEventListener('touchstart', (e) => {
                preventScroll(e);
                handleKeyDown('ArrowDown');
            });
            btnDown.addEventListener('touchend', (e) => {
                preventScroll(e);
                handleKeyUp('ArrowDown');
            });

            btnSpace.addEventListener('touchstart', (e) => {
                preventScroll(e);
                handleKeyDown('Space');
            });
            btnSpace.addEventListener('touchend', (e) => {
                preventScroll(e);
                handleKeyUp('Space');
            });

            // Main game loop
            function gameLoop(timestamp) {
                const deltaTime = timestamp - lastFrameTime;
                lastFrameTime = timestamp;

                if (!gameActive) return;

                // Oven movement
                if (keysPressed.ArrowUp) {
                    ovenY = Math.min(ovenY + ovenMoveSpeed, 400);
                    document.getElementById('oven').style.bottom = ovenY + 'px';
                    if (pizzaInHand && !pizzaThrown) {
                        pizza.style.bottom = (ovenY + 30) + 'px';
                    }
                }
                if (keysPressed.ArrowDown) {
                    ovenY = Math.max(ovenY - ovenMoveSpeed, 50);
                    document.getElementById('oven').style.bottom = ovenY + 'px';
                    if (pizzaInHand && !pizzaThrown) {
                        pizza.style.bottom = (ovenY + 30) + 'px';
                    }
                }

                // If pizza thrown, check collisions
                if (pizzaThrown) {
                    const pizzaRect = pizza.getBoundingClientRect();

                    // Collisions with targets
                    targets.forEach(target => {
                        if (!target.hit) {
                            const targetRect = target.element.getBoundingClientRect();
                            if (
                                pizzaRect.right > targetRect.left &&
                                pizzaRect.left < targetRect.right &&
                                pizzaRect.bottom > targetRect.top &&
                                pizzaRect.top < targetRect.bottom
                            ) {
                                // Hit a target
                                target.hit = true;
                                target.element.style.backgroundColor = 'rgba(255, 215, 0, 0.7)';
                                target.element.style.animation = 'targetHit 0.5s ease';
                                score += target.points;
                                updateScore();

                                // Hit effect
                                const hitEffect = document.createElement('div');
                                hitEffect.textContent = `+${target.points}`;
                                hitEffect.style.position = 'absolute';
                                hitEffect.style.color = '#FFD700';
                                hitEffect.style.fontWeight = 'bold';
                                hitEffect.style.fontSize = '24px';
                                hitEffect.style.textShadow = '0 0 10px rgba(255, 215, 0, 0.7), 2px 2px 4px rgba(0,0,0,0.5)';
                                hitEffect.style.left = `${target.x}px`;
                                hitEffect.style.top = `${target.y - 30}px`;
                                hitEffect.style.zIndex = '150';
                                gameContainer.appendChild(hitEffect);

                                let hitOpacity = 1;
                                let posY = target.y - 30;
                                const hitInterval = setInterval(() => {
                                    hitOpacity -= 0.05;
                                    posY -= 2;
                                    hitEffect.style.opacity = hitOpacity;
                                    hitEffect.style.top = `${posY}px`;

                                    if (hitOpacity <= 0) {
                                        clearInterval(hitInterval);
                                        if (hitEffect.parentNode) {
                                            gameContainer.removeChild(hitEffect);
                                        }
                                    }
                                }, 40);

                                // Maybe create powerup
                                createPowerup();
                            }
                        }
                    });

                    // Collisions with powerups
                    powerups.forEach(powerup => {
                        if (!powerup.collected) {
                            const powerupRect = powerup.element.getBoundingClientRect();
                            if (
                                pizzaRect.right > powerupRect.left &&
                                pizzaRect.left < powerupRect.right &&
                                pizzaRect.bottom > powerupRect.top &&
                                pizzaRect.top < powerupRect.bottom
                            ) {
                                // Collected
                                powerup.collected = true;
                                gameContainer.removeChild(powerup.element);

                                // Apply effect
                                if (powerup.type === 'S') {
                                    activePowerups.slowBar = true;
                                    setTimeout(() => { activePowerups.slowBar = false; }, 10000);

                                    const effectIcon = document.createElement('div');
                                    effectIcon.innerHTML = '⏱️';
                                    effectIcon.style.position = 'absolute';
                                    effectIcon.style.fontSize = '30px';
                                    effectIcon.style.left = '20px';
                                    effectIcon.style.bottom = '100px';
                                    effectIcon.style.zIndex = '200';
                                    effectIcon.style.filter = 'drop-shadow(0 0 5px gold)';
                                    effectIcon.style.animation = 'fadeInOut 10s forwards';
                                    gameContainer.appendChild(effectIcon);

                                    setTimeout(() => {
                                        if (effectIcon.parentNode) {
                                            gameContainer.removeChild(effectIcon);
                                        }
                                    }, 10000);

                                } else if (powerup.type === 'D') {
                                    activePowerups.extraDistance = true;
                                    setTimeout(() => { activePowerups.extraDistance = false; }, 10000);

                                    const effectIcon = document.createElement('div');
                                    effectIcon.innerHTML = '🚀';
                                    effectIcon.style.position = 'absolute';
                                    effectIcon.style.fontSize = '30px';
                                    effectIcon.style.left = '60px';
                                    effectIcon.style.bottom = '100px';
                                    effectIcon.style.zIndex = '200';
                                    effectIcon.style.filter = 'drop-shadow(0 0 5px #00BFFF)';
                                    effectIcon.style.animation = 'fadeInOut 10s forwards';
                                    gameContainer.appendChild(effectIcon);

                                    setTimeout(() => {
                                        if (effectIcon.parentNode) {
                                            gameContainer.removeChild(effectIcon);
                                        }
                                    }, 10000);

                                } else if (powerup.type === 'P') {
                                    pizzasLeft += 4;
                                    updatePizzasLeft();

                                    const pizzaAlert = document.createElement('div');
                                    pizzaAlert.textContent = "+4 PIZZAS!";
                                    pizzaAlert.style.position = "absolute";
                                    pizzaAlert.style.color = "#FF6347";
                                    pizzaAlert.style.fontWeight = "bold";
                                    pizzaAlert.style.fontSize = "32px";
                                    pizzaAlert.style.left = "400px";
                                    pizzaAlert.style.top = "100px";
                                    pizzaAlert.style.textShadow = "0 0 10px rgba(255,99,71,0.7), 2px 2px 4px rgba(0,0,0,0.5)";
                                    pizzaAlert.style.zIndex = "200";
                                    gameContainer.appendChild(pizzaAlert);

                                    for (let i = 0; i < 4; i++) {
                                        const pizzaIcon = document.createElement('div');
                                        pizzaIcon.innerHTML = '🍕';
                                        pizzaIcon.style.position = "absolute";
                                        pizzaIcon.style.fontSize = "24px";
                                        pizzaIcon.style.left = `${350 + i * 25}px`;
                                        pizzaIcon.style.top = "150px";
                                        pizzaIcon.style.zIndex = "200";
                                        pizzaIcon.style.animation = `pizzaFall ${0.5 + i * 0.2}s forwards ease-out`;
                                        gameContainer.appendChild(pizzaIcon);

                                        setTimeout(() => {
                                            if (pizzaIcon.parentNode) {
                                                gameContainer.removeChild(pizzaIcon);
                                            }
                                        }, 2000);
                                    }

                                    let opacity = 1;
                                    const fadeInterval = setInterval(() => {
                                        opacity -= 0.05;
                                        pizzaAlert.style.opacity = opacity;
                                        if (opacity <= 0) {
                                            clearInterval(fadeInterval);
                                            if (pizzaAlert.parentNode) {
                                                gameContainer.removeChild(pizzaAlert);
                                            }
                                        }
                                    }, 50);
                                }
                            }
                        }
                    });
                }

                requestAnimationFrame(gameLoop);
            }

            // Focus handler
            window.addEventListener('click', function() {
                document.getElementById('streamlit-app-warning').style.display = 'none';
                gameContainer.focus();
            });

            // Make sure container can receive keyboard events
            gameContainer.tabIndex = 0;
        });
        </script>
    </body>
    </html>
    """

    # Simple style override for your Streamlit layout
    st.markdown(
        """
        <style>
        /* Just for the outer container in Streamlit. */
        .outer-game-wrapper {
            width: 100%;
            max-width: 900px;  /* so the entire embed doesn't overflow on desktop */
            margin: 0 auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("""
    ### How to Play
    1. Click inside the game area to give it focus  
    2. Use **SPACE** to get a pizza and charge/throw  
    3. Use **UP/DOWN** arrow keys to move the oven  
    4. Hit targets to score points and collect powerups!  
    """)

    st.markdown('<div class="outer-game-wrapper">', unsafe_allow_html=True)
    
    # Setting a height ~800–1000 px usually fits large desktop screens.
    # On mobile, users can scroll within the iframe if needed.
    components.html(game_html, height=900, scrolling=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    ### About This Game
    This is a simple Pizza Toss game built by Avyaan Dani. 
    """)

if __name__ == "__main__":
    main()
