"""
Куйвалайнен Д.А.
kuyvalaynen@gmail.com
ЗЕБЗ-01-16
"""

import sys

from card_table import CardTable
from player import Player
from messages import \
    MSG_GAME_TITLE,                  \
    MSG_CHECK_VALUES_AND_TRY_AGAIN,  \
    MSG_CARD_AND_PLAYER_COUNT,       \
    MSG_PLAYER_NUMBER,               \
    MSG_CURRENT_SCORE,               \
    MSG_GAME_BEGAN,                  \
    MSG_PLAYER_IS_MAKING_A_CHOICE,   \
    MSG_NO_CARD_WITH_NUMBER,         \
    MSG_GAME_OVER


class Game:
    """Класс Game реализует логику игры.

    Методы:
      - run(): запуск игры;
      - _...: дополнительные методы.
    """

    CARDS_COUNT_MIN = 2
    CARDS_COUNT_MAX = 36
    PLAYERS_COUNT_MIN = 2
    PLAYERS_COUNT_MAX = 5

    def _can_run(self, cards_count, players_count):
        """Вернуть True, если находятся в допустимом диапазоне:
          - 'cards_count': [Game.CARDS_COUNT_MIN, Game.CARDS_COUNT_MAX];
          - 'players_count': [Game.PLAYERS_COUNT_MIN, Game.PLAYERS_COUNT_MIN].
        """
        card_range_bool = Game.CARDS_COUNT_MIN <= cards_count and\
            cards_count <= Game.CARDS_COUNT_MAX
        player_range_bool = Game.PLAYERS_COUNT_MIN <= players_count and\
            players_count <= Game.PLAYERS_COUNT_MAX
        if card_range_bool and player_range_bool:
            return True
        else:
            return False

    def _get_game_params(self):
        cmd_params = False
        if len(sys.argv) == 3:
            try:
                cards_count, players_count = int(sys.argv[1]), \
                                             int(sys.argv[2])
                cmd_params = True
            except Exception:
                pass

        while True:
            try:
                print(
                    MSG_CARD_AND_PLAYER_COUNT.format(
                        Game.CARDS_COUNT_MIN, Game.CARDS_COUNT_MAX,
                        Game.PLAYERS_COUNT_MIN, Game.PLAYERS_COUNT_MAX),
                    end="")

                if cmd_params:
                    print(cards_count, players_count,
                          "(аргументы командной строки)")
                    cmd_params = False
                else:
                    params = input()
                    cards_count, players_count = map(int, params.split())

                assert self._can_run(cards_count, players_count)
                break
            except (AssertionError, ValueError):
                print(MSG_CHECK_VALUES_AND_TRY_AGAIN)
            except Exception:
                raise

        return cards_count, players_count

    def _get_players_names(self, players_count):
        players_names = []
        for i in range(1, players_count + 1):
            players_names.append(input(MSG_PLAYER_NUMBER.format(i)))
        return players_names

    def _get_current_score(self, players):
        line = ""
        for player in players:
            line += player.name + " - " + str(player.card_list.sum()) + ", "
        line = line[:-2]

        return line

    def _sorted_by_score_and_name(self, players):
        return sorted(
            players,
            key=lambda player: player.card_list.sum(),
            reverse=True)

    def run(self):
        print(MSG_GAME_TITLE)

        cards_count, players_count = self._get_game_params()
        players_names = self._get_players_names(players_count)


        table = CardTable(cards_count)
        players = [Player(name) for name in players_names]

        print("\n" + MSG_GAME_BEGAN)
        while not table.is_empty():
            for player in players:

                print(table)

                while True:
                    try:
                        print(
                            "  " +
                            MSG_PLAYER_IS_MAKING_A_CHOICE.format(player.name),
                            end="")
                        index = player.make_choice()
                        card = table.take_card(index)
                        player.add_card(card)
                        break
                    except ValueError:
                        print(MSG_CHECK_VALUES_AND_TRY_AGAIN)
                    except IndexError:
                        print(MSG_NO_CARD_WITH_NUMBER.format(index))

                if table.is_empty():
                    break

            print(MSG_CURRENT_SCORE.format(self._get_current_score(players)))

        print("\n" + MSG_GAME_OVER)

        rating = self._sorted_by_score_and_name(players)
        print(MSG_CURRENT_SCORE.format(self._get_current_score(rating)))
