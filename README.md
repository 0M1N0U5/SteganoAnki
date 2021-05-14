# CyberSecurity-APT-Stego
<p align="center">
  <a href="https://github.com/0M1N0U5/CyberSecurity-APT-Stego">
    <img src="./Anki/media/SteganoAnki.png" alt="Logo" width="600" height="350">
  </a>
</p>
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#author">Authors</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>
<h1 style="display: inline-block" id="about-the-project">About The Project 📖 </h1>
SteganoAnki is a tool that uses Anki app to hide 🕵 secrets inside Anki decks images using a python script with a steganography technique🎩
This project was created in May 2021 for the subject "Persistent Threats and Information Leakage" in the Master of Cybersecurity🎓 
<h1 style="display: inline-block" id="built-with">Built With 🛠️</h1>
<ul>
 <li> Python programming language was used for coding. Link to web: https://www.python.org/
</li>
<li> Anki app was used to verify our script worked correctly and the database was updated with the hidden secret. Link to web: https://apps.ankiweb.net/
</li>
<li> AnkiPandas was used to access Anki decks databases using python. Link to repository: https://github.com/klieret/AnkiPandas
</li>
</ul>

<h1 style="display: inline-block" id="getting-started">Getting Started 🚀</h1>
To get a local copy up and running follow these simple steps.
<h2 style="display: inline-block" id="prerequisites">Prerequisites📋</h2>
Run "requirements.txt" --> <a href="https://github.com/0M1N0U5/CyberSecurity-APT-Stego/blob/main/Anki/requirements.txt">📑</a>	
<h2 style="display: inline-block" id="installation">Installation 🔧</h2>
<p>Clone the repository: </p> <code> $ git clone https://github.com/0M1N0U5/CyberSecurity-APT-Stego </code>
<h1 style="display: inline-block" id="usage">Usage⚙️</h1>

<p>This line will open SteganoAnki command line tool: </p>
<p><code> $ python3 steganoAnki.py</code></p>
<p>To look for its documentation of how to use the commands, use this line:</p>
<p><code> $ python3 steganoAnki.py -h</code></p>
<p>There are three modes available:</p> 
  <ul>
  <li>Endode (hide secret)</li>
  <li>Decode (discover if there is any secret)</li>
  <li>Estimation (calculate bext pixels to use to avoid controversial zones)</li>
  </ul>

<h1 style="display: inline-block" id="license">License 📄</h1> 

Distributed under the MIT License. See `LICENSE` for more information.