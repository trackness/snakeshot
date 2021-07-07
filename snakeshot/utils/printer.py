from string import Template

from snakeshot.model.tournament import Tournament


class Printer:
    @classmethod
    def print(cls, tournaments: dict[str, Tournament]):
        widths = {"t": 6, "r": 1, "m": 2, "p": 28}
        for tour, t in tournaments.items():
            Printer._print_header(widths)
            for r in t.rounds:
                if r.idx != 0:
                    Printer._print_divider("round", widths)
                n_m: int = 2 ** (6 - r.idx)
                for m in r.matches:
                    Printer._print_line(
                        {
                            "t": tour,
                            "r": r.idx + 1,
                            "m": f"{m.idx + 1:{widths.get('m')}} / {n_m:{widths.get('m')}}",
                            "p1": m.players[0].full_name,
                            "p2": m.players[1].full_name,
                            "pw": m.winner_expected.full_name,
                        },
                        widths,
                    )
            Printer._print_divider("foot", widths)

    @classmethod
    def _print_header(cls, widths: dict):
        Printer._print_divider("head_upper", widths)
        Printer._print_line(
            {
                "t": "Tour",
                "r": "R",
                "m": "Match",
                "p1": "Player 1",
                "p2": "Player 2",
                "pw": "Winner",
            },
            widths,
        )
        Printer._print_divider("head_lower", widths)

    @classmethod
    def _print_divider(cls, divider: str, widths: dict):
        i = "═"
        ts = {
            "head_upper": Template("╔═$t═╦═$r═╤═$m═══$m═╦═$p═╤═$p═╦═$p═╗"),
            "head_lower": Template("╠═$t═╬═$r═╪═$m═══$m═╬═$p═╪═$p═╬═$p═╣"),
            "round": Template("╠═$t═╬═$r═╪═$m═══$m═╬═$p═╪═$p═╬═$p═╣"),
            "foot": Template("╚═$t═╩═$r═╧═$m═══$m═╩═$p═╧═$p═╩═$p═╝"),
        }
        print(
            ts.get(divider).substitute(
                t=i * widths.get("t"),
                r=i * widths.get("r"),
                m=i * widths.get("m"),
                p=i * widths.get("p"),
            )
        )

    @classmethod
    def _print_line(cls, values: dict, widths: dict):
        t = Template("║ $t ║ $r | $m ║ $p1 | $p2 ║ $pw ║")
        print(
            t.substitute(
                t=f"{values.get('t'):{widths.get('t')}}",
                r=f"{values.get('r'):{widths.get('r')}}",
                m=f"{values.get('m'):{widths.get('m') * 2 + 3}}",
                p1=f"{values.get('p1'):{widths.get('p')}}",
                p2=f"{values.get('p2'):{widths.get('p')}}",
                pw=f"{values.get('pw'):{widths.get('p')}}",
            )
        )
