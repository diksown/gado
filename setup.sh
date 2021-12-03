# install
# sudo cp gado /usr/local/bin/
# sudo ln -s /usr/local/bin/gado /usr/local/bin/gado++

# sudo mkdir /usr/local/share/gado
# cp data/poetry.json /usr/local/share/

if [[ $1 == "install" ]]; then
	echo "Installing gado..."
	# do stuff
	echo "gado installed! Run `gado` to start."
elif [[ $1 == "uninstall" ]]; then
	# TODO: prompt user
	echo "Uninstalling gado..."
	# do stuff
	echo "gado uninstalled."
else
	echo "To install, type ./setup.sh install"
	echo "To uninstall, type ./setup.sh uninstall"
fi