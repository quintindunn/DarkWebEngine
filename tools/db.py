import json
import os
import time


def main(loaded=False):
    if __name__ == "__main__":
        data_folder = "../data/"
    else:
        data_folder = "data/"
    files = os.listdir(data_folder)
    word_dict = {}
    print("Loading data, please wait...")
    start_time = time.time()
    if not loaded:
        for file in files:
            if file.startswith("--xjfbpuj56rdazx4iolylxplbvyft2onuerjeimlcqwaihp3s6r4xebqd.onion"):
                continue
            print("loading \"" + file + "\"")

            with open(data_folder + file, 'r') as f:
                data = json.loads(f.read())

            url = list(data.keys())[0]
            words = data[url]['words']
            for word in words:
                write_word = word['word'].replace("\\n", "").replace("\\t", "").lower()
                write_word = write_word.replace("#", "").replace(".", "").replace("!", "").replace("$", "").replace(",", "").\
                    replace("(", "").replace(")", "")
                if write_word == "":
                    continue
                if write_word not in word_dict.keys():
                    word_dict[write_word] = {}
                word_dict[write_word][url] = {
                        "word": write_word,
                        "count": word['count']
                    }
            with open("output.json", 'w') as f:
                f.write(json.dumps(word_dict))
    else:
        with open("output.json", 'r') as f:
            word_dict = json.loads(f.read())
    end_time = time.time()
    time_took = end_time - start_time
    rounded_time_took = round(time_took, 2)
    print("Loaded data took " + str(rounded_time_took) + " seconds.")
    term = input("Search: ")

    results = {}
    term = term.split()
    for word in term:
        if word not in word_dict.keys():
            continue
        for i in word_dict[word]:
            count, url = str(word_dict[word][i]['count']), i
            if url not in results.keys():
                results[url] = {}
            results[url][word] = count

    new_results = []
    for url in results:
        total = 0
        for i in results[url].keys():
            total += int(results[url][i])
        append = [total, url]
        new_results.append(append)

    new_results.sort(reverse=True)

    num_results = 1
    if len(new_results) < 1:
        print("Sorry no results were found :(")
    else:
        print("1: " + new_results.pop(0)[1])
        if len(new_results) > 0:
            print("2: " + new_results.pop(0)[1])
            if len(new_results) > 0:
                print("3: " + new_results.pop(0)[1])
                if len(new_results) > 0:
                    print("4: " + new_results.pop(0)[1])
                    if len(new_results) > 0:
                        print("5: " + new_results.pop(0)[1])

    input("press enter to search again.")
    print("\n"*5)
    main(loaded=True)