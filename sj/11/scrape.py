from urllib.request import urlopen

hadoopPage = "https://hadoop.apache.org"

page = urlopen(hadoopPage)

with open('C:\\Users\\Amruta K\\Desktop\\hadoopApache','ab') as f:
	f.writelines(page)