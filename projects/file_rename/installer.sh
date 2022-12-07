#!/bin/sh
echo "DETAILS:HIDE"
curr_ver="1.0"
latest_ver=$(curl -s https://www.podracer.app/get/version.txt)
arch="$(uname -m)"  # -i is only linux, -m is linux and apple
usr="$(pwd)"
Rename="/Applications/Rename.app"
echo "REFRESH\n"
echo "Initializing Installer..."
echo "NOTIFICATION:Installing Rename!\n"
sleep 1
echo "Checking for updates..."
if [[ $curr_ver = $latest_ver ]]
    then
    echo
else
    echo "ALERT:Update Available|There's a newer version of Rename available for download. Please install the latest version to ensure stability"
    sleep 7
    echo "Existing Installer..."
    open https://www.mafshari.work
    echo "QUITAPP"
fi
cd
if test -d "$Rename"; then
    rm -r $Rename
    echo "Removing existing installation"
    sleep 3
fi
echo "Detecting System Architecture..."
if [[ "$arch" = x86_64* ]]; then
    if [[ "$(uname -a)" = *ARM64* ]]; then 
        curl -s -L -o Rename.zip "https://drive.google.com/uc?export=download&id=1z-2VDlGsw0df9hY_eLtCuBs4RUbFZLH5&confirm=t"
        echo 'Downloading Rename for Apple Silicon'
        echo "PROGRESS:10"
        echo "PROGRESS:12"
        echo "PROGRESS:14"
        echo "PROGRESS:16"
        echo "PROGRESS:18"
        echo "PROGRESS:20"
        echo "PROGRESS:22"
        echo "PROGRESS:24"
        echo "PROGRESS:26"
        echo "PROGRESS:28"
    else
        #echo 'x64'
        echo "PROGRESS:10"
        echo "PROGRESS:12"
        echo "PROGRESS:14"
        echo "PROGRESS:16"
        echo "PROGRESS:18"
        curl -s -L -o Rename.zip "https://drive.google.com/uc?export=download&id=18NvcaVjInsaKLTPDnJ8FGztd-cGnrwob&confirm=t"
        echo 'Downloading Rename for Intel x64'
        echo "PROGRESS:20"
        echo "PROGRESS:22"
        echo "PROGRESS:24"
        echo "PROGRESS:26"
        echo "PROGRESS:28"
    fi
elif [[ "$arch" = i*86 ]]; then
    #echo 'x32'
    echo "PROGRESS:10"
    echo "PROGRESS:12"
    echo "PROGRESS:14"
    echo "PROGRESS:16"
    echo "PROGRESS:18"
    curl -s -L -o Rename.zip "https://drive.google.com/uc?export=download&id=18NvcaVjInsaKLTPDnJ8FGztd-cGnrwob&confirm=t"
    echo 'Downloading Rename for Intel x86'
    echo "PROGRESS:20"
    echo "PROGRESS:22"
    echo "PROGRESS:24"
    echo "PROGRESS:26"
    echo "PROGRESS:28"
fi
echo "PROGRESS:30"
echo "PROGRESS:31"
echo "PROGRESS:32"
echo "PROGRESS:33"
echo "PROGRESS:34"
# curl -s -L -o Rename.zip "https://drive.google.com/uc?export=download&id=1AlRpr_J0kQAhYJkAzcgPlJxowplVPEOP&confirm=t"
echo "PROGRESS:35"
echo "PROGRESS:36"
echo "PROGRESS:37"
curl -s -L -o Rename.icns "https://drive.google.com/uc?export=download&id=1kDTeC6IESOFPW83NcKzpLn2n-vB-yO86"
echo "PROGRESS:38"
sleep 1
echo "PROGRESS:39"
echo "PROGRESS:40"
sleep 1
echo "PROGRESS:4"
echo "PROGRESS:41"
echo "PROGRESS:42"
echo "PROGRESS:43"
sleep 1
echo "PROGRESS:44"
echo "PROGRESS:45"
sleep 1
echo "PROGRESS:46"
echo "PROGRESS:47"
sleep 1
echo "PROGRESS:48"
echo "PROGRESS:49"
echo "PROGRESS:50"
echo "Installing Rename"
unzip -qq -o Rename.zip
echo "PROGRESS:52"
echo "PROGRESS:54"
sleep 1
echo "PROGRESS:56"
echo "PROGRESS:58"
sleep 1
echo "PROGRESS:60"
cp Rename.icns Rename.app/Contents/Resources/icon-windowed.icns
rm -r Rename.app/Icon
cp Rename.icns Rename.app/Icon.icns
echo "PROGRESS:70"
cp -R Rename.app /Applications
echo "Finalizing..."
sleep 1
rm -r Rename.app
echo "PROGRESS:80"
sleep 1
rm -r Rename.icns
rm -r Rename.zip
echo "PROGRESS:90"
rm -r Rename.app
rm -r __MACOSX
sleep 1
echo "PROGRESS:100"
echo "Installation Complete!"
echo "ALERT:All Done!|Rename has sucessfully been installed!\n"
echo "NOTIFICATION:Rename has been installed!\n"
# echo "Launching Rename..."
# sleep 4
# open /Applications/Rename.app
sleep 1
#open Rename\ Install\ Log.app
# echo "ALERT:Allow Rename|System Preferences > Security & Privacy > 'Open Anyway'\n"
sleep 1
echo "QUITAPP"