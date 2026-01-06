from nicegui import ui
import time
import random
import env
TEXTS_BEGINNER = [
    "The cat sat on the mat.",
    "Run fast and jump high.",
    "Blue sky and green grass.",
    "I like to read books.",
    "She sings a nice song."
]

TEXTS_HIGH = [
    "The quick brown fox jumps over the lazy dog. This classic sentence contains every letter of the alphabet and is often used for typing practice.",
    "Technology is best when it brings people together. It allows us to connect and share ideas instantly across the globe without any delay.",
    "Success is not final, failure is not fatal: it is the courage to continue that counts in the end. Keep pushing forward every day."
]


TEXTS_MUCH_HIGH = [
    "Coding is like poetry; it requires precision, creativity, and a deep understanding of the language. Just like a poet arranges words to create emotion, a developer arranges code to create functionality. It is an art form that evolves constantly with new technologies and methodologies emerging every day. Mastery takes time and patience.",
    "To improve your typing speed, practice daily and focus on accuracy rather than just raw speed. Start slowly, ensure every keystroke is correct, and gradually increase your pace. Over time, your muscle memory will develop, and you will find your fingers dancing across the keyboard without conscious effort. Consistency is the key to unlocking your full potential."
]


TEXT_LEVELS = {
    "Beginner": TEXTS_BEGINNER,
    "High": TEXTS_HIGH,
    "Much High": TEXTS_MUCH_HIGH
}


current_difficulty = "Beginner"
current_target_text = ""
start_time = None
is_test_running = False


btn_beginner = None
btn_high = None
btn_much_high = None
display_label = None
input_field = None



def get_wpm(text_length, time_elapsed_sec):
    if time_elapsed_sec == 0: return 0
    return round((text_length / 5) / (time_elapsed_sec / 60))

def calculate_accuracy(original, typed):
    if not typed: return 0
    correct_chars = 0
    loop_len = min(len(original), len(typed))
    for i in range(loop_len):
        if typed[i] == original[i]:
            correct_chars += 1
    return round((correct_chars / len(typed)) * 100) if typed else 0

def update_button_styles():
    """Updates colors of buttons based on current difficulty"""
    global btn_beginner, btn_high, btn_much_high, current_difficulty
    
    inactive_classes = "bg-gray-200 text-gray-700"
    active_classes = "bg-indigo-600 text-white"

    btn_beginner.classes(remove='bg-indigo-600 text-white', add=inactive_classes)
    btn_high.classes(remove='bg-indigo-600 text-white', add=inactive_classes)
    btn_much_high.classes(remove='bg-indigo-600 text-white', add=inactive_classes)

    if current_difficulty == "Beginner":
        btn_beginner.classes(remove=inactive_classes, add=active_classes)
    elif current_difficulty == "High":
        btn_high.classes(remove=inactive_classes, add=active_classes)
    elif current_difficulty == "Much High":
        btn_much_high.classes(remove=inactive_classes, add=active_classes)

def update_display_html(typed_text=""):
    """Updates the HTML label with Green/Red colors"""
    global current_target_text, display_label
    
    html_content = ""
    
    for i in range(len(current_target_text)):
        original_char = current_target_text[i]
        
        # Handle newlines properly for display
        if original_char == '\n':
            html_content += '<br>'
            continue

        if i < len(typed_text):
            typed_char = typed_text[i]
            if typed_char == original_char:
                html_content += f'<span class="text-green-600 font-bold">{original_char}</span>'
            else:
                html_content += f'<span class="text-red-500 bg-red-100 rounded px-0.5 font-bold">{typed_char}</span>'
        else:
            html_content += f'<span class="text-gray-400">{original_char}</span>'
            
    display_label.content = html_content

def reset_test(keep_text=False):
    """Resets the test. If keep_text=True, uses same text, else picks new."""
    global is_test_running, start_time, current_target_text, input_field
    
    is_test_running = False
    start_time = None
    input_field.value = ""
    
    if not keep_text:
        texts = TEXT_LEVELS[current_difficulty]
        current_target_text = random.choice(texts)
    
    update_display_html()

def set_difficulty(level):
    """Changes the difficulty level and resets the test"""
    global current_difficulty
    current_difficulty = level
    reset_test(keep_text=False)
    update_button_styles()

def finish_test(input_value):
    """Calculates stats and shows dialog"""
    global is_test_running
    is_test_running = False
    
    end_time = time.time()
    time_taken = end_time - start_time if start_time else 0
    
    accuracy = calculate_accuracy(current_target_text, input_value)
    wpm = get_wpm(len(input_value.split(' ')), time_taken)
    
    with ui.dialog() as dialog, ui.card().classes('w-full max-w-md p-8 rounded-3xl shadow-2xl bg-white'):
        ui.label("Test Completed!").classes("text-3xl font-extrabold text-indigo-600 mb-6 text-center")
        
        with ui.column().classes("w-full gap-4"):
            with ui.row().classes("justify-between items-center bg-gray-100 p-4 rounded-xl"):
                ui.label("Time").classes("text-gray-500 font-bold")
                ui.label(f"{time_taken:.1f} sec").classes("text-xl font-black text-gray-900")
            
            with ui.row().classes("justify-between items-center bg-indigo-50 p-4 rounded-xl"):
                ui.label("True WPM").classes("text-gray-500 font-bold")
                ui.label(f"{wpm}").classes("text-xl font-black text-indigo-600")
                
            with ui.row().classes("justify-between items-center bg-green-50 p-4 rounded-xl"):
                ui.label("Accuracy").classes("text-gray-500 font-bold")
                ui.label(f"{accuracy}%").classes("text-xl font-black text-green-600")

        ui.separator().classes("my-4")
        
        with ui.row().classes("w-full gap-2"):
            ui.button("Retry Same", on_click=lambda: (dialog.close(), reset_test(keep_text=True)))\
                .classes("flex-1 bg-gray-200 text-gray-800 font-bold py-3 rounded-xl hover:bg-gray-300")
            
            ui.button("Change Text", on_click=lambda: (dialog.close(), reset_test(keep_text=False)))\
                .classes("flex-1 bg-indigo-600 text-white font-bold py-3 rounded-xl hover:bg-indigo-700")

    dialog.open()

def stop_test():
    """Manually stops the test"""
    if is_test_running:
        finish_test(input_field.value)
    else:
        ui.notify("Test has not started yet!", type='warning')

def on_text_change(e):
    global start_time, is_test_running
    
    typed_text = e.value
    
    if not is_test_running and len(typed_text) == 1:
        start_time = time.time()
        is_test_running = True
    
    if is_test_running:
        update_display_html(typed_text)
        if len(typed_text) >= len(current_target_text):
            finish_test(typed_text)

@ui.page("/typing_test")
def typing_page():
    global current_target_text, display_label, input_field, btn_beginner, btn_high, btn_much_high
    
    # Background styling
    ui.add_head_html("""
    <style>
        body { background: #f1f5f9; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .typewriter-text { white-space: pre-wrap; word-break: break-word; }
    </style>
    """)
    

    with ui.row().classes("w-full items-center justify-between px-8 py-4 bg-white shadow-sm sticky top-0 z-50"):
        ui.label("Typing Master").classes("text-2xl font-extrabold text-gray-800 tracking-wide")
        
        with ui.row().classes("gap-2"):
            btn_beginner = ui.button("Beginner", on_click=lambda: set_difficulty("Beginner")).classes("px-4 py-2 rounded-full font-bold transition-all")
            btn_high = ui.button("High", on_click=lambda: set_difficulty("High")).classes("px-4 py-2 rounded-full font-bold transition-all")
            btn_much_high = ui.button("Much High", on_click=lambda: set_difficulty("Much High")).classes("px-4 py-2 rounded-full font-bold transition-all")

        ui.button("Stop Test", on_click=stop_test).classes("bg-red-500 text-white px-6 py-2 rounded-full font-bold hover:bg-red-600")


    current_difficulty = "Beginner"
    btn_beginner.classes(remove='bg-gray-200 text-gray-700', add='bg-indigo-600 text-white')
    btn_high.classes(add='bg-gray-200 text-gray-700')
    btn_much_high.classes(add='bg-gray-200 text-gray-700')
    current_target_text = random.choice(TEXTS_BEGINNER)

    
    with ui.element().classes("w-full h-full grid grid-cols-2 gap-2"):
        input_field = ui.textarea(
            placeholder="Start typing here...",
            on_change=on_text_change
        ).props(
            'outlined rows=2 input-class="text-lg" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false" no-resize'
        ).classes("w-full")
        display_label = ui.html('', sanitize=False).classes(
            "typewriter-text text-2xl leading-loose font-medium tracking-wide text-left w-full outline-1 outline-gray-400 p-2 rounded-md"
        )
