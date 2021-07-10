from string import Template

from snakeshot.model.tournament import Tournament


class Printer:
    @classmethod
    def table(cls, slam: dict) -> dict:
        return {
            tour: Printer._table_tournament(tour, tournament)
            for tour, tournament in slam.items()
        }

    @classmethod
    def _table_tournament(cls, tour: str, t: Tournament):
        widths = {"t": 6, "r": 1, "m": 2, "p": 33}
        result: list = [*Printer._table_header(widths)]
        for r_idx, r in enumerate(t.rounds):
            if r_idx != 0:
                result.append(Printer._table_divider("round", widths))
            n_m: int = 2 ** (6 - r_idx)
            for m_idx, m in enumerate(r.matches):
                result.append(
                    Printer._table_line(
                        {
                            "t": tour,
                            "r": r_idx + 1,
                            "m": f"{m_idx + 1:{widths.get('m')}} / {n_m:{widths.get('m')}}",
                            "p1": m.rankings[0].summary("draw"),
                            "p2": m.rankings[1].summary("draw"),
                            "pw": m.winner_expected.summary("draw"),
                        },
                        widths,
                    )
                )
        result.append(Printer._table_divider("foot", widths))
        return result

    @classmethod
    def _table_header(cls, widths: dict) -> list:
        return [
            Printer._table_divider("head_upper", widths),
            Printer._table_line(
                {
                    "t": "Tour",
                    "r": "R",
                    "m": "Match",
                    "p1": "Player 1",
                    "p2": "Player 2",
                    "pw": "Winner",
                },
                widths,
            ),
            Printer._table_divider("head_lower", widths),
        ]

    @classmethod
    def _table_divider(cls, divider: str, widths: dict) -> str:
        i = "═"
        ts = {
            "head_upper": Template("╔═$t═╦═$r═╤═$m═══$m═╦═$p═╤═$p═╦═$p═╗"),
            "head_lower": Template("╠═$t═╬═$r═╪═$m═══$m═╬═$p═╪═$p═╬═$p═╣"),
            "round": Template("╠═$t═╬═$r═╪═$m═══$m═╬═$p═╪═$p═╬═$p═╣"),
            "foot": Template("╚═$t═╩═$r═╧═$m═══$m═╩═$p═╧═$p═╩═$p═╝"),
        }
        return ts.get(divider).substitute(
            t=i * widths.get("t"),
            r=i * widths.get("r"),
            m=i * widths.get("m"),
            p=i * widths.get("p"),
        )

    @classmethod
    def _table_line(cls, values: dict, widths: dict) -> str:
        t = Template("║ $t ║ $r | $m ║ $p1 | $p2 ║ $pw ║")
        return t.substitute(
            t=f"{values.get('t'):{widths.get('t')}}",
            r=f"{values.get('r'):{widths.get('r')}}",
            m=f"{values.get('m'):{widths.get('m') * 2 + 3}}",
            p1=f"{values.get('p1'):{widths.get('p')}}",
            p2=f"{values.get('p2'):{widths.get('p')}}",
            pw=f"{values.get('pw'):{widths.get('p')}}",
        )
