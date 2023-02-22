# Frontend - Trivia API

## Overview
The frontend app was built using create-react-app with some further modifications. The following changes have been made to the starter frontend code:

  * Change of styling and layout to improve visual appearance and usability.
  * Improved icon rendering - using a default icon in case a corresponding svg file is not available.
  * Interface enhancement for creating new categories on the frontend (and backend) side.

## Setting up the frontend

### Prerequisites

* **Installing Node and NPM** - This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

### Installing Dependencies

In your terminal, please navigate to the `/frontend` folder and run:

```bash
npm install
```

### Running the frontend in development mode

In your terminal, please navigate to the `/frontend` folder and run the following command to start the frontend development server:

```bash
npm start
```
> Please note that the option `--openssl-legacy-provider` may be required for compatibility reasons in order to launch it on newer versions of Node.js. This option can be added to the `package.json` file:

```
  "scripts": {
    "start": "node --openssl-legacy-provider node_modules/react-scripts/scripts/start.js",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  }
```

Open http://localhost:3000 in your browser to view Trivia App.

