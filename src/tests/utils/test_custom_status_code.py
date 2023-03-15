from utils.base.status import StatCode


class TestCustomStatusCode:
    code = StatCode

    def test_http_200_ok(self):
        assert self.code.HTTP_200_OK == 200

    def test_http_201_created(self):
        assert self.code.HTTP_201_CREATED == 201

    def test_http_400_bad_request(self):
        assert self.code.HTTP_400_BAD_REQUEST == 400

    def test_http_401_failed_authentication(self):
        assert self.code.HTTP_401_FAILED_AUTHENTICATION == 401

    def test_http_403_forbidden(self):
        assert self.code.HTTP_403_FORBIDDEN == 403

    def test_http_404_not_found(self):
        assert self.code.HTTP_404_NOT_FOUND == 404

    def test_http_432_user_not_found(self):
        assert self.code.HTTP_432_USER_NOT_FOUND == 432

    def test_http_433_invalid_token(self):
        assert self.code.HTTP_433_INVALID_TOKEN == 433

    def test_http_434_already_verified(self):
        assert self.code.HTTP_434_ALREADY_VERIFIED == 434

    def test_http_435_invalid_uidb64(self):
        assert self.code.HTTP_435_INVALID_UIDB64 == 435

    def test_http_436_no_id(self):
        assert self.code.HTTP_436_NO_ID == 436

    def test_http_437_no_email(self):
        assert self.code.HTTP_437_NO_EMAIL == 437

    def test_http_438_not_verified(self):
        assert self.code.HTTP_438_NOT_VERIFIED == 438

    def test_http_439_account_deactivated(self):
        assert self.code.HTTP_439_ACCOUNT_DEACTIVATED == 439

    def test_http_440_invalid_signature(self):
        assert self.code.HTTP_440_INVALID_SIGNATURE == 440

    def test_http_441_no_business_account(self):
        assert self.code.HTTP_441_NO_BUSINESS_ACCOUNT == 441

    def test_http_442_bad_payment_request(self):
        assert self.code.HTTP_442_BAD_PAYMENT_REQUEST == 442
