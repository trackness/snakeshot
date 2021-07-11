import os

from jinja2 import Template, Environment, FileSystemLoader

from loguru import logger


class Renderer:
    @classmethod
    def write(cls, name: str, year: int, slam: dict) -> str:
        logger.info(f"Generating {name} {year} html tables")

        logger.info("Loading template")
        template: Template = Environment(
            loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "./"))
        ).get_template("template.html")

        logger.info("Making template substitutions")
        return template.render(title=f"{name} {year}", slam=slam)

        # with open("index.html", "w") as f:
        #     f.write(subs)
        # return subs
