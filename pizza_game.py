const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
canvas.width = 800;
canvas.height = 600;

// Game state
let gameState = {
    pizzasRemaining: 10, // Player starts with 10 pizzas
    level: 1,
    activePizzas: [],
    targets: [],
    powerUps: [],
    score: 0,
    targetsHit: 0,
    totalTargets: 3 // Need to hit 3 targets to advance level
};

// Pizza object
class Pizza {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.radius = 20;
        this.velocityX = 0;
        this.velocityY = 0;
        this.active = true;
    }

    update() {
        this.x += this.velocityX;
        this.y += this.velocityY;
        this.velocityY += 0.2; // Gravity

        // Deactivate if out of bounds
        if (this.y > canvas.height || this.x < 0 || this.x > canvas.width) {
            this.active = false;
        }
    }

    draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = '#e67e22'; // Pizza color
        ctx.fill();
        
        // Draw pepperoni
        for (let i = 0; i < 5; i++) {
            const angle = (i / 5) * Math.PI * 2;
            const pepX = this.x + Math.cos(angle) * (this.radius * 0.6);
            const pepY = this.y + Math.sin(angle) * (this.radius * 0.6);
            
            ctx.beginPath();
            ctx.arc(pepX, pepY, this.radius * 0.2, 0, Math.PI * 2);
            ctx.fillStyle = '#c0392b'; // Pepperoni color
            ctx.fill();
        }
    }
}

// Target object
class Target {
    constructor() {
        this.width = 60;
        this.height = 80;
        this.x = Math.random() * (canvas.width - this.width);
        this.y = Math.random() * (canvas.height / 2 - this.height);
        this.hit = false;
    }

    draw() {
        if (!this.hit) {
            ctx.fillStyle = '#3498db';
            ctx.fillRect(this.x, this.y, this.width, this.height);
        }
    }

    checkCollision(pizza) {
        if (this.hit) return false;
        
        return pizza.x + pizza.radius > this.x && 
               pizza.x - pizza.radius < this.x + this.width &&
               pizza.y + pizza.radius > this.y && 
               pizza.y - pizza.radius < this.y + this.height;
    }
}

// PowerUp object 
class PowerUp {
    constructor() {
        this.radius = 15;
        this.x = Math.random() * (canvas.width - this.radius * 2) + this.radius;
        this.y = Math.random() * (canvas.height / 2 - this.radius * 2) + this.radius;
        this.type = Math.random() < 0.5 ? 'extra' : 'super'; // 50% chance for each type
        this.active = true;
    }

    draw() {
        if (!this.active) return;
        
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        
        // Different colors for different power-up types
        if (this.type === 'extra') {
            ctx.fillStyle = '#2ecc71'; // Green for regular power-up (extra pizzas)
        } else {
            ctx.fillStyle = '#9b59b6'; // Purple for super power-up (7 pizzas)
        }
        
        ctx.fill();
        
        // Draw a "P" inside the power-up
        ctx.fillStyle = 'white';
        ctx.font = '15px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(this.type === 'extra' ? '+3' : '+7', this.x, this.y);
    }

    checkCollision(x, y) {
        if (!this.active) return false;
        
        const distance = Math.sqrt(Math.pow(this.x - x, 2) + Math.pow(this.y - y, 2));
        return distance < this.radius + 10; // +10 for easier collision
    }
}

// Initialize game
function initGame() {
    gameState = {
        pizzasRemaining: 10,
        level: 1,
        activePizzas: [],
        targets: [],
        powerUps: [],
        score: 0,
        targetsHit: 0,
        totalTargets: 3
    };
    
    // Create targets
    for (let i = 0; i < gameState.totalTargets; i++) {
        gameState.targets.push(new Target());
    }
    
    // Create power-ups
    gameState.powerUps.push(new PowerUp());
    
    // Add another power-up
    if (Math.random() < 0.7) { // 70% chance for a second power-up
        gameState.powerUps.push(new PowerUp());
    }
}

// Handle mouse movement
let mouseX = 0;
let mouseY = 0;
canvas.addEventListener('mousemove', (e) => {
    const rect = canvas.getBoundingClientRect();
    mouseX = e.clientX - rect.left;
    mouseY = e.clientY - rect.top;
    
    // Check for power-up collision
    gameState.powerUps.forEach(powerUp => {
        if (powerUp.active && powerUp.checkCollision(mouseX, mouseY)) {
            // Apply power-up effects
            if (powerUp.type === 'extra') {
                gameState.pizzasRemaining += 3;
            } else { // 'super' power-up
                gameState.pizzasRemaining += 7; // Add 7 more pizzas as requested
            }
            
            powerUp.active = false;
        }
    });
});

// Handle mouse click (throw pizza)
canvas.addEventListener('click', (e) => {
    if (gameState.pizzasRemaining > 0) {
        const rect = canvas.getBoundingClientRect();
        const clickX = e.clientX - rect.left;
        const clickY = e.clientY - rect.top;
        
        // Create a new pizza at the bottom of the screen
        const pizza = new Pizza(canvas.width / 2, canvas.height - 50);
        
        // Calculate velocity based on click position
        const deltaX = clickX - pizza.x;
        const deltaY = clickY - pizza.y;
        const distance = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
        const speed = 10;
        
        pizza.velocityX = (deltaX / distance) * speed;
        pizza.velocityY = (deltaY / distance) * speed;
        
        gameState.activePizzas.push(pizza);
        gameState.pizzasRemaining--;
    }
});

// Game loop
function gameLoop() {
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw and update pizzas
    gameState.activePizzas = gameState.activePizzas.filter(pizza => pizza.active);
    gameState.activePizzas.forEach(pizza => {
        pizza.update();
        pizza.draw();
        
        // Check for collisions with targets
        gameState.targets.forEach(target => {
            if (!target.hit && target.checkCollision(pizza)) {
                target.hit = true;
                gameState.targetsHit++;
                gameState.score += 100;
                pizza.active = false;
                
                // Check if all targets are hit
                if (gameState.targetsHit >= gameState.totalTargets) {
                    advanceToNextLevel();
                }
            }
        });
    });
    
    // Draw targets
    gameState.targets.forEach(target => target.draw());
    
    // Draw power-ups
    gameState.powerUps.forEach(powerUp => powerUp.draw());
    
    // Draw game info
    ctx.fillStyle = 'black';
    ctx.font = '20px Arial';
    ctx.textAlign = 'left';
    ctx.fillText(`Pizzas: ${gameState.pizzasRemaining}`, 20, 30);
    ctx.fillText(`Score: ${gameState.score}`, 20, 60);
    ctx.fillText(`Level: ${gameState.level}`, 20, 90);
    ctx.fillText(`Targets: ${gameState.targetsHit}/${gameState.totalTargets}`, 20, 120);
    
    // Check for game over
    if (gameState.pizzasRemaining === 0 && gameState.activePizzas.length === 0 && gameState.targetsHit < gameState.totalTargets) {
        ctx.fillStyle = 'red';
        ctx.font = '40px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('GAME OVER', canvas.width / 2, canvas.height / 2);
        ctx.font = '20px Arial';
        ctx.fillText('Click to restart', canvas.width / 2, canvas.height / 2 + 40);
        
        // Add click listener to restart
        canvas.onclick = () => {
            initGame();
            canvas.onclick = null; // Remove the event listener
        };
        
        return; // Stop the game loop
    }
    
    // Continue the game loop
    requestAnimationFrame(gameLoop);
}

// Function to advance to the next level
function advanceToNextLevel() {
    gameState.level++;
    gameState.targetsHit = 0;
    gameState.pizzasRemaining += 5; // Bonus pizzas for completing a level
    
    // Clear targets and create new ones (more for higher levels)
    gameState.targets = [];
    for (let i = 0; i < gameState.totalTargets; i++) {
        gameState.targets.push(new Target());
    }
    
    // Clear power-ups and create new ones
    gameState.powerUps = [];
    const numPowerUps = 1 + Math.floor(Math.random() * 2); // 1-2 power-ups per level
    for (let i = 0; i < numPowerUps; i++) {
        gameState.powerUps.push(new PowerUp());
    }
    
    // Display level up message
    ctx.fillStyle = 'green';
    ctx.font = '40px Arial';
    ctx.textAlign = 'center';
    ctx.fillText(`LEVEL ${gameState.level}!`, canvas.width / 2, canvas.height / 2);
}

// Start the game
initGame();
gameLoop();
