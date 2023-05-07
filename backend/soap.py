import requests
import xml.etree.ElementTree as ET

url = "http://legislatie.just.ro/apiws/FreeWebService.svc?wsdl"

SOAPEnvelope = """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Header>
    <Action s:mustUnderstand="1" xmlns="http://schemas.microsoft.com/ws/2005/05/addressing/none">http://tempuri.org/IFreeWebService/GetToken</Action>
  </s:Header>
  <s:Body>
    <GetToken xmlns="http://tempuri.org/" />
  </s:Body>
</s:Envelope>"""

options = {
    "Content-Type": "text/xml; charset=utf-8"
}

response = requests.post(url, data=SOAPEnvelope, headers=options)
print(response.text)
with open("response.xml","wb") as f:
    f.write(response.content)
