p=http://webproxy.collab.science.gc.ca:8888/

export http_proxy=${p}
export https_proxy=${p}
export HTTP_PROXY=${p}
export HTTPS_PROXY=${p}

export no_proxy=localhost,science.gc.ca,142.98.16.0/19,142.98.32.0/20,142.98.224.0/21,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,127.0.0.0/8
