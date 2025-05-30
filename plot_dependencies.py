import dishka.plotter
import uvloop
from dishka import AsyncContainer, make_async_container

from src.setup import Settings
from src.setup import get_providers


def make_container(settings: Settings) -> AsyncContainer:
    return make_async_container(*get_providers(), context={Settings: settings})


async def main() -> None:
    settings: Settings = Settings()
    container = make_container(settings)
    print(dishka.plotter.render_mermaid(container))


if __name__ == "__main__":
    uvloop.run(main())
