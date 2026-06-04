# 🚀 Release Notes - Version 0.0.6
## "The Accessibility & Extensibility Update"

We are excited to announce the release of v0.0.6, a major update focused on making **Modular Snake Pro** more inclusive, customizable, and open to the community.

---

### 🌟 Key Highlights

#### ♿ Accessibility & Inclusivity
- **Font Scaling**: Players can now adjust the UI text size (1.0x to 1.5x) in the settings menu to improve readability.
- **Colorblind Mode**: Added support for **Protanopia**, **Deuteranopia**, and **Tritanopia** palettes, ensuring that critical gameplay elements (like food and snake colors) are distinguishable for everyone.

#### 🌍 Localization Support
- **Multi-language Framework**: All game text has been decoupled from the source code.
- **Language Switching**: Support for multiple languages is now integrated, allowing the game to be translated and played by a global audience.

#### 🛠️ Modding & Extensibility
- **Mod Loader**: Introduced a new `ModManager` that allows the community to create and share mods.
- **Custom Themes**: You can now add your own visual skins by creating a simple `mod.json` file in the `mods/` folder.

#### ⚙️ Enhanced Settings System
- **Centralized Control**: A new, polished Settings menu allows real-time toggling of Music, SFX, Accessibility options, and Language.
- **Persistence**: All preferences are saved automatically to `settings.json`.

#### 📊 Advanced Analytics
- **Data-Driven Balance**: Integrated a background analytics engine that tracks session data and death causes, helping us tune the game difficulty and balance for future updates.

---

### 🛠️ Technical Improvements
- **Standalone Executable**: Added official support for PyInstaller bundling.
- **Resource Management**: Implemented a robust resource path resolver to ensure assets load correctly in both development and bundled environments.
- **Performance**: Optimized UI rendering to maintain a stable 60 FPS even with scaled fonts and accessibility filters.

### 📋 QA Status
- **Stability**: PASS ✅
- **Performance**: PASS ✅
- **Accessibility**: PASS ✅
- **Localization**: PASS ✅

---

**Thank you for playing Modular Snake Pro!**
*Your feedback helps us make the game better. Please report any bugs or suggest new mods in the repository issues.*