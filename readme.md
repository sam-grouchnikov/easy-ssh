Your one stop shop for AI model training: manage your SSH connections, AI model training loops, and metric logs all in one place!

**Important**: You may use, clone, and modify the app to your liking. However you may NOT close-source any of the source code, nor may you sell this as a service. See full terms in LICENSE.md.

## How to install

1. clone the repository to your desired path

```commandline
git clone https://github.com/sam-grouchnikov/easy-ssh.git
```

2. Run the application file in the folder

```
python application.py
```

## Features
* Connect to a specified remote server via SSH
* View log graphs from the Weights & Biases API
* Edit files remotely with an easy-to-use file editor
* Interact with the command line with both typed commands and buttons

## Disclaimers/Limitations
* Only supports/tested on Pytorch Lightning + WandB workflows
* Still contains minor bugs - not ready for production-level distribution
* Terminal experience NOT fully mirrored
  * When a training loop is ran, only the progress bar is displayed on screen
  * Not all commands' outputs are fully displayed correctly
  * Terminal output only shows progress bar for model training loops (will fix soon)

## Version History

1.0.0 - First Release 🥳

## Future Releases/Features
* Small bug fixes
    * Button UI updates in certain situations
    * cat-based file editor fixes
* Authentic terminal experience
  * Mirrored experience from Windows PowerShell
* Light-mode
* Support for more AI model training libraries
  * Tensorflow + Tensorboard workflows
  * Normal Pytorch DDP support (torchrun commands)