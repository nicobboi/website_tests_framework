# FRONTEND framework

The frontend framework is a [ReactJS](https://react.dev/) app.

## General workflow

All frontend files are in `frontend/`.

By default, the dependencies are managed with [npm](https://docs.npmjs.com/), go there and install it.

From `./app/` you can install all the dependencies with:

```console
$ npm install
```

Next, open your editor at `./app/` (instead of the project root: `./`), so that you see an `./app/` directory with your code inside. 

You can add or modify the components from `./app/src/`: *App.js* is the main app, `./app/src/pages` contains all the direct children of *App.js* and `./app/src/components` contains all the children components of the pages and the default layout.

Modify global SCSS in `.app/src/_global.scss`, while if you want to add custom scss to only one component, create your scss file into the component folder and import it in the component .jsx file as module (you must named it *your-scss-file*.module.scss).

If you want to install new packages, just launch `npm install your-package` inside `./app/`.

Is suggested to develop locally by running `npm start`, instead of using the docker container, so you can view your changes in real time. 