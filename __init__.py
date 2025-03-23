import os
import re
import subprocess
from aqt import mw, gui_hooks
from aqt.qt import QKeySequence, QAction, QPushButton, QHBoxLayout
from aqt.editor import Editor

def get_audio_filename_from_field(note):
    if 'SentenceAudio' in note:
        match = re.search(r'\[sound:(.*?)\]', note['SentenceAudio'])
        if match:
            return match.group(1)
    return None

def get_sentence_audio_path(note):
    filename = get_audio_filename_from_field(note)
    if not filename:
        mw.statusBar().showMessage("No audio file found in SentenceAudio field.", 3000)
        return
    
    media_path = os.path.expanduser("~\\AppData\\Roaming\\Anki2\\User 1\\collection.media")
    file_path = os.path.join(media_path, filename)
    return file_path

def get_note():
    card = mw.reviewer.card
    if not card:
        return
    
    note = card.note()
    return note

def open_audio_in_external(editor = None):
    if not editor:
        note = get_note()
    else:
        note = editor.note

    if not note:
        return

    file_path = get_sentence_audio_path(note)

    if not file_path:
        return
    
    if not os.path.exists(file_path):
        mw.statusBar().showMessage("Audio file not found in media folder.", 3000)
        return
    
    external_tool = os.path.expanduser(r"~\AppData\Roaming\GameSentenceMiner\ocenaudio\ocenaudio\ocenaudio.exe")  # Change this to your preferred program
    subprocess.Popen([external_tool, file_path], shell=True)
    
def show_in_filemanager(editor = None):

    if not editor:
        note = get_note()
    else:
        note = editor.note

    if not note:
        return
    
    file_path = get_sentence_audio_path(note)

    if not file_path:
        return
    
    subprocess.Popen(f'explorer /select, "file://{file_path}" ')


def add_toolbar_buttons(html_buttons: list[str], editor: Editor) -> None:
    html_buttons.extend([(
        editor.addButton(
            icon=None,
            func=open_audio_in_external,
            cmd="open_audio_in_external",
            tip="Open Audio in External Tool",
            keys="F14",
        )
    ),
        editor.addButton(
            icon=None,
            func=show_in_filemanager,
            cmd="show_in_filemanager",
            tip="Open Audio in Folder",
            keys="F15",
        )
    ])


def setup_hotkey():
    action = QAction("Open Audio Externally", mw)
    action.setShortcut(QKeySequence("F14"))
    action.triggered.connect(open_audio_in_external)
    mw.form.menuTools.addAction(action)
    
    action_copy = QAction("Open Audio in Folder", mw)
    action_copy.setShortcut(QKeySequence("F15"))
    action_copy.triggered.connect(show_in_filemanager)
    mw.form.menuTools.addAction(action_copy)

gui_hooks.editor_did_init_buttons.append(add_toolbar_buttons)
# editor_did_init.append(add_buttons_to_editor)

setup_hotkey()
