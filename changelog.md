# Changelog

## [2022.4.21 - Branding]

### Added

-   `src/frontend/images/favicon.ico` serves as app icon

### Changed

-   `README.md` now contains basic info

## [2022.4.21 - Electron Setup]

### Added

-   `src/frontend` contains all electron application elements
    -   `src/frontend/fonts` for embedded fonts
        -   [asul](https://fonts.google.com/specimen/Asul)
        -   [orbitron](https://fonts.google.com/specimen/Orbitron)
        -   [ubuntu](https://fonts.google.com/specimen/Ubuntu)
    -   `src/frontend/scripts` for typescript files
        -   `main.ts` initializes browser window
        -   `preload.ts` incorporates NodeJS before runtime
        -   `renderer.ts` modifies layout at runtime
    -   `src/frontend/styles` for css files
        -   `index.css` stylizes index.html
    -   `src/frontend/templates` for html files
        -   `index.html` serves as entrypoints
-   new scripts in `package.json` to streamline `npm start`

### Changed

-   moved pre-existing files in `src` into `src/simulator`

-   modified `.gitignore` to make linting/formatting configs and `package.lock` visible

## [2022.4.18 - Setup Complete]
