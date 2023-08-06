import asyncio
import random
import re
from itertools import starmap
from typing import (
    Callable,
    Iterable,
    List,
    Optional,
    Tuple,
    TypeVar,
    Union,
    cast,
)

from nonebot import on_command, on_message, on_notice
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    Message,
    MessageEvent,
    MessageSegment,
    PokeNotifyEvent,
)
from nonebot.matcher import Matcher
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from typing_extensions import TypeVarTuple, Unpack

from nonebot_plugin_autoreply.util import VarDictType, get_var_dict, replace_message_var

from .config import (
    FilterModel,
    MatchModel,
    MatchType,
    MessageSegmentModel,
    ReplyModel,
    ReplyType,
    config,
    reload_replies,
    replies,
)

T = TypeVar("T")
TArgs = TypeVarTuple("TArgs")


def check_list(
    function: Callable[[Unpack[TArgs]], bool],
    will_check: Iterable[Tuple[Unpack[TArgs]]],
    is_any: bool = False,
) -> bool:
    # 感谢 nb2 群内 Bryan不可思议 佬的帮助！！
    iterator = starmap(function, will_check)
    return any(iterator) if is_any else all(iterator)


def check_filter(will_check: FilterModel[T], val: Optional[T]) -> bool:
    # 判断黑名单 值不在列表中ok
    ok = val not in will_check.values
    if will_check.type == "white":  # 白名单则反过来
        ok = not ok
    return ok


def check_message(match: MatchModel, event: MessageEvent) -> bool:
    if match.type == "poke":
        return False

    if match.match is None:
        raise ValueError("存在 type 不为 poke，且 match 为空的不合法匹配规则")

    if match.to_me and (not event.is_tome()):
        return False

    msg_str = str(event.message)
    msg_plaintext = event.message.extract_plain_text()
    match_template = match.match

    if match.strip:
        msg_str = msg_str.strip()
        msg_plaintext = msg_plaintext.strip()

    if match.type == "regex":
        flag = re.I if match.ignore_case else 0
        return bool(
            (re.search(match_template, msg_str, flag))
            or (
                re.search(match_template, msg_plaintext, flag)
                if match.allow_plaintext
                else False
            ),
        )

    if match.ignore_case:
        # regex 匹配已经处理过了，这边不需要管
        msg_str = msg_str.lower()
        match_template = match_template.lower()

    if match.type == "full":
        return (msg_str == match_template) or (
            msg_plaintext == match_template if match.allow_plaintext else False
        )

    # default fuzzy
    if (not msg_str) or (match.allow_plaintext and (not msg_plaintext)):
        return False
    return (match_template in msg_str) or (
        (match_template in msg_plaintext) if match.allow_plaintext else False
    )


def check_poke(match: MatchModel, event: PokeNotifyEvent) -> bool:
    if match.type != "poke":
        return False
    return event.is_tome() if match.to_me else True


def check_match(match: MatchType, event: Union[MessageEvent, PokeNotifyEvent]) -> bool:
    if isinstance(match, str):
        match = MatchModel(match=match)

    if match.possibility < 1 and random.random() > match.possibility:
        return False

    return (
        check_message(match, event)
        if isinstance(event, MessageEvent)
        else check_poke(match, event)
    )


async def message_checker(
    event: Union[MessageEvent, PokeNotifyEvent],
    state: T_State,
) -> bool:
    group = (
        event.group_id
        if isinstance(event, (GroupMessageEvent, PokeNotifyEvent))
        else None
    )

    state_reply = []
    for reply in replies:
        filter_checks = [(reply.groups, group), (reply.users, event.user_id)]
        match_checks = [(x, event) for x in reply.matches]

        if not (
            check_list(check_filter, filter_checks)
            and check_list(check_match, match_checks, True)
        ):
            continue

        state_reply.append(random.choice(reply.replies))
        if reply.block:
            break

    state["reply"] = state_reply
    return bool(state_reply)


def get_reply_msgs(
    reply: ReplyType,
    var_dict: VarDictType,
    refuse_multi: bool = False,
) -> Tuple[List[Message], Optional[Tuple[int, int]]]:
    if isinstance(reply, str):
        str_is_plain = reply.startswith("@")
        if str_is_plain:
            reply = reply[1:]

        reply = ReplyModel(type="plain" if str_is_plain else "normal", message=reply)

    elif isinstance(reply, list):
        reply = ReplyModel(type="array", message=reply)

    rt = reply.type
    msg = reply.message

    if rt == "plain":
        return [Message() + cast(str, msg)], None

    if rt == "array":
        return (
            [
                replace_message_var(
                    Message(
                        MessageSegment(type=x.type, data=x.data)
                        for x in cast(List[MessageSegmentModel], msg)
                    ),
                    var_dict,
                ),
            ],
            None,
        )

    if rt == "multi":
        if refuse_multi:
            raise ValueError("Nested `multi` is not allowed")
        return (
            [
                get_reply_msgs(x, var_dict, True)[0][0]
                for x in cast(List[ReplyModel], msg)
            ],
            reply.delay,
        )

    # default normal
    return [replace_message_var(Message(cast(str, msg)), var_dict)], None


message_matcher = on_message(
    rule=message_checker,
    block=config.autoreply_block,
    priority=config.autoreply_priority,
)

poke_matcher = on_notice(
    rule=message_checker,
    block=config.autoreply_block,
    priority=config.autoreply_priority,
)


@message_matcher.handle()
@poke_matcher.handle()
async def _(
    bot: Bot,
    event: Union[MessageEvent, PokeNotifyEvent],
    matcher: Matcher,
    state: T_State,
):
    reply: List[ReplyType] = state["reply"]

    var_dict = await get_var_dict(bot, event)
    reply_msgs = [get_reply_msgs(x, var_dict) for x in reply]

    for msgs, delay in reply_msgs:
        for x in msgs:
            await matcher.send(x)

        if delay:
            await asyncio.sleep(random.randint(*delay) / 1000)


reload_matcher = on_command("重载自动回复", permission=SUPERUSER)


@reload_matcher.handle()
async def _(matcher: Matcher):
    success, fail = reload_replies()
    await matcher.finish(f"重载回复配置完毕~\n成功 {success} 个，失败 {fail} 个")
