import json

from nonebot import require

require('nonebot_plugin_localstore')
from nonebot_plugin_localstore import get_data_file


class Data:
    players = {}
    file_path = get_data_file('BF5', 'Players.json')

    def __init__(self):
        if not self.file_path.exists():
            self.file_path.parent.mkdir(exist_ok=True)
            self.save()
        else:
            self.load()

    def load(self):
        data = self.file_path.read_text('Utf-8')
        self.players = json.loads(data)

    def save(self):
        data = json.dumps(self.players)
        self.file_path.write_text(data, 'Utf-8')

    def search_player_name(self, user_id: int):
        for user_name, (test_user_id, _) in self.players.items():
            if test_user_id == user_id:
                return user_name
