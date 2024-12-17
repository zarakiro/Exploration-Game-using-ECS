
# Jungle Adventure Game (ECS-based)

This is a video game created using the **Entity-Component-System (ECS)** architecture, inspired by classic endless runner games like **Temple Run** and **Subway Surfer**. The game follows the theme of jungle exploration, where the player takes on the role of an adventurer who must avoid various obstacles to progress.

---
## Game preview
![image](https://github.com/user-attachments/assets/09acb492-4485-4c0a-aabe-0fcb5309c4cf)

## **Game Overview**

In this game, the player controls an adventurer navigating through a jungle filled with different obstacles. The goal is to survive as long as possible while avoiding hurdles like holes, logs, and other traps. The game continuously progresses, and the speed increases with the score.

**Key Features:**
- **Endless runner**: The terrain scrolls continuously, and the player must avoid obstacles.
- **ECS Architecture**: The game uses the ECS paradigm for clean and modular code.
- **Jungle theme**: The setting is inspired by a dense jungle, with various environmental hazards.
- **Obstacles**: Holes and logs that require the player to jump or crouch to avoid them.
- **Score**: The score increases as the player survives longer, and the game speed increases as the score grows.

---

## **How to Play**

1. **Controls**:
   - **Left/Right Arrow Keys** or **A/D**: Move the character between three parallel paths.
   - **Down Arrow** or **S**: Crouch to avoid logs.
   - **Up Arrow** or **W**: Jump to avoid holes.

2. **Objective**: The goal is to survive as long as possible by avoiding obstacles. The longer you survive, the higher your score gets.

3. **Game Over**: The game ends when the player collides with an obstacle they cannot avoid.

4. **Menu**:
   - On game start, you are shown a menu with the option to **Play** or **Quit**.
   - After a game over, you are presented with a screen showing your score and options to either **Retry** or **Quit**.

---

## **Installation**

To play the game on your machine, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/jungle-adventure-ecs.git
   cd jungle-adventure-ecs
   ```

2. Install dependencies:
   Make sure you have Python 3 installed and then install the necessary libraries:
   ```bash
   pip install pygame
   ```

3. Run the game:
   After installing the dependencies, run the game with the following command:
   ```bash
   python game.py
   ```

---

## **Project Structure**

- **game.py**: Main file containing the game logic.
- **assets/**: Directory containing images and other assets used in the game (e.g., character images, obstacle images, backgrounds).
- **ecs/**: Contains the core ECS architecture, including:
   - `Entity.py`: Defines the basic entity structure.
   - `Component.py`: Base class for components.
   - `System.py`: Base class for systems.
- **README.md**: Documentation for the project (this file).

---

## **How It Works**

### **ECS Architecture**

The game uses the **Entity-Component-System (ECS)** model to separate game logic into distinct systems, improving modularity and flexibility.

1. **Entities**: Objects in the game world (e.g., player, obstacles).
2. **Components**: Attributes or data associated with entities (e.g., position, velocity).
3. **Systems**: Logic that operates on entities with specific components (e.g., movement system, collision system, rendering system).

This structure allows for easy modification and extension of the game’s features.

---

## **Future Improvements**

- Add more types of obstacles (e.g., traps, enemies).
- Implement power-ups (e.g., invincibility, speed boost).
- Add sound effects and background music.
- Optimize game performance for larger maps.

---

## **Contributing**

Feel free to fork the repository and submit pull requests with improvements or bug fixes. If you want to contribute, please ensure you adhere to the following guidelines:

- Write clean and well-documented code.
- Test your changes before submitting a pull request.

---

## **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Enjoy the game, and may you survive the jungle! 🌿👣
```
