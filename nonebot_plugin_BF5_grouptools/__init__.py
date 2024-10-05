from httpx import AsyncClient

from nonebot import on_request, on_notice
from nonebot.adapters.onebot.v11 import Bot, GroupRequestEvent, GroupIncreaseNoticeEvent

players = {}

client = AsyncClient()
notice_matcher = on_notice()
request_matcher = on_request()


async def request(url: str, params: dict, retry_count: int = 3):
    response = await client.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    if retry_count > 0:
        return await request(url, params, retry_count - 1)
    return None


@request_matcher.handle()
async def _(event: GroupRequestEvent, bot: Bot):
    user_name = event.comment.lstrip('答案：')
    response = await request('https://api.bfvrobot.net/api/v2/bfv/checkPlayer', params={'name': user_name})
    if response is not None:
        if response.get('data'):
            global players
            players.setdefault(event.user_id, user_name)
            await bot.set_group_add_request(flag=event.flag, sub_type=event.sub_type, approve=True)
            await request_matcher.finish()
        await bot.set_group_add_request(
            flag=event.flag, sub_type=event.sub_type,
            approve=False, reason=F'未找到名为 {user_name} 的玩家！请检查输入是否正确，然后再次尝试。'
        )
        await request_matcher.finish()
    await bot.set_group_add_request(flag=event.flag, sub_type=event.sub_type, approve=False,
                                    reason='请求超时，请等待几秒钟后再次尝试。')
    await request_matcher.finish()


@notice_matcher.handle()
async def _(event: GroupIncreaseNoticeEvent, bot: Bot):
    if user_name := players.get(event.user_id):
        await bot.set_group_card(group_id=event.group_id, user_id=event.user_id, card=user_name)
        await notice_matcher.finish(F'欢迎新人加入！已自动修改您的群名片为游戏名称：{user_name}', at_sender=True)
    await notice_matcher.finish('未找到您的申请记录，请联系管理员。', at_sender=True)
