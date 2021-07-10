from jinja2 import Template, Environment, FileSystemLoader


class Renderer:
    @classmethod
    def write(cls, slam: str, year: int, tournament: dict) -> str:
        subs = (
            Environment(loader=FileSystemLoader("./templates"))
            .get_template("template.html")
            .render(title=f"{slam} {year}", tables=tournament)
        )

        with open("index.html", "w") as f:
            f.write(subs)

        return subs


# if __name__ == "__main__":
#     html = Renderer.write("Wimbledon", 2021, "")
#     print(html)
