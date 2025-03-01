import streamlit as st
import streamlit.components.v1 as components

def main():
    # Make Streamlit fill the page width, hide sidebar by default
    st.set_page_config(
        page_title="Pizza Toss Game",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Hide header, footer, and menu to get a full‐page feel
    st.markdown(
        """
        <style>
        /* Hide the Streamlit header, footer, and main menu */
        header {visibility: hidden;}
        footer {visibility: hidden;}
        MainMenu {visibility: hidden;}

        /* Remove top/bottom padding on main block to get a more "fullscreen" look */
        .css-18e3th9, .css-1d391kg, .css-1v3fvcr {
            padding: 0 !important;
            margin: 0 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # This HTML now includes mobile buttons: #mobile-controls
    # We'll attach JS event listeners so they replicate "ArrowUp"/"ArrowDown"/"Space".
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

            /* The rest of your game styles remain as before... */

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

            /* Oven, pizza, targets, powerups, etc. ... same as your previous code. */
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
            /* ... omitted for brevity, keep the rest of your pizza, target, power bar, etc. CSS ... */

            /*
             * (Comment out old scaling media queries)
             * @media (max-width: 850px) {...} 
             */

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
            <!-- The game info, instructions, oven, pizza, etc. go here ... -->
            <div id="game-info">
                Score: <span id="score">0</span> | Pizzas: <span id="pizzas-left">5</span>
            </div>
            <div id="streamlit-app-warning">
                Click inside the game area and press SPACE to start! (Desktop)
            </div>

            <div id="oven">
                <!-- Oven internals ... -->
            </div>

            <div id="pizza" style="display: none;"></div>
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
                /*
                 * Original JS code for game logic, variables, 
                 * targets, createPizza, startGame, etc... 
                 * (We won't re-paste it all here for brevity,
                 *  but keep your entire logic from before.)
                 */
                
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
                    document.getElementById('oven').style.bottom = ovenY + 'px';

                    // remove old targets/powerups if needed
                    // create new targets
                    // etc.
                    updateScore();
                    updatePizzasLeft();
                    requestAnimationFrame(gameLoop);
                }

                function updateScore() {
                    scoreDisplay.textContent = score;
                }
                function updatePizzasLeft() {
                    pizzasLeftDisplay.textContent = pizzasLeft;
                }

                // [Add all your game logic for createPizza, throwPizza, collisions, etc. here]
                // For example:

                let lastFrameTime = 0;
                function gameLoop(timestamp) {
                    if (!gameActive) return;
                    const deltaTime = timestamp - lastFrameTime;
                    lastFrameTime = timestamp;

                    // handle oven movement
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

                    // throw animation + collision checks ...
                    requestAnimationFrame(gameLoop);
                }

                function endGame() {
                    gameActive = false;
                    gameOverPanel.style.display = 'block';
                    finalScoreDisplay.textContent = score;
                }

                // KEYBOARD CONTROLS (desktop)
                document.addEventListener('keydown', (e) => {
                    if (!gameActive) return;
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
                    if (!gameActive) return;
                    if (e.code === 'ArrowUp' || e.code === 'ArrowDown') {
                        keysPressed[e.code] = false;
                    }
                    if (e.code === 'Space') {
                        e.preventDefault();
                        onSpaceUp();
                    }
                });

                // MOBILE CONTROLS
                // We'll replicate the same events as arrow + space.
                const btnUp = document.getElementById('mobile-up');
                const btnDown = document.getElementById('mobile-down');
                const btnThrow = document.getElementById('mobile-throw');

                // We use touchstart/touchend or mousedown/mouseup
                // so the user can press/hold on mobile.
                function handleUpPressStart() {
                    if (gameActive) keysPressed.ArrowUp = true;
                }
                function handleUpPressEnd() {
                    keysPressed.ArrowUp = false;
                }
                function handleDownPressStart() {
                    if (gameActive) keysPressed.ArrowDown = true;
                }
                function handleDownPressEnd() {
                    keysPressed.ArrowDown = false;
                }
                function handleThrowPressStart() {
                    if (gameActive) {
                        onSpaceDown();
                    }
                }
                function handleThrowPressEnd() {
                    if (gameActive) {
                        onSpaceUp();
                    }
                }

                // Attach to both touch & mouse (for cross‐device)
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

                // The same logic you had for pressing Space:
                function onSpaceDown() {
                    // e.g. create pizza or start charging
                }
                function onSpaceUp() {
                    // e.g. release throw
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
    # If you want absolutely no scroll, pick a large fixed height (like 1500)
    # or even `height=None, scrolling=False` to let CSS manage the internal size.
    components.html(game_html, height=None, scrolling=False)


if __name__ == "__main__":
    main()
