
import cx_Freeze
import os
import sys

base = None
if sys.platform == "win32":
    base = "Win32GUI"
executables = [cx_Freeze.Executable("run.py", base = "Win32GUI")]
packageData = ["border.py",
                                        "bullet.py",
                                        "button.py",
                                        "collect.py",
                                        "consts.py",
                                        "data.py",
                                        "explosion.py",
                                        "feature.py",
                                        "game_board.py",
                                        "manager.py",
                                        "missile.py",
                                        "border.py",
                                        "mobile.py",
                                        "run.py",
                                        "runway.py",
                                        "tank.py",
                                        "texts.py"] 

                                                                       ]}
cx_Freeze.setup(
    name="spaceWar",
    version="1.1",
    package_data = {"cx_Freeze" : packageData }
    options={"build_exe": {"packages": ["pygame", "numpy", "random",
                                        "math",
                                        "time",
                                        },
                                        
                                        "include_files": ["0.png",
                                                                       "1.png",
                                                                       "2.png",
                                                                       "3.png",
                                                                       "4.png",
                                                                       "5.png",
                                                                       "add_life.png",
                                                                       "begin.png",
                                                                       "begin_pressed.png",
                                                                       "expl0.jpg",
                                                                       "expl1.jpg",
                                                                       "expl2.jpg",
                                                                       "features.png",
                                                                       "laserGreen.png",
                                                                       "laserGreenShot.png",
                                                                       "laserRed.png",
                                                                       "laserRedShot.png",
                                                                       "missile.jpg",
                                                                       "p1.png",
                                                                       "pressed.png",
                                                                       "rules.png",
                                                                       "rules_pressed.png",
                                                                       "runway.jpg",
                                                                       "settings.png",
                                                                       "settings_pressed.png",
                                                                       "shield.png",
                                                                       "ship0.jpg",
                                                                       "ship1.jpg",
                                                                       "ship10.jpg",
                                                                       "ship11.jpg",
                                                                       "ship12.jpg",
                                                                       "ship13.jpg",
                                                                       "ship14.jpg",
                                                                       "ship15.jpg",
                                                                       "ship16.jpg",
                                                                       "ship17.jpg",
                                                                       "ship2.jpg",
                                                                       "ship3.jpg",
                                                                       "ship4.jpg",
                                                                       "ship5.jpg",
                                                                       "ship6.jpg",
                                                                       "ship7.jpg",
                                                                       "ship8.jpg",
                                                                       "ship9.jpg",
                                                                       "space.png",
                                                                       "start_screen.png",
                                                                       "tank_shield.jpg",
                                                                       "unpressed.png"
    description="game",
    executables=executables
)
