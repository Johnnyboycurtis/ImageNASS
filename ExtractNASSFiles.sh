echo "Downloading NASSCIREN Data Sets"

wget https://one.nhtsa.gov/DOT/NHTSA/NVS/CIREN/20151230_CIREN_Public_Data.zip .

echo "Extracting files"
unzip 20151230_CIREN_Public_Data.zip

echo "Converting files to CSV"
python extract_CIREN.py

echo "Done" 
