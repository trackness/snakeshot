from jinja2 import Template, Environment, FileSystemLoader

from snakeshot.model.slam import Slam
from loguru import logger


class Renderer:
    @classmethod
    def write(cls, name: str, year: int, slam: dict) -> str:
        logger.info(f"Generating {name} {year} html tables")
        subs = (
            Environment(loader=FileSystemLoader("./templates"))
            .get_template("template.html")
            .render(title=f"{name} {year}", slam=slam)
        )

        with open("index.html", "w") as f:
            f.write(subs)

        return subs


# if __name__ == "__main__":
#     print(
#         Renderer.write(
#             "Wimbledon",
#             2021,
#             {
#                 "Mens": [0, 1, 2],
#                 "Womens": [3, 4, 5],
#             }
#         )
#     )
