import torchdata.datapipes as dp
import torchtext.transforms as T
import os
root="captions"
file_paths=[root+"/"+file_+"/"+file_+".txt" for file_ in os.listdir(root)]
data_pipe = dp.iter.IterableWrapper(file_paths)
data_pipe = dp.iter.FileOpener(data_pipe, mode='rb')
data_pipe = data_pipe.parse_csv(skip_lines=0, delimiter='\t', as_tuple=True)

# Print the first few lines of the data
for i, item in enumerate(data_pipe):
    if i < 5:  # Print only the first 5 items for demonstration
        print(item)
    else:
        break