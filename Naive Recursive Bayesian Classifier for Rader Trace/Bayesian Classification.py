import argparse
import numpy as np
import math


def classification(pdf1, datasets, args):
    probability = []
    num = len(datasets)
    for i in range(2*num):
        probability.append(0)

    for i in range(num):
        for t in range(len(datasets[0])):
            if t == 0:
                probability_a = 0.5
                probability_b = 0.5
            if datasets[i][t] == 0:
                continue

            p_a, p_b = probability_a, probability_b
            t_ab = p_a * 0.1 + p_b * (1 - 0.1)
            t_ba = p_b * 0.1 + p_a * (1 - 0.1)
            t_b = p_b * (0.1 - 0.1) + p_a * (1 - 0.1 + 0.1)

            p1 = pdf1[1][int(2 * datasets[i][t])]
            p2 = pdf1[0][int(2 * datasets[i][t])]

            if args.extra_feature == True:
                sunny = datasets[i][t] - datasets[i][t - 1]
                if abs(sunny > 0):
                    probability_a = t_ab * p1
                    probability_b = t_b * p2
            else:
                probability_a = t_ab * p1
                probability_b = t_ba * p2

            a = 2 * i + 1
            b = 2 * i

            tm = probability_b + probability_a
            probability_a = probability_a / tm
            probability_b = probability_b / tm
            probability[a] = probability_a
            probability[b] = probability_b

    return probability


def out_clean(files):
    if files == './pdf.txt':
        sequence = 400
    elif files == './data.txt':
        sequence = 300
    file = open(files)
    datasets = file.readlines()
    pretreatment_data = list()

    for i in datasets:
        d = i.strip('\n').split(',')
        pretreatment_data.append(d)

    sum = len(pretreatment_data)
    for j in range(0, sum):
        for k in range(sequence):
            j_k = float(pretreatment_data[j][k])
            pretreatment_data[j].append(j_k)
        del (pretreatment_data[j][0:sequence])

    return pretreatment_data


def main(args):
    file1 = './pdf.txt'
    file2 = './data.txt'

    # Data cleaning
    file1 = out_clean(file1)
    lang_file1 = len(file1)
    # Data normalization
    sum = 0
    for i in range(lang_file1):
        lang_file1_i = len(file1[i])

        for j in range(lang_file1_i):
            sum = sum + file1[i][j]

        for k in range(lang_file1_i):
            file1[i][k] = file1[i][k] / sum

        sum = 0
        for l in range(lang_file1_i):
            sum = sum + file1[i][l]
        sum = 0

    file2 = out_clean(file2)
    lang_file2 = len(file2)
    lang_file2_i = len(file2[i])
    # Data conversion
    for i in range(lang_file2):
        for j in range(lang_file2_i):
            if np.isnan(file2[i][j]):
                file2[i][j] = 0
            else:
                file2[i][j] = math.floor(file2[i][j])

    pro1 = classification(file1, file2, args)
    if args.extra_feature == True:
        print("The predicted result considering additional features is: ")
    else:
        print("The predicted result without considering additional features is: ")
    for number in range(int(len(pro1) / 2)):
        print("Class Probabilities For Object ", number + 1)
        print("\t\t Bird:", pro1[2 * number])
        print("\t\t Airplane: ", pro1[2 * number + 1])
        if pro1[2 * number] >= pro1[2 * number + 1]:
            print("\t\t Object is most Likely a BIRD")
        else:
            print("\t\t Object is most Likely a PLANE")



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('--extra_feature', default=True, help='Whether to add additional features')
    args = parser.parse_args()
    main(args)
