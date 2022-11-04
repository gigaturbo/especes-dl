import argparse
import requests
from multiprocessing import Pool
from os.path import join

parser = argparse.ArgumentParser()
parser.add_argument('--dir', type=str, help="Save directory")
parser.add_argument('--nproc', type=int, help="Number of processes", default=8)
args = parser.parse_args()

def download_pdf(url, loc):
    try:
        r = requests.get(url)
        if r.status_code == requests.codes.ok:
            content = r.content
            with open(loc, 'wb') as f:
                f.write(content)
            print(f"Done: {url} saved at {loc}")
            return True
        return False
    except:
        return False


# -------------------------------------------------------------------------------------------------<

url_root = "https://especes.org/wp-content/uploads"

to_dl = [(f"{url_root}/2019/08/ESPECESnum_01HSnp.pdf", join(args.dir, "ESPECES_HS_01.pdf")),
         (f"{url_root}/2019/07/ESPECESnum_02HSnp.pdf", join(args.dir, "ESPECES_HS_02.pdf"))]

for magno in range(45,0,-1):
    for np in ["np", "NP", ""]:
        for year in range(2022,2010,-1):
            for month in range(12,0,-1):
                pdf_url = f"{url_root}/{year}/{month:02d}/ESPECESnum_{magno:02d}{np}.pdf"
                to_dl.append((pdf_url, join(args.dir, f"ESPECES_{magno}.pdf")))

with Pool(args.nproc) as pool :
    pool.starmap(download_pdf, to_dl)