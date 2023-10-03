import json
import re

def norm(val):

  res_list = [s for s in re.split("([A-Z][^A-Z]*)", val) if s]

  s = ' '.join(res_list)

  return s.title()

# for simplicity - avoid buildings that have a larger version or a dedicated producer unlocked by future tech
avoid = {
  "sandMine": "Sand Mine",
  "sulfurMine": "Sulfur Mine",
  "ironMine": "Iron Mine",
  "copperMine": "Copper Mine",
  "aluminiumMine": "Aluminium Mine",
  "uraniumMine": "Uranium Mine",
  "iridiumMine": "Iridium Mine",
  "crudeOilExtractor": "Crude Oil Extractor",
  "airProcessor": "Air Processor"
}

with open('buildings2.json') as json_file:
  data = json.load(json_file)

  conversion = 5000
  cnv = {}
  buildings = {}
  buildingOutput = {}
  resources = {}

  for building, d in data.items():
    if "productionLogic" in d:
      try:
        pd = d["productionLogic"]["productionDefinition"]

        if len(pd["consumables"]) == 0 and len(pd["producables"]) == 0:
          #print("skipping " + building)
          continue

        if building in avoid:
         # print("avoiding " + building)
          continue

        if building not in buildings:
          buildings[building] = {}

        buildings[building]["building"] = norm(building)
        buildings[building]["time"] = pd["timeSteps"] / conversion

        buildings[building]["inputs"] = {}

      except KeyError:
        # we can just ignore all buildings that dont have production logic
        continue


      try:
        ks = pd["consumables"]

        for k in ks:

          if k["resourceName"] not in resources:
            resources[k["resourceName"]] = norm(k["resourceName"])

          buildings[building]["inputs"][k["resourceName"]] = k["amount"];
      except KeyError:
        pass

      try:
        ps = pd["producables"]

        count = 0
        for p in ps:

          # take the first output - damn organic waste
          if count == 0:
            if p["resourceName"] not in resources:
              resources[p["resourceName"]] = norm(p["resourceName"])

            buildingOutput[p["resourceName"]] = building

            buildings[building]["output"] = (p["resourceName"])
            buildings[building]["output_val"] = (p["amount"])

            count += 1

          # print(f'{building} produces {p["resourceName"]} at {round(p["amount"] / buildings[building]["time"], 2)}')

      except KeyError:
        pass

  print("dataResouces = " + json.dumps(resources, indent=2) + ";\n")

  print("resourceBuildingMap = " + json.dumps(buildingOutput, indent=2) + ";\n")

  print("data = " + json.dumps(buildings, indent=2) + ";\n")
