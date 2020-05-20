"""

This is a simple classifier with a purpose to predict whether a person will earn more than $50.000/y based on age,
workclass, education, marital status, occupation, relationship status, race, sex, capital gain, capital loss and hours
worked during one week. The data used is collected form the UCI Machine Learning Depository.

The program starts by stripping the whitespace and separating the data by ",", storing the numerical data as
integers. Textual data instances are counted and used as relative value.

Inspecting the outcome of individual cases in the training data, the program calculates the averages for each specific entry.
Those averages are then averaged again to create the classifier data, with which the test will be conducted.

Comparing the averages of the test data with the averages of the classifier, the program makes a decision, classifying
the individual case as "over" or "under" 50K and counting the result predictions. The test data is inspected once again,
counting the actual classes of "over" and "under", computing the accuracy of the classifier.

"""

import string
import httplib2

DATA_URL = "http://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data"
PERCENT = 95

"""

This function takes the data url saved as a string and transforms the raw data into a usable form, returning it as a 
list of lists.

"""


def create_data(DATA_URL):
    ready_data = []

    under_count = 0
    over_count = 0

    workclass = {}
    occupation = {}
    marital_status = {}
    relationship = {}
    race = {}
    sex = {}

    try:
        data_input = httplib2.Http(".cache")
        data_headers, data = data_input.request(DATA_URL)
        data = data.decode().strip(" ").split("\n")

        ready_data = []

        under_count = 0
        over_count = 0

        workclass = {}
        occupation = {}
        marital_status = {}
        relationship = {}
        race = {}
        sex = {}

        for entry in data:
            entry = entry.split(",")
            entry[0] = int(entry[0])
            entry[4] = int(entry[4])
            entry[10] = int(entry[10])
            entry[11] = int(entry[11])
            entry[12] = int(entry[12])
            entry[2] = None
            entry[3] = None
            entry[13] = None

            if entry[-1].strip(" ") == "<=50K":
                under_count += 1
            else:
                over_count += 1

            if entry[1] in workclass:
                workclass[entry[1]] += 1
            else:
                workclass[entry[1]] = 1

            if entry[5] in marital_status:
                marital_status[entry[5]] += 1
            else:
                marital_status[entry[5]] = 1

            if entry[6] in occupation:
                occupation[entry[6]] += 1
            else:
                occupation[entry[6]] = 1

            if entry[7] in relationship:
                relationship[entry[7]] += 1
            else:
                relationship[entry[7]] = 1

            if entry[8] in race:
                race[entry[8]] += 1
            else:
                race[entry[8]] = 1

            if entry[9] in sex:
                sex[entry[9]] += 1
            else:
                sex[entry[9]] = 1

            ready_data.append(entry)

    except Exception as e:
        pass

    for entry in ready_data:

        if entry[-1].strip(" ") == "<=50K":
            entry[1] = workclass[entry[1]] / under_count
            entry[5] = marital_status[entry[5]] / under_count
            entry[6] = occupation[entry[6]] / under_count
            entry[7] = relationship[entry[7]] / under_count
            entry[8] = race[entry[8]] / under_count
            entry[9] = sex[entry[9]] / under_count
        else:
            entry[1] = workclass[entry[1]] / over_count
            entry[5] = marital_status[entry[5]] / over_count
            entry[6] = occupation[entry[6]] / over_count
            entry[7] = relationship[entry[7]] / over_count
            entry[8] = race[entry[8]] / over_count
            entry[9] = sex[entry[9]] / over_count

    return ready_data


"""

This function takes a chunk of data and calculates the average values of individual attributes for both outcomes.
Another average is made from both of the outcomes, resulting in data that may be used by the program to makes its 
decision, called the classifier. 

"""


def classifier(training_data):
    over_data = []
    under_data = []
    classifier_data = [0] * 14
    over_avg = [0] * 14
    under_avg = [0] * 14

    over_count = 0
    under_count = 0

    for entry in training_data:
        if entry[14].lstrip() == '<=50K':
            under_count += 1
            under_data.append(entry)
        else:
            over_count += 1
            over_data.append(entry)

    temp_zip_over = zip(*over_data)
    temp_list_over = list(temp_zip_over)
    temp_zip_under = zip(*under_data)
    temp_list_under = list(temp_zip_under)

    over_avg[0] = sum(temp_list_over[0]) / over_count
    over_avg[1] = sum(temp_list_over[1]) / over_count
    over_avg[2] = None
    over_avg[3] = None
    over_avg[4] = sum(temp_list_over[4]) / over_count
    over_avg[5] = sum(temp_list_over[5]) / over_count
    over_avg[6] = sum(temp_list_over[6]) / over_count
    over_avg[7] = sum(temp_list_over[7]) / over_count
    over_avg[8] = sum(temp_list_over[8]) / over_count
    over_avg[9] = sum(temp_list_over[9]) / over_count
    over_avg[10] = sum(temp_list_over[10]) / over_count
    over_avg[11] = sum(temp_list_over[11]) / over_count
    over_avg[12] = sum(temp_list_over[12]) / over_count
    over_avg[13] = ">50K"

    under_avg[0] = sum(temp_list_under[0]) / under_count
    under_avg[1] = sum(temp_list_under[1]) / under_count
    under_avg[2] = None
    under_avg[3] = None
    under_avg[4] = sum(temp_list_under[4]) / under_count
    under_avg[5] = sum(temp_list_under[5]) / under_count
    under_avg[6] = sum(temp_list_under[6]) / under_count
    under_avg[7] = sum(temp_list_under[7]) / under_count
    under_avg[8] = sum(temp_list_under[8]) / under_count
    under_avg[9] = sum(temp_list_under[9]) / under_count
    under_avg[10] = sum(temp_list_under[10]) / under_count
    under_avg[11] = sum(temp_list_under[11]) / under_count
    under_avg[12] = sum(temp_list_under[12]) / under_count
    under_avg[13] = "<=50K"

    classifier_data[0] = (over_avg[0] + under_avg[0]) / 2
    classifier_data[1] = (over_avg[1] + under_avg[1]) / 2
    classifier_data[2] = None
    classifier_data[3] = None
    classifier_data[4] = (over_avg[4] + under_avg[4]) / 2
    classifier_data[5] = (over_avg[5] + under_avg[5]) / 2
    classifier_data[6] = (over_avg[6] + under_avg[6]) / 2
    classifier_data[7] = (over_avg[7] + under_avg[7]) / 2
    classifier_data[8] = (over_avg[8] + under_avg[8]) / 2
    classifier_data[9] = (over_avg[9] + under_avg[9]) / 2
    classifier_data[10] = (over_avg[10] + under_avg[10]) / 2
    classifier_data[11] = (over_avg[11] + under_avg[11]) / 2
    classifier_data[12] = (over_avg[12] + under_avg[12]) / 2
    classifier_data[13] = ">50K"

    return classifier_data


"""

This function uses a chunk of data know as test data and the classifier as reference values. It iterates through the 
test data and compares the individual cases' attributes with the classifier, counting the instances where an attribute 
is "over" or "under". Each individual case is then classified according to the number of "over" and "under" attributes.
Accuracy is expressed as a quotient of the counted and predicted cases.

"""


def test(test_data, classifier_data):
    results = []
    over_predicted = 0
    under_predicted = 0
    over_counted = 0
    under_counted = 0

    for entry in test_data:
        entry_index_over_count = 0
        entry_index_under_count = 0
        outcome = entry[-1]

        for index in range(14):
            try:
                if entry[index] > classifier_data[entry[index]]:
                    entry_index_over_count += 1
                else:
                    entry_index_under_count += 1
            except Exception as e:
                continue

        if entry_index_under_count > entry_index_over_count:
            entry_index_under_count = "Under 50K"
            entry_index_over_count = ""
            under_predicted += 1
        else:
            entry_index_over_count = "Over 50K"
            entry_index_under_count = ""
            over_predicted += 1

        result = ([outcome, entry_index_under_count, entry_index_over_count])
        results.append(result)

    for entry in test_data:
        if entry[-1].strip(" ") == "<=50K":
            under_counted += 1
        elif entry[-1].strip(" ") == ">50K":
            over_counted += 1
        else:
            pass

    accuracy = (under_counted / under_predicted) * 100

    print("Classifier accuracy: %.2f%%" % accuracy)


"""

This function creates data chunks used for training and testing the classifier, as well as controling the program flow,
and data movement between functions. 

"""


def main():
    data = create_data(DATA_URL)
    training_data = data[:int(len(data) * PERCENT / 100)]
    classifier_data = classifier(training_data)
    test_data = data[int(len(data) * PERCENT / 100):]
    test(test_data, classifier_data)


"""

This function starts the program in the main functions, in case it exists. 

"""

if __name__ == '__main__':
    main()

"""

Author: Matija Pozega

Student number: D18124803

"""
