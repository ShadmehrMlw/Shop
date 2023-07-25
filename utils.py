from django.contrib.auth.mixins import UserPassesTestMixin
from kavenegar import *
def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI('4C2B794A5665745A594E74612F2F47632F3855535965596F41453245356276373037614B384941357075773D')
        params = {
            'sender': '0018018949161',
            'receptor': phone_number,
            'message': f'{code}کد فعالسازی شما: '
        }
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)


class UserLoginAccessToRegisterMixin(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_authenticated
