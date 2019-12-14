Optimized for use on Windows 10 machine.  
  
Workflow (supervised): [DONE]  
1. Get as much as possible data using 'collect_images.py' (gets 2500 samples);  
2. Sort data manually in sub-folders;  
3. Train data, get wights file;  
   (it takes ~11-13 seconds to classify images..  
   cannot handle it within 5 seconds as task suggests)  
4. Request reCapteha, classify images, send solution;  
  
Workflow (unsupervised):  
1. Get as much as possible data using 'collect_images.py';  
2. Train unsupervised algorithm to sort all data to classes;  
3. Name classes;  
4. Request reCapteha, classify images, send solution;  