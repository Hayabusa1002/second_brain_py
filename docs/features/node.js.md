# Node.js Setup — Windows (MINGW64)

## 1. Download and install Node.js

1. Go to `https://nodejs.org`
2. Download the **LTS** version (left button)
3. Run the `.msi` installer
   - Accept license
   - Leave default installation path
   - On the "Tools for Native Modules" screen: check the box if you plan to use packages that require compilation (optional but recommended)
   - Click Install

## 2. Verify installation

Open a NEW terminal (MINGW64 or PowerShell) after the install finishes:

```bash
node --version
# Expected: v22.x.x or higher

npm --version
# Expected: 10.x.x or higher
```

> Important: always open a new terminal after installing — the old one won't have the updated PATH.

## 3. (Optional) Install a Node version manager

If you need to switch between Node versions in the future, use `nvm-windows`:

1. Download the installer from: `https://github.com/coreybutler/nvm-windows/releases`
2. Run `nvm-setup.exe`
3. Then use:

```bash
nvm install lts
nvm use lts
```

## 4. Configure npm for the project

Inside the project root (`second_brain_py/`), no global config is needed.
Packages are installed per-project with `npm install` inside `frontend/app/`.

## 5. Next steps after Node is installed

```bash
# Move to frontend folder
cd frontend

# Create React app with Vite
npm create vite@latest app -- --template react

# Enter the app folder
cd app

# Install dependencies
npm install

# Install project-specific packages
npm install @tabler/react @tabler/icons-react react-router-dom axios
```

## Troubleshooting

| Problem                   | Solution                                                      |
|---------------------------|---------------------------------------------------------------|
| `npm: command not found`  | Close and reopen the terminal after installing Node           |
| `EACCES permission error` | Run terminal as administrator                                 |
| `npm warn deprecated`     | Normal warnings, not errors — proceed                         |
| Slow install              | Use `npm install --prefer-offline` if you've installed before |
