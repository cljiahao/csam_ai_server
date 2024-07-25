<div align="center">
  <h1>
   CSAM AI Server
  </h1>
</div>

<div align="center">
  <h4>
    <h3>:computer: :robot:</h3>
    <strong>Data / Defects Collection and Prediction using Deep Learning AI Model Web Application</strong>
    <br>
    A <code>React</code> web applicaton with <code>Python (FASTAPI & Tensorflow)</code> backend
  </h4>
</div>

<br />

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#introduction">Introduction</a></li>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#pre-requisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#features">Features</a></li>
    <li><a href="#contributors">Contributors</a></li>
  </ol>
</details>

## About the project

### Introduction

This project is a two part program ([CSAM AI Server](http://github.com/cljiahao/csam_ai_server) and [CSAM Train Server](http://github.com/cljiahao/csam_ai_training)) for hollistic approach in collecting, training and presenting the prediction.

CSAM AI Server consist of <strong><i>two</i></strong> pages: CSAM Data Collection :chart_with_upwards_trend:, CSAM AI :sparkles:.

Using React & Python Libraries, a full-stack web application was created to assist daily production on defects detection.

Previously required manual judgement by zooming in and out of image window to look for defects on individual chips.
There are roughly 4,000 chips per image and each are to be inspected for defects.

To minimise manual work strain, this project serves as a prediction software in which
it processes the image and show predicted defects to the user for final judgement.

---

### Built With

[![My Skills](https://skillicons.dev/icons?i=vite,react,tailwind,fastapi,opencv,tensorflow,nginx,docker,python,js,html,css)](https://skillicons.dev) 

## Getting Started

These are the required applications and libraries for the project

### Pre-requisites

- Git
- Python v3.11 and above
- Node v20.14.0 and above
- Any editor of your choice (Recommend <a href="https://code.visualstudio.com/"><img src="https://skillicons.dev/icons?i=vscode" width="20"/></a> )

### Installation

Below are the steps to install the libraries to start your journey

1. Clone Repo
   ```sh
   git clone https://github.com/cljiahao/csam_ai_server.git
   ```
2. Either run individually in backend and frontend src folder or via Docker compose
3. Close command line and start coding!!! :computer:

## Features

### From V1
- [x] Defects categorizing by colour
- [x] Selection of ROI via image or thumbnail
- [x] Improve image processing speed using threading
- [x] Easy Navigation between pages
- [x] Upload settings and trained model via zip 

### From v2
- [ ] Better documentation
- [ ] Add logging
- [ ] Cleaner code structure and readability
- [ ] Testing integration
- [ ] CI/CD for auto build, test and merge
- [ ] Convert to Vite
- [ ] Convert to PyTorch

## Contributors

<p align="right">(<a href="#readme-top">back to top</a>)</p>