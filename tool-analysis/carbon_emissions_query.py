import os

total_count_first_validation = 0
total_emissions_first_validation = 0
total_emissions_second_experiments = 0
total_count_second_experiments = 0
for root, dirs, files in os.walk("./first_validation/results"):
    path = root.split(os.sep)
    for file in files:
        table_name = file[:-4]
        full_path = "./first_validation/results/" + os.path.basename(root) + "/" + file

        query = f"""csvsql --query "select COUNT(*), SUM(emissions_kg)  from {table_name} where (dataset == 'ChlorineConcentration' and model == 'FCN') or (dataset=='StarLightCurves' and model=='RESNET') or (dataset=='PhalangesOutlinesCorrect' and model=='MLP')" {full_path}"""

        res = os.popen(query).read().strip("COUNT(*),SUM(emissions_kg)").split(',')
        total_emissions_first_validation += float(res[1])
        total_count_first_validation += float(res[0])

for root, dirs, files in os.walk("./../backend/static/experiment_results/time_series/"):
    path = root.split(os.sep)
    if path[0].endswith('filtered'): continue
    for file in files:
        table_name = file[:-4]
        full_path = "./../backend/static/experiment_results/time_series" + os.path.basename(root) + "/" + file

        query = f"""csvsql --query "select COUNT(*), SUM(emissions_kg)  from {table_name}" {full_path}"""

        res = os.popen(query).read().strip("COUNT(*),SUM(emissions_kg)").split(',')
        total_count_second_experiments += int(res[0])
        total_emissions_second_experiments += float(res[1])


print(total_emissions_first_validation)
print(total_count_first_validation)

print('second')
print(total_emissions_second_experiments)
print(total_count_second_experiments)
