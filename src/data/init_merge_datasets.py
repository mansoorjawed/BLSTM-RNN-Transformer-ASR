import json
import csv
import os

# intended format TSV: filename - sentence

def get_svarah_data(svarah_dir_path):
    """
    This function gets file name and the sentence spoken in the audio
    :param manifest_path: path to the manifest from which to extract data
    :return: formatted list of what needs to be written to the new TSV file.
    the data for new TSV is just audio path in the svarah folder and the
    transcription.
    """

    manifest_path = os.path.join(svarah_dir_path, "svarah_manifest.json")
    json_data = []
    with open(manifest_path, "r") as file:
        count = 0
        for line in file:
            json_obj = json.loads(line)
            json_obj_data = [json_obj["audio_filepath"], json_obj["text"]]
            json_obj_data[0] = os.path.join(svarah_dir_path
                                            + "/" + json_obj_data[0])
            json_data.append(json_obj_data)

            count += 1
            if count % 1000 == 0:
                print(f"{count} done in svarah")
    return json_data

def get_cv_data(cv_dir_path):
    """
    This function gets file name and the sentence spoken in the audio
    :param validated.tsv: path to file that includes data related to audios
    :return: formatted list of what needs to be written to the new TSV file.
    the data for new TSV is just audio path in the cv folder and the
    transcription.
    """
    validated_file_path = os.path.join(cv_dir_path, "validated.tsv")
    cv_data = []
    with open(validated_file_path, newline='', encoding='utf-8') as file:
        # Create a CSV reader object, specifying the delimiter as a tab character
        reader = csv.reader(file, delimiter='\t')

        # Names of all the relevant usable files
        files_in_dir = os.listdir(os.path.join(cv_dir_path
                                               + "/ind_pak_clips_wav/"))
        file_without_extension = {os.path.splitext(file)[0]
                                  for file in files_in_dir}

        count = 0
        for row in reader:
            # check if the file name (without the format) matches
            # if it matches,  record the file path and text in the clip
            file_name = row[1][:-4]
            if (file_name in file_without_extension):
                text = row[2].split('\t')[0]
                cv_row_data = [file_name, text]
                cv_row_data[0] = os.path.join(cv_dir_path
                                              + "/ind_pak_clips_wav/"
                                              + cv_row_data[0]
                                              + ".wav")
                cv_data.append(cv_row_data)

                count += 1
                if (count % 1000 == 0):
                    print(f"{count} done in cv")

    return cv_data

def write_to_tsv(combined_files):
    """
    This function writes the file paths and transcriptions of each file to a TSV
    file to be referred to later
    :param combined_files: files record that include file path and transcription
    :return: none
    """
    headers =["path", "transcription"]
    file_path = "D:/University/Data/audio_data.tsv"

    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter='\t')

        # Write the headers
        writer.writerow(headers)

        # Write the data
        for row in combined_files:
            writer.writerow(row)


# Get the names of all the audio files in Svarah
svarah_path = "D:/University/Data/svarah"
svarah_data = get_svarah_data(svarah_path)

# Get the names of all the audio files in CV
cv_path = "D:/University/Data/cv-corpus/en"
cv_data = get_cv_data(cv_path)

# combine the two mainly the local file paths and the text in the audio
combined_files = cv_data + svarah_data

# write the files to a tsv file
write_to_tsv(combined_files)







