check_if_sudo() {
	if [[ $EUID -ne 0 ]]; then
		echo "you should run this with sudo." 
		exit 1
	fi
}

install_gado() {
	cp gado /usr/bin/
	ln -s /usr/bin/gado /usr/bin/gado++
	# TODO: replace this for something better (requirements.txt or smth)
	pip install -q pronouncing
	mkdir /usr/share/gado
	cp data/poetry.json /usr/share/gado/
}

uninstall_gado() {
	# TODO: maybe remove pronouncing?
	rm /usr/bin/gado
	rm /usr/bin/gado++
	rm -r /usr/share/gado
	pip uninstall -qy pronouncing
}

if [[ $1 == "install" ]]; then
	check_if_sudo
	echo "installing gado..."
	install_gado
	echo "gado installed! Run 'gado' to start."
elif [[ $1 == "uninstall" ]]; then
	check_if_sudo
	echo -n "do you want to uninstall gado? [y/n] "
	read answer
	if [[ $answer != "y" ]]; then
		exit
	fi
	uninstall_gado
	echo "uninstalling gado..."
	
	echo "gado uninstalled."
else
	echo "setup for gado - generate poetry using gcc!"
	echo ""
	echo "usage: sudo ./setup.sh [install|uninstall]"
fi