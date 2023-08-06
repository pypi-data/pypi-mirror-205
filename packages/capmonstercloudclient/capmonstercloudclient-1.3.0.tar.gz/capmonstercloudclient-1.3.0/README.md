# Zennolab.CapMonsterCloud.Client

Official python client library for [capmonster.cloud](https://capmonster.cloud/) captcha recognition service

## Installation

    python3 -m pip install capmonstercloudclient

## Usage

***
    import asyncio

    from capmonstercloudclient import CapMonsterClient, ClientOptions
    from capmonstercloudclient.requests import RecaptchaV2ProxylessRequest

    client_options = ClientOptions(api_key=<YOUR_API_KEY>)
    cap_monster_client = CapMonsterClient(options=client_options)

    async def solve_captcha():
        return await cap_monster_client.solve_captcha(recaptcha2request)

    recaptcha2request = RecaptchaV2ProxylessRequest(websiteUrl="https://lessons.zennolab.com/captchas/recaptcha/v2_simple.php?level=high",
                                                    websiteKey="6Lcg7CMUAAAAANphynKgn9YAgA4tQ2KI_iqRyTwd")

    responses = asyncio.run(solve_captcha())
    print(responses)
***

Supported captcha recognition requests:

- FunCaptchaProxylessRequest
- FunCaptchaRequest
- GeeTestProxylessRequest
- GeeTestRequest
- HCaptchaProxylessRequest
- HCaptchaRequest
- ImageToTextRequest
- RecaptchaV2ProxylessRequest
- RecaptchaV2Request
- RecaptchaV3ProxylessRequest
- RecaptchaV2EnterpriseProxylessRequest
- RecaptchaV2EnterpriseRequest
- TurnstileProxylessRequest
- TurnstileRequest
- RecaptchaComplexImageTaskRequest
- HcaptchaComplexImageTaskRequest