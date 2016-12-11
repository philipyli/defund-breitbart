pip install -U selenium
--or--
python3 -m pip install -U selenium

pip install Pillow
 --or--
 python3 -m pip install Pillow

--code below good for debugging large pieces of output in python terminal--
sys.stdout = open("c:\\goat.txt", "w")
print(browser.page_source)