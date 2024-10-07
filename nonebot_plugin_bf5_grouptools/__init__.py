import json

from nonebot import on_request, on_notice, on_command
from nonebot.plugin import PluginMetadata
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import (
    GroupIncreaseNoticeEvent, GroupRequestEvent, GroupMessageEvent, Message, Bot
)

from .data import Data
from .network import request_player, request_ban

__plugin_meta__ = PluginMetadata(
    name='BF5_grouptools',
    description='基于 Nonebot2 的战地 5 QQ 群管理插件。',
    usage='通过 管理群 -> 加群方式 -> 需要身份认证 中开启 需要回答问题并由管理员审核 并将机器人账号设为管理员。',
    type='application',
    homepage="https://github.com/Lonely-Sails/nonebot-plugin-BF5-grouptools",
    supported_adapters={'~onebot.v11'},
)

data = Data()

notice_matcher = on_notice()
request_matcher = on_request()
query_ban_matcher = on_command('pb=')


@request_matcher.handle()
async def _(event: GroupRequestEvent, bot: Bot):
    _, user_name = event.comment.split('\n')
    user_name = user_name.lstrip('答案：')
    response = await request_player(user_name)
    if response is None:
        await bot.set_group_add_request(
            flag=event.flag, sub_type=event.sub_type, approve=False,
            reason='请求超时，请等待几秒钟后再次尝试。'
        )
        await request_matcher.finish()
    if response:
        data.players[user_name] = (event.user_id, response['personaId'])
        data.save()
        await bot.set_group_add_request(flag=event.flag, sub_type=event.sub_type, approve=True)
        await request_matcher.finish()
    await bot.set_group_add_request(
        flag=event.flag, sub_type=event.sub_type,
        approve=False, reason=F'未找到名为 {user_name} 的玩家！请检查输入是否正确，然后再次尝试。'
    )
    await request_matcher.finish()


@notice_matcher.handle()
async def _(event: GroupIncreaseNoticeEvent, bot: Bot):
    if user_name := data.search_player_name(event.user_id):
        await bot.set_group_card(group_id=event.group_id, user_id=event.user_id, card=user_name)
        await notice_matcher.finish(F'欢迎新人加入！已自动修改您的群名片为游戏名称：{user_name}', at_sender=True)
    await notice_matcher.finish('未找到您的申请记录，请联系管理员。', at_sender=True)


@query_ban_matcher.handle()
async def _(event: GroupMessageEvent, args: Message = CommandArg()):
    args = args.extract_plain_text().strip()
    if args not in data.players:
        response = await request_player(args)
        if response is None:
            await query_ban_matcher.finish('查询超时，请稍后再试。', at_sender=True)
        if not response:
            await query_ban_matcher.finish(F'未找到名为 {args} 的玩家！请检查输入是否正确，然后再次尝试。', at_sender=True)
        data.players[args] = (None, response['personaId'])
        data.save()
    _, persona_id = data.players[args]
    response = await request_ban(persona_id)
    if response is None:
        await query_ban_matcher.finish('查询超时，请稍后再试。', at_sender=True)
    if response:
        message_lines = [F'玩家 {args} 的封禁记录如下：']
        for index, ban_info in enumerate(response):
            message_lines.append(F'{index + 1}.服务器 {ban_info['serverName']}')
            message_lines.append(F'- 时间：{ban_info['createTime']}  原因：{ban_info['reason']}')
        await query_ban_matcher.finish('\n'.join(message_lines), at_sender=True)
    await query_ban_matcher.finish(F'玩家 {args} 还没有被封禁过。', at_sender=True)
