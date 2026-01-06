from nicegui import ui
from env import *
import typing_test

def header():
    with ui.row().classes("w-full items-center justify-between px-12 py-5 bg-black"):        
        ui.label(APP_NAME).classes("text-white text-3xl font-extrabold tracking-wide")
        ui.button("Start Typing",on_click=lambda: ui.navigate.to("/typing_test")).classes(BTN_CLASS).style(f"background:{PRIMARY_COLOR}")

def feature(title, subtitle):
    with ui.column().classes("p-6 rounded-2xl bg-gray-100"):
        ui.label(title).classes("text-lg font-bold")
        ui.label(subtitle).classes("text-gray-600")


def floating_chip(text, color_classes, animation_class):
    ui.label(text).classes(
        f"""
        absolute px-4 py-2 rounded-full font-bold shadow-lg
        {color_classes} {animation_class}
        """
    )

def hero():
    with ui.card().classes(
        "w-full max-w-7xl p-14 rounded-[2.5rem] bg-white shadow-2xl overflow-hidden"
    ):

        with ui.element().classes("relative w-full gap-2 flex flex-row"):
            with ui.column().classes("gap-4 w-full h-full"):
                ui.label("Typing Master Pro").classes(
                    "text-6xl font-black text-gray-900"
                )
                ui.label("A complete typing experience").classes(
                    "text-xl text-gray-500"
                )
            # # RIGHT FLOATING ELEMENTS
            # with ui.element().classes(
            #     "absolute pointer-events-none left-0 h-[50px] w-full mt-20"
            # ):
            #     floating_chip("Speed", "bg-indigo-100 text-indigo-700", "float-1")
            #     floating_chip("Accuracy", "bg-green-100 text-green-700", "float-2")
            #     floating_chip("Focus", "bg-yellow-100 text-yellow-700", "float-3")
            #     floating_chip("Discipline", "bg-pink-100 text-pink-700", "float-4")
            #     floating_chip("Growth", "bg-purple-100 text-purple-700", "float-5")

        with ui.element().classes("grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 mt-6 w-full"):
                feature("Smart Design", "Clean UI focused on productivity")
                feature("Modern Look", "Minimal yet premium visuals")
                feature("User Friendly", "Easy to use for everyone")
                feature("Performance", "Optimized for smooth usage")

# def stats():
#     with ui.card().classes("w-full max-w-7xl p-10 rounded-[2.5rem] bg-white shadow-xl"):
#         with ui.row().classes("justify-between text-center"):
#             with ui.column():
#                 ui.label("200+").classes("text-5xl font-black text-indigo-600")
#                 ui.label("Modules").classes("text-gray-500")
#             with ui.column():
#                 global online_label
#                 online_label = ui.label(str(line_count())).classes("text-5xl font-black text-green-600")
#                 ui.label("Users").classes("text-gray-500")
#             with ui.column():
#                 ui.label("99.9%").classes("text-5xl font-black text-yellow-600")
#                 ui.label("Stability").classes("text-gray-500")
#             with ui.column():
#                 ui.label("∞").classes("text-5xl font-black text-pink-600")
#                 ui.label("Practice").classes("text-gray-500")

def info_blocks():
    with ui.card().classes("w-full max-w-7xl p-12 rounded-[2.5rem] bg-white shadow-xl"):
        ui.label("Why Choose Typing Master").classes("text-4xl font-extrabold mb-8")
        with ui.row().classes("gap-6 flex-wrap"):
            for title, text in [
                ("Mental Sharpness", "Typing improves reaction speed"),
                ("Time Saving", "Faster typing saves hours"),
                ("Professional Skill", "Required in modern careers"),
                ("Confidence Boost", "Accuracy builds confidence"),
                ("Daily Habit", "Small practice big results"),
                ("Keyboard Mastery", "Control without thinking"),
                ("Productivity", "Work faster with focus"),
                ("Consistency", "Progress every day")
            ]:
                with ui.column().classes("w-[23%] p-5 rounded-xl bg-gray-100"):
                    ui.label(title).classes("text-lg font-bold")
                    ui.label(text).classes("text-gray-600")

def footer():
    with ui.row().classes("w-full justify-center py-5 bg-black text-gray-400"):
        ui.label("© 2025 Typing Master Pro · Designed for Growth|Rehmani-typer")
        
@ui.page("/")
def main_page():
    ui.add_head_html("""
    <style>
        body { background: #f1f5f9; }
/* Width of the scrollbar */
::-webkit-scrollbar {
  width: 10px;
  height: 10px; /* for horizontal scrollbars */
}

/* Track (background) */
::-webkit-scrollbar-track {
  background: #f1f1f1;
}

/* Handle (the draggable part) */
::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 0px;
}

/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
  background: #555;
}

@keyframes float {
  0%   { transform: translateY(0px); }
  50%  { transform: translateY(-12px); }
  100% { transform: translateY(0px); }
}

.float-1 { top: -120px; right: 40px; animation: float 6s ease-in-out infinite; }
.float-2 { top: -40px; right: 140px; animation: float 7s ease-in-out infinite; }
.float-3 { top: 40px; right: 20px; animation: float 5.5s ease-in-out infinite; }
.float-4 { top: 120px; right: 120px; animation: float 6.5s ease-in-out infinite; }
.float-5 { top: 200px; right: 60px; animation: float 7.5s ease-in-out infinite; }
</style>
""")
    header()
    with ui.column().classes("w-full items-center gap-6 mt-2 px-6"):
        hero()
        info_blocks()
        footer()
    # user_connected()

ui.run(title=APP_NAME, port=8080)
