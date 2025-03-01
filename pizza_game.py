import streamlit as st
import streamlit.components.v1 as components

def main():
    st.set_page_config(
        page_title="Avyaan's Pizza Toss Game",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    st.title("Avyaan's Pizza Toss Game")
    
    # HTML/JS code for the game - properly formatted as a string for Streamlit
    game_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
         <meta charset="UTF-8">
         <meta name="viewport" content="width=device-width, initial-scale=1.0">
         <title>Pizza Toss Game</title>
         <style>
             /* Your existing CSS styling */
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
             /* ... (rest of your CSS) ... */
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
              
              <div id="game-over" style="display: none;">
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
                   
                   // Start the game function
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
                             cheese.style.transform = 'rotate(' + (Math.random() * 360) + 'deg)';
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
                   
                   // A simple game loop function
                   function gameLoop(currentTime) {
                        if (!gameActive) return;
                        // Update time for smooth animation
                        lastFrameTime = currentTime;
                        
                        // Example: update power bar if charging
                        if (powerCharging) {
                             powerLevel += powerBarSpeed;
                             if (powerLevel > 300) {
                                  powerBarSpeed = -powerBarSpeed;
                             } else if (powerLevel < 0) {
                                  powerBarSpeed = -powerBarSpeed;
                             }
                             powerBar.style.width = powerLevel + 'px';
                        }
                        
                        // Continue game loop
                        requestAnimationFrame(gameLoop);
                   }
                   
                   // Create confetti for game over effect
                   function createConfetti() {
                        const confetti = document.createElement('div');
                        confetti.style.position = 'absolute';
                        confetti.style.width = '5px';
                        confetti.style.height = '5px';
                        confetti.style.background = '#' + Math.floor(Math.random()*16777215).toString(16);
                        confetti.style.left = Math.random() * gameContainer.offsetWidth + 'px';
                        confetti.style.top = '-10px';
                        gameContainer.appendChild(confetti);
                        
                        let confettiSpeed = 2 + Math.random() * 3;
                        function fall() {
                             let top = parseFloat(confetti.style.top);
                             if (top < gameContainer.offsetHeight) {
                                  confetti.style.top = (top + confettiSpeed) + 'px';
                                  requestAnimationFrame(fall);
                             } else {
                                  gameContainer.removeChild(confetti);
                             }
                        }
                        fall();
                   }
                   
                   // End the game
                   function endGame() {
                        gameActive = false;
                        pizza.style.display = 'none';
                        
                        // Create confetti effect
                        for (let i = 0; i < 100; i++) {
                             createConfetti();
                        }
                        
                        // Animate final score display
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
              });
         </script>
    </body>
    </html>
    """
    
    # Simple style override for your Streamlit layout
    st.markdown(
        """
        <style>
        /* Outer container styling in Streamlit that's responsive */
        .outer-game-wrapper {
            width: 100%;
            max-width: 900px;
            margin: 0 auto;
        }
        
        /* Make text more readable on mobile */
        @media (max-width: 768px) {
            .mobile-instructions {
                font-size: 16px !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Render the game HTML using Streamlit components
    components.html(game_html, height=600)

if __name__ == '__main__':
    main()
