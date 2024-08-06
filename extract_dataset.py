import shutil
import argparse
import os
from glob import glob
from tqdm import tqdm

# extract the dataset structure from downloaded zips.
def extract(root_path: str, output_path: str, type: str):
    if(not os.path.exists(output_path)):
        os.makedirs(output_path)

    list_dataset_type = type.split(",")
    list_of_zips = glob(root_path+"/*.zip")

    datasets = {
        "train":[zip_file for zip_file in list_of_zips if "train" in zip_file],
        "test": [zip_file for zip_file in list_of_zips if "test" in zip_file]
    }

    for dataset_type in list_dataset_type:
        print("Extract", dataset_type, "dataset")
        
        for train_zip in tqdm(datasets[dataset_type]):
            filename = train_zip.split(os.path.sep)[-1].split("_")
            experience_folder_name = filename[1] +"_"+filename[2].split(".")[0]
            extract_folder_path = os.path.join(output_path, dataset_type, experience_folder_name)
            os.makedirs(extract_folder_path)
            shutil.unpack_archive(train_zip, extract_folder_path)



if __name__ == "__main__":
    ...
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--zip_folder_path', required=True, type=str, 
                        help="path which contains train and test zip experiences.")
    parser.add_argument("-o", "--output_path", required=True, 
                        help="path which extract all the experience with the dataset structure")
    parser.add_argument("-t", "--type", default="train,test", help="List of dataset to extract. The accepted values are: 'train', 'train,test', 'test'")
    args = parser.parse_args()
    assert os.path.exists(args.zip_folder_path), "Path {} doesn't exist".format(args.root_path)
    extract(args.zip_folder_path, args.output_path, args.type)

