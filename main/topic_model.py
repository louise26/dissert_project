import turicreate as tc
import os

def open_policy(file, file_location, remove_short_threshold=4):
    
    '''
    This function opens each policy, removes lines that are smaller than a certain threshold, 
    and groups all the text of the policy into one single line. 
    '''
    
    f = open(f"{file_location}/{file}")
    
    #list of strings (1 element per line)
    lines = f.readlines()
    #keep lines that contain more words than the number set in "removed_short_threshold"
    lines = [l for l in lines if len(l.split(' ')) > remove_short_threshold]
    #add all the content of one policy text into one line
    line_policy = ' '.join([l.replace('\n',' ').replace('\t', ' ') for l in lines])
    
    return line_policy

def run_preprocessing(file_location, save_file_location, remove_short_threshold, policy_size_threshold):

    '''
    This function is used to clean the corpus of policies, creating new versions of the policies to avoid losing the original ones. 
    '''
   
    files = os.listdir(file_location)
    
    #for eahc file in the policies directory, apply preprocessing
    for f in files:
        if f == '.DS_Store':
            continue
        if 'preprocessed' in f:
            continue
        preprocessed_text = open_policy(f, file_location=file_location, remove_short_threshold=remove_short_threshold)
        
        #create new files addeding "prepocessed_" prefix in a new directory
        if len(preprocessed_text.split(' ')) > policy_size_threshold:
            new_file = open(f'{save_file_location}/preprocessed_{f}','w')
            new_file.write(preprocessed_text)
            new_file.close()
            
def clean_corpus(docs):
    '''
    This function is used to clean the full corpus of text once it is gathered in one SFrame.
    '''
    
    #add terms to stop_words list 
    set(list(tc.text_analytics.stop_words())+["www", "https","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","2019","2020","2021"])
    #count occurance of a word for each row of the SArray
    docs = tc.text_analytics.count_words(docs['X1'])
    #remove stop words from docs
    clean_docs = docs.dict_trim_by_keys(tc.text_analytics.stop_words(), exclude=True)
    
    return clean_docs


##### MAIN #####

#folder to get policies from
input_folder = 'policies'
#folder to store filtered policies
output_folder = 'preprocessed_policies'
#set threshold to remove any lines in a policy that have less than a certain number of words
remove_short_threshold = 4
#set threshold to remove policies that have less than a certain number of words
policy_size_threshold = 100

#apply run_prepocessing function to create a new policies folder after cleaning and filtering
run_preprocessing(input_folder, output_folder,remove_short_threshold,policy_size_threshold)

#import policies and convert them to SFrame 
docs = tc.SFrame.read_csv('preprocessed_policies/*.txt', header=False, delimiter='\c')

#clean SFrame docs
clean_docs = clean_corpus(docs)

#learn topic model 
model = tc.topic_model.create(clean_docs)