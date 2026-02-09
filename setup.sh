if ! (return 0 2>/dev/null) ; then
    echo "Error: This script must be sourced." >&2
    exit 1
fi

root_dir=$(cd -P $(dirname ${BASH_SOURCE[0]}) && pwd)
venv_path=${root_dir}/venv/bin/activate

if [ ! -f "${venv_path}" ] ; then
    echo "Error: 'venv' not found" >&2
    return 1
fi

source ${venv_path}
