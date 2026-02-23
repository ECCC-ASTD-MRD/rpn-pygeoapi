if ! (return 0 2>/dev/null); then
	echo "Error: This script must be sourced." >&2
	exit 1
fi

if ! command -v conda &>/dev/null; then
	echo "Error: Conda is not installed or not in your PATH." >&2
	return 1
fi

my-load-conda() {
	__conda_setup="$('/home/$USER/site5/miniconda3/bin/conda' 'shell.bash' 'hook' 2>/dev/null)"
	if [ $? -eq 0 ]; then
		eval "$__conda_setup"
	else
		if [ -f "/home/$USER/site5/miniconda3/etc/profile.d/conda.sh" ]; then
			. "/home/$USER/site5/miniconda3/etc/profile.d/conda.sh"
		else
			export PATH="/home/$USER/site5/miniconda3/bin:$PATH"
		fi
	fi
	unset __conda_setup
}

if ! declare -f conda >/dev/null; then
	my-load-conda
	echo "Conda was loaded into your current shell."
fi

env_name="venv"

if conda info --envs | grep -q "$env_name"; then
	conda activate venv
	echo "Already exists."
else
	echo "Run initial-setup.sh"
fi
