echo Building.....
pyinstaller --onefile --windowed --add-data="assets;assets" --icon=icon.ico main.py
echo OK!
pause