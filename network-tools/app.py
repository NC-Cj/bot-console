from gevent import monkey

monkey.patch_all()

from flask import jsonify

from config import RecordTable, ScapyTable
from modules import app


@app.route('/getInfo/<types>/')
def get_info(types):
    lookup = {
        'online': [ScapyTable.show_online, True],
        'hide': [ScapyTable.show_online, False],
        'record': [RecordTable.show_record, False]
    }
    action, data = lookup.get(types)
    source = {"data": action(data)}

    return jsonify(source)


app.register_blueprint(action_blue)
app.register_blueprint(cmd_blue)
app.register_blueprint(log_blue)

# 仅放在本地环境中使用
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=1234)
