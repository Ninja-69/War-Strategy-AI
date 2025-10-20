import pandas as pd

battles = []

def add(name, year, loc, terrain, att_troops, def_troops, att_tac, def_tac, outcome, lesson):
    battles.append({'name': name, 'year': year, 'location': loc, 'terrain': terrain, 'attacker_troops': att_troops, 'defender_troops': def_troops, 'attacker_tactics': att_tac, 'defender_tactics': def_tac, 'outcome': outcome, 'key_lesson': lesson})

add("Thermopylae", "480 BC", "Greece", "Mountain pass", "70,000-300,000 Persians", "7,000 Greeks", "Mass assault", "Phalanx chokepoint", "Persian victory", "Terrain multiplies defense")
add("Cannae", "216 BC", "Italy", "Open plains", "86,000 Romans", "50,000 Carthaginians", "Frontal assault", "Double envelopment", "Carthaginian victory", "Tactics beat numbers")
add("Waterloo", "1815", "Belgium", "Rolling hills", "72,000 French", "68,000 Allies", "Artillery cavalry", "Defensive squares", "Allied victory", "Reserves swing battles")
add("Stalingrad", "1942-43", "Russia", "Urban ruins", "1M+ Germans", "1.1M+ Soviets", "Urban assault", "Building defense", "Soviet victory", "Urban favors defenders")
add("D-Day", "1944", "Normandy", "Beach cliffs", "156,000 Allied", "50,000 Germans", "Amphibious assault", "Atlantic Wall", "Allied victory", "Air superiority key")
add("Midway", "1942", "Pacific", "Naval", "4 Japanese carriers", "3 US carriers", "Carrier strike", "Codebreaking ambush", "US victory", "Intel beats material")
add("Agincourt", "1415", "France", "Muddy field", "12,000 French", "6,000 English", "Cavalry charge", "Longbow stakes", "English victory", "Range plus terrain")
add("Kursk", "1943", "Russia", "Open steppe", "900,000 Germans", "1.9M Soviets", "Panzer offensive", "Defense in depth", "Soviet victory", "Defense blunts armor")

df = pd.DataFrame(battles)
df.to_csv('data/battles/battles_v1.csv', index=False)
print(f"
✅ Created {len(battles)} battle database!")
print(df[['name', 'year']].to_string(index=False))
