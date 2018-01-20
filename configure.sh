#!/bin/bash

CONFIGURE_ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

python2.7 "$CONFIGURE_ROOT_DIR/etc/ConfigureScript.py"
if [ -f "$CONFIGURE_ROOT_DIR/.scancode-server/bin/activate" ]; then
    source $CONFIGURE_ROOT_DIR/.scancode-server/bin/activate
fi