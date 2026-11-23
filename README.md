# Robot & Helicopter (OpenGL)

Computer Graphics course project: an animated, textured **robot** and **helicopter** in one scene,
controlled with keyboard and mouse. Python + pygame + PyOpenGL, no game engine.

## Authors

- **Денис Иванов** (121223066) - the robot (`robot.py`)
- **Владислав Пешев** (121223059) - the helicopter (`helicopter.py`)
- shared: `main.py`, `world.py`, `shapes.py`, `textures.py`

## Run

```
python -m pip install -r requirements.txt
python main.py
```

## Controls

| Key / mouse | Robot | Helicopter |
|---|---|---|
| W / S | walk forward / backward | fly forward / backward |
| A / D | turn left / right | turn left / right (in the air) |
| Shift | run | - |
| F | wave | - |
| Q / E | - | up / down (rotor must spin up first) |
| Tab | switch to the other one | |
| left mouse drag, wheel | rotate camera, zoom | |
| Esc | quit | |

## Files

| File | What it does | Lines |
|---|---|---|
| `main.py` | window, game loop, Tab switching, camera, simple collision | ~150 |
| `robot.py` | robot model (boxes) + walk / wave / idle animation with `sin()` | ~170 |
| `helicopter.py` | helicopter model + spinning rotors, take-off, flying, tilting, landing | ~165 |
| `world.py` | grass, helipad, round shadows | ~60 |
| `shapes.py` | box with texture coordinates, sphere, cylinder | ~70 |
| `textures.py` | loads a PNG into an OpenGL texture | ~25 |
| `make_textures.py` | (optional) recreates the PNGs in `textures/` | ~95 |

Any PNG in `textures/` can be replaced with a real photo (keep the file name).

Documentation: `docs/121223066_121223059_CP_Robot_Helicopter_CG.pdf`
