import bisect


def main():
    zip_gen = csv_reader("zips.csv")
    zip_dict = extract_zip_data(zip_gen)
    plan_gen = csv_reader("plans.csv")
    plans_dict = extract_plan_data(plan_gen)
    slcsp_gen = csv_reader("slcsp.csv")
    slcsp_dict = prep_slcsp_dict(slcsp_gen, zip_dict, plans_dict)
    write_slcsp_file("slcsp_solution.csv", slcsp_dict)


def csv_reader(path):
    with open(path) as f:
        next(f)
        for line in f:
            line_data = line.strip('\n').split(",")
            yield line_data
            

def extract_zip_data(csv_gen):
    zips = {}
    for line in csv_gen:
        rate_area = zips.get(line[0]) 
        if rate_area:
            zips[line[0]].add((line[1], line[-1]))
        else:
            zips[line[0]] = {(line[1], line[-1])}
    return zips


def extract_plan_data(csv_gen):
    silver_plans = {}
    for line in csv_gen:
        if line[2].lower().capitalize() == "Silver":
            try:
                bisect.insort(silver_plans[(line[1], line[-1])], line[-2])
            except KeyError:
                silver_plans[(line[1], line[-1])] = [line[-2]]
    return silver_plans


def format_float(float_num):
    str_float = str(float_num)
    if len(str_float[str_float.find('.'):]) < 3:
        str_float = str_float + '0'
    return str_float


def find_second_smallest(ordered_list, guess_index):
    if guess_index >= len(ordered_list):
        return ""
    list_min = float(ordered_list[0])
    second_min = float(ordered_list[guess_index])
    if second_min != list_min:
        return format_float(second_min)
    else:
        guess_index += 1      
        return find_second_smallest(ordered_list, guess_index)


def prep_slcsp_dict(slcsp_generator, dict_of_zips, dict_of_plans):
    counter = 1
    slcsp_pairs ={}
    for zip_code in slcsp_generator:
        plan_num = dict_of_zips.get(zip_code[0], [])
        if len(plan_num) != 1:
            price = ""
        else:
            price_list = dict_of_plans.get(next(iter(plan_num)), [KeyError])
            price = find_second_smallest(price_list, 1)
        slcsp_pairs[counter]=[zip_code[0], price]
        counter+=1
    return slcsp_pairs


def write_slcsp_file(path, kv_pairs):
    with open(path, 'w') as f:
        f.writelines("zipcode,rate\n")
        for num in range(1, len(kv_pairs)+1):
            print(kv_pairs[num][0], kv_pairs[num][1])
            f.writelines("{}, {}\n".format(kv_pairs[num][0], kv_pairs[num][1]))


if __name__ == "__main__":
    main()
    input("press Enter to close")

