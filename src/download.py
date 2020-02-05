import requests 
import os
import sys
my_path = os.path.abspath(os.path.dirname(__file__))

def download_file(url = 'https://datacatalog.urban.org/sites/default/files/rac_all.csv',
                  filename = '../data/raw/rac_all.csv'):
    print("Downloading from {} to {}".format(url, filename))
    response = requests.get(url, stream = True )
    with open(filename,  'wb') as f:
        total_length = response.headers.get('content-length')
        if total_length is None: # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
                sys.stdout.flush()
                
if __name__ == '__main__':
    download_file()