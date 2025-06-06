const {
  app,
  BrowserWindow
} = require('electron')

const path = require('path')
const fs = require("fs")
const isDev = require("electron-is-dev")
const execFile = require("child_process").execFile

const API_PROD_PATH = path.join(process.resourcesPath, "../lib/api/api.exe")
const API_DEV_PATH = path.join(__dirname, "../../../engine/api.py")
const INDEX_PATH = path.join(__dirname, '../../src/render/index.html')
const app_instance = app.requestSingleInstanceLock()

let pyshell = null
let child = null

// check if current app is Production or Development using electron-is-dev library
// current app is not production, just run the API from api.py,else run the api from API_PROD_PATH
// if (isDev) {
//   try {
//     require('electron-reloader')(module)
//   } catch (_) {}
//
//   const {
//     PythonShell
//   } = require('python-shell')
//
//   pyshell = PythonShell.run(API_DEV_PATH, {}, function (err, results) {
//     if (err) console.error(err)
//     else console.log(results)
//   })
// } else {
//   child = execFile(API_PROD_PATH, {
//     windowsHide: true,
//   })
// }

if (!isDev) {
  child = execFile(API_PROD_PATH, {
    windowsHide: true,
  })
}

//create Main Window
function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: true,
      contextIsolation: false,
      enableRemoteModule: true
    }
  })

  // and load the index.html of the app.
  if (isDev){
    mainWindow.loadURL("http://localhost:5173")
  }
  else{
    mainWindow.loadFile(INDEX_PATH)
  }
  // Open the DevTools.
  if (isDev) mainWindow.webContents.openDevTools()


  // only one instance exists
  // change to focus if window is minimized
  if (!app_instance) {
    app.quit()
  } else {
    app.on("second-instance", (event, commandline, workingDirectory) => {
      if (mainWindow) {
        if (mainWindow.isMinimized()) mainWindow.restore()
        mainWindow.focus()
      }
    })
  }
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(() => {
  createWindow()
  app.on('activate', function () {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

// kill all child process before-quit
app.on("before-quit", function () {
  if (isDev) {
    pyshell.kill()
  } else {
    child.kill("SIGINT")
  }
})

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit()
})

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.