from nicegui import ui

APP_NAME = "Typing Master Pro"

PRIMARY_COLOR = "#4f46e5"   
SECONDARY_COLOR = "#0f172a" 
ACCENT_COLOR = "#22c55e"    

BTN_CLASS = "px-6 py-2 rounded-xl text-white font-bold"
CARD_CLASS = "w-full max-w-3xl p-6 rounded-2xl shadow-lg bg-white"
TEXT_TITLE = "text-3xl font-extrabold"
TEXT_SUB = "text-gray-500"

def Button(
        text: str = "", 
        on_click = lambda: (),
        link="",
        new_tab=False,
        config: dict|None = None
    ):
    if not config: config = {}
    btn = ui.button(text=text, on_click=on_click, **config).props("unelevated push").classes("bg-btn-l dark:bg-btn-d")
    if link:
        btn.props(f'href="{link}"')
    if new_tab:
        btn.props(f'target="_blank"')
    return btn

def navBar(icon = "", links:dict|None = None, bkp="sm"):
    with ui.element().classes("w-fit h-fit") as nav:
        with ui.element().classes(f"items-center justify-between gap-2 hidden {bkp}:!flex", remove='hidden') as desktop:
            for name,opts in (links or {}).items():
                if isinstance(opts, (dict)):
                    condition = opts.pop("cond", True)
                    if condition:
                        Button(name, **opts)
                else:
                    Button(name, link=opts)
        with Button(config=dict(icon="menu")).classes(f"flex {bkp}:hidden") as mobile:
            with ui.menu().props("auto-close"):
                with ui.element().classes("flex flex-col w-fit gap-1 p-1 bg-secondary"):
                    for name,opts in (links or {}).items():
                        if isinstance(opts, (dict)):
                            condition = opts.pop("cond", True)
                            if condition:
                                Button(name, **opts).classes("w-full")
                        else:
                            Button(name, link=opts).classes("w-full")
    return nav, desktop, mobile