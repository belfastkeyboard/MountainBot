from interactions import Client, Intents, OptionType, slash_command, SlashContext, slash_option

from utils.file import load_mountains_from_json, save_mountains_to_json
from utils.string import sanitise_string
from globals import token, filepath, channel_id
from mountain import Mountain, MountainList

# globals.py file hides below data, not contained in this repository
FILEPATH: str = filepath
BOT_TOKEN: str = token
CHANNEL_ID: int = channel_id


@slash_command(name="mountains", description="view list of mountains")
async def mountains(ctx: SlashContext) -> None:
    if ctx.channel.id != CHANNEL_ID:
        await ctx.send(content="Cannot be used in this channel! :(", ephemeral=True)
        return

    _mountain_list: MountainList = load_mountains_from_json(FILEPATH)

    await ctx.channel.purge(predicate=lambda m: m.author.id == ctx.channel.bots[0].id)

    _message = await ctx.send(str(_mountain_list))
    await _message.pin()

    await ctx.channel.purge(predicate=lambda m: m.author.id == ctx.channel.bots[0].id and m.pinned is False)

    return


@slash_command(name="add_mountain", description="add a mountain to the list")
@slash_option(name="province", description="the province the mountain is in", required=True, opt_type=OptionType.STRING)
@slash_option(name="county", description="the county the mountain is in", required=True, opt_type=OptionType.STRING)
@slash_option(name="mountain", description="the name of the mountain", required=True, opt_type=OptionType.STRING)
@slash_option(name="height", description="the height of the peak (in metres)", required=True,
              opt_type=OptionType.NUMBER)
@slash_option(name="hikers", description="hikers who have reached the peak (separated by space)", required=False,
              opt_type=OptionType.STRING)
async def add_mountain(ctx: SlashContext,
                       province: str, county: str, mountain: str, height: int, hikers: str = "") -> None:

    if ctx.channel.id != CHANNEL_ID:
        await ctx.send(content="Cannot be used in this channel! :(", ephemeral=True)
        return

    if hikers:
        hikers: list[str] = [hiker.strip().title() for hiker in hikers.split(None)]
        _mountain: Mountain = Mountain(province, county, mountain, height, hikers)
    else:
        _mountain: Mountain = Mountain(province, county, mountain, height)

    _mountains: MountainList = load_mountains_from_json(FILEPATH)

    _mountains.push_back(_mountain)

    save_mountains_to_json(FILEPATH, _mountains.get_dict())

    await ctx.send(content=f"{mountain} added! :)", ephemeral=True)

    return


@slash_command(name="remove_mountain", description="remove a mountain from the list")
@slash_option(name="mountain", description="the name of the mountain to remove", required=True,
              opt_type=OptionType.STRING)
async def remove_mountain(ctx: SlashContext, mountain: str) -> None:
    if ctx.channel.id != CHANNEL_ID:
        await ctx.send(content="Cannot be used in this channel! :(", ephemeral=True)
        return

    _mountains: MountainList = load_mountains_from_json(FILEPATH)

    _result: bool = _mountains.erase(sanitise_string(mountain))

    if _result:
        save_mountains_to_json(FILEPATH, _mountains.get_dict())
        await ctx.send(content=f"{mountain} removed! :)", ephemeral=True)
    else:
        await ctx.send(content=f"Could not remove {mountain}! :(", ephemeral=True)

    return


@slash_command(name="edit_mountain", description="edit mountain details")
@slash_option(name="mountain", description="the name of the mountain", required=True, opt_type=OptionType.STRING)
@slash_option(name="province", description="the name of the province to edit", required=False,
              opt_type=OptionType.STRING)
@slash_option(name="county", description="the name of the county to edit", required=False,
              opt_type=OptionType.STRING)
@slash_option(name="name", description="the name of the mountain to edit", required=False, opt_type=OptionType.STRING)
@slash_option(name="height", description="the height of the mountain to edit", required=False,
              opt_type=OptionType.INTEGER)
@slash_option(name="hikers", description="the names of the hikers to edit (names separated by space)", required=False,
              opt_type=OptionType.STRING)
async def edit_mountain(ctx: SlashContext, mountain: str, province: str = "",
                        county: str = "", name: str = "", height: int = 0, hikers: str = "") -> None:

    if ctx.channel.id != CHANNEL_ID:
        await ctx.send(content="Cannot be used in this channel! :(", ephemeral=True)
        return

    _mountains: MountainList = load_mountains_from_json(FILEPATH)

    mountain = sanitise_string(mountain)
    _mountain: Mountain = _mountains.find(mountain)

    if not _mountain.name:
        await ctx.send(content=f"Could not find {mountain}! :(", ephemeral=True)
        return

    # _mnt_attrs: list = _mountain.copy()
    # _mountain_copy: Mountain = Mountain(_mnt_attrs[0], _mnt_attrs[1], _mnt_attrs[2], _mnt_attrs[3], _mnt_attrs[4])
    _mountain_copy = _mountain.copy()
    _mountains.erase(_mountain.name)

    if hikers:
        hikers: list[str] = [hiker.strip().title() for hiker in hikers.split(None)]

    _mountain_copy.set_attrs(province, county, name, height, hikers)
    _mountains.push_back(_mountain_copy)

    save_mountains_to_json(FILEPATH, _mountains.get_dict())
    await ctx.send(content=f"{mountain} edited! :)", ephemeral=True)

    return


@slash_command(name="add_hikers", description="add hikers' names to a mountain ( if they reached the peak ;) )")
@slash_option(name="mountain", description="the name of the mountain", required=True, opt_type=OptionType.STRING)
@slash_option(name="hikers", description="the names of the hikers (names separated by space)", required=True,
              opt_type=OptionType.STRING)
async def add_hikers(ctx: SlashContext, mountain: str, hikers: str) -> None:
    if ctx.channel.id != CHANNEL_ID:
        await ctx.send(content="Cannot be used in this channel! :(", ephemeral=True)
        return

    _mountains: MountainList = load_mountains_from_json(FILEPATH)

    mountain = sanitise_string(mountain)
    _mountain: Mountain = _mountains.find(mountain)

    if not _mountain.name:
        await ctx.send(content=f"Could not find {mountain}! :(", ephemeral=True)
        return

    hikers: list[str] = [hiker.strip().title() for hiker in hikers.split(None)]
    added_hikers: list[str] = []
    redunant_hikers: list[str] = []

    for hiker in hikers:
        if hiker not in _mountain.hiked:
            _mountain.hiked.append(hiker)
            added_hikers.append(hiker)
        else:
            redunant_hikers.append(hiker)

    if added_hikers:
        await ctx.send(content=f"{", ".join(added_hikers)} added! :)", ephemeral=True)
        save_mountains_to_json(FILEPATH, _mountains.get_dict())
    if redunant_hikers:
        await ctx.send(content=f"{", ".join(redunant_hikers)} already added! :/", ephemeral=True)

    return


@slash_command(name="remove_hikers", description="remove hikers from a mountain")
@slash_option(name="mountain", description="the name of the mountain", required=True, opt_type=OptionType.STRING)
@slash_option(name="hikers", description="the name of the hikers to remove (names separated by space)", required=True,
              opt_type=OptionType.STRING)
async def remove_hikers(ctx: SlashContext, mountain: str, hikers: str) -> None:
    if ctx.channel.id != CHANNEL_ID:
        await ctx.send(content="Cannot be used in this channel! :(", ephemeral=True)
        return

    _mountains: MountainList = load_mountains_from_json(FILEPATH)

    mountain = sanitise_string(mountain)
    _mountain: Mountain = _mountains.find(mountain)

    if not _mountain.name:
        await ctx.send(content=f"{mountain} not found! :(", ephemeral=True)
        return

    hikers: list[str] = [hiker.strip().title() for hiker in hikers.split(None)]
    hikers_removed: list[str] = []
    hikers_not_found: list[str] = []

    for hiker in hikers:
        if hiker not in _mountain.hiked:
            hikers_not_found.append(hiker)
        else:
            _mountain.hiked.remove(hiker)
            hikers_removed.append(hiker)

    save_mountains_to_json(FILEPATH, _mountains.get_dict())

    if hikers_removed:
        await ctx.send(content=f"{", ".join(hikers_removed)} removed! :)", ephemeral=True)
    if hikers_not_found:
        await ctx.send(content=f"{", ".join(hikers_not_found)} not found! :(", ephemeral=True)

    return


@slash_command(name="clean_up", description="clean up the channel (retains pinned posts)")
async def clean_up(ctx: SlashContext) -> None:
    if ctx.channel.id != CHANNEL_ID:
        await ctx.send(content="Cannot be used in this channel! :(", ephemeral=True)
        return

    await ctx.send(content="Purging channel! Goodbye... :/", ephemeral=True)

    await ctx.channel.purge(predicate=lambda m: m.pinned is False)

    return


@slash_command(name="commands", description="get a list of commands")
async def commands(ctx: SlashContext) -> None:
    if ctx.channel.id != CHANNEL_ID:
        await ctx.send(content="Cannot be used in this channel! :(", ephemeral=True)
        return

    message: str = ("List of commands:\n"
                    "* /mountains\n"
                    "* /add_mountain\n"
                    "* /remove_mountain\n"
                    "* /edit_mountain\n"
                    "* /add_hikers\n"
                    "* /remove_hikers\n"
                    "* /clean_up\n")

    await ctx.send(content=message, ephemeral=True)

    return


def main() -> None:
    intents: Intents = Intents.DEFAULT | Intents.GUILD_MESSAGES | Intents.MESSAGE_CONTENT

    mt_bot = Client(token=BOT_TOKEN, intents=intents)

    mt_bot.start()

    return


if __name__ == "__main__":
    main()
