
import requests
def reset(email: str) -> str:
        url = "https://i.instagram.com/api/v1/accounts/send_password_reset/"
        headers = {}
        headers['Content-Length']='319'
        headers['Content-Type']='application/x-www-form-urlencoded;charset=UTF-8'
        headers['Host']='i.instagram.com'
        headers['Connection']='Keep-Alive'
        headers['User-Agent']='Instagram6.12.1Android(26/8.0.0;560dpi;1440x2560;samsung/Verizon;SM-G930V;heroqltevzw;qcom;en_US)'
        headers['Cookie']='mid=YwEuiAABAAGBdZ2ajZXFL5EOuNSE;csrftoken=ayOokI9GUT5f9Up0aLulP8mSehjppSys'
        headers['Cookie2']='$Version=1'
        headers['Accept-Language']='en-US'
        headers['X-IG-Connection-Type']='WIFI'
        headers['X-IG-Capabilities']='AQ=='
        headers['Accept-Encoding']='gzip' 
        data = f"ig_sig_key_version=4&signed_body=e97dc9c43a2967793f2dd2b4f567fae41b45e8a2b545a3ec4acd5faca5879e7a.%7B%22user_email%22%3A%22{email}%22%2C%22device_id%22%3A%22android-074b337ee8f413e0%22%2C%22guid%22%3A%228013fb43-e663-4a10-a892-5ffea66a508b%22%2C%22_csrftoken%22%3A%22ayOokI9GUT5f9Up0aLulP8mSehjppSys%22%7D"
        res = requests.post(url,headers=headers,data=data).json()['obfuscated_email'] 
        return {'rest':res}