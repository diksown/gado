check_if_sudo() {
	if [[ $EUID -ne 0 ]]; then
		echo "you should run this with sudo." 
		exit 1
	fi
}

command_exists() {
	command -v "$1" >/dev/null 2>&1 || {
		echo $1 "is not installed. please install it first."
		exit 1
	} 
}

install_gado() {
	command_exists gcc
	command_exists pip
	cp gado /usr/bin/
	ln -s /usr/bin/gado /usr/bin/gado++

	# TODO: replace this for something better (requirements.txt or smth)
	pip install -q pronouncing
	
	mkdir -p /usr/share/gado/data
	echo "downloading poetry database..."
	curl --progress-bar https://www.gutenberg.org/files/100/100-0.txt --output /usr/share/gado/data/shakespeare.txt
	python create_db.py
}

uninstall_gado() {
	rm /usr/bin/gado
	rm /usr/bin/gado++
	rm -r /usr/share/gado

	# TODO: should you really remove pronouncing?
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