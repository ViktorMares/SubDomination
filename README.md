# Description
SubDomination - Subdomain Enumeration. A simple Python script for Subdomain Enumeration. 

The idea is very simple, use subdomain enumeration tools & add a little bit of functionality on top. The tool basically takes the output of a normal subdomain enumeration tool, it then removes all unnecessary subdomains (that do not belong to the requested domain) and sends a request to each one of them, to show you in a nice colored output, the status code for each one of them.


# Installation & Usage
```
git clone https://github.com/ViktorMares/SubDomination.git
```
```
cd SubDomination
```
```
chmod +x subdomination.py
```
```
./subdomination.py -d example.com
```

# Sample Output:
![image](https://user-images.githubusercontent.com/80492489/213639202-5c6556b4-e3bb-4885-88e7-22b0985dd2f3.png)
