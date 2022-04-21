import { app, BrowserWindow } from 'electron'
import * as path from 'path'

function createWindow() {
    const mainWindow = new BrowserWindow({
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
        },
        show: false,
    })

    mainWindow.loadFile(path.join(__dirname, '../templates/index.html'))
    console.log(__dirname)

    // COMMENT OUT FOR RELEASE
    mainWindow.webContents.openDevTools()

    mainWindow.maximize()
    mainWindow.show()
}

app.on('ready', () => {
    createWindow()

    app.on('activate', function () {
        if (BrowserWindow.getAllWindows().length === 0) createWindow()
    })
})

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit()
    }
})

// In this file you can include the rest of your app"s specific main process
// code. You can also put them in separate files and require them here.
