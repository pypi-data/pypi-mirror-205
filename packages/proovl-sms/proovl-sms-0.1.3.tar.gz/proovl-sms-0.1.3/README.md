<h1 align="center">proovl-sms</h1>

<p>
  <strong>A Python library for sending SMS messages using Proovl API</strong>
</p>


<h2>Installation</h2>

Install using pip:

`pip install proovl-sms`


<h2>Parameters</h2>
<p>The following parameters are required to send an SMS message:</p>

<ul>
  <li><code>user</code>: Your Proovl API user ID. You can obtain this from your <a href="https://www.proovl.com">Proovl account</a>.</li>
  <li><code>token</code>: Your Proovl API authentication token. You can obtain this from your Proovl account.</li>
  <li><code>from_num</code>: The sender's name or phone number. This must be registered with Proovl. Leave this blank if you want to use the default sender name.</li>
</ul>


<h2>Usage:</h2>

<pre>
```python
from proovl_sms import Proovl

# Initialize Proovl with your Proovl user, token, and from number
proovl = Proovl(user='your_proovl_user', token='your_proovl_token', from_num='your_from_number')

# Send a single SMS message
response = proovl.send_sms(destination='destination_number', message='Hello, world!')
print(response)
```
</pre>

<h2>Bulk SMS:</h2>

<pre>
```python
from proovl_sms import Proovl

# Initialize Proovl with your Proovl user, token, and from numbers
proovl = Proovl(user='your_proovl_user', token='your_proovl_token', from_num='your_from_number')

# Send a bulk SMS message
results = proovl.send_bulk_sms(destinations='destination1;destination2;destination3;destination4;destination5', message='Hello, world!')
for result in results:
    print(result['number'], result['response'])
```
</pre>

<h2>Credits</h2>
<p>The proovl-sms package was developed by Tomas. You can obtain your own Proovl account and API credentials from <a href="https://www.proovl.com">proovl.com</a>.</p>
