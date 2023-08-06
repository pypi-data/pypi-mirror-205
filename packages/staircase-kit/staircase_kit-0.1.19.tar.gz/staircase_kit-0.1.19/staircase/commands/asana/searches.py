import rich
import click
from itertools import product

from staircase.lib.fzf import prompt
from staircase.staircase_asana import StaircaseAsana, SEARCHES_BY_TEAM
from staircase.lib.click import async_cmd
from staircase.command_providers import user_config_provider
from staircase.config import UserConfig


@click.command(name="searches")
@user_config_provider()
@async_cmd
async def command(user_config: UserConfig):
    if not user_config.asana_token:
        raise Exception("No asana token in config")
    asana = StaircaseAsana(token=user_config.asana_token)

    teams = asana.get_staircase_teams()

    verbose_names = []
    searches_combinations = product(SEARCHES_BY_TEAM, teams)
    # Genearting constructed searches
    searches = map(
        lambda search_combination: search_combination[0](
            team=search_combination[1], staircase_asana=asana
        ),
        searches_combinations,
    )

    enumed_searches = list(enumerate(searches))
    for idx, search in enumed_searches:
        verbose_names.append(f"{idx}: {search.verbose_name}")

    selected = prompt(verbose_names)[0]
    idx = int(selected.split(":")[0])
    search = enumed_searches[idx][1]


    rich.print(search.search_url)

