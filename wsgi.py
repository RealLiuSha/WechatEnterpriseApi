# -*- coding:utf-8 -*-
# Author:      LiuSha
# Email:       itchenyi@gmail.com
from aimee.app import app_init
from aimee.config import (
    BASE_DIR,
    HTTP_HOST,
    HTTP_PORT
)

import os
import sys
import optparse


def main(app, default_host=HTTP_HOST, default_port=HTTP_PORT):
    parser = optparse.OptionParser()
    parser.add_option("-H", "--host",
                      help="Hostname of the Flask app " +
                           "[default %s]" % default_host,
                      default=default_host)
    parser.add_option("-P", "--port",
                      help="Port for the Flask app " +
                           "[default %s]" % default_port,
                      default=default_port)
    parser.add_option("-d", "--debug",
                      help="Debug for the Flask app " +
                           "[default False]",
                      default=False)
    parser.add_option("-i", "--init",
                      help="Database init for app" +
                           "[default False]",
                      default=False)

    options, _ = parser.parse_args()
    if options.init:
        from aimee.model import db

        db.create_all()

    app.run(
        debug=options.debug,
        host=options.host,
        port=int(options.port),
        use_reloader=options.debug
    )


application = app_init()
activate_this = os.path.join(BASE_DIR, '.env', 'bin', 'activate_this.py')

with open(activate_this) as f:
    code = compile(f.read(), activate_this, 'exec')
    exec(code, dict(__file__=activate_this))

sys.path.insert(0, BASE_DIR)


if __name__ == "__main__":
    main(app=application)
