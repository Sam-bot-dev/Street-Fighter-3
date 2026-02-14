# Street-Fighter-V2 🥊🎮  
**Play fighting games using your body movements — no controller required.**

Street-Fighter-V2 is a Python-based motion controller that uses your **webcam + AI pose detection** to recognize actions like **punches and kicks**, then converts them into **keyboard inputs** for your game/emulator.

Built with **MediaPipe + OpenCV**, designed for smooth real-time gameplay.

---

## 🚀 Demo Idea
- Raise your hand / punch in the air → character punches in-game  
- Move your body → game reacts via keyboard controls  
- Works great for fighting games like Street Fighter (and more)

---

## ✨ Features
✅ Real-time webcam pose tracking  
✅ Skeleton overlay on screen (lines + joints)  
✅ Action detection (Punch / Kick)  
✅ Keyboard control output (works with most games/emulators)  
✅ Cooldown system to prevent key spamming  
✅ Easy to customize key bindings  

---

## 🧠 How It Works (Simple)
1. **OpenCV** captures your webcam feed  
2. **MediaPipe Pose** detects your body landmarks (joints)  
3. Street-Fighter-V2 checks movement rules like:
   - hand above shoulder = punch  
   - both hands up = special move (optional)  
4. It triggers a **keyboard press** to control the game

---

## 🛠️ Tech Stack
- **Python 3**
- **OpenCV**
- **MediaPipe**
- **PyAutoGUI** (or Pynput for advanced control)

---

## 📦 Installation

### 1) Clone the repository
```bash
git clone https://github.com/Sam-bot-dev/Street-fighter-3.git
cd Street-fighter-3   
```
Will add later 

## Contributors

<p align="center">
  <table>
    <tr>
      <td align="center" width="50%">
        <div>
          <img src="https://avatars.githubusercontent.com/Sam-bot-dev?s=120" width="120px;" height="120px;" alt="Bhavesh"/>
        </div>
        <div><strong>⭐ Team Leader</strong></div>
        <div><strong>Bhavesh</strong></div>
        <a href="https://github.com/Sam-bot-dev">🌐 GitHub</a>
      </td>
       <td align="center" width="50%">
        <div>
          <img src="https://avatars.githubusercontent.com/Ivar2621?s=120" width="120px;" height="120px;" alt="Hetarth"/>
        </div>
        <div><strong>🧩 Head Teammate</strong></div>
        <div><strong>Hetarth</strong></div>
        <a href="https://github.com/Ivar2621">🌐 GitHub</a>
      </td>
    </tr>
  </table>
</p>
