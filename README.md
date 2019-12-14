Optimized for use on Windows 10 machine.  
  
Workflow (supervised): [DONE]  
1. Get as much as possible data using 'collect_images.py' (gets 2500 samples);  
2. Sort data manually in sub-folders;  
3. Train data, get wights file;  
4. Request reCapteha, classify images, send solution;  
    [it takes ~11-13 seconds to classify images..  
    cannot handle it within 5 seconds as task suggests..  
    need more CPU/RAM?]   

Workflow (unsupervised): [TODO]  
1. Get as much as possible data using 'collect_images.py';  
2. Train unsupervised algorithm to sort all data to classes;  
3. Name classes;  
4. Request reCapteha, classify images, send solution;  


Run as follows:  

(train on existing data)  
    > retrain.py --image_dir training_images  

(train on new data)  
    > rm trainin_images/*  
    > interact.py collect  
    > retrain.py --image_dir training_images  

(request reCAPTEHA and categorize images)  
    > interact.py verify  
