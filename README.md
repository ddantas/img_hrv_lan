# img_hrv_lan
Heart rate variability graphical user interface. Captures a dataset of two subjects interacting on two ccomputers in a LAN while seeing images shown on screen.

## Environment setup

The project requires Python 3.8. We recommend the creation of a virtual environment to facilitate the usage of the code.

Use the code below in the terminal to install Python 3.8 in the system, as explained [here](https://www.linuxcapable.com/how-to-install-python-3-8-on-ubuntu-22-04-lts/).

> <code>$ sudo apt update && sudo apt upgrade</code>
> 
> <code>$ sudo apt install software-properties-common -y</code>
> 
> <code>$ sudo add-apt-repository ppa:deadsnakes/ppa -y</code>
> 
> <code>$ sudo apt update</code>
> 
> <code>$ sudo apt install python3.8 python3.8-dev python3.8-venv -y</code>

Create the virtual environment with

> <code>$ python3.8 -m venv_polar</code>

Activate the virtual environment with

> <code>$ source venv_polar/bin/activate</code>

Alternatively, copy the line above to a file called <code>activate_venv_polar</code> and run

> <code>$ . ./activate_venv_polar</code>

Update pip and install idle with

> <code>(venv_polar)$ python -m pip install --upgrade pip</code>
> 
> <code>(venv_polar)$ pip install idle</code>

Call <code>idle</code> inside the virtual environment with

> <code>(venv_polar)$ python -m idlelib.idle</code>

Deactivate the virtual environment with

> <code>(venv_polar)$ deactivate</code>

## Tips about git usage

Now git requires an SSH key to update your repository. Github documentation has instructions about [how to generate an SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) and [how to create a personal access token \(PAT\)](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token).

Use the code below in the terminal to avoid the need to input the PAT when doing a <code> git push</code>:

> <code>$ git config credential.helper store</code>

## Tips about Markdown syntax

Basic details about Markdown syntax can be found [here](https://www.markdownguide.org/basic-syntax/).

## Tips about time synchronization when executing a routine

Before the start of a capture/routine, make sure that all computers, that are part of the process, have their clocks synchronized by following these steps:

- First, make sure that all computers are connected to a NTP server, so that your system's clock is synchronized with the internet's. Run `sudo systemctl start systemd-timesyncd` on your terminal to start a service that takes care of that. To check if the service is up, run `sudo systemctl status systemd-timesyncd`. 

- Second, every computer should be using the same NTP server. To change this you should edit the configuration file for `timesyncd`, which is usually at `/etc/systemd/timesyncd.conf`.
Note: during development and testing, the server used was Ubuntu's default NTP server (ntp.ubuntu.com).

- Finally, apply the synchronization to the hardware clock of every computer. Even though your system is synced with the internet, your hardware might still be following your previous clock. To do that, run `sudo hwclock --systohc` on your terminal.

Use `timedatectl` to check if everything is working. If everything is fine, all the clocks should be synced and you should have these two lines as part of the output of your command :
> **System clock synchronized: yes**\
> **NTP service: active** 

You can run the command in a loop to see how time is passing in every clock using `for i in {1.1000}; do timedatectl; done;`.
