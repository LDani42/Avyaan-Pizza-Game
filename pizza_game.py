import streamlit as st
import streamlit.components.v1 as components

def main():
    # Make Streamlit fill the page width, hide sidebar by default
    st.set_page_config(
        page_title="Pizza Toss Game",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Hide header, footer, and menu to get a full-page feel
    st.markdown(
        """
        <style>
        /* Hide the Streamlit header, footer, and main menu */
        header {visibility: hidden;}
        footer {visibility: hidden;}
        #MainMenu {visibility: hidden;}

        /* Remove top/bottom padding on main block to get a more "fullscreen" look */
        .css-18e3th9, .css-1d391kg, .css-1v3fvcr {
            padding: 0 !important;
            margin: 0 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Full game HTML with complete implementation
    game_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <!-- Important for mobile scaling -->
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Pizza Toss Game</title>
        <style>
            /* Make the entire browser area for the game. We'll rely on the parent iframe size. */
            html, body {
                margin: 0; 
                padding: 0; 
                width: 100%; 
                height: 100%;
                overflow: hidden; 
                font-family: 'Arial', sans-serif;
                background: black;
            }

            /* 
             * #game-container: fluid width, keep aspect ratio, 
             * so it scales on smaller devices. 
             */
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
            
            #pizza {
                position: absolute;
                width: 60px;
                height: 60px;
                background: #E8BE62;
                border-radius: 50%;
                left: 80px;
                bottom: 180px;
                transform: rotate(0deg);
                display: none;
                z-index: 10;
            }
            
            #pizza::before {
                content: '';
                position: absolute;
                width: 80%;
                height: 80%;
                top: 10%;
                left: 10%;
                border-radius: 50%;
                background: #E94F37;
            }
            
            #pizza::after {
                content: '';
                position: absolute;
                width: 10%;
                height: 10%;
                background: #FFCF99;
                border-radius: 50%;
                top: 45%;
                left: 20%;
                box-shadow: 20px -15px 0 #FFCF99, 5px 20px 0 #FFCF99, 
                            25px 10px 0 #FFCF99, 15px -5px 0 #FFCF99;
            }
            
            .target {
                position: absolute;
                width: 80px;
                height: 80px;
                background: rgba(255, 255, 255, 0.9);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                font-size: 20px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                color: #222;
                border: 2px solid #222;
            }
            
            .powerup {
                position: absolute;
                width: 40px;
                height: 40px;
                background: rgba(255, 215, 0, 0.9);
                border-radius: 8px;
                box-shadow: 0 0 15px rgba(255, 215, 0, 0.8);
                animation: pulse 1.5s infinite;
            }
            
            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.1); }
                100% { transform: scale(1); }
            }
            
            #power-bar-container {
                position: absolute;
                left: 50px;
                bottom: 100px;
                width: 120px;
                height: 15px;
                background: rgba(0, 0, 0, 0.3);
                border-radius: 10px;
                overflow: hidden;
            }
            
            #power-bar {
                width: 0%;
                height: 100%;
                background: linear-gradient(90deg, #ff4800, #ff0000);
                border-radius: 10px;
                transition: width 0.1s linear;
            }
            
            #instructions, #game-over {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.8);
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                color: white;
                text-align: center;
                padding: 20px;
                z-index: 1000;
            }
            
            #game-over {
                display: none;
            }
            
            #instructions h2, #game-over h2 {
                font-size: 28px;
                margin-bottom: 20px;
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
            }
            
            #instructions p {
                font-size: 16px;
                margin-bottom: 25px;
                line-height: 1.6;
                max-width: 80%;
            }
            
            #instructions button, #game-over button {
                background: #E94F37;
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 18px;
                border-radius: 30px;
                cursor: pointer;
                transition: all 0.2s ease;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }
            
            #instructions button:hover, #game-over button:hover {
                background: #FF6347;
                transform: translateY(-2px);
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
            }

            /* 
             * MOBILE CONTROLS (on-screen buttons)
             * We'll position them at the bottom center. 
             */
            #mobile-controls {
                position: absolute;
                bottom: 0;
                left: 50%;
                transform: translateX(-50%);
                display: flex;
                gap: 10px;
                margin-bottom: 10px;
                z-index: 9999;
            }
            #mobile-controls button {
                background-color: rgba(0,0,0,0.6);
                color: white;
                font-size: 18px;
                border: 2px solid #fff;
                border-radius: 8px;
                padding: 12px 20px;
                cursor: pointer;
            }
            #mobile-controls button:active {
                background-color: rgba(255,255,255,0.3);
            }

            /* If on a wider screen (desktop), hide them so they don't block. 
               You can tweak the breakpoint as you wish. */
            @media (min-width: 768px) {
                #mobile-controls {
                    display: none;
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
                Click inside the game area and press SPACE to start! (Desktop)
            </div>

            <div id="oven"></div>
            <div id="pizza"></div>
            <div id="power-bar-container">
                <div id="power-bar"></div>
            </div>

            <!-- Overlays for instructions, game over, etc. -->
            <div id="instructions"> 
                <h2>Pizza Toss Game</h2>
                <p>
                  On Desktop: Press SPACE to get a pizza + hold/release for throw.<br>
                  Arrow UP/DOWN move the oven.<br>
                  On Mobile: Use on-screen buttons below.<br><br>
                  Collect powerups, hit targets for points!
                </p>
                <button id="start-game">Start Game</button>
            </div>

            <div id="game-over">
                <h2>Game Over!</h2>
                <p>Your final score: <span id="final-score">0</span></p>
                <button id="restart-game">Play Again</button>
            </div>

            <!-- MOBILE CONTROLS -->
            <div id="mobile-controls">
                <button id="mobile-up">UP</button>
                <button id="mobile-down">DOWN</button>
                <button id="mobile-throw">THROW</button>
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
                let powerCharging = false;
                let powerLevel = 0;
                let chargeInterval;
                let ovenY = 150;
                let ovenMoveSpeed = 5;
                let targets = [];
                let powerups = [];
                let pizzaX = 80;
                let pizzaY = 180;
                let pizzaRotation = 0;
                let pizzaVelocityX = 0;
                let pizzaVelocityY = 0;
                let pizzaGravity = 0.2;
                let pizzaThrowSound;
                let targetHitSound;
                let powerupSound;

                // For keyboard + mobile control
                const keysPressed = {
                    ArrowUp: false,
                    ArrowDown: false
                };
                
                // DOM references
                const gameContainer = document.getElementById('game-container');
                const instructionsPanel = document.getElementById('instructions');
                const gameOverPanel = document.getElementById('game-over');
                const finalScoreDisplay = document.getElementById('final-score');
                const scoreDisplay = document.getElementById('score');
                const pizzasLeftDisplay = document.getElementById('pizzas-left');
                const pizza = document.getElementById('pizza');
                const powerBar = document.getElementById('power-bar');
                const oven = document.getElementById('oven');

                // Start / restart
                document.getElementById('start-game').addEventListener('click', function() {
                    instructionsPanel.style.display = 'none';
                    startGame();
                });
                
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
                    ovenY = 150;
                    oven.style.bottom = ovenY + 'px';

                    // Remove old targets/powerups
                    clearTargetsAndPowerups();
                    
                    // Create new targets
                    createTargets();
                    
                    // Create a couple powerups
                    setTimeout(createPowerup, 3000);
                    
                    updateScore();
                    updatePizzasLeft();
                    requestAnimationFrame(gameLoop);
                }
                
                function clearTargetsAndPowerups() {
                    // Remove existing targets
                    targets.forEach(target => {
                        if (target.element && target.element.parentNode) {
                            target.element.parentNode.removeChild(target.element);
                        }
                    });
                    targets = [];
                    
                    // Remove existing powerups
                    powerups.forEach(powerup => {
                        if (powerup.element && powerup.element.parentNode) {
                            powerup.element.parentNode.removeChild(powerup.element);
                        }
                    });
                    powerups = [];
                }
                
                function createTargets() {
                    // Create 5 targets at random positions
                    for (let i = 0; i < 5; i++) {
                        const targetElement = document.createElement('div');
                        targetElement.className = 'target';
                        
                        // Random position (avoid the left side where oven is)
                        const x = 250 + Math.random() * (gameContainer.clientWidth - 350);
                        const y = 50 + Math.random() * (gameContainer.clientHeight - 100);
                        
                        // Random point value (10, 20, or 30)
                        const points = (Math.floor(Math.random() * 3) + 1) * 10;
                        
                        targetElement.style.left = x + 'px';
                        targetElement.style.bottom = y + 'px';
                        targetElement.textContent = points;
                        
                        gameContainer.appendChild(targetElement);
                        
                        targets.push({
                            element: targetElement,
                            x: x,
                            y: y,
                            width: 80,
                            height: 80,
                            points: points
                        });
                    }
                }
                
                function createPowerup() {
                    if (!gameActive) return;
                    
                    const powerupElement = document.createElement('div');
                    powerupElement.className = 'powerup';
                    
                    // Random position (avoid left side)
                    const x = 200 + Math.random() * (gameContainer.clientWidth - 300);
                    const y = 50 + Math.random() * (gameContainer.clientHeight - 100);
                    
                    powerupElement.style.left = x + 'px';
                    powerupElement.style.bottom = y + 'px';
                    
                    gameContainer.appendChild(powerupElement);
                    
                    powerups.push({
                        element: powerupElement,
                        x: x,
                        y: y,
                        width: 40,
                        height: 40,
                        type: 'extra-pizza'  // for now just one type
                    });
                    
                    // Schedule next powerup
                    setTimeout(createPowerup, 8000 + Math.random() * 5000);
                }

                function updateScore() {
                    scoreDisplay.textContent = score;
                }
                
                function updatePizzasLeft() {
                    pizzasLeftDisplay.textContent = pizzasLeft;
                }
                
                function createPizza() {
                    if (!pizzaInHand && !pizzaThrown && pizzasLeft > 0) {
                        pizzasLeft--;
                        updatePizzasLeft();
                        
                        pizzaInHand = true;
                        pizza.style.display = 'block';
                        pizzaX = 80;
                        pizzaY = ovenY + 30;
                        pizza.style.left = pizzaX + 'px';
                        pizza.style.bottom = pizzaY + 'px';
                    }
                }
                
                function throwPizza() {
                    if (pizzaInHand && !pizzaThrown) {
                        pizzaThrown = true;
                        pizzaInHand = false;
                        
                        // Apply velocity based on power level
                        const angle = Math.PI / 4;  // 45 degrees
                        const power = Math.max(1, powerLevel);
                        
                        pizzaVelocityX = Math.cos(angle) * power * 0.6;
                        pizzaVelocityY = Math.sin(angle) * power * 0.6;
                        
                        // Stop charging and reset power bar
                        stopCharging();
                    }
                }
                
                function startCharging() {
                    if (pizzaInHand && !powerCharging) {
                        powerCharging = true;
                        powerLevel = 0;
                        powerBar.style.width = '0%';
                        
                        chargeInterval = setInterval(() => {
                            powerLevel += 2;
                            if (powerLevel > 100) powerLevel = 100;
                            powerBar.style.width = powerLevel + '%';
                        }, 50);
                    }
                }
                
                function stopCharging() {
                    if (powerCharging) {
                        powerCharging = false;
                        clearInterval(chargeInterval);
                        powerBar.style.width = '0%';
                    }
                }
                
                function checkCollisions() {
                    if (!pizzaThrown) return;
                    
                    const pizzaRect = {
                        x: pizzaX,
                        y: pizzaY,
                        width: 60,
                        height: 60
                    };
                    
                    // Check target collisions
                    for (let i = 0; i < targets.length; i++) {
                        const target = targets[i];
                        
                        if (isColliding(pizzaRect, target)) {
                            // Hit a target!
                            score += target.points;
                            updateScore();
                            
                            // Remove the target
                            target.element.parentNode.removeChild(target.element);
                            targets.splice(i, 1);
                            
                            // Add a new target
                            setTimeout(() => {
                                if (gameActive) createTargets();
                            }, 1000);
                            
                            // Remove the pizza
                            resetPizza();
                            break;
                        }
                    }
                    
                    // Check powerup collisions
                    for (let i = 0; i < powerups.length; i++) {
                        const powerup = powerups[i];
                        
                        if (isColliding(pizzaRect, powerup)) {
                            // Got a powerup!
                            if (powerup.type === 'extra-pizza') {
                                pizzasLeft++;
                                updatePizzasLeft();
                            }
                            
                            // Remove the powerup
                            powerup.element.parentNode.removeChild(powerup.element);
                            powerups.splice(i, 1);
                            
                            break;
                        }
                    }
                    
                    // Check if pizza is out of bounds
                    if (pizzaX > gameContainer.clientWidth + 100 || 
                        pizzaY < -100 || 
                        pizzaX < -100 || 
                        pizzaY > gameContainer.clientHeight + 100) {
                        resetPizza();
                    }
                }
                
                function isColliding(rect1, rect2) {
                    return (
                        rect1.x < rect2.x + rect2.width &&
                        rect1.x + rect1.width > rect2.x &&
                        rect1.y < rect2.y + rect2.height &&
                        rect1.y + rect1.height > rect2.y
                    );
                }
                
                function resetPizza() {
                    pizzaThrown = false;
                    pizza.style.display = 'none';
                    
                    // Check if game over
                    if (pizzasLeft === 0 && !pizzaInHand) {
                        endGame();
                    }
                }

                let lastFrameTime = 0;
                function gameLoop(timestamp) {
                    if (!gameActive) return;
                    
                    const deltaTime = timestamp - lastFrameTime;
                    lastFrameTime = timestamp;
                    
                    // Handle oven movement
                    if (keysPressed.ArrowUp) {
                        ovenY = Math.min(ovenY + ovenMoveSpeed, gameContainer.clientHeight - 150);
                        oven.style.bottom = ovenY + 'px';
                        if (pizzaInHand && !pizzaThrown) {
                            pizzaY = ovenY + 30;
                            pizza.style.bottom = pizzaY + 'px';
                        }
                    }
                    
                    if (keysPressed.ArrowDown) {
                        ovenY = Math.max(ovenY - ovenMoveSpeed, 50);
                        oven.style.bottom = ovenY + 'px';
                        if (pizzaInHand && !pizzaThrown) {
                            pizzaY = ovenY + 30;
                            pizza.style.bottom = pizzaY + 'px';
                        }
                    }
                    
                    // Update pizza physics if thrown
                    if (pizzaThrown) {
                        // Update position
                        pizzaX += pizzaVelocityX * (deltaTime / 16);
                        pizzaY += pizzaVelocityY * (deltaTime / 16);
                        
                        // Apply gravity
                        pizzaVelocityY -= pizzaGravity * (deltaTime / 16);
                        
                        // Update rotation
                        pizzaRotation += 5 * (deltaTime / 16);
                        
                        // Update pizza display
                        pizza.style.left = pizzaX + 'px';
                        pizza.style.bottom = pizzaY + 'px';
                        pizza.style.transform = 'rotate(' + pizzaRotation + 'deg)';
                        
                        // Check for collisions
                        checkCollisions();
                    }
                    
                    requestAnimationFrame(gameLoop);
                }

                function endGame() {
                    gameActive = false;
                    gameOverPanel.style.display = 'flex';
                    finalScoreDisplay.textContent = score;
                }

                // KEYBOARD CONTROLS (desktop)
                document.addEventListener('keydown', (e) => {
                    if (e.code === 'ArrowUp' || e.code === 'ArrowDown') {
                        keysPressed[e.code] = true;
                        e.preventDefault();
                    }
                    if (e.code === 'Space' && !e.repeat) {
                        e.preventDefault();
                        onSpaceDown();
                    }
                });
                
                document.addEventListener('keyup', (e) => {
                    if (e.code === 'ArrowUp' || e.code === 'ArrowDown') {
                        keysPressed[e.code] = false;
                    }
                    if (e.code === 'Space') {
                        e.preventDefault();
                        onSpaceUp();
                    }
                });

                // MOBILE CONTROLS
                const btnUp = document.getElementById('mobile-up');
                const btnDown = document.getElementById('mobile-down');
                const btnThrow = document.getElementById('mobile-throw');

                // We use touchstart/touchend or mousedown/mouseup
                // so the user can press/hold on mobile.
                function handleUpPressStart() {
                    keysPressed.ArrowUp = true;
                }
                
                function handleUpPressEnd() {
                    keysPressed.ArrowUp = false;
                }
                
                function handleDownPressStart() {
                    keysPressed.ArrowDown = true;
                }
                
                function handleDownPressEnd() {
                    keysPressed.ArrowDown = false;
                }
                
                function handleThrowPressStart() {
                    onSpaceDown();
                }
                
                function handleThrowPressEnd() {
                    onSpaceUp();
                }

                // Attach to both touch & mouse (for cross-device)
                btnUp.addEventListener('touchstart', handleUpPressStart);
                btnUp.addEventListener('touchend', handleUpPressEnd);
                btnUp.addEventListener('mousedown', handleUpPressStart);
                btnUp.addEventListener('mouseup', handleUpPressEnd);
                btnUp.addEventListener('mouseleave', handleUpPressEnd);

                btnDown.addEventListener('touchstart', handleDownPressStart);
                btnDown.addEventListener('touchend', handleDownPressEnd);
                btnDown.addEventListener('mousedown', handleDownPressStart);
                btnDown.addEventListener('mouseup', handleDownPressEnd);
                btnDown.addEventListener('mouseleave', handleDownPressEnd);

                btnThrow.addEventListener('touchstart', handleThrowPressStart);
                btnThrow.addEventListener('touchend', handleThrowPressEnd);
                btnThrow.addEventListener('mousedown', handleThrowPressStart);
                btnThrow.addEventListener('mouseup', handleThrowPressEnd);
                btnThrow.addEventListener('mouseleave', handleThrowPressEnd);

                // The logic for pressing Space:
                function onSpaceDown() {
                    if (!gameActive) return;
                    
                    if (!pizzaInHand && !pizzaThrown) {
                        createPizza();
                    }
                    
                    if (pizzaInHand && !pizzaThrown) {
                        startCharging();
                    }
                }
                
                function onSpaceUp() {
                    if (!gameActive) return;
                    
                    if (pizzaInHand && !pizzaThrown && powerCharging) {
                        throwPizza();
                    }
                }

                // Focus the container
                window.addEventListener('click', function() {
                    document.getElementById('streamlit-app-warning').style.display = 'none';
                    gameContainer.focus();
                });
                gameContainer.tabIndex = 0;

            });
        </script>
    </body>
    </html>
    """

    # Now we embed this HTML in Streamlit with a large or "auto" height.
    components.html(game_html, height=None, scrolling=False)


if __name__ == "__main__":
    main()
