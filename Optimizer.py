from AuditorySupercube import AuditorySupercube
from fuzzywuzzy import process, fuzz
import matplotlib.pyplot as plt
import os

given_alg = "U U U U D D D D R R R R L L L L F F F F B B B B"
# given_tps = 2
# a_cube.apply_alg(given_alg, given_tps, simulation=True)
# a_cube.play_simulation(silent=True)
csv = open(f"csv/data.csv", "a")
csv.write("file_name,window_size,stdv,alt_min,received_alg,similarity\n")
for (root, dirs, files) in os.walk('resources/sounds'):
    for file in files:
        for window_size in (range(1, 11)):  # + range(10, 201, 30)):
            for stdv in range(25, 301, 25):
                for alt_min in range(50, 551, 100):
                    a_cube = AuditorySupercube(f'test_sounds/{file}', window_size, stdv / 100, alt_min)
                    a_cube.log.info(f"Starting analysis with window size: {window_size}, stdv: {stdv/100}, alt min: {alt_min}")
                    received_alg = a_cube.extract_alg_from_audio()
                    similarity = fuzz.ratio(received_alg, given_alg)
                    a_cube.log.info(f"Given Alg: {given_alg}\nReceived Alg: {received_alg}")
                    a_cube.log.info(f"Similarity: {similarity}%")
                    a_cube.log.info("MATCH!" if given_alg.strip() == received_alg.strip() else "MISMATCH :(")
                    a_cube.log.info(f"Finished analysis with window size: {window_size}, stdv: {stdv/100}, alt min: {alt_min}")
                    a_cube.log.save_to_disk()
                    csv.write(f"{file},{window_size},{stdv/100},{alt_min},{received_alg},{similarity}\n")
                    csv.flush()
csv.close()

# pos = AuditorySupercube()
# pos.transmitAlg("U U U U D D D D R R R R L L L L F F F F B B B B", 1.5)
# pos.playSound()
# pos.parseAlg("U U U U", 2)
# pos.playSound()
# pos.parseAlg("D D D D", 2)
# pos.playSound()
# pos.parseAlg("R R R R", 2)
# pos.playSound()
# pos.parseAlg("L L L L", 2)
# pos.playSound()
# pos.parseAlg("F F F F", 2)
# pos.playSound()
# pos.parseAlg("B B B B", 2)
# pos.playSound()
