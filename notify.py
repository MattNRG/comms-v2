# Source - https://stackoverflow.com/a/41318195
# Posted by Christopher Shroba, modified by community. See post 'Timeline' for change history
# Retrieved 2026-07-13, License - CC BY-SA 4.0

import os

def message(title, text):
    if not os.name == 'posix': return
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))