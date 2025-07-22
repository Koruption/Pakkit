
import sys
import shutil
import textwrap

text = """In the neon-slick gutters of New Osaka’s lower rings, where the rain never stops and the light is always artificial, Riko lit a synth-cig and watched the city stutter. Above her, corporate sky-barges drifted like gods in low orbit, their hulls etched with shifting glyphs of adspace and threat. Down here, everything buzzed—retinal overlays, AI static bleeding through faulty neural links, the murmur of ambient data slithering like ghosts in the mesh. Riko’s left eye caught fire with warning runes—her black market cranial socket was pulling something heavy from the deep net, a half-dead signal coded in bone and sorrow. She spat into the drainage slit, her spit glowing faintly blue from nanite residue. The job was simple: break into a dead man's memory vault before his soul copy decayed. But in a city like this, nothing stayed dead for long. Not the ghosts, not the code, not even her. The gang called her a slicer. The corps called her a security risk. She called herself awake. And as she zipped her coat—leather, modded, wired into her nervous system like a second skin—she wondered how many more nights the city would let her live before it turned her into another flickering obituary in someone else’s feed. The sky was bleeding static again—low orbit satellites misfiring like drunk sentinels, painting jagged red strobes across the smog-choked skyline of Sector-9. Below, the city thrummed with its usual pulse of synthetic adrenaline: hover-rickshaws zipping between billboard monoliths, ad-drones whispering psychotropic jingles, and the ever-present hum of the Grid wrapping around every surface like a digital skin. Kaelin walked alone, boots crunching on broken glass and spent shell casings, his neural HUD flickering with half-legible warnings: REVENANT TRACE DETECTED. POSSIBLE LOOPBACK. He didn’t care. They could track his echo, scramble his bio-signature, maybe even reroute his memories if they were fast enough—but they’d never find the original, because he hadn’t been original in years. Not since the last upload. Not since the last overwrite. He passed under a broken streetlamp, the kind that tried to scan your face and gave up halfway through. Even the machines were tired. Behind him, a kid jacked into a public access port slumped sideways, pupils glowing, lost in a labyrinth of monetized dreams. Kaelin didn’t look. He just kept walking, past the shrines of burnt-out servers, past the half-melted mechs used for target practice, deeper into the maze of low-tier districts where reality ran thinner and the line between code and flesh was a rumor no one bothered verifying anymore."""


def screen_width():
    columns, rows = shutil.get_terminal_size()
    return columns, rows

def get_wrapped(text: str):
    cols, _ = screen_width()
    wrapped = textwrap.wrap(text, width=cols)
    return wrapped
