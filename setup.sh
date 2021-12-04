check_if_sudo() {
	if [[ $EUID -ne 0 ]]; then
		echo "you should run this with sudo." 
		exit 1
	fi
}

command_exists() {
	command -v "$1" >/dev/null 2>&1
}

ask_to_install() {
	command_exists $1 || {
		echo $1 "is not installed. please install it first."
		exit 1
	}
}

install_gado() {
	if command_exists gado; then
		echo "gado is already installed. updating..."
	else
		echo "installing gado..."
	fi

	ask_to_install gcc
	ask_to_install pip

	# TODO: replace this for something better (requirements.txt or smth)
	pip install -q pronouncing

	mkdir -p /usr/share/gado/data
	echo "downloading poetry database... (~5.5MB)"
	curl --progress-bar https://www.gutenberg.org/files/100/100-0.txt \
		--output /usr/share/gado/data/shakespeare.txt
	python create_db.py

	cp gado.py /usr/bin/gado
	ln -sf /usr/bin/gado /usr/bin/gado++
	echo "gado installed! Run 'gado' to start."
}

uninstall_gado() {
	echo "uninstalling gado..."

	rm -f /usr/bin/gado
	rm -f /usr/bin/gado++
	rm -rf /usr/share/gado

	# TODO: should you really remove pronouncing?
	pip uninstall -qy pronouncing >/dev/null 2>&1

	echo "gado uninstalled."
}

if [[ $1 == "install" ]]; then
	check_if_sudo
	install_gado
elif [[ $1 == "uninstall" ]]; then
	check_if_sudo
	echo -n "do you want to uninstall gado? [y/n] "
	read answer
	if [[ $answer != "y" ]]; then
		exit
	fi
	uninstall_gado
else
	echo "setup for gado - generate poetry using gcc!"
	echo ""
	echo "usage: sudo ./setup.sh [install|uninstall]"
fi