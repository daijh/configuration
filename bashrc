THIS_FILE=$(realpath $BASH_SOURCE)
THIS_DIR=$(dirname ${THIS_FILE})

# proxy
export http_proxy=http://proxy-prc.intel.com:913
export https_proxy=http://proxy-prc.intel.com:913

# python modules
export PYTHON_MODULES=${THIS_DIR}/python_modules
export PYTHONPATH=${PYTHON_MODULES}:${PYTHON_MODULES}/pm_packages:$PYTHONPATH

