// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// No Node.js APIs are available in this process unless
// nodeIntegration is set to true in webPreferences.
// Use preload.js to selectively enable features
// needed in the renderer process.

function showTab(tabName: string) {
    let tabcontent_array: NodeListOf<HTMLElement>,
        tablinks_array: NodeListOf<HTMLElement>

    tabcontent_array = document.querySelectorAll<HTMLElement>('div.tabcontent')
    tabcontent_array.forEach((tabcontent) => {
        tabcontent.style.display = 'none'
    })

    tablinks_array = document.querySelectorAll<HTMLElement>('div.tablinks')
    tablinks_array.forEach((tablink) => {
        tablink.className = tablink.className.replace(' active', '')
    })

    document.getElementById(tabName).style.display = 'block'
}

const tablinks = document.getElementsByClassName('tablinks')
for (let i = 0; i < tablinks.length; i++) {
    tablinks[i].addEventListener('click', () => {
        showTab(tablinks[i].textContent)
    })
}

// Get the element with id="defaultOpen" and click on it
document.getElementById('defaultOpen').click()
